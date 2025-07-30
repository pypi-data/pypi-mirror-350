"""
Same-chain DEX swap execution operations.
"""

import asyncio
from typing import Dict, Any

from ..utils.constants import (
    OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE, 
    RPC_URLS, EXPLORER_URLS, CHAIN_NAMES
)
from ..utils.okx_client import make_okx_request
from ..utils.blockchain import (
    get_web3_connection, validate_private_key, is_native_token,
    check_token_allowance, execute_token_approval, get_token_info, build_transaction
)
from ..utils.formatters import format_readable_amount


async def execute_dex_swap(from_token: str, to_token: str, amount: str, chain_id: str, 
                          user_wallet_address: str, private_key: str, slippage: str = "0.5") -> str:
    """Execute a DEX token swap using OKX API and broadcast the transaction to the blockchain."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    if chain_id not in RPC_URLS:
        return f"❌ Unsupported chain ID: {chain_id}. Supported chains: {', '.join(RPC_URLS.keys())}"
    
    # Progressive slippage values for retries
    slippage_values = [slippage, "1.0", "2.0", "3.0"]
    max_retries = 3
    
    # Get Web3 connection
    web3 = get_web3_connection(chain_id)
    if not web3:
        return f"❌ Failed to connect to any blockchain network for chain {chain_id}"
    
    # Validate private key and wallet address
    validation = validate_private_key(private_key, user_wallet_address)
    if not validation['valid']:
        return f"❌ {validation['error']}"
    
    private_key = validation['private_key']
    
    # Retry loop with progressive slippage increase
    for attempt in range(max_retries + 1):
        current_slippage = slippage_values[min(attempt, len(slippage_values) - 1)]
        
        if attempt > 0:
            print(f"🔄 Retry attempt {attempt + 1}/{max_retries + 1} with {current_slippage}% slippage...")
            await asyncio.sleep(3)  # Wait between retries
        
        try:
            # Build URL for swap endpoint
            base_url = f"{OKX_API_BASE}/api/v5/dex/aggregator/swap"
            params = [
                f"chainId={chain_id}",
                f"fromTokenAddress={from_token}",
                f"toTokenAddress={to_token}",
                f"amount={amount}",
                f"userWalletAddress={user_wallet_address}",
                f"slippage={current_slippage}"
            ]
            full_url = f"{base_url}?{'&'.join(params)}"
            
            # Get swap data from OKX API
            data = await make_okx_request(full_url)

            if not data:
                if attempt < max_retries:
                    continue
                return f"❌ Unable to get swap data for {from_token} -> {to_token}."

            if data.get("code") != "0":
                error_msg = data.get('msg', 'Unknown error')
                if attempt < max_retries and ("slippage" in error_msg.lower() or "price" in error_msg.lower()):
                    continue
                return f"❌ API Error: {error_msg}"

            if not data.get("data"):
                if attempt < max_retries:
                    continue
                return "❌ No swap data available for this token pair."

            swap_info = data["data"][0] if isinstance(data["data"], list) else data["data"]
            router_result = swap_info.get('routerResult', {})
            tx_data = swap_info.get('tx', {})
            
            if not tx_data:
                if attempt < max_retries:
                    continue
                return "❌ No transaction data received from API"
            
            # Extract token information for display
            from_token_info = router_result.get('fromToken', {})
            to_token_info = router_result.get('toToken', {})
            
            # Format amounts for display
            from_amount = router_result.get('fromTokenAmount', 'N/A')
            to_amount = router_result.get('toTokenAmount', 'N/A')
            from_decimals = int(from_token_info.get('decimal', 18))
            to_decimals = int(to_token_info.get('decimal', 18))
            
            from_amount_readable = format_readable_amount(from_amount, from_decimals, from_token_info.get('tokenSymbol', ''))
            to_amount_readable = format_readable_amount(to_amount, to_decimals, to_token_info.get('tokenSymbol', ''))
            
            # Check if this is a native token swap
            is_native = is_native_token(from_token, chain_id)
            
            approval_result = None
            
            # Handle token approval for ERC-20 tokens (not needed for native tokens)
            if not is_native:
                print(f"🔍 Checking token approval for {from_token_info.get('tokenSymbol', 'Unknown')}...")
                
                # Get the DEX router address from transaction data
                dex_router_address = tx_data.get('to')
                if not dex_router_address:
                    if attempt < max_retries:
                        continue
                    return "❌ Unable to determine DEX router address for approval"
                
                # Check current allowance
                current_allowance = await check_token_allowance(
                    chain_id, from_token, user_wallet_address, dex_router_address, web3
                )
                
                required_amount = int(amount)
                
                print(f"   Current allowance: {current_allowance}")
                print(f"   Required amount: {required_amount}")
                
                if current_allowance < required_amount:
                    print(f"   ⚠️  Insufficient allowance. Executing approval transaction...")
                    
                    # Execute approval with a higher amount to avoid frequent approvals
                    approve_amount = str(required_amount * 2)
                    
                    approval_result = await execute_token_approval(
                        chain_id, from_token, approve_amount, user_wallet_address, private_key, web3
                    )
                    
                    if not approval_result['success']:
                        if attempt < max_retries:
                            continue
                        return f"❌ Token approval failed: {approval_result['error']}"
                    
                    print(f"   ✅ Approval successful: {approval_result['tx_hash']}")
                    await asyncio.sleep(3)  # Wait for approval to be processed
                else:
                    print(f"   ✅ Sufficient allowance already exists")
            else:
                print(f"🔍 Native token swap detected - no approval needed")
            
            # Build and execute swap transaction
            transaction = build_transaction(tx_data, chain_id, user_wallet_address, web3)
            
            # Sign the transaction
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
            
            # Send the transaction
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_hash_hex = tx_hash.hex()
            
            # Wait for transaction receipt
            try:
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)  # 5 minutes timeout
                
                if receipt.status == 1:
                    # Transaction successful
                    explorer_url = f"{EXPLORER_URLS.get(chain_id, '')}{tx_hash_hex}"
                    
                    result = f"""
