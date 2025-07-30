"""
Cross-chain DEX swap execution operations.
"""

from ..utils.constants import (
    OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE, 
    RPC_URLS, EXPLORER_URLS, CHAIN_NAMES
)
from ..utils.okx_client import make_okx_request
from ..utils.blockchain import get_web3_connection, validate_private_key, build_transaction


async def execute_cross_chain_swap(from_chain: str, to_chain: str, from_token: str, to_token: str, 
                                  amount: str, user_wallet_address: str, private_key: str, slippage: str = "0.5") -> str:
    """Execute a cross-chain DEX token swap using OKX API."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    if from_chain not in RPC_URLS:
        return f"❌ Unsupported source chain ID: {from_chain}. Supported chains: {', '.join(RPC_URLS.keys())}"
    
    try:
        # Initialize Web3 connection for source chain
        web3 = get_web3_connection(from_chain)
        if not web3:
            return f"❌ Failed to connect to source blockchain network for chain {from_chain}"
        
        # Validate private key and wallet address
        validation = validate_private_key(private_key, user_wallet_address)
        if not validation['valid']:
            return f"❌ {validation['error']}"
        
        private_key = validation['private_key']
        
        # Try multiple cross-chain swap endpoints
        endpoints = [
            "/api/v5/dex/cross-chain/build-tx",
            "/api/v5/dex/aggregator/cross-chain/swap",
            "/api/v5/dex/cross-chain/swap"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{OKX_API_BASE}{endpoint}"
                params = [
                    f"fromChainId={from_chain}",
                    f"toChainId={to_chain}",
                    f"fromTokenAddress={from_token}",
                    f"toTokenAddress={to_token}",
                    f"amount={amount}",
                    f"userWalletAddress={user_wallet_address}",
                    f"slippage={slippage}"
                ]
                full_url = f"{url}?{'&'.join(params)}"
                
                print(f"🔍 Trying cross-chain endpoint: {endpoint}")
                data = await make_okx_request(full_url)

                if not data:
                    print(f"❌ No response from {endpoint}")
                    continue

                if data.get("code") != "0":
                    error_msg = data.get('msg', 'Unknown error')
                    print(f"❌ API Error from {endpoint}: {error_msg}")
                    continue

                if not data.get("data"):
                    print(f"❌ No data from {endpoint}")
                    continue

                # Successfully got swap data
                swap_info = data["data"][0] if isinstance(data["data"], list) else data["data"]
                tx_data = swap_info.get('tx', {})
                
                if not tx_data:
                    print(f"❌ No transaction data from {endpoint}")
                    continue
                
                # Extract transaction details
                router_result = swap_info.get('routerResult', {})
                from_token_info = router_result.get('fromToken', {})
                to_token_info = router_result.get('toToken', {})
                
                # Build and execute transaction for source chain
                transaction = build_transaction(tx_data, from_chain, user_wallet_address, web3)
                
                # Sign and send the transaction
                signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                tx_hash_hex = tx_hash.hex()
                
                # Wait for transaction receipt
                try:
                    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
                    
                    if receipt.status == 1:
                        # Get explorer URLs
                        source_explorer = f"{EXPLORER_URLS.get(from_chain, '')}{tx_hash_hex}"
                        
                        # Get chain names
                        from_chain_name = CHAIN_NAMES.get(from_chain, f"Chain {from_chain}")
                        to_chain_name = CHAIN_NAMES.get(to_chain, f"Chain {to_chain}")
                        
                        return f"""
✅ CROSS-CHAIN SWAP INITIATED SUCCESSFULLY!

=== SWAP DETAILS ===
Route: {from_chain_name} → {to_chain_name}
From Token: {from_token_info.get('tokenSymbol', 'Unknown')}
To Token: {to_token_info.get('tokenSymbol', 'Unknown')}
Bridge Provider: {swap_info.get('bridgeProvider', 'OKX DEX')}

=== SOURCE CHAIN TRANSACTION ===
Chain: {from_chain_name} (ID: {from_chain})
Transaction Hash: {tx_hash_hex}
Block Number: {receipt.blockNumber}
Gas Used: {receipt.gasUsed:,}
Status: SUCCESS ✅

=== BRIDGE INFORMATION ===
Estimated Bridge Time: {swap_info.get('estimatedTime', 'N/A')} seconds
Bridge Fee: {swap_info.get('bridgeFee', 'N/A')}
Destination Chain: {to_chain_name} (ID: {to_chain})

=== EXPLORER LINKS ===
Source Transaction: {source_explorer}

🌉 Your cross-chain swap has been initiated!
⏳ Please wait for the bridge to complete the transfer to {to_chain_name}.
💡 You can track the bridge progress using the transaction hash above.

Note: Cross-chain swaps typically take 5-30 minutes depending on the bridge and network congestion.
"""
                    else:
                        return f"""
❌ CROSS-CHAIN SWAP FAILED

Transaction Hash: {tx_hash_hex}
Status: FAILED
Block Number: {receipt.blockNumber}
Gas Used: {receipt.gasUsed:,}

The transaction was mined but failed during execution.
Please check the transaction on the block explorer for more details.
"""
                        
                except Exception as e:
                    return f"""
⏳ CROSS-CHAIN SWAP SUBMITTED BUT CONFIRMATION PENDING

Transaction Hash: {tx_hash_hex}
Status: PENDING

The transaction has been submitted but confirmation is taking longer than expected.
You can check the status manually using the transaction hash above.

Error details: {str(e)}
"""
                
            except Exception as e:
                print(f"❌ Error with cross-chain endpoint {endpoint}: {str(e)}")
                continue
        
        # If all cross-chain endpoints failed, suggest alternative approach
        return f"""❌ CROSS-CHAIN SWAP NOT AVAILABLE

Unable to execute cross-chain swap from chain {from_chain} to {to_chain}.

💡 ALTERNATIVE APPROACH:
1. First, get a regular quote on {from_chain} to swap to a bridge token (USDC/USDT)
2. Use a separate bridge service to move the stable token to chain {to_chain}
3. Then swap the stable token to your target token on chain {to_chain}

This multi-step approach often provides better rates and more reliable execution.

Would you like me to help you with step 1 - swapping to a bridge token on {from_chain}?
"""
    
    except Exception as e:
        return f"❌ Error executing cross-chain swap: {str(e)}"


def register_cross_chain_swap_tools(mcp):
    """Register cross-chain swap related MCP tools."""
    
    @mcp.tool()
    async def execute_cross_chain_swap_tool(from_chain: str, to_chain: str, from_token: str, to_token: str, 
                                           amount: str, user_wallet_address: str, private_key: str, slippage: str = "0.5") -> str:
        """Execute a cross-chain DEX token swap using OKX API.

        Args:
            from_chain: Source chain ID
            to_chain: Destination chain ID
            from_token: From token contract address
            to_token: To token contract address
            amount: Amount to swap (in token units)
            user_wallet_address: User's wallet address for the swap
            private_key: Private key for signing the transaction (without 0x prefix)
            slippage: Slippage tolerance (e.g., "0.5" for 0.5%, default: "0.5")
        """
        return await execute_cross_chain_swap(from_chain, to_chain, from_token, to_token, amount, user_wallet_address, private_key, slippage)