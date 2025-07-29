"""Analyst data tools."""

import json

import yfinance as yf
from mcp.server import FastMCP


def register_analyst_data_tools(mcp: FastMCP):
    """Register analyst data tools with the MCP server."""

    @mcp.tool()
    async def get_recommendations(ticker: str) -> str:
        """Get analyst recommendations for a stock.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing analyst recommendations
        """
        stock = yf.Ticker(ticker)
        recs = stock.recommendations
        if recs is not None and not recs.empty:
            return recs.to_json(date_format="iso")
        return json.dumps({"error": "No recommendations available"})

    @mcp.tool()
    async def get_analyst_price_targets(ticker: str) -> str:
        """Get analyst price targets and estimates.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing price targets
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        price_targets = {
            "targetHighPrice": info.get("targetHighPrice"),
            "targetLowPrice": info.get("targetLowPrice"),
            "targetMeanPrice": info.get("targetMeanPrice"),
            "targetMedianPrice": info.get("targetMedianPrice"),
            "recommendationMean": info.get("recommendationMean"),
            "recommendationKey": info.get("recommendationKey"),
            "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions"),
        }
        return json.dumps(price_targets, indent=2)

    @mcp.tool()
    async def get_upgrades_downgrades(ticker: str) -> str:
        """Get recent upgrades and downgrades.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing upgrades/downgrades
        """
        stock = yf.Ticker(ticker)
        upgrades = stock.upgrades_downgrades
        if upgrades is not None and not upgrades.empty:
            return upgrades.to_json(date_format="iso")
        return json.dumps({"error": "No upgrades/downgrades data available"})

    @mcp.tool()
    async def get_recommendations_summary(ticker: str) -> str:
        """Get recommendations summary.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing recommendations summary
        """
        stock = yf.Ticker(ticker)
        rec_summary = stock.recommendations_summary
        if rec_summary is not None and not rec_summary.empty:
            return rec_summary.to_json(date_format="iso")
        return json.dumps({"error": "No recommendations summary available"})
