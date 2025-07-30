"""
Open-MCP: An open-source Python package for Model Context Protocol.

This package provides client and server implementations for the Model Context Protocol,
enabling seamless integration between language models and external tools/data sources.
"""

from .client import MCPClient
from .server import MCPServer
from .models import (
    MCPMessage,
    MCPRequest,
    MCPResponse,
    MCPError,
    Tool,
    Resource,
    Prompt,
)

__version__ = "0.0.1"
__author__ = "Gaurav Chauhan"
__email__ = "2796gaurav@gmail.com"
__license__ = "MIT"
__description__ = "An open-source Python package for MCP (Model Context Protocol)"

__all__ = [
    "MCPClient",
    "MCPServer", 
    "MCPMessage",
    "MCPRequest",
    "MCPResponse", 
    "MCPError",
    "Tool",
    "Resource",
    "Prompt",
    "__version__",
]