"""Tests for MCP client."""

import pytest
from unittest.mock import AsyncMock, patch
import json

from open_mcp.client import MCPClient, MCPClientError
from open_mcp.models.base import Tool, ToolResult


class TestMCPClient:
    """Test cases for MCP client."""

    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client initialization."""
        client = MCPClient("http://localhost:8000")
        assert client.server_url == "http://localhost:8000"
        assert client.timeout == 30.0
        assert client.max_retries == 3

    @pytest.mark.asyncio
    async def test_invalid_server_url(self):
        """Test client with invalid server URL."""
        with pytest.raises(MCPClientError, match="Invalid server URL"):
            MCPClient("invalid-url")

    @pytest.mark.asyncio
    async def test_context_manager(self, mock_httpx_client):
        """Test client as context manager."""
        with patch('httpx.AsyncClient', return_value=mock_httpx_client):
            async with MCPClient("http://localhost:8000") as client:
                assert client._session is not None
            # Session should be closed after exiting context
            mock_httpx_client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_discover_tools(self, mock_httpx_client, sample_tool):
        """Test tool discovery."""
        # Mock response for tools/list
        mock_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [sample_tool.model_dump()]
            }
        }
        mock_httpx_client.post.return_value.json.return_value = mock_response
        
        with patch('httpx.AsyncClient', return_value=mock_httpx_client):
            async with MCPClient("http://localhost:8000") as client:
                tools = await client.list_tools()
                assert len(tools) == 1
                assert tools[0].name == "calculator"

    @pytest.mark.asyncio
    async def test_call_tool(self, mock_httpx_client):
        """Test tool execution."""
        # Mock successful tool call response
        mock_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "content": 8,
                "isError": False,
                "metadata": {"execution_time": "0.1s"}
            }
        }
        mock_httpx_client.post.return_value.json.return_value = mock_response
        
        with patch('httpx.AsyncClient', return_value=mock_httpx_client):
            client = MCPClient("http://localhost:8000")
            client._tools = {"calculator": Tool(name="calculator", description="Test tool")}
            
            result = await client.call_tool("calculator", {"operation": "add", "a": 3, "b": 5})
            
            assert isinstance(result, ToolResult)
            assert result.content == 8
            assert not result.is_error
            assert result.metadata["execution_time"] == "0.1s"

    @pytest.mark.asyncio
    async def test_call_unknown_tool(self):
        """Test unknown tool call."""
        client = MCPClient("http://localhost:8000")
        with pytest.raises(MCPClientError, match="Unknown tool: unknown_tool"):
            await client.call_tool("unknown_tool", {})
