# MCP Server YFinance

A Model Context Protocol (MCP) server that provides stock market data using YFinance.

## Features

- Get basic stock information (price, market cap, sector, etc.)
- Fetch historical price data with customizable periods
- Retrieve analyst recommendations
- Download data for multiple stocks simultaneously
- Access dividend history

## Usage

This MCP server can be used with various LLM applications that support the Model Context Protocol:

- **Claude Desktop**: Anthropic's desktop application for Claude
- **Cursor**: AI-powered code editor with MCP support
- **Custom MCP clients**: Any application implementing the MCP client specification

## Usage with Claude Desktop

1. Install Claude Desktop from https://claude.ai/download
2. Open your Claude Desktop configuration:

   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add the following configuration:

```json
{
  "mcpServers": {
    "yfinance": {
      "command": "uvx",
      "args": [
        "mcp-server-yfinance@latest"
      ]
    }
  }
}
```

4. Restart Claude Desktop

### Available Tools

1. `get_stock_info(ticker: str)`
   - Get basic information about a stock
   - Example: `get_stock_info("AAPL")`

2. `get_historical_data(ticker: str, period: str = "1mo", interval: str = "1d")`
   - Get historical price data
   - Periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
   - Intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

3. `get_recommendations(ticker: str)`
   - Get analyst recommendations for a stock

4. `get_multiple_tickers(tickers: list[str], period: str = "1d")`
   - Get data for multiple stocks at once
   - Example: `get_multiple_tickers(["AAPL", "GOOGL"])`

5. `get_dividends(ticker: str)`
   - Get dividend history for a stock

## Development

To test the MCP server locally, install the `uvx` and `npx` and run the following command:

```bash
npx @modelcontextprotocol/inspector uvx mcp-server-yfinance@latest
```

This command will start the MCP server and open the MCP Inspector in your default web browser. You can then interact with the server and test its functionality.

## License

AGPLv3+ License - see [LICENSE](LICENSE) for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request