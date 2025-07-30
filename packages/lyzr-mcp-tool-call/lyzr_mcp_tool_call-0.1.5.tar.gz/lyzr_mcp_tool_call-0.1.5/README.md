# Lyzr MCP Tool Call

## Overview

The Lyzr MCP Tool Call enables seamless integration between MCP (Model Context Protocol) clients and Lyzr agents. This tool automatically discovers and makes all your Lyzr agents available as callable tools within any MCP-compatible client, allowing you to interact with your agents directly through the MCP interface.

## Features

- 🤖 **Automatic Agent Discovery**: Automatically fetches and exposes all your Lyzr agents as MCP tools
- 🔧 **Universal MCP Compatibility**: Works with any MCP client (Claude Desktop, etc.)
- ⚡ **Zero Installation**: Run directly with `uv` - no local installation required
- 🔐 **Secure Authentication**: Uses your Lyzr API credentials for secure access
- 🚀 **Real-time Access**: Direct communication with your Lyzr agents

## Installation

### Using uv (Recommended)

This tool leverages [uv](https://docs.astral.sh/uv/) for seamless execution. With uv, no specific installation is needed - we use `uvx` to directly run the tool.

#### Install uv

[Installing uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

#### Run the Tool

Once uv is installed, you can run the Lyzr MCP tool directly:

```bash
uvx lyzr-mcp-tool-call@latest
```

## Configuration

### Claude Desktop Setup

To use this tool with Claude Desktop, add the following configuration to your `claude_desktop_config.json` file:

#### Location of config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Configuration:

```json
{
  "mcpServers": {
    "lyzr-mcp-tool-call": {
      "command": "uvx",
      "args": ["lyzr-mcp-tool-call@latest"],
      "env": {
        "LYZR_API_KEY": "your-lyzr-api-key-here",
        "LYZR_USER_ID": "your-user-id"
      }
    }
  }
}
```

### Environment Variables

You need to provide the following environment variables:

- `LYZR_API_KEY`: Your Lyzr API key
- `LYZR_USER_ID`: Your Lyzr user ID

## Usage

1. Configure the tool in your MCP client (e.g., Claude Desktop)
2. Restart your MCP client
3. Your Lyzr agents will appear as available tools
4. Call any agent directly through the MCP interface
5. Receive responses from your Lyzr agents in real-time

## Troubleshooting

### Common Issues

**Tool not appearing in MCP client:**
- Verify your `claude_desktop_config.json` syntax is correct
- Ensure your API credentials are valid
- Restart your MCP client after configuration changes

**Authentication errors:**
- Double-check your `LYZR_API_KEY` and `LYZR_USER_ID`
- Ensure your Lyzr account has access to the agents you're trying to use

**Connection issues:**
- Verify you have an active internet connection
- Check if there are any firewall restrictions

## Requirements

- [uv](https://docs.astral.sh/uv/) package manager
- Valid Lyzr account
- MCP-compatible client (Claude Desktop, etc.)

## Support

For issues and support:
- Contact Lyzr support for API-related issues [support@lyzr.ai](mailto:support@lyzr.ai)
- Ensure you're using the latest version with `uvx lyzr-mcp-tool-call@latest`