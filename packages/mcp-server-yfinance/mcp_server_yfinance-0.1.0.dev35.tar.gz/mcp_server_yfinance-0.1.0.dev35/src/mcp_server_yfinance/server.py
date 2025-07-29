"""MCP Server Markets - YFinance integration"""

from mcp.server import FastMCP

from .tools import (
    register_analyst_data_tools,
    register_calendar_tools,
    register_corporate_actions_tools,
    register_crypto_tools,
    register_extended_market_tools,
    register_financial_statements_tools,
    register_fund_tools,
    register_historical_data_tools,
    register_market_data_tools,
    register_news_tools,
    register_options_tools,
    register_stock_info_tools,
    register_technical_analysis_tools,
)

mcp = FastMCP("Market Data Server", "1.0.0")

# Register all tool modules
register_stock_info_tools(mcp)
register_historical_data_tools(mcp)
register_analyst_data_tools(mcp)
register_financial_statements_tools(mcp)
register_options_tools(mcp)
register_calendar_tools(mcp)
register_market_data_tools(mcp)
register_crypto_tools(mcp)
register_technical_analysis_tools(mcp)
register_corporate_actions_tools(mcp)
register_extended_market_tools(mcp)
register_news_tools(mcp)
register_fund_tools(mcp)


def main():
    """Main function to start the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
