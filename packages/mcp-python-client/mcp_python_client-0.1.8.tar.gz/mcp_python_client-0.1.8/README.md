# MCP Python Client

A reusable Python client for interacting with MCP (Machine Conversation Protocol) servers and LLMs.

## Features

- Connect to and interact with multiple MCP servers
- Call tools provided by MCP servers
- Process user queries using various LLM models via LiteLLM
- Support for synchronous and asynchronous operations
- Streaming response support

## Installation

```bash
pip install mcp-python-client
```

## Quick Start

```python
import asyncio
from mcp_python_client import MCPClient

async def main():
    # Create a client with your preferred LLM settings
    client = MCPClient(
        model="anthropic/claude-3-sonnet-20240229",
        api_key="your_api_key_here"  # Or set via env var
    )
    
    # Connect to MCP servers defined in your config
    await client.connect_to_all_servers()
    
    # Process a query
    query = "What is the current weather in New York?"
    
    # Stream response
    async for chunk in client.aprocess_query(query):
        print(chunk, end="", flush=True)
    
    # Clean up
    await client.cleanup()

# Run the example
asyncio.run(main())
```

## Configuration

The client looks for a configuration file in the following locations:

1. Path specified when creating the client
2. `~/.config/mcp-client/config.json`
3. `~/.mcp-client.json`
4. `./mcp-client.json`
5. `./config.json`

Example configuration file:

```json
{
  "mcpServers": {
    "shell-server": {
      "command": "mcp-shell-server",
      "args": ["--use_cache"],
      "env": {
        "SHELL_SERVER_CACHE_DIR": "/tmp/shell-server-cache"
      }
    },
    "python-server": {
      "command": "mcp-python-server",
      "args": []
    }
  }
}
```

## Advanced Usage

See the [documentation](https://github.com/yourusername/mcp-python-client) for more advanced usage examples and API details.

## Publishing
``` 
uv build
uv publish
```
## License

MIT
