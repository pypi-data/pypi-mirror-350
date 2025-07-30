"""MCP Client implementation."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable
from urllib.parse import urlparse

import httpx
from pydantic import ValidationError

from ..models.base import (
    BaseMessage,
    MCPError,
    Tool,
    Resource,
    Prompt,
    ToolCall,
    ToolResult,
)
from ..models.messages import MCPRequest, MCPResponse
from ..utils.logging import get_logger
from ..utils.validation import validate_message


logger = get_logger(__name__)


class MCPClientError(Exception):
    """MCP Client specific errors."""
    pass


class MCPClient:
    """
    MCP (Model Context Protocol) Client.
    
    Handles communication with MCP servers and provides methods for
    tool execution, resource access, and prompt management.
    """
    
    def __init__(
        self,
        server_url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize MCP Client.
        
        Args:
            server_url: URL of the MCP server
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            headers: Additional HTTP headers
        """
        self.server_url = server_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = headers or {}
        
        # Validate server URL
        parsed = urlparse(server_url)
        if not parsed.scheme or not parsed.netloc:
            raise MCPClientError(f"Invalid server URL: {server_url}")
            
        self._session: Optional[httpx.AsyncClient] = None
        self._message_id = 0
        self._tools: Dict[str, Tool] = {}
        self._resources: Dict[str, Resource] = {}
        self._prompts: Dict[str, Prompt] = {}
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
        
    async def connect(self) -> None:
        """Establish connection to MCP server."""
        if self._session is None:
            self._session = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers,
            )
            
        # Initialize connection and discover capabilities
        await self._initialize()
        logger.info(f"Connected to MCP server: {self.server_url}")
        
    async def disconnect(self) -> None:
        """Disconnect from MCP server."""
        if self._session:
            await self._session.aclose()
            self._session = None
        logger.info("Disconnected from MCP server")
        
    async def _initialize(self) -> None:
        """Initialize connection and discover server capabilities."""
        try:
            # Discover available tools
            await self._discover_tools()
            
            # Discover available resources  
            await self._discover_resources()
            
            # Discover available prompts
            await self._discover_prompts()
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP client: {e}")
            raise MCPClientError(f"Initialization failed: {e}")
            
    async def _discover_tools(self) -> None:
        """Discover available tools from server."""
        response = await self._send_request("tools/list")
        if response and "tools" in response:
            for tool_data in response["tools"]:
                try:
                    tool = Tool(**tool_data)
                    self._tools[tool.name] = tool
                except ValidationError as e:
                    logger.warning(f"Invalid tool data: {e}")
                    
    async def _discover_resources(self) -> None:
        """Discover available resources from server."""
        response = await self._send_request("resources/list")
        if response and "resources" in response:
            for resource_data in response["resources"]:
                try:
                    resource = Resource(**resource_data)
                    self._resources[resource.name] = resource
                except ValidationError as e:
                    logger.warning(f"Invalid resource data: {e}")
                    
    async def _discover_prompts(self) -> None:
        """Discover available prompts from server."""
        response = await self._send_request("prompts/list")
        if response and "prompts" in response:
            for prompt_data in response["prompts"]:
                try:
                    prompt = Prompt(**prompt_data)
                    self._prompts[prompt.name] = prompt
                except ValidationError as e:
                    logger.warning(f"Invalid prompt data: {e}")
                    
    def _get_next_id(self) -> int:
        """Get next message ID."""
        self._message_id += 1
        return self._message_id
        
    async def _send_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Send request to MCP server.
        
        Args:
            method: RPC method name
            params: Method parameters
            
        Returns:
            Response data
            
        Raises:
            MCPClientError: If request fails
        """
        if not self._session:
            raise MCPClientError("Client not connected")
            
        request = MCPRequest(
            id=self._get_next_id(),
            method=method,
            params=params or {},
        )
        
        try:
            response = await self._session.post(
                self.server_url,
                json=request.model_dump(),
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response
            if not validate_message(data):
                raise MCPClientError("Invalid response format")
                
            # Check for errors
            if "error" in data:
                error = MCPError(**data["error"])
                raise MCPClientError(f"Server error: {error.message}")
                
            return data.get("result")
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error in MCP request: {e}")
            raise MCPClientError(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise MCPClientError(f"Invalid response: {e}")
            
    # Public API methods
    
    async def list_tools(self) -> List[Tool]:
        """Get list of available tools."""
        return list(self._tools.values())
        
    async def get_tool(self, name: str) -> Optional[Tool]:
        """Get specific tool by name."""
        return self._tools.get(name)
        
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        """
        Execute a tool.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool execution result
            
        Raises:
            MCPClientError: If tool execution fails
        """
        if name not in self._tools:
            raise MCPClientError(f"Unknown tool: {name}")
            
        try:
            response = await self._send_request(
                "tools/call",
                {
                    "name": name,
                    "arguments": arguments,
                }
            )
            
            return ToolResult(
                content=response.get("content"),
                is_error=response.get("isError", False),
                metadata=response.get("metadata"),
            )
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise MCPClientError(f"Tool '{name}' execution failed: {e}")
            
    async def list_resources(self) -> List[Resource]:
        """Get list of available resources."""
        return list(self._resources.values())
        
    async def get_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        """
        Get resource content by URI.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content
        """
        try:
            response = await self._send_request(
                "resources/read",
                {"uri": uri}
            )
            return response
            
        except Exception as e:
            logger.error(f"Resource access failed: {e}")
            raise MCPClientError(f"Failed to access resource '{uri}': {e}")
            
    async def list_prompts(self) -> List[Prompt]:
        """Get list of available prompts."""
        return list(self._prompts.values())
        
    async def get_prompt(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Get prompt content.
        
        Args:
            name: Prompt name
            arguments: Prompt arguments
            
        Returns:
            Rendered prompt content
        """
        if name not in self._prompts:
            raise MCPClientError(f"Unknown prompt: {name}")
            
        try:
            response = await self._send_request(
                "prompts/get",
                {
                    "name": name,
                    "arguments": arguments or {},
                }
            )
            return response.get("content")
            
        except Exception as e:
            logger.error(f"Prompt access failed: {e}")
            raise MCPClientError(f"Failed to get prompt '{name}': {e}")