"""Base models for MCP protocol."""

from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class MCPVersion(str, Enum):
    """MCP protocol version."""
    V1_0 = "1.0"


class MessageType(str, Enum):
    """Types of MCP messages."""
    REQUEST = "request"
    RESPONSE = "response" 
    NOTIFICATION = "notification"
    ERROR = "error"


class BaseMessage(BaseModel):
    """Base class for all MCP messages."""
    
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )
    
    jsonrpc: str = Field(default="2.0", description="JSON-RPC version")
    id: Optional[Union[str, int]] = Field(default=None, description="Message ID")


class MCPError(BaseModel):
    """MCP error representation."""
    
    code: int = Field(description="Error code")
    message: str = Field(description="Error message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional error data")


class Tool(BaseModel):
    """Represents an MCP tool."""
    
    name: str = Field(description="Tool name")
    description: str = Field(description="Tool description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters schema")
    required: List[str] = Field(default_factory=list, description="Required parameters")


class Resource(BaseModel):
    """Represents an MCP resource."""
    
    uri: str = Field(description="Resource URI")
    name: str = Field(description="Resource name")
    description: Optional[str] = Field(default=None, description="Resource description")
    mime_type: Optional[str] = Field(default=None, description="MIME type")


class Prompt(BaseModel):
    """Represents an MCP prompt."""
    
    name: str = Field(description="Prompt name")
    description: str = Field(description="Prompt description")
    arguments: List[Dict[str, Any]] = Field(default_factory=list, description="Prompt arguments")


class ToolCall(BaseModel):
    """Represents a tool call."""
    
    name: str = Field(description="Tool name")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")


class ToolResult(BaseModel):
    """Represents a tool execution result."""
    
    content: Any = Field(description="Tool result content")
    is_error: bool = Field(default=False, description="Whether the result is an error")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Result metadata")


class MCPMessage(BaseModel):
    """Sample MCPMessage model."""
    content: str = Field(..., description="The message content")
    sender: str = Field(..., description="The sender of the message")