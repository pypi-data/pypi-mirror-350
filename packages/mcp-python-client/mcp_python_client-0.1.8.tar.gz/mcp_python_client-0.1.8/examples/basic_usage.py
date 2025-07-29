#!/usr/bin/env python3
"""Basic usage example for the MCP Python Client."""

import os
import sys
import asyncio
from loguru import logger
from mcp_python_client import MCPClient

async def main():
    """Run a sample query with the MCP client."""
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    # Initialize the client with your API key and model
    client = MCPClient(
        model="anthropic/claude-3-sonnet-20240229",  # Use your preferred model
        api_key=os.environ.get("ANTHROPIC_API_KEY")  # Or pass directly
    )
    
    # Connect to all MCP servers defined in your config
    try:
        await client.connect_to_all_servers()
        logger.info(f"Connected to {len(client.sessions)} MCP servers")
    except Exception as e:
        logger.warning(f"Failed to connect to MCP servers: {e}")
        logger.info("Continuing without MCP servers")
    
    # Process a query
    query = "What is the current time? Tell me a joke about programming."
    logger.info(f"Processing query: {query}")
    
    # Stream the response
    print("\nStreaming response:")
    async for chunk in client.aprocess_query(query):
        print(chunk, end="", flush=True)
    
    print("\n\nNon-streaming response:")
    response = client.process_query(query, temperature=0.2)
    print(response)
    
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
