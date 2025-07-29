"""Market data and trending tools."""

import json
from typing import List

import yfinance as yf
from mcp.server import FastMCP


def register_market_data_tools(mcp: FastMCP):
    """Register market data tools with the MCP server."""

    @mcp.tool()
    async def get_market_status() -> str:
        """Get current market status and trading hours.

        Returns:
            JSON string containing market status information
        """
        # Note: yfinance doesn't have a direct market status endpoint
        # This is a simplified implementation using a major index
        try:
            spy = yf.Ticker("SPY")
            info = spy.info

            market_info = {
                "marketState": info.get("marketState", "UNKNOWN"),
                "exchangeTimezone": info.get("exchangeTimezoneName", "America/New_York"),
                "regularMarketTime": info.get("regularMarketTime"),
                "preMarketPrice": info.get("preMarketPrice"),
                "postMarketPrice": info.get("postMarketPrice"),
                "currency": info.get("currency", "USD"),
            }

            return json.dumps(market_info, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": f"Failed to get market status: {str(e)}"})

    @mcp.tool()
    async def get_trending_tickers(region: str = "US", count: int = 10) -> str:
        """Get trending tickers (Note: Limited functionality in yfinance).

        Args:
            region: Market region (US, CA, etc.)
            count: Number of trending tickers to return

        Returns:
            JSON string containing trending tickers
        """
        # Note: yfinance has limited trending data capabilities
        # This returns popular tickers as an example
        popular_tickers = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "NVDA",
            "META",
            "NFLX",
            "AMD",
            "CRM",
            "ORCL",
            "ADBE",
            "INTC",
            "CSCO",
            "PEP",
            "KO",
            "WMT",
            "DIS",
            "V",
            "MA",
        ]

        try:
            selected_tickers = popular_tickers[:count]
            trending_data = []

            for ticker in selected_tickers:
                stock = yf.Ticker(ticker)
                info = stock.info
                trending_data.append(
                    {
                        "symbol": ticker,
                        "shortName": info.get("shortName", ""),
                        "currentPrice": info.get("currentPrice"),
                        "regularMarketChangePercent": info.get("regularMarketChangePercent"),
                        "marketCap": info.get("marketCap"),
                        "volume": info.get("volume"),
                    }
                )

            return json.dumps(
                {"region": region, "count": len(trending_data), "trending_tickers": trending_data}, indent=2
            )

        except Exception as e:
            return json.dumps({"error": f"Failed to get trending tickers: {str(e)}"})

    @mcp.tool()
    async def get_sector_performance() -> str:
        """Get sector performance using sector ETFs.

        Returns:
            JSON string containing sector performance data
        """
        sector_etfs = {
            "Technology": "XLK",
            "Healthcare": "XLV",
            "Financials": "XLF",
            "Consumer Discretionary": "XLY",
            "Communication Services": "XLC",
            "Industrials": "XLI",
            "Consumer Staples": "XLP",
            "Energy": "XLE",
            "Utilities": "XLU",
            "Real Estate": "XLRE",
            "Materials": "XLB",
        }

        try:
            sector_performance = []

            for sector, etf in sector_etfs.items():
                stock = yf.Ticker(etf)
                info = stock.info
                hist = stock.history(period="2d")

                if len(hist) >= 2:
                    daily_change = ((hist.iloc[-1]["Close"] - hist.iloc[-2]["Close"]) / hist.iloc[-2]["Close"]) * 100
                else:
                    daily_change = None

                sector_performance.append(
                    {
                        "sector": sector,
                        "etf_symbol": etf,
                        "current_price": info.get("currentPrice"),
                        "daily_change_percent": daily_change,
                        "volume": info.get("volume"),
                    }
                )

            return json.dumps({"sector_performance": sector_performance}, indent=2)

        except Exception as e:
            return json.dumps({"error": f"Failed to get sector performance: {str(e)}"})

    @mcp.tool()
    async def get_index_data(indices: List[str] = None) -> str:
        """Get major market indices data.

        Args:
            indices: List of index symbols (default: major US indices)

        Returns:
            JSON string containing index data
        """
        if indices is None:
            indices = ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"]

        index_names = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones Industrial Average",
            "^IXIC": "NASDAQ Composite",
            "^RUT": "Russell 2000",
            "^VIX": "CBOE Volatility Index",
        }

        try:
            index_data = []

            for index in indices:
                stock = yf.Ticker(index)
                hist = stock.history(period="2d")

                if len(hist) >= 2:
                    current_price = hist.iloc[-1]["Close"]
                    previous_close = hist.iloc[-2]["Close"]
                    daily_change = current_price - previous_close
                    daily_change_percent = (daily_change / previous_close) * 100
                else:
                    current_price = None
                    daily_change = None
                    daily_change_percent = None

                index_data.append(
                    {
                        "symbol": index,
                        "name": index_names.get(index, index),
                        "current_price": current_price,
                        "daily_change": daily_change,
                        "daily_change_percent": daily_change_percent,
                        "volume": hist.iloc[-1]["Volume"] if len(hist) > 0 else None,
                    }
                )

            return json.dumps({"indices": index_data}, indent=2)

        except Exception as e:
            return json.dumps({"error": f"Failed to get index data: {str(e)}"})
