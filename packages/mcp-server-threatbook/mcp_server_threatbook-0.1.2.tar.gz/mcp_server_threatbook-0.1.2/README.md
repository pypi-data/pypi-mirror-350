# MCP Server For Threatbook


## Configuration
```json
{
  "mcpServers": {
    "mcp-server-threatbook": {
      "command": "python",
      "args": ["-m", "mcp-server-threatbook"],
      "env": {
        "THREATBOOK_APIKEY": "<YOUR_APIKEY>"
      }
    }
  }
}
```
