"""Extended market data tools for yfinance MCP server."""

import json
from typing import List, Optional

import yfinance as yf
from mcp.server import FastMCP


def register_extended_market_tools(mcp: FastMCP):
    """Register extended market data tools with the MCP server."""

    @mcp.tool()
    async def download_bulk_data(
        tickers: List[str],
        period: str = "1mo",
        interval: str = "1d",
        group_by: str = "ticker",
        auto_adjust: bool = True,
        prepost: bool = False,
        threads: bool = True,
    ) -> str:
        """Download bulk historical data for multiple tickers efficiently.

        Args:
            tickers: List of ticker symbols
            period: Data period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
            interval: Data interval (1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo)
            group_by: Group by 'ticker' or 'column'
            auto_adjust: Auto-adjust prices for dividends and splits
            prepost: Include pre and post market data
            threads: Use threading for faster downloads

        Returns:
            JSON string containing bulk historical data
        """
        try:
            data = yf.download(
                tickers=" ".join(tickers),
                period=period,
                interval=interval,
                group_by=group_by,
                auto_adjust=auto_adjust,
                prepost=prepost,
                threads=threads,
            )

            if data.empty:
                return json.dumps({"error": "No data available for the given tickers"})

            return json.dumps(
                {"tickers": tickers, "period": period, "interval": interval, "data": data.to_dict()},
                indent=2,
                default=str,
            )

        except Exception as e:
            return json.dumps({"error": f"Failed to download bulk data: {str(e)}"})

    @mcp.tool()
    async def get_ticker_history_metadata(ticker: str) -> str:
        """Get comprehensive ticker history metadata.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing history metadata
        """
        try:
            stock = yf.Ticker(ticker)

            # Get different types of historical data metadata
            metadata = {
                "symbol": ticker,
                "available_periods": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
                "available_intervals": [
                    "1m",
                    "2m",
                    "5m",
                    "15m",
                    "30m",
                    "60m",
                    "90m",
                    "1h",
                    "1d",
                    "5d",
                    "1wk",
                    "1mo",
                    "3mo",
                ],
            }

            # Try to get some sample data to verify ticker exists
            try:
                hist = stock.history(period="5d")
                if not hist.empty:
                    metadata["data_available"] = True
                    metadata["latest_date"] = str(hist.index[-1])
                    metadata["earliest_available"] = str(hist.index[0])
                    metadata["columns"] = list(hist.columns)
                else:
                    metadata["data_available"] = False
            except Exception:
                metadata["data_available"] = False

            return json.dumps(metadata, indent=2)

        except Exception as e:
            return json.dumps({"error": f"Failed to get metadata: {str(e)}"})

    @mcp.tool()
    async def get_exchange_info(ticker: str) -> str:
        """Get detailed exchange and trading information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing exchange information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            exchange_info = {
                "symbol": ticker,
                "exchange": info.get("exchange"),
                "fullExchangeName": info.get("fullExchangeName"),
                "exchangeTimezoneName": info.get("exchangeTimezoneName"),
                "exchangeTimezoneShortName": info.get("exchangeTimezoneShortName"),
                "market": info.get("market"),
                "marketState": info.get("marketState"),
                "quoteType": info.get("quoteType"),
                "currency": info.get("currency"),
                "financialCurrency": info.get("financialCurrency"),
                "gmtOffSetMilliseconds": info.get("gmtOffSetMilliseconds"),
                "regularMarketTime": info.get("regularMarketTime"),
                "preMarketTime": info.get("preMarketTime"),
                "postMarketTime": info.get("postMarketTime"),
                "tradeable": info.get("tradeable"),
                "triggerable": info.get("triggerable"),
            }

            return json.dumps(exchange_info, indent=2, default=str)

        except Exception as e:
            return json.dumps({"error": f"Failed to get exchange info: {str(e)}"})

    @mcp.tool()
    async def get_market_hours(ticker: str) -> str:
        """Get market hours and session information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            JSON string containing market hours data
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            market_hours = {
                "symbol": ticker,
                "exchange": info.get("exchange"),
                "timezone": info.get("exchangeTimezoneName"),
                "marketState": info.get("marketState"),
                "regularMarketTime": info.get("regularMarketTime"),
                "regularMarketPrice": info.get("regularMarketPrice"),
                "regularMarketPreviousClose": info.get("regularMarketPreviousClose"),
                "preMarketPrice": info.get("preMarketPrice"),
                "preMarketChange": info.get("preMarketChange"),
                "preMarketChangePercent": info.get("preMarketChangePercent"),
                "preMarketTime": info.get("preMarketTime"),
                "postMarketPrice": info.get("postMarketPrice"),
                "postMarketChange": info.get("postMarketChange"),
                "postMarketChangePercent": info.get("postMarketChangePercent"),
                "postMarketTime": info.get("postMarketTime"),
            }

            return json.dumps(market_hours, indent=2, default=str)

        except Exception as e:
            return json.dumps({"error": f"Failed to get market hours: {str(e)}"})

    @mcp.tool()
    async def validate_tickers(tickers: List[str]) -> str:
        """Validate a list of ticker symbols.

        Args:
            tickers: List of ticker symbols to validate

        Returns:
            JSON string containing validation results
        """
        try:
            validation_results = []

            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker)

                    # Try to get basic info to validate ticker
                    info = stock.info
                    hist = stock.history(period="2d")

                    is_valid = bool(info.get("symbol") and not hist.empty)

                    validation_results.append(
                        {
                            "ticker": ticker,
                            "valid": is_valid,
                            "name": info.get("shortName") if is_valid else None,
                            "exchange": info.get("exchange") if is_valid else None,
                            "quoteType": info.get("quoteType") if is_valid else None,
                        }
                    )

                except Exception:
                    validation_results.append({"ticker": ticker, "valid": False, "error": "Failed to retrieve data"})

            valid_count = sum(1 for result in validation_results if result["valid"])

            return json.dumps(
                {
                    "total_tickers": len(tickers),
                    "valid_count": valid_count,
                    "invalid_count": len(tickers) - valid_count,
                    "results": validation_results,
                },
                indent=2,
            )

        except Exception as e:
            return json.dumps({"error": f"Failed to validate tickers: {str(e)}"})

    @mcp.tool()
    async def get_currency_data(base_currency: str = "USD", target_currencies: Optional[List[str]] = None) -> str:
        """Get currency exchange rate data.

        Args:
            base_currency: Base currency code (e.g., 'USD')
            target_currencies: List of target currency codes (default: major currencies)

        Returns:
            JSON string containing currency data
        """
        try:
            if target_currencies is None:
                target_currencies = ["EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY"]

            currency_data = []

            for target in target_currencies:
                if target == base_currency:
                    continue

                currency_pair = f"{base_currency}{target}=X"

                try:
                    ticker = yf.Ticker(currency_pair)
                    hist = ticker.history(period="2d")
                    info = ticker.info

                    if not hist.empty:
                        current_rate = hist.iloc[-1]["Close"]

                        # Calculate daily change if we have enough data
                        daily_change = None
                        daily_change_percent = None
                        if len(hist) >= 2:
                            previous_rate = hist.iloc[-2]["Close"]
                            daily_change = current_rate - previous_rate
                            daily_change_percent = (daily_change / previous_rate) * 100

                        currency_data.append(
                            {
                                "pair": currency_pair,
                                "base": base_currency,
                                "target": target,
                                "rate": current_rate,
                                "daily_change": daily_change,
                                "daily_change_percent": daily_change_percent,
                                "name": info.get("shortName"),
                            }
                        )

                except Exception:
                    # Skip currencies that cause errors
                    continue

            return json.dumps(
                {"base_currency": base_currency, "currency_rates": currency_data, "count": len(currency_data)}, indent=2
            )

        except Exception as e:
            return json.dumps({"error": f"Failed to get currency data: {str(e)}"})
