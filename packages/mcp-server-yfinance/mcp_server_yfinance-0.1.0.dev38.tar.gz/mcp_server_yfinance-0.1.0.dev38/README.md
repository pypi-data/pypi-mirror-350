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

## Usage with VS Code

For quick installation, use one of the one-click installation buttons below:

[![Install with UVX in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=yfinance&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-yfinance%22%5D%7D) [![Install with UVX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-UV-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=yfinance&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-yfinance%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others. 

> Note that the `mcp` key is not needed in the `.vscode/mcp.json` file.

#### UVX

```json
{
  "mcp": {
    "servers": {
      "yfinance": {
        "command": "uvx",
        "args": [
          "mcp-server-yfinance@latest"
        ]
      }
    }
  }
}
```

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