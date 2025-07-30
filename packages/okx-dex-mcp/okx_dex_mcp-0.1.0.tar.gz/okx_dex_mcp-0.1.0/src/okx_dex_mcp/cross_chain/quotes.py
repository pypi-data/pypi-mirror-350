"""
Cross-chain DEX quote operations.
"""

from ..utils.constants import (
    OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_API_BASE, 
    CHAIN_NAMES, BRIDGE_TOKENS
)
from ..utils.okx_client import make_okx_request
from ..same_chain.quotes import get_dex_quote


async def get_cross_chain_quote(from_chain: str, to_chain: str, from_token: str, to_token: str, amount: str) -> str:
    """Get a cross-chain DEX trading quote."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    # Try multiple cross-chain endpoints
    endpoints = [
        "/api/v5/dex/cross-chain/quote",
        "/api/v5/dex/aggregator/cross-chain/quote",
        "/api/v5/dex/cross-chain/build-tx"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{OKX_API_BASE}{endpoint}"
            params = [
                f"fromChainId={from_chain}",
                f"toChainId={to_chain}",
                f"fromTokenAddress={from_token}",
                f"toTokenAddress={to_token}",
                f"amount={amount}"
            ]
            full_url = f"{url}?{'&'.join(params)}"
            
            print(f"🔍 Trying endpoint: {endpoint}")
            data = await make_okx_request(full_url)

            if not data:
                print(f"❌ No response from {endpoint}")
                continue

            if data.get("code") != "0":
                error_msg = data.get('msg', 'Unknown error')
                print(f"❌ API Error from {endpoint}: {error_msg}")
                
                # If it's a specific error about cross-chain not being supported, try alternative approach
                if "not support" in error_msg.lower() or "invalid" in error_msg.lower():
                    continue
                else:
                    return f"❌ API Error: {error_msg}"

            if not data.get("data"):
                print(f"❌ No data from {endpoint}")
                continue

            # Successfully got data
            quote_info = data["data"][0] if isinstance(data["data"], list) else data["data"]
            
            # Enhanced formatting for cross-chain quote
            from_token_info = quote_info.get('fromToken', {})
            to_token_info = quote_info.get('toToken', {})
            
            # Calculate readable amounts
            from_amount = quote_info.get('fromTokenAmount', amount)
            to_amount = quote_info.get('toTokenAmount', 'N/A')
            from_decimals = int(from_token_info.get('decimal', 18))
            to_decimals = int(to_token_info.get('decimal', 18))
            
            if from_amount != 'N/A':
                try:
                    from_amount_readable = f"{int(from_amount) / (10 ** from_decimals):.6f}"
                except:
                    from_amount_readable = str(from_amount)
            else:
                from_amount_readable = 'N/A'
                
            if to_amount != 'N/A':
                try:
                    to_amount_readable = f"{int(to_amount) / (10 ** to_decimals):.6f}"
                except:
                    to_amount_readable = str(to_amount)
            else:
                to_amount_readable = 'N/A'
            
            from_chain_name = CHAIN_NAMES.get(from_chain, f"Chain {from_chain}")
            to_chain_name = CHAIN_NAMES.get(to_chain, f"Chain {to_chain}")
            
            result = f"""✅ CROSS-CHAIN DEX QUOTE FOUND

=== ROUTE DETAILS ===
From: {from_chain_name} (Chain ID: {from_chain})
To: {to_chain_name} (Chain ID: {to_chain})

=== TOKEN DETAILS ===
From Token: {from_token_info.get('tokenSymbol', 'Unknown')} (${from_token_info.get('tokenUnitPrice', 'N/A')})
To Token: {to_token_info.get('tokenSymbol', 'Unknown')} (${to_token_info.get('tokenUnitPrice', 'N/A')})

=== SWAP AMOUNTS ===
Input: {from_amount_readable} {from_token_info.get('tokenSymbol', '')}
Output: {to_amount_readable} {to_token_info.get('tokenSymbol', '')}

=== FEES & TIMING ===
Bridge Fee: {quote_info.get('bridgeFee', 'N/A')}
Gas Fee: {quote_info.get('gasFee', 'N/A')}
Estimated Time: {quote_info.get('estimatedTime', 'N/A')} seconds
Price Impact: {quote_info.get('priceImpactPercentage', 'N/A')}%

=== ADDITIONAL INFO ===
Route: {quote_info.get('routeType', 'Standard')}
Provider: {quote_info.get('bridgeProvider', 'OKX DEX')}
Endpoint Used: {endpoint}

💡 This quote is for cross-chain swapping. The tokens will be bridged between chains.
"""
            
            return result
            
        except Exception as e:
            print(f"❌ Error with endpoint {endpoint}: {str(e)}")
            continue
    
    # If all endpoints failed, try a fallback approach using regular quotes on each chain
    print("🔄 Trying fallback approach with individual chain quotes...")
    
    try:
        # Get quote on source chain
        from_quote = await get_dex_quote(from_token, from_token, amount, from_chain)  # Same token to get price
        to_quote = await get_dex_quote(to_token, to_token, "1000000", to_chain)  # Same token to get price
        
        if "❌" not in from_quote and "❌" not in to_quote:
            return f"""⚠️ DIRECT CROSS-CHAIN QUOTE NOT AVAILABLE

