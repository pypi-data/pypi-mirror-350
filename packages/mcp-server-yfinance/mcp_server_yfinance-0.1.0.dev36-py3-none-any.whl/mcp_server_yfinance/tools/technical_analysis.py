"""Technical analysis and trading tools."""

import json

import yfinance as yf
from mcp.server import FastMCP


def register_technical_analysis_tools(mcp: FastMCP):
    """Register technical analysis tools with the MCP server."""

    @mcp.tool()
    async def get_technical_indicators(ticker: str, period: str = "6mo") -> str:
        """Get technical analysis indicators for a stock.

        Args:
            ticker: Stock ticker symbol
            period: Data period for calculations

        Returns:
            JSON string containing technical indicators
        """
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return json.dumps({"error": "No historical data available"})

        # Calculate simple technical indicators
        current_price = hist["Close"].iloc[-1]
        high_52w = hist["High"].max()
        low_52w = hist["Low"].min()
        avg_volume = hist["Volume"].mean()

        # Moving averages
        sma_20 = hist["Close"].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else None
        sma_50 = hist["Close"].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
        sma_200 = hist["Close"].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else None

        # Price position in 52-week range
        price_position = ((current_price - low_52w) / (high_52w - low_52w)) * 100

        indicators = {
            "current_price": current_price,
            "52_week_high": high_52w,
            "52_week_low": low_52w,
            "price_position_in_52w_range_percent": price_position,
            "average_volume": avg_volume,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "price_vs_sma_20": ((current_price - sma_20) / sma_20 * 100) if sma_20 else None,
            "price_vs_sma_50": ((current_price - sma_50) / sma_50 * 100) if sma_50 else None,
            "price_vs_sma_200": ((current_price - sma_200) / sma_200 * 100) if sma_200 else None,
        }

        return json.dumps(indicators, indent=2)

    @mcp.tool()
    async def get_volatility_metrics(ticker: str, period: str = "1y") -> str:
        """Get volatility and risk metrics for a stock.

        Args:
            ticker: Stock ticker symbol
            period: Data period for calculations

        Returns:
            JSON string containing volatility metrics
        """
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return json.dumps({"error": "No historical data available"})

        # Calculate daily returns
        daily_returns = hist["Close"].pct_change().dropna()

        # Volatility metrics
        daily_volatility = daily_returns.std()
        annualized_volatility = daily_volatility * (252**0.5)  # 252 trading days

        # Additional metrics
        max_daily_gain = daily_returns.max()
        max_daily_loss = daily_returns.min()
        positive_days = (daily_returns > 0).sum()
        negative_days = (daily_returns < 0).sum()
        total_days = len(daily_returns)

        volatility_data = {
            "daily_volatility": daily_volatility,
            "annualized_volatility": annualized_volatility,
            "max_daily_gain_percent": max_daily_gain * 100,
            "max_daily_loss_percent": max_daily_loss * 100,
            "positive_days": int(positive_days),
            "negative_days": int(negative_days),
            "total_trading_days": total_days,
            "positive_days_percentage": (positive_days / total_days * 100) if total_days > 0 else 0,
        }

        return json.dumps(volatility_data, indent=2)

    @mcp.tool()
    async def get_support_resistance_levels(ticker: str, period: str = "6mo") -> str:
        """Get potential support and resistance levels based on historical data.

        Args:
            ticker: Stock ticker symbol
            period: Data period for analysis

        Returns:
            JSON string containing support/resistance levels
        """
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return json.dumps({"error": "No historical data available"})

        highs = hist["High"]
        lows = hist["Low"]
        current_price = hist["Close"].iloc[-1]

        # Simple support/resistance calculation
        # Find recent significant highs and lows
        resistance_levels = []
        support_levels = []

        # Get top 5 highest highs as potential resistance
        top_highs = highs.nlargest(10).unique()
        for high in top_highs:
            if high > current_price:
                resistance_levels.append(float(high))

        # Get top 5 lowest lows as potential support
        bottom_lows = lows.nsmallest(10).unique()
        for low in bottom_lows:
            if low < current_price:
                support_levels.append(float(low))

        # Sort and limit results
        resistance_levels = sorted(resistance_levels)[:5]
        support_levels = sorted(support_levels, reverse=True)[:5]

        levels_data = {
            "current_price": current_price,
            "resistance_levels": resistance_levels,
            "support_levels": support_levels,
            "nearest_resistance": resistance_levels[0] if resistance_levels else None,
            "nearest_support": support_levels[0] if support_levels else None,
        }

        return json.dumps(levels_data, indent=2)