✅ SWAP EXECUTED SUCCESSFULLY!

=== SWAP DETAILS ===
From Token: {from_token_info.get('tokenSymbol', 'Unknown')} (${from_token_info.get('tokenUnitPrice', 'N/A')})
To Token: {to_token_info.get('tokenSymbol', 'Unknown')} (${to_token_info.get('tokenUnitPrice', 'N/A')})
Chain: {CHAIN_NAMES.get(chain_id, chain_id)}
From Amount: {from_amount_readable}
To Amount: {to_amount_readable}
Price Impact: {router_result.get('priceImpactPercentage', 'N/A')}%
Successful Slippage: {current_slippage}%
Attempts Made: {attempt + 1}

=== TRANSACTION DETAILS ===
Transaction Hash: {tx_hash_hex}
Block Number: {receipt.blockNumber}
Gas Used: {receipt.gasUsed:,}
Gas Price: {transaction.get('gasPrice', 0):,} wei
Status: SUCCESS ✅

=== EXPLORER LINK ===
{explorer_url}
"""
                    
                    # Add approval information if approval was executed
                    if approval_result and approval_result['success']:
                        approval_explorer = f"{EXPLORER_URLS.get(chain_id, '')}{approval_result['tx_hash']}"
                        result += f"""
=== APPROVAL TRANSACTION ===
Approval Hash: {approval_result['tx_hash']}
Approval Explorer: {approval_explorer}
"""
                    
                    result += "\n🎉 Your swap has been completed successfully!"
                    
                    # Add retry success information if retries were used
                    if attempt > 0:
                        result += f"\n💪 Success achieved after {attempt + 1} attempts with {current_slippage}% slippage!"
                    
                    return result
                else:
                    # Transaction failed - check if we should retry
                    failure_msg = f"""
❌ TRANSACTION FAILED

Transaction Hash: {tx_hash_hex}
Status: FAILED
Block Number: {receipt.blockNumber}
Gas Used: {receipt.gasUsed:,}
Attempt: {attempt + 1}/{max_retries + 1}
Slippage Used: {current_slippage}%

The transaction was mined but failed during execution."""
                    
                    if attempt < max_retries:
                        print(failure_msg)
                        print(f"🔄 Retrying with higher slippage ({slippage_values[attempt + 1]}%)...")
                        continue
                    else:
                        return failure_msg + f"""

This could be due to:
- Insufficient slippage tolerance (tried up to {current_slippage}%)
- Price movement during execution
- Insufficient gas limit
- Token liquidity issues
- Market volatility

All retry attempts have been exhausted. Please check the transaction on the block explorer for more details.
"""
                        
            except Exception as e:
                timeout_msg = f"""
⏳ TRANSACTION SUBMITTED BUT CONFIRMATION PENDING