However, here's what we found:

=== SOURCE CHAIN ({from_chain}) ===
{from_quote[:300]}...

=== DESTINATION CHAIN ({to_chain}) ===
{to_quote[:300]}...

💡 SUGGESTED APPROACH:
1. Swap {from_token} to a bridge token (like USDC/USDT) on chain {from_chain}
2. Bridge the stable token from chain {from_chain} to chain {to_chain}
3. Swap the stable token to {to_token} on chain {to_chain}

This multi-step approach often provides better rates and liquidity for cross-chain swaps.
"""
    except Exception as e:
        pass
    
    return f"""❌ CROSS-CHAIN QUOTE UNAVAILABLE

Unable to fetch cross-chain quote from chain {from_chain} to {to_chain}.

This could be due to:
• Limited cross-chain liquidity for this token pair
• Unsupported bridge routes between these chains
• Temporary API issues

💡 ALTERNATIVES:
1. Try swapping on the same chain where the token has better liquidity
2. Use a multi-step approach: swap → bridge → swap
3. Check if both tokens are available on a single chain with good liquidity

Supported chains: Ethereum (1), BSC (56), Polygon (137), Avalanche (43114), Arbitrum (42161), Optimism (10), Base (8453)
"""


async def get_bridge_token_suggestions(chain_id: str) -> str:
    """Get suggested bridge tokens for cross-chain swaps on a specific chain."""
    if not all([OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE]):
        return "❌ OKX API credentials not configured. Please set OKX_API_KEY, OKX_SECRET_KEY, and OKX_PASSPHRASE in .env file."
    
    chain_name = CHAIN_NAMES.get(chain_id, f"Chain {chain_id}")
    tokens = BRIDGE_TOKENS.get(chain_id, {})
    
    if not tokens:
        return f"""❌ No bridge token suggestions available for chain {chain_id}.

Supported chains for bridge tokens:
• Ethereum (1)
• BSC (56) 
• Polygon (137)
• Avalanche (43114)
• Arbitrum (42161)
• Optimism (10)
• Base (8453)
"""
    
    result = f"""🌉 BRIDGE TOKEN SUGGESTIONS FOR {chain_name.upper()}

These tokens typically have the best cross-chain liquidity and bridge support:

"""
    
    # Try to get current prices and liquidity for each bridge token
    for symbol, address in tokens.items():
        try:
            # Get a small quote to check if the token is active
            quote_result = await get_dex_quote(address, address, "1000000", chain_id)
            if "❌" not in quote_result and "API Error" not in quote_result:
                result += f"✅ {symbol}\n"
                result += f"   Address: {address}\n"
                result += f"   Status: Active with good liquidity\n\n"
            else:
                result += f"⚠️  {symbol}\n"
                result += f"   Address: {address}\n"
                result += f"   Status: Limited liquidity\n\n"
        except:
            result += f"📍 {symbol}\n"
            result += f"   Address: {address}\n"
            result += f"   Status: Available (liquidity check failed)\n\n"
    
    result += f"""💡 BRIDGE STRATEGY RECOMMENDATIONS:

1. **USDC/USDT**: Best for stable value transfers
   - Widely supported across all major bridges
   - Minimal price volatility during bridge time
   - High liquidity on most chains

2. **Native Wrapped Tokens**: Good for specific chains
   - WETH for Ethereum-based chains
   - WMATIC for Polygon
   - WAVAX for Avalanche

3. **Multi-Step Approach**:
   - Swap your token → Bridge token (on source chain)
   - Bridge the bridge token → Destination chain  
   - Bridge token → Target token (on destination chain)

🔗 Popular Bridge Services:
• Stargate (LayerZero)
• Multichain (Anyswap)
• Hop Protocol
• Synapse Protocol
• Across Protocol

Note: Always verify bridge token addresses and use reputable bridge services.
"""
    
    return result


def register_cross_chain_quote_tools(mcp):
    """Register cross-chain quote related MCP tools."""
    
    @mcp.tool()
    async def get_cross_chain_quote_tool(from_chain: str, to_chain: str, from_token: str, to_token: str, amount: str) -> str:
        """Get a cross-chain DEX trading quote.

        Args:
            from_chain: Source chain ID
            to_chain: Destination chain ID
            from_token: From token contract address
            to_token: To token contract address
            amount: Amount to swap
        """
        return await get_cross_chain_quote(from_chain, to_chain, from_token, to_token, amount)
    
    @mcp.tool()
    async def get_bridge_token_suggestions_tool(chain_id: str) -> str:
        """Get suggested bridge tokens for cross-chain swaps on a specific chain.

        Args:
            chain_id: Chain ID to get bridge token suggestions for
        """
        return await get_bridge_token_suggestions(chain_id) 