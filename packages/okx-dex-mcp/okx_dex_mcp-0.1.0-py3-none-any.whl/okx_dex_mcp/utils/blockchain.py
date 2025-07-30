"""
Blockchain utilities for Web3 operations, token approvals, and allowance checks.
"""

from web3 import Web3
from eth_account import Account
from typing import Dict, Optional

from .constants import RPC_URLS, NATIVE_TOKENS, DEFAULT_GAS_PRICES
from .okx_client import make_okx_request
from ..utils.constants import OKX_API_BASE


def get_web3_connection(chain_id: str) -> Optional[Web3]:
    """Get Web3 connection for a specific chain with backup RPC endpoints."""
    if chain_id not in RPC_URLS:
        return None
    
    # Try to connect to Web3 with backup RPC endpoints
    for rpc_url in RPC_URLS[chain_id]:
        try:
            web3 = Web3(Web3.HTTPProvider(rpc_url))
            if web3.is_connected():
                return web3
        except Exception:
            continue
    
    return None


def validate_private_key(private_key: str, wallet_address: str) -> Dict[str, any]:
    """Validate private key and wallet address match."""
    try:
        if private_key.startswith('0x'):
            private_key = private_key[2:]
        account = Account.from_key(private_key)
        if account.address.lower() != wallet_address.lower():
            return {'valid': False, 'error': 'Private key does not match the provided wallet address'}
        return {'valid': True, 'account': account, 'private_key': private_key}
    except Exception as e:
        return {'valid': False, 'error': f'Invalid private key: {str(e)}'}


def is_native_token(token_address: str, chain_id: str) -> bool:
    """Check if the token is a native token (ETH, BNB, MATIC, etc.)."""
    return token_address.lower() == NATIVE_TOKENS.get(chain_id, "").lower()


async def check_token_allowance(chain_id: str, token_address: str, owner_address: str, spender_address: str, web3: Web3) -> int:
    """Check current token allowance for a spender."""
    try:
        # Convert addresses to checksum format
        token_address = web3.to_checksum_address(token_address)
        owner_address = web3.to_checksum_address(owner_address)
        spender_address = web3.to_checksum_address(spender_address)
        
        # ERC-20 allowance function ABI
        allowance_abi = [
            {
                "constant": True,
                "inputs": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"}
                ],
                "name": "allowance",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        # Create contract instance
        contract = web3.eth.contract(address=token_address, abi=allowance_abi)
        
        # Call allowance function
        allowance = contract.functions.allowance(owner_address, spender_address).call()
        return allowance
        
    except Exception as e:
        print(f"Error checking allowance: {str(e)}")
        return 0


async def execute_token_approval(chain_id: str, token_contract_address: str, approve_amount: str, user_wallet_address: str, private_key: str, web3: Web3) -> Dict[str, any]:
    """Execute token approval transaction."""
    try:
        # Get approval transaction data
        base_url = f"{OKX_API_BASE}/api/v5/dex/aggregator/approve-transaction"
        params = [
            f"chainId={chain_id}",
            f"tokenContractAddress={token_contract_address}",
            f"approveAmount={approve_amount}"
        ]
        full_url = f"{base_url}?{'&'.join(params)}"
        
        data = await make_okx_request(full_url)
        
        if not data or data.get("code") != "0" or not data.get("data"):
            return {'success': False, 'tx_hash': '', 'error': 'Failed to get approval transaction data'}
        
        approval_data = data["data"][0] if isinstance(data["data"], list) else data["data"]
        
        # Prepare approval transaction
        nonce = web3.eth.get_transaction_count(user_wallet_address)
        
        approval_tx = {
            'to': approval_data.get('dexContractAddress'),
            'value': 0,  # Approval transactions don't send ETH
            'gas': int(approval_data.get('gasLimit', '100000')),
            'nonce': nonce,
            'data': approval_data.get('data', '0x'),
            'chainId': int(chain_id),
        }
        
        # Handle gas pricing
        if approval_data.get('gasPrice'):
            approval_tx['gasPrice'] = int(approval_data['gasPrice'])
        else:
            approval_tx['gasPrice'] = web3.eth.gas_price
        
        # Sign and send approval transaction
        signed_approval = web3.eth.account.sign_transaction(approval_tx, private_key)
        approval_hash = web3.eth.send_raw_transaction(signed_approval.raw_transaction)
        approval_hash_hex = approval_hash.hex()
        
        # Wait for approval confirmation
        approval_receipt = web3.eth.wait_for_transaction_receipt(approval_hash, timeout=120)
        
        if approval_receipt.status == 1:
            return {'success': True, 'tx_hash': approval_hash_hex, 'error': ''}
        else:
            return {'success': False, 'tx_hash': approval_hash_hex, 'error': 'Approval transaction failed'}
            
    except Exception as e:
        return {'success': False, 'tx_hash': '', 'error': f'Approval error: {str(e)}'}


def get_token_info(web3: Web3, token_address: str) -> Dict[str, any]:
    """Get token information (symbol, decimals, name)."""
    try:
        # Convert to checksum address
        token_address = web3.to_checksum_address(token_address)
        
        # ERC-20 token info ABI
        token_abi = [
            {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"}
        ]
        
        contract = web3.eth.contract(address=token_address, abi=token_abi)
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        name = contract.functions.name().call()
        
        return {
            'success': True,
            'symbol': symbol,
            'decimals': decimals,
            'name': name
        }
        
    except Exception as e:
        return {
            'success': False,
            'symbol': 'Unknown',
            'decimals': 18,
            'name': 'Unknown Token',
            'error': str(e)
        }


def build_transaction(tx_data: Dict[str, any], chain_id: str, user_wallet_address: str, web3: Web3) -> Dict[str, any]:
    """Build a transaction object with proper gas handling."""
    nonce = web3.eth.get_transaction_count(user_wallet_address)
    
    # Build transaction object with improved gas handling
    gas_limit = int(tx_data.get('gas', '0'))
    if gas_limit == 0:
        gas_limit = 200000  # Default gas limit
    
    transaction = {
        'to': tx_data.get('to'),
        'value': int(tx_data.get('value', '0')),
        'gas': int(gas_limit * 1.5),  # Increase gas limit by 50%
        'nonce': nonce,
        'data': tx_data.get('data', '0x'),
        'chainId': int(chain_id),  # Add chain ID for EIP-155 replay protection
    }
    
    # Handle gas pricing - use EIP-1559 if available, otherwise legacy
    if 'maxFeePerGas' in tx_data and 'maxPriorityFeePerGas' in tx_data:
        # EIP-1559 transaction
        transaction['maxFeePerGas'] = int(tx_data['maxFeePerGas'])
        transaction['maxPriorityFeePerGas'] = int(tx_data['maxPriorityFeePerGas'])
    elif 'gasPrice' in tx_data:
        # Legacy transaction
        transaction['gasPrice'] = int(tx_data['gasPrice'])
    else:
        # Fallback: get current gas price from network
        try:
            gas_price = web3.eth.gas_price
            transaction['gasPrice'] = gas_price
        except:
            # If gas price fetch fails, use a reasonable default
            transaction['gasPrice'] = DEFAULT_GAS_PRICES.get(chain_id, 20000000000)
    
    return transaction 