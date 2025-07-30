# pandas-query-mcp

This is a MCP (Model Context Protocol) server for pandas-query.


## Setup

```json
{
  "mcpServers": {
    "pandas-query-mcp": {
      "command": "uvx",
      "args": [
        "pandas-query-mcp",
        "--file",
        "<file path>",
        "--sheet",
        "<sheet name or index>"
      ],
      "alwaysAllow": [
        "describe",
        "head",
        "tail",
        "query"
      ],
      "disabled": false
    }
  }
}
```
