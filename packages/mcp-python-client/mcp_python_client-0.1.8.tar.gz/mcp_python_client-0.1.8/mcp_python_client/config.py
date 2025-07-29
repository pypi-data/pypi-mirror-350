"""Configuration handling for the MCP Python Client."""

import json
import os
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, Field

class ServerConfig(BaseModel):
    """Configuration for a single MCP server."""
    
    command: str
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] | None = Field(default_factory=dict)


class MCPConfig(BaseModel):
    """Configuration for MCP servers and client options."""
    
    mcp_servers: dict[str, ServerConfig] = Field(default_factory=dict, alias="mcpServers")
    
    @classmethod
    def load_from_file(cls, config_path: Optional[str] = None) -> "MCPConfig":
        """Load the MCP server configuration from a file.
        
        Args:
            config_path: Path to the configuration file. If None, will look for config in default locations.
            
        Returns:
            MCPConfig: The loaded configuration
            
        Raises:
            FileNotFoundError: If no configuration file is found
            ValueError: If there is an error loading or parsing the configuration
        """
        # If config_path is provided, try to load from there
        if config_path and os.path.isfile(config_path):
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                return cls.model_validate(config_data)
            except Exception as e:
                raise ValueError(f"Error loading config from {config_path}: {str(e)}")
        
        # Default locations to check
        default_locations = [
            Path.home() / ".config/mcp-client/config.json",
            Path.home() / ".mcp-client.json",
            Path.cwd() / "mcp-client.json",
            Path.cwd() / "config.json",
        ]
        
        # Try each location
        for location in default_locations:
            if location.is_file():
                try:
                    with open(location, 'r') as f:
                        config_data = json.load(f)
                    return cls.model_validate(config_data)
                except Exception:
                    continue
        
        # If we got here, no valid config was found
        config_files = '\n'.join(str(loc) for loc in default_locations)
        raise FileNotFoundError(
            "MCP configuration not found. Please create a config file at one of the following locations:\n"
            f"{config_files}\n"
            "Or specify a config file path when creating the client."
        )
    
    def get_server_config(self, server_name: str) -> ServerConfig:
        """Get configuration for a specific server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            ServerConfig: The server configuration
            
        Raises:
            ValueError: If the server is not found in the configuration
        """
        if server_name not in self.mcp_servers:
            raise ValueError(f"Server '{server_name}' not found in configuration")
        
        return self.mcp_servers[server_name]
    
    def list_servers(self) -> list[str]:
        """Get a list of all configured server names.
        
        Returns:
            list[str]: List of server names
        """
        return list(self.mcp_servers.keys())
