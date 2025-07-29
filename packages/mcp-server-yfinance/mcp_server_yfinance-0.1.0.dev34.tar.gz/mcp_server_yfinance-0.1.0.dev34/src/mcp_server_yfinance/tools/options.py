"""Options trading tools."""

import json
from typing import Optional

import yfinance as yf
from mcp.server import FastMCP


def register_options_tools(mcp: FastMCP):
    """Register options tools with the MCP server."""

    @mcp.tool()
    async def get_options_expiration_dates(ticker: str) -> str:
        """Get available options expiration dates.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing expiration dates
        """
        stock = yf.Ticker(ticker)
        try:
            expirations = stock.options
            return json.dumps({"expiration_dates": list(expirations)})
        except Exception as e:
            return json.dumps({"error": f"No options data available: {str(e)}"})

    @mcp.tool()
    async def get_option_chain(ticker: str, expiration_date: Optional[str] = None) -> str:
        """Get options chain data for a specific expiration date.

        Args:
            ticker: Stock ticker symbol
            expiration_date: Expiration date in YYYY-MM-DD format (if None, uses nearest expiration)

        Returns:
            JSON string containing options chain data
        """
        stock = yf.Ticker(ticker)
        try:
            if expiration_date:
                option_chain = stock.option_chain(expiration_date)
            else:
                # Use the first available expiration date
                expirations = stock.options
                if not expirations:
                    return json.dumps({"error": "No options data available"})
                option_chain = stock.option_chain(expirations[0])

            result = {
                "calls": option_chain.calls.to_dict("records") if hasattr(option_chain, "calls") else [],
                "puts": option_chain.puts.to_dict("records") if hasattr(option_chain, "puts") else [],
            }
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to get options data: {str(e)}"})

    @mcp.tool()
    async def get_options_volume_analysis(ticker: str, expiration_date: Optional[str] = None) -> str:
        """Get options volume and open interest analysis.

        Args:
            ticker: Stock ticker symbol
            expiration_date: Expiration date in YYYY-MM-DD format (if None, uses nearest expiration)

        Returns:
            JSON string containing volume analysis
        """
        stock = yf.Ticker(ticker)
        try:
            if expiration_date:
                option_chain = stock.option_chain(expiration_date)
            else:
                # Use the first available expiration date
                expirations = stock.options
                if not expirations:
                    return json.dumps({"error": "No options data available"})
                option_chain = stock.option_chain(expirations[0])

            calls = option_chain.calls
            puts = option_chain.puts

            analysis = {
                "total_call_volume": calls["volume"].sum() if "volume" in calls.columns else 0,
                "total_put_volume": puts["volume"].sum() if "volume" in puts.columns else 0,
                "total_call_open_interest": calls["openInterest"].sum() if "openInterest" in calls.columns else 0,
                "total_put_open_interest": puts["openInterest"].sum() if "openInterest" in puts.columns else 0,
                "put_call_ratio_volume": (puts["volume"].sum() / calls["volume"].sum())
                if "volume" in calls.columns and calls["volume"].sum() > 0
                else None,
                "put_call_ratio_oi": (puts["openInterest"].sum() / calls["openInterest"].sum())
                if "openInterest" in calls.columns and calls["openInterest"].sum() > 0
                else None,
            }

            return json.dumps(analysis, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to analyze options data: {str(e)}"})

    @mcp.tool()
    async def get_options_by_moneyness(
        ticker: str,
        expiration_date: Optional[str] = None,
        moneyness_range: float = 0.1,
    ) -> str:
        """Get options filtered by moneyness (proximity to current stock price).

        Args:
            ticker: Stock ticker symbol
            expiration_date: Expiration date in YYYY-MM-DD format (if None, uses nearest expiration)
            moneyness_range: Range around current price (e.g., 0.1 for ±10%)

        Returns:
            JSON string containing filtered options data
        """
        stock = yf.Ticker(ticker)
        try:
            current_price = stock.info.get("currentPrice")
            if not current_price:
                return json.dumps({"error": "Could not get current stock price"})

            if expiration_date:
                option_chain = stock.option_chain(expiration_date)
            else:
                # Use the first available expiration date
                expirations = stock.options
                if not expirations:
                    return json.dumps({"error": "No options data available"})
                option_chain = stock.option_chain(expirations[0])

            price_min = current_price * (1 - moneyness_range)
            price_max = current_price * (1 + moneyness_range)

            calls = option_chain.calls
            puts = option_chain.puts

            filtered_calls = calls[(calls["strike"] >= price_min) & (calls["strike"] <= price_max)]
            filtered_puts = puts[(puts["strike"] >= price_min) & (puts["strike"] <= price_max)]

            result = {
                "current_price": current_price,
                "price_range": {"min": price_min, "max": price_max},
                "calls": filtered_calls.to_dict("records"),
                "puts": filtered_puts.to_dict("records"),
            }

            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to filter options data: {str(e)}"})