Transaction Hash: {tx_hash_hex}
Status: PENDING
Attempt: {attempt + 1}/{max_retries + 1}

The transaction has been submitted to the blockchain but confirmation is taking longer than expected."""
                
                if attempt < max_retries:
                    print(timeout_msg)
                    print("🔄 Retrying with new transaction...")
                    continue
                else:
                    return timeout_msg + f"""
You can check the status manually using the transaction hash above.

Error details: {str(e)}
"""
        
        except Exception as e:
            error_msg = f"Swap execution failed on attempt {attempt + 1}: {str(e)}"
            if attempt < max_retries:
                print(f"❌ {error_msg}")
                print("🔄 Retrying...")
                continue
            else:
                return f"❌ Error executing swap after {max_retries + 1} attempts: {str(e)}"
    
    return f"❌ All {max_retries + 1} swap attempts failed. Please try again later or adjust parameters."


async def check_token_allowance_status(chain_id: str, token_contract_address: str, 
                                     owner_address: str, spender_address: str) -> str:
    """Check current token allowance for a spender address. (Utility function for debugging)"""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    if chain_id not in RPC_URLS:
        return f"❌ Unsupported chain ID: {chain_id}. Supported chains: {', '.join(RPC_URLS.keys())}"
    
    try:
        # Get Web3 connection
        web3 = get_web3_connection(chain_id)
        if not web3:
            return f"❌ Failed to connect to blockchain network for chain {chain_id}"
        
        # Check allowance
        allowance = await check_token_allowance(chain_id, token_contract_address, owner_address, spender_address, web3)
        
        # Get token info for better display
        token_info = get_token_info(web3, token_contract_address)
        
        # Convert allowance to human readable format
        allowance_readable = format_readable_amount(str(allowance), token_info['decimals'], token_info['symbol'])
        
        # Determine allowance status
        if allowance == 0:
            status = "❌ NO ALLOWANCE"
            recommendation = "You need to approve this token before swapping."
        elif allowance >= 2**256 - 1:  # Max uint256 (unlimited approval)
            status = "✅ UNLIMITED ALLOWANCE"
            recommendation = "Token has unlimited approval - no further approval needed."
        else:
            status = "⚠️ LIMITED ALLOWANCE"
            recommendation = "Token has limited approval - may need additional approval for large swaps."
        
        return f"""
📊 TOKEN ALLOWANCE STATUS

=== TOKEN INFORMATION ===
Token: {token_info['symbol']} ({token_info['name']})
Contract: {token_contract_address}
Chain: {CHAIN_NAMES.get(chain_id, chain_id)}
Decimals: {token_info['decimals']}

=== ALLOWANCE DETAILS ===
Owner: {owner_address}
Spender: {spender_address}
Current Allowance: {allowance_readable}
Raw Allowance: {allowance}
Status: {status}

=== RECOMMENDATION ===
{recommendation}

💡 Token approvals are handled automatically during swaps.
"""
    
    except Exception as e:
        return f"❌ Error checking token allowance: {str(e)}"


def register_same_chain_swap_tools(mcp):
    """Register same-chain swap related MCP tools."""
    
    @mcp.tool()
    async def execute_dex_swap_tool(from_token: str, to_token: str, amount: str, chain_id: str, 
                                   user_wallet_address: str, private_key: str, slippage: str = "0.5") -> str:
        """Execute a DEX token swap using OKX API and broadcast the transaction to the blockchain.
        Includes automatic retry logic with progressive slippage increase and automatic token approval handling.

        Args:
            from_token: From token contract address
            to_token: To token contract address  
            amount: Amount to swap (in token units)
            chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
            user_wallet_address: User's wallet address for the swap
            private_key: Private key for signing the transaction (without 0x prefix)
            slippage: Slippage tolerance (e.g., "0.5" for 0.5%, default: "0.5")
        """
        return await execute_dex_swap(from_token, to_token, amount, chain_id, user_wallet_address, private_key, slippage)
    
    @mcp.tool()
    async def check_token_allowance_status_tool(chain_id: str, token_contract_address: str, 
                                               owner_address: str, spender_address: str) -> str:
        """Check current token allowance for a spender address. (Debugging utility)

        Args:
            chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
            token_contract_address: Token contract address to check
            owner_address: Token owner's wallet address
            spender_address: Spender's address (usually DEX router)
        """
        return await check_token_allowance_status(chain_id, token_contract_address, owner_address, spender_address) 