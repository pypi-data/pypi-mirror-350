# NetMind MCPServer MCP

This is an MCP (Model Context Protocol) server that provides endpoints for managing and interacting with  [NetMind MCP Servers](https://netmind.ai/AIServices), including querying servers, retrieving server details, and handling user reviews and ratings.


## Components

### Tools

- query_server:  Query the server list with optional fuzzy name matching and pagination.
- get_server: Retrieves detailed information about a specific server by its name.
- add_update_rating_review: Adds or updates a rating and review for a specific server.
- Lists reviews and ratings for a specific server.

## Installation

### Requires [UV](https://github.com/astral-sh/uv) (Fast Python package and project manager)

If uv isn't installed.

```bash
# Using Homebrew on macOS
brew install uv
```

or

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Environment Variables

You can obtain an API key from [Netmind](https://www.netmind.ai/user/apiToken)

- `NETMIND_API_TOKEN`: Your Netmind API key

### Cursor & Claude Desktop && Windsurf Installation

Add this tool as a mcp server by editing the Cursor/Claude/Windsurf config file.

```json
{
  "mcpServers": {
    "netmind-mcpserver-mcp": {
      "env": {
        "NETMIND_API_TOKEN": "XXXXXXXXXXXXXXXXXXXX"
      },
      "command": "uvx",
      "args": [
        "netmind-mcpserver-mcp"
      ]
    }
  }
}
```

#### Cursor

- On MacOS: `/Users/your-username/.cursor/mcp.json`
- On Windows: `C:\Users\your-username\.cursor\mcp.json`

#### Claude

- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`


### Windsurf

- On MacOS: `/Users/your-username/.codeium/windsurf/mcp_config.json`
- On Windows: `C:\Users\your-username\.codeium\windsurf\mcp_config.json`