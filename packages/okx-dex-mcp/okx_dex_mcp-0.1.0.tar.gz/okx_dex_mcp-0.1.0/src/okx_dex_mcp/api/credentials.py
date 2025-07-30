"""
OKX API credentials management and validation.
"""

from ..utils.constants import OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE, OKX_SANDBOX
from ..utils.okx_client import make_okx_request


async def check_api_credentials() -> str:
    """Check if OKX API credentials are properly configured."""
    if not OKX_API_KEY:
        return "❌ OKX_API_KEY not found in environment variables"
    if not OKX_SECRET_KEY:
        return "❌ OKX_SECRET_KEY not found in environment variables"
    if not OKX_PASSPHRASE:
        return "❌ OKX_PASSPHRASE not found in environment variables"
    
    # Test API connection with a DEX endpoint
    url = f"{OKX_API_BASE}/api/v5/dex/aggregator/supported/chain"
    data = await make_okx_request(url)
    
    if data and data.get("code") == "0":
        chains_count = len(data.get("data", []))
        return f"✅ OKX API credentials are valid\n📊 Found {chains_count} supported chains\n🔧 Sandbox mode: {'ON' if OKX_SANDBOX else 'OFF'}"
    else:
        error_msg = data.get('msg', 'Unknown error') if data else 'No response'
        return f"❌ API credentials invalid or API error: {error_msg}"


def register_credential_tools(mcp):
    """Register credential-related MCP tools."""
    
    @mcp.tool()
    async def check_api_credentials_tool() -> str:
        """Check if OKX API credentials are properly configured."""
        return await check_api_credentials() 