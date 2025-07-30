"""
Same-chain DEX quote operations.
"""

from ..utils.constants import OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE
from ..utils.okx_client import make_okx_request
from ..utils.formatters import format_dex_quote, get_slippage_recommendation


async def get_dex_quote(from_token: str, to_token: str, amount: str, chain_id: str) -> str:
    """Get a DEX trading quote for token swap with improved slippage recommendations."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    # Build URL for quote endpoint
    base_url = f"{OKX_API_BASE}/api/v5/dex/aggregator/quote"
    params = [
        f"chainId={chain_id}",
        f"fromTokenAddress={from_token}",
        f"toTokenAddress={to_token}",
        f"amount={amount}"
    ]
    full_url = f"{base_url}?{'&'.join(params)}"
    
    data = await make_okx_request(full_url)

    if not data:
        return f"❌ Unable to get quote for {from_token} -> {to_token}."

    if data.get("code") != "0":
        return f"❌ API Error: {data.get('msg', 'Unknown error')}"

    if not data.get("data"):
        return "❌ No quote data available for this token pair."

    quote_info = data["data"][0] if isinstance(data["data"], list) else data["data"]
    
    # Enhanced quote formatting with slippage recommendations
    formatted_quote = format_dex_quote(quote_info)
    slippage_guidance = get_slippage_recommendation(quote_info)
    
    return formatted_quote + slippage_guidance


async def get_token_approval_transaction(chain_id: str, token_contract_address: str, approve_amount: str) -> str:
    """Get token approval transaction data for DEX operations. (Internal utility function)"""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    # Build URL for approval endpoint
    base_url = f"{OKX_API_BASE}/api/v5/dex/aggregator/approve-transaction"
    params = [
        f"chainId={chain_id}",
        f"tokenContractAddress={token_contract_address}",
        f"approveAmount={approve_amount}"
    ]
    full_url = f"{base_url}?{'&'.join(params)}"
    
    data = await make_okx_request(full_url)

    if not data:
        return f"❌ Unable to get approval transaction data for token {token_contract_address}."

    if data.get("code") != "0":
        return f"❌ API Error: {data.get('msg', 'Unknown error')}"

    if not data.get("data"):
        return "❌ No approval transaction data available."

    approval_data = data["data"][0] if isinstance(data["data"], list) else data["data"]
    
    return f"""✅ TOKEN APPROVAL TRANSACTION DATA

=== APPROVAL DETAILS ===
Chain ID: {chain_id}
Token Contract: {token_contract_address}
Approve Amount: {approve_amount}
DEX Contract: {approval_data.get('dexContractAddress', 'N/A')}
Gas Limit: {approval_data.get('gasLimit', 'N/A')}
Gas Price: {approval_data.get('gasPrice', 'N/A')} wei

=== TRANSACTION DATA ===
Data: {approval_data.get('data', 'N/A')[:100]}...

💡 This approval transaction must be executed before performing the token swap.
"""


def register_same_chain_quote_tools(mcp):
    """Register same-chain quote related MCP tools."""
    
    @mcp.tool()
    async def get_dex_quote_tool(from_token: str, to_token: str, amount: str, chain_id: str) -> str:
        """Get a DEX trading quote for token swap with improved slippage recommendations.

        Args:
            from_token: From token contract address
            to_token: To token contract address  
            amount: Amount to swap (in token units)
            chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
        """
        return await get_dex_quote(from_token, to_token, amount, chain_id) 