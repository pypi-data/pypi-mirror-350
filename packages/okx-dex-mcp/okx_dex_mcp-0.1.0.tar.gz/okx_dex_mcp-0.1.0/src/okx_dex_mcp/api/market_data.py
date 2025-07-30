"""
Market data and token information from OKX DEX API.
"""

from ..utils.constants import OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE
from ..utils.okx_client import make_okx_request
from ..utils.formatters import format_chain_tokens


async def get_supported_dex_chains() -> str:
    """Get list of supported chains for DEX operations."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    url = f"{OKX_API_BASE}/api/v5/dex/aggregator/supported/chain"
    data = await make_okx_request(url)

    if not data:
        return "Unable to fetch supported DEX chains."

    if data.get("code") != "0":
        return f"API Error: {data.get('msg', 'Unknown error')}"

    chains = data.get("data", [])
    if not chains:
        return "No supported chains found."

    result = "Supported DEX Chains:\n\n"
    for chain in chains:
        chain_id = chain.get('chainId', 'Unknown')
        chain_name = chain.get('chainName', 'Unknown')
        
        result += f"• {chain_name} (ID: {chain_id})\n"
    
    return result


async def get_chain_top_tokens(chain_id: str, limit: int = 20) -> str:
    """Get top tokens by market cap on a specific chain."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    if limit > 50:
        limit = 50
        
    url = f"{OKX_API_BASE}/api/v5/dex/aggregator/all-tokens?chainId={chain_id}&limit={limit}"
    data = await make_okx_request(url)

    if not data:
        return f"Unable to fetch top tokens for chain {chain_id}."

    if data.get("code") != "0":
        return f"API Error: {data.get('msg', 'Unknown error')}"

    tokens = data.get("data", [])
    if not tokens:
        return f"No tokens found for chain {chain_id}."

    return format_chain_tokens(tokens, chain_id)


async def search_dex_tokens(query: str, chain_id: str = "") -> str:
    """Search for DEX tokens by name or symbol."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    # Try multiple popular chains if no specific chain is provided
    chains_to_search = [chain_id] if chain_id else ["1", "56", "137", "43114"]  # ETH, BSC, Polygon, Avalanche
    
    all_tokens = []
    for chain in chains_to_search:
        url = f"{OKX_API_BASE}/api/v5/dex/aggregator/all-tokens?chainId={chain}&limit=100"
        data = await make_okx_request(url)
        
        if data and data.get("code") == "0" and data.get("data"):
            # Filter tokens that match the query
            matching_tokens = [
                token for token in data["data"]
                if query.lower() in token.get('tokenSymbol', '').lower() or 
                   query.lower() in token.get('tokenName', '').lower()
            ]
            all_tokens.extend(matching_tokens)
    
    if not all_tokens:
        return f"No DEX tokens found matching: {query}"
    
    # Remove duplicates and sort by market cap
    unique_tokens = []
    seen_addresses = set()
    for token in all_tokens:
        addr = token.get('tokenContractAddress', '')
        if addr not in seen_addresses:
            seen_addresses.add(addr)
            unique_tokens.append(token)
    
    result = f"DEX tokens matching '{query}' ({len(unique_tokens)} found):\n\n"
    
    for i, token in enumerate(unique_tokens[:10]):  # Top 10 results
        symbol = token.get('tokenSymbol', 'N/A')
        name = token.get('tokenName', 'N/A')
        address = token.get('tokenContractAddress', 'N/A')
        chain = token.get('chainId', 'Unknown')
        
        result += f"--- Result {i+1} ---\n"
        result += f"Token: {symbol} ({name})\n"
        result += f"Contract Address: {address}\n"
        result += f"Chain ID: {chain}\n\n"
    
    return result


async def get_dex_market_summary(token_query: str, chain_id: str = "1") -> str:
    """Get a comprehensive DEX market summary for a token."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    # First search for the token
    search_results = await search_dex_tokens(token_query, chain_id)
    
    if "No DEX tokens found" in search_results:
        return search_results
    
    # Try to get additional chain information
    chains_info = await get_supported_dex_chains()
    
    result = f"=== DEX MARKET SUMMARY FOR {token_query.upper()} ===\n\n"
    result += "TOKEN SEARCH RESULTS:\n"
    result += search_results + "\n"
    result += "=" * 60 + "\n\n"
    result += "AVAILABLE CHAINS:\n"
    result += chains_info[:500] + "..." if len(chains_info) > 500 else chains_info
    
    return result


def register_market_data_tools(mcp):
    """Register market data related MCP tools."""
    
    @mcp.tool()
    async def get_supported_dex_chains_tool() -> str:
        """Get list of supported chains for DEX operations."""
        return await get_supported_dex_chains()
    
    @mcp.tool()
    async def get_chain_top_tokens_tool(chain_id: str, limit: int = 20) -> str:
        """Get top tokens by market cap on a specific chain.

        Args:
            chain_id: Chain ID (e.g., "1" for Ethereum, "56" for BSC)
            limit: Number of tokens to return (max 50)
        """
        return await get_chain_top_tokens(chain_id, limit)
    
    @mcp.tool()
    async def search_dex_tokens_tool(query: str, chain_id: str = "") -> str:
        """Search for DEX tokens by name or symbol.

        Args:
            query: Search term (token name or symbol)
            chain_id: Optional chain ID to filter results
        """
        return await search_dex_tokens(query, chain_id)
    
    @mcp.tool()
    async def get_dex_market_summary_tool(token_query: str, chain_id: str = "1") -> str:
        """Get a comprehensive DEX market summary for a token.

        Args:
            token_query: Token symbol or name to search for
            chain_id: Chain ID to search on (default: "1" for Ethereum)
        """
        return await get_dex_market_summary(token_query, chain_id) 