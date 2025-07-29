"""Unit tests for the MCP Python Client."""

import os
import json
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_python_client import MCPClient
from mcp_python_client.config import MCPConfig, ServerConfig

# Sample config for testing
TEST_CONFIG = {
    "mcpServers": {
        "test-server": {
            "command": "test-command",
            "args": ["--test"],
            "env": {"TEST_ENV": "test-value"}
        }
    }
}

@pytest.fixture
def config_file(tmp_path):
    """Create a temporary config file for testing."""
    config_path = tmp_path / "test_config.json"
    with open(config_path, "w") as f:
        json.dump(TEST_CONFIG, f)
    return str(config_path)

@pytest.fixture
def mock_litellm():
    """Mock litellm for testing."""
    with patch("mcp_python_client.client.mcp_client.litellm") as mock:
        yield mock

@pytest.fixture
def mock_stdio_client():
    """Mock MCP stdio client for testing."""
    with patch("mcp_python_client.client.mcp_client.stdio_client") as mock:
        # Setup the nested AsyncMock objects
        mock_stdio = AsyncMock()
        mock_write_stream = AsyncMock()
        mock_transport = (mock_stdio, mock_write_stream)
        
        # Configure the mock to return our prepared transport
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_transport
        mock.return_value = mock_context
        
        yield mock

@pytest.fixture
def mock_client_session():
    """Mock MCP ClientSession for testing."""
    with patch("mcp_python_client.client.mcp_client.ClientSession") as mock:
        # Create a mock session with the necessary methods and attributes
        mock_session = AsyncMock()
        mock_session.list_tools = AsyncMock()
        
        # Configure the mock tool response
        mock_tool = MagicMock()
        mock_tool.name = "test-tool"
        mock_tool.description = "A test tool"
        mock_tool.inputSchema = {"type": "object", "properties": {}}
        
        # Set the list_tools response
        mock_response = MagicMock()
        mock_response.tools = [mock_tool]
        mock_session.list_tools.return_value = mock_response
        
        # Configure the mock session context manager
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_session
        mock.return_value = mock_context
        
        yield mock, mock_session

class TestMCPClient:
    """Test cases for the MCPClient class."""
    
    def test_init_with_config(self, config_file):
        """Test initializing the client with a config file."""
        client = MCPClient(config_path=config_file)
        assert client.model == "anthropic/claude-3-7-sonnet-20241024"  # Default model
        assert isinstance(client.config, MCPConfig)
        assert "test-server" in client.config.mcp_servers
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    def test_init_with_env_var(self):
        """Test initializing the client with API key from env var."""
        client = MCPClient(model="anthropic/claude-3-opus-20240229")
        assert client.api_key == "test-key"
        assert client.model == "anthropic/claude-3-opus-20240229"
    
    def test_init_missing_api_key(self):
        """Test initializing the client without API key."""
        with patch.dict(os.environ, clear=True):
            with pytest.raises(ValueError, match="API key is required"):
                MCPClient()
    
    @pytest.mark.asyncio
    async def test_connect_to_server(self, config_file, mock_stdio_client, mock_client_session):
        """Test connecting to an MCP server."""
        mock_session_class, mock_session = mock_client_session
        
        client = MCPClient(config_path=config_file, api_key="test-key")
        await client.connect_to_server("test-server")
        
        # Check if the correct server parameters were used
        mock_stdio_client.assert_called_once()
        mock_session_class.assert_called_once()
        mock_session.initialize.assert_called_once()
        mock_session.list_tools.assert_called_once()
        
        # Check if session and tools were stored correctly
        assert "test-server" in client.sessions
        assert "test-server" in client.server_tools
    
    @pytest.mark.asyncio
    async def test_get_available_tools(self, config_file, mock_stdio_client, mock_client_session):
        """Test getting available tools."""
        client = MCPClient(config_path=config_file, api_key="test-key")
        await client.connect_to_server("test-server")
        
        tools = client.get_available_tools()
        assert len(tools) == 1
        assert tools[0]["type"] == "function"
        assert tools[0]["function"]["name"] == "test_server__test-tool"
        
        # Check the tool map
        assert "test_server__test-tool" in client.tool_map
        assert client.tool_map["test_server__test-tool"] == ("test-server", "test-tool")
    
    @pytest.mark.asyncio
    async def test_cleanup(self, config_file):
        """Test client cleanup."""
        client = MCPClient(config_path=config_file, api_key="test-key")
        
        # Mock the exit_stack
        client.exit_stack = AsyncMock()
        await client.cleanup()
        
        # Check if aclose was called
        client.exit_stack.aclose.assert_called_once()
