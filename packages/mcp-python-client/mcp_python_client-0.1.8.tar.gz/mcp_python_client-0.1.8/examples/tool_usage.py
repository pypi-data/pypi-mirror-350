#!/usr/bin/env python3
"""Example demonstrating MCP tool usage with the MCP Python Client."""

import os
import sys
import json
import asyncio
from loguru import logger
from mcp_python_client import MCPClient

async def main():
    """Run a sample query that uses MCP tools."""
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    # Create a sample config file if it doesn't exist
    config_path = os.path.join(os.getcwd(), "config.json")
    if not os.path.exists(config_path):
        logger.info(f"Creating sample config at {config_path}")
        with open(config_path, "w") as f:
            json.dump({
                "mcpServers": {
                    "shell-server": {
                        "command": "mcp-shell-server",
                        "args": [],
                        "env": {}
                    }
                }
            }, f, indent=2)
        logger.info("Sample config created. You'll need to install the mcp-shell-server package.")
    
    # Initialize the client
    client = MCPClient(
        config_path=config_path,
        model="anthropic/claude-3-sonnet-20240229",
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    # Connect to servers
    try:
        await client.connect_to_all_servers()
        logger.info(f"Connected to {len(client.sessions)} servers with {len(client.get_available_tools())} tools")
    except Exception as e:
        logger.error(f"Failed to connect to servers: {e}")
        logger.info("Make sure you have the required MCP servers installed.")
        return
    
    # Process a query that would benefit from using tools
    query = "What files are in the current directory? What's the content of the README.md file?"
    logger.info(f"Processing query: {query}")
    
    # Stream the response which may include tool calls
    print("\nResponse with tool usage:")
    async for chunk in client.aprocess_query(
        query, 
        system_prompt="You are a helpful assistant that uses tools to answer questions."
    ):
        print(chunk, end="", flush=True)
    
    # Clean up
    await client.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Example interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Error in example: {e}")
        sys.exit(1)
