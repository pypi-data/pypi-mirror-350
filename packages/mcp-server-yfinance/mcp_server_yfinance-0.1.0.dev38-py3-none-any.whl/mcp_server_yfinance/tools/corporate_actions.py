"""Corporate actions and dividend tools for yfinance MCP server."""

from typing import Optional

import pandas as pd
import yfinance as yf
from mcp.server import FastMCP


def register_corporate_actions_tools(mcp: FastMCP):
    """Register corporate actions and dividend tools."""

    @mcp.tool("get_dividends_history")
    def get_dividends(
        symbol: str,
        period: str = "1y",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        """
        Get dividend history for a stock.

        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)

        Returns:
            Dictionary containing dividend data
        """
        try:
            ticker = yf.Ticker(symbol)

            if start_date and end_date:
                dividends = ticker.dividends.loc[start_date:end_date]
            else:
                dividends = ticker.history(period=period).dividends

            # Filter out zero dividends
            dividends = dividends[dividends > 0]

            return {
                "symbol": symbol,
                "dividends": dividends.to_dict(),
                "total_dividends": float(dividends.sum()),
                "dividend_count": len(dividends),
                "period": period if not (start_date and end_date) else f"{start_date} to {end_date}",
            }
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool("get_splits_history")
    def get_splits(symbol: str, period: str = "5y") -> dict:
        """
        Get stock split history.

        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')

        Returns:
            Dictionary containing stock split data
        """
        try:
            ticker = yf.Ticker(symbol)
            splits = ticker.splits

            # Filter splits within the period
            if period != "max":
                history = ticker.history(period=period)
                if not history.empty:
                    start_date = history.index[0]
                    splits = splits[splits.index >= start_date]

            return {"symbol": symbol, "splits": splits.to_dict(), "split_count": len(splits), "period": period}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool("get_actions")
    def get_actions(symbol: str, period: str = "1y") -> dict:
        """
        Get all corporate actions (dividends and splits) for a stock.

        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')

        Returns:
            Dictionary containing all corporate actions
        """
        try:
            ticker = yf.Ticker(symbol)
            actions = ticker.actions

            # Filter actions within the period
            if period != "max":
                history = ticker.history(period=period)
                if not history.empty:
                    start_date = history.index[0]
                    actions = actions[actions.index >= start_date]

            return {"symbol": symbol, "actions": actions.to_dict(), "period": period, "total_actions": len(actions)}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool("get_dividend_yield")
    def get_dividend_yield(symbol: str) -> dict:
        """
        Calculate dividend yield and related metrics.

        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')

        Returns:
            Dictionary containing dividend yield metrics
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Get trailing twelve months dividends
            dividends = ticker.dividends
            if len(dividends) > 0:
                # Get dividends from last 12 months
                latest_date = dividends.index[-1]
                one_year_ago = latest_date - pd.DateOffset(years=1)
                ttm_dividends = dividends[dividends.index > one_year_ago].sum()
            else:
                ttm_dividends = 0

            current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            dividend_yield = (ttm_dividends / current_price * 100) if current_price > 0 else 0

            return {
                "symbol": symbol,
                "current_price": current_price,
                "ttm_dividends": float(ttm_dividends),
                "dividend_yield_percent": round(dividend_yield, 2),
                "forward_dividend_rate": info.get("dividendRate"),
                "forward_dividend_yield": info.get("dividendYield"),
                "payout_ratio": info.get("payoutRatio"),
                "ex_dividend_date": info.get("exDividendDate"),
                "dividend_date": info.get("dividendDate"),
            }
        except Exception as e:
            return {"error": str(e)}
