"""
Formatting utilities for DEX data display.
"""

from typing import Dict, List, Any
from .constants import STABLECOINS


def format_dex_quote(quote_data: Dict[str, Any]) -> str:
    """Format DEX quote data into a readable string."""
    try:
        # Extract basic information
        from_token = quote_data.get('fromToken', {})
        to_token = quote_data.get('toToken', {})
        
        # Extract DEX information safely
        dex_router_list = quote_data.get('dexRouterList', [])
        dex_sources = []
        if dex_router_list:
            for router in dex_router_list:
                if isinstance(router, dict):
                    sub_routers = router.get('subRouterList', [])
                    for sub_router in sub_routers:
                        if isinstance(sub_router, dict):
                            dex_protocols = sub_router.get('dexProtocol', [])
                            for protocol in dex_protocols:
                                if isinstance(protocol, dict):
                                    dex_name = protocol.get('dexName', 'Unknown')
                                    percent = protocol.get('percent', '0')
                                    dex_sources.append(f"{dex_name} ({percent}%)")
        
        dex_sources_str = ', '.join(dex_sources) if dex_sources else 'N/A'
        
        # Format amounts for better readability
        from_amount = quote_data.get('fromTokenAmount', 'N/A')
        to_amount = quote_data.get('toTokenAmount', 'N/A')
        from_decimals = int(from_token.get('decimal', 18))
        to_decimals = int(to_token.get('decimal', 18))
        
        # Convert to human readable amounts
        if from_amount != 'N/A':
            from_amount_readable = f"{int(from_amount) / (10 ** from_decimals):.6f}"
        else:
            from_amount_readable = 'N/A'
            
        if to_amount != 'N/A':
            to_amount_readable = f"{int(to_amount) / (10 ** to_decimals):.6f}"
        else:
            to_amount_readable = 'N/A'
        
        return f"""
From Token: {from_token.get('tokenSymbol', 'Unknown')} (${from_token.get('tokenUnitPrice', 'N/A')})
To Token: {to_token.get('tokenSymbol', 'Unknown')} (${to_token.get('tokenUnitPrice', 'N/A')})
Chain: {quote_data.get('chainId', 'Unknown')}
From Amount: {from_amount_readable} {from_token.get('tokenSymbol', '')}
To Amount: {to_amount_readable} {to_token.get('tokenSymbol', '')}
Estimated Gas: {quote_data.get('estimateGasFee', 'N/A')}
Price Impact: {quote_data.get('priceImpactPercentage', 'N/A')}%
Trade Fee: {quote_data.get('tradeFee', 'N/A')}
DEX Sources: {dex_sources_str}
"""
    except Exception as e:
        return f"Error formatting quote data: {str(e)}"


def format_chain_tokens(tokens_data: List[Dict[str, Any]], chain_id: str) -> str:
    """Format chain tokens into a readable string."""
    if not tokens_data:
        return f"No tokens found for chain: {chain_id}."
    
    result = f"Top tokens on chain {chain_id} ({len(tokens_data)} found):\n\n"
    
    for i, token in enumerate(tokens_data[:15]):  # Show top 15 tokens
        symbol = token.get('tokenSymbol', 'N/A')
        name = token.get('tokenName', 'N/A')
        address = token.get('tokenContractAddress', 'N/A')
        
        result += f"{i+1}. {symbol} ({name})\n"
        result += f"   Address: {address}\n\n"
    
    return result


def get_slippage_recommendation(quote_info: Dict[str, Any]) -> str:
    """Get intelligent slippage recommendations based on price impact and token types."""
    try:
        price_impact = float(quote_info.get('priceImpactPercentage', '0').replace('%', ''))
        
        # Determine recommended slippage based on price impact and token volatility
        if abs(price_impact) < 0.1:
            recommended_slippage = "0.5%"
            risk_level = "LOW"
        elif abs(price_impact) < 0.5:
            recommended_slippage = "1.0%"
            risk_level = "MEDIUM"
        elif abs(price_impact) < 1.0:
            recommended_slippage = "2.0%"
            risk_level = "HIGH"
        else:
            recommended_slippage = "3.0%"
            risk_level = "VERY HIGH"
        
        # Check if tokens are stablecoins (lower slippage needed)
        from_symbol = quote_info.get('fromToken', {}).get('tokenSymbol', '').upper()
        to_symbol = quote_info.get('toToken', {}).get('tokenSymbol', '').upper()
        
        is_stable_pair = from_symbol in STABLECOINS and to_symbol in STABLECOINS
        
        if is_stable_pair and abs(price_impact) < 0.5:
            recommended_slippage = "0.3%"
            risk_level = "STABLE"
        
        return f"""
💡 SLIPPAGE RECOMMENDATIONS:
Risk Level: {risk_level}
Recommended Slippage: {recommended_slippage}
Price Impact: {price_impact}%

Slippage Guidelines:
• Stable pairs (USDC/USDT): 0.3-0.5%
• Major tokens (ETH/BTC): 0.5-1.0%
• Altcoins: 1.0-2.0%
• High volatility: 2.0-3.0%

⚠️  Higher price impact requires higher slippage tolerance!
"""
        
    except:
        # Fallback if price impact parsing fails
        return """
💡 SLIPPAGE RECOMMENDATIONS:
• Conservative: 0.5%
• Standard: 1.0%
• Aggressive: 2.0%
• High volatility: 3.0%
"""


def format_readable_amount(amount: str, decimals: int, symbol: str = "") -> str:
    """Convert token amount from wei to human readable format."""
    try:
        if amount == 'N/A' or not amount:
            return 'N/A'
        readable = f"{int(amount) / (10 ** decimals):.6f}"
        return f"{readable} {symbol}".strip()
    except:
        return f"{amount} {symbol}".strip() 