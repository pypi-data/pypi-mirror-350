"""Stock information tools."""

import json
from typing import List

import yfinance as yf
from mcp.server import FastMCP


def register_stock_info_tools(mcp: FastMCP):
    """Register stock information tools with the MCP server."""

    @mcp.tool()
    async def get_stock_info(ticker: str) -> str:
        """Get basic information about a stock.

        Args:
            ticker: Stock ticker symbol (e.g. 'AAPL')

        Returns:
            JSON string containing stock information
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        relevant_info = {
            "symbol": info.get("symbol"),
            "shortName": info.get("shortName"),
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "currentPrice": info.get("currentPrice"),
            "previousClose": info.get("previousClose"),
            "open": info.get("open"),
            "dayLow": info.get("dayLow"),
            "dayHigh": info.get("dayHigh"),
            "volume": info.get("volume"),
            "averageVolume": info.get("averageVolume"),
            "beta": info.get("beta"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "dividendYield": info.get("dividendYield"),
            "payoutRatio": info.get("payoutRatio"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "priceToBook": info.get("priceToBook"),
            "debtToEquity": info.get("debtToEquity"),
            "returnOnEquity": info.get("returnOnEquity"),
            "returnOnAssets": info.get("returnOnAssets"),
            "freeCashflow": info.get("freeCashflow"),
            "operatingCashflow": info.get("operatingCashflow"),
            "website": info.get("website"),
            "country": info.get("country"),
            "city": info.get("city"),
            "phone": info.get("phone"),
            "fullTimeEmployees": info.get("fullTimeEmployees"),
            "longBusinessSummary": info.get("longBusinessSummary"),
        }
        return json.dumps(relevant_info, indent=2)

    @mcp.tool()
    async def get_multiple_tickers(tickers: List[str], period: str = "1d") -> str:
        """Get current data for multiple stock tickers.

        Args:
            tickers: List of stock ticker symbols (e.g. ['AAPL', 'GOOGL'])
            period: Data period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)

        Returns:
            JSON string containing data for all requested tickers
        """
        tickers_str = " ".join(tickers)
        data = yf.download(
            tickers_str,
            period=period,
            group_by="ticker",
            auto_adjust=True,
        )
        if data is None or data.empty:
            return json.dumps({"error": "No data available for the given tickers"})
        return data.to_json(date_format="iso")

    @mcp.tool()
    async def get_company_officers(ticker: str) -> str:
        """Get company officers and key personnel information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing company officers data
        """
        stock = yf.Ticker(ticker)
        officers = stock.get_info().get("companyOfficers", [])
        return json.dumps(officers, indent=2)

    @mcp.tool()
    async def get_institutional_holders(ticker: str) -> str:
        """Get institutional holders information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing institutional holders data
        """
        stock = yf.Ticker(ticker)
        holders = stock.institutional_holders
        if holders is not None:
            return holders.to_json(date_format="iso")
        return json.dumps({"error": "No institutional holders data available"})

    @mcp.tool()
    async def get_major_holders(ticker: str) -> str:
        """Get major holders breakdown.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing major holders data
        """
        stock = yf.Ticker(ticker)
        holders = stock.major_holders
        if holders is not None:
            return holders.to_json()
        return json.dumps({"error": "No major holders data available"})

    @mcp.tool()
    async def get_mutualfund_holders(ticker: str) -> str:
        """Get mutual fund holders information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing mutual fund holders data
        """
        stock = yf.Ticker(ticker)
        holders = stock.mutualfund_holders
        if holders is not None:
            return holders.to_json(date_format="iso")
        return json.dumps({"error": "No mutual fund holders data available"})
