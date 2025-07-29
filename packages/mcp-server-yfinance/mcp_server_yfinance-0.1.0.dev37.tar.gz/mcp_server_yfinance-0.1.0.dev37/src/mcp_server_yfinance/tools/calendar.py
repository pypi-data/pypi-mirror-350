"""Calendar and events tools."""

import json

import yfinance as yf
from mcp.server import FastMCP


def register_calendar_tools(mcp: FastMCP):
    """Register calendar tools with the MCP server."""

    @mcp.tool()
    async def get_earnings_calendar(ticker: str) -> str:
        """Get earnings calendar information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing earnings calendar data
        """
        stock = yf.Ticker(ticker)
        calendar = stock.calendar
        if calendar is not None and not calendar.empty:
            return calendar.to_json(date_format="iso")
        return json.dumps({"error": "No earnings calendar data available"})

    @mcp.tool()
    async def get_earnings_dates(ticker: str) -> str:
        """Get upcoming and past earnings dates.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing earnings dates
        """
        stock = yf.Ticker(ticker)
        info = stock.info

        earnings_info = {
            "earningsDate": info.get("earningsDate"),
            "exDividendDate": info.get("exDividendDate"),
            "dividendDate": info.get("dividendDate"),
            "lastEarningsDate": info.get("lastEarningsDate"),
        }

        return json.dumps(earnings_info, indent=2, default=str)

    @mcp.tool()
    async def get_market_calendar_info(ticker: str) -> str:
        """Get market calendar information for a stock.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing market calendar info
        """
        stock = yf.Ticker(ticker)
        info = stock.info

        market_info = {
            "exchange": info.get("exchange"),
            "exchangeTimezoneName": info.get("exchangeTimezoneName"),
            "exchangeTimezoneShortName": info.get("exchangeTimezoneShortName"),
            "gmtOffSetMilliseconds": info.get("gmtOffSetMilliseconds"),
            "market": info.get("market"),
            "marketState": info.get("marketState"),
            "regularMarketTime": info.get("regularMarketTime"),
            "regularMarketPreviousClose": info.get("regularMarketPreviousClose"),
            "preMarketPrice": info.get("preMarketPrice"),
            "preMarketTime": info.get("preMarketTime"),
            "postMarketPrice": info.get("postMarketPrice"),
            "postMarketTime": info.get("postMarketTime"),
        }

        return json.dumps(market_info, indent=2, default=str)
