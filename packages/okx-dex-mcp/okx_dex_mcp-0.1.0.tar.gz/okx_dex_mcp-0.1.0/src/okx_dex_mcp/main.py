#!/usr/bin/env python3
"""
OKX DEX Trading MCP Server
Main entry point for the Model Context Protocol server providing DEX trading capabilities.
"""

import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("okx-dex-quotes")

# Import and register tools
from .api.credentials import register_credential_tools
from .api.market_data import register_market_data_tools
from .same_chain.quotes import register_same_chain_quote_tools
from .same_chain.swaps import register_same_chain_swap_tools
from .cross_chain.quotes import register_cross_chain_quote_tools
from .cross_chain.swaps import register_cross_chain_swap_tools

def register_all_tools():
    """Register all MCP tools with the server."""
    register_credential_tools(mcp)
    register_market_data_tools(mcp)
    register_same_chain_quote_tools(mcp)
    register_same_chain_swap_tools(mcp)
    register_cross_chain_quote_tools(mcp)
    register_cross_chain_swap_tools(mcp)

async def demo_okx_dex_operations():
    """Demonstrate OKX DEX trading operations."""
    from .api.credentials import check_api_credentials
    from .api.market_data import search_dex_tokens, get_dex_market_summary, get_supported_dex_chains, get_chain_top_tokens
    
    print("🔥 OKX DEX Trading MCP Demo")
    print("=" * 50)
    
    # First check API credentials
    print("\n0. Checking API credentials...")
    cred_status = await check_api_credentials()
    print(cred_status)
    
    if "❌" in cred_status:
        print("\n⚠️  Please configure your OKX API credentials in a .env file:")
        print("1. Copy the .env.example file to .env")
        print("2. Fill in your OKX API credentials")
        print("3. Get API keys from: https://www.okx.com/account/my-api")
        return
    
    # Example 1: Get supported chains
    print("\n1. Getting supported DEX chains...")
    chains = await get_supported_dex_chains()
    print(chains[:400] + "..." if len(chains) > 400 else chains)
    
    # Example 2: Search for a popular token
    print("\n2. Searching for USDC tokens...")
    usdc_tokens = await search_dex_tokens("USDC", "1")  # Search on Ethereum
    print(usdc_tokens[:600] + "..." if len(usdc_tokens) > 600 else usdc_tokens)
    
    # Example 3: Get top tokens on Ethereum
    print("\n3. Getting top tokens on Ethereum...")
    eth_tokens = await get_chain_top_tokens("1", 5)  # Top 5 tokens on Ethereum
    print(eth_tokens[:500] + "..." if len(eth_tokens) > 500 else eth_tokens)
    
    # Example 4: Get market summary for ETH
    print("\n4. Getting ETH market summary...")
    eth_summary = await get_dex_market_summary("ETH", "1")
    print(eth_summary[:700] + "..." if len(eth_summary) > 700 else eth_summary)

def main():
    """Main entry point for the MCP server."""
    print("🚀 Starting OKX DEX Trading MCP Server...")
    
    # Register all tools
    register_all_tools()
    
    # Start MCP server
    print("📡 MCP server running on stdio transport...")
    mcp.run(transport='stdio')

def demo_main():
    """Entry point for demo mode."""
    print("Welcome to OKX DEX Trade MCP!")
    print("This project provides tools for:")
    print("• Getting real-time DEX token prices via OKX")
    print("• Searching DEX tokens across multiple chains")
    print("• Getting DEX trading quotes and price impact")
    print("• Cross-chain DEX quote functionality")
    print("• Analyzing top tokens by chain")
    print("\nSupported via OKX DEX API:")
    print("• Ethereum, BSC, Polygon, Avalanche, and more!")
    print("• Comprehensive DEX aggregation data")
    print("• Real-time pricing and liquidity info")
    print("\n📋 Requirements:")
    print("• OKX API credentials (free account at okx.com)")
    print("• .env file with API keys configured")
    
    print("\nRunning OKX DEX operations demo...")
    try:
        asyncio.run(demo_okx_dex_operations())
    except Exception as e:
        print(f"Demo failed: {e}")
        print("This might be due to missing API credentials or internet connection.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_main()
    else:
        main() 