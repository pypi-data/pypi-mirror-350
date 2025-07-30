# Open-MCP

[![PyPI version](https://badge.fury.io/py/open-mcp.svg)](https://badge.fury.io/py/open-mcp)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/open-mcp.svg)](https://anaconda.org/conda-forge/open-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/open-mcp.svg)](https://pypi.org/project/open-mcp/)
[![Documentation Status](https://readthedocs.org/projects/open-mcp/badge/?version=latest)](https://open-mcp.readthedocs.io/en/latest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An open-source Python package for **Model Context Protocol (MCP)** - enabling seamless integration between language models and external tools, data sources, and services.

## 🚀 Features

- **🔧 Tool Integration**: Execute external tools and functions from language models
- **📊 Resource Access**: Access and manage external data sources and files  
- **💬 Prompt Management**: Dynamic prompt templates with parameter substitution
- **🌐 Client & Server**: Full MCP client and server implementations
- **⚡ Async Support**: Built with modern async/await patterns
- **🔒 Type Safe**: Full type hints and Pydantic validation
- **🧪 Well Tested**: Comprehensive test suite with high coverage
- **📚 Documented**: Complete API documentation and examples

## 📦 Installation

### Via pip (PyPI)

```bash
pip install open-mcp
```

### Via uv (Recommended)

```bash
uv add open-mcp
```

### Via conda

```bash
conda install -c conda-forge open-mcp
```

### Development Installation

```bash
git clone https://github.com/2796gaurav/open-mcp.git
cd open-mcp
uv sync --all-extras --dev
```

## 🏃 Quick Start

### MCP Client

```python
import asyncio
from open_mcp import MCPClient

async def main():
    async with MCPClient("http://localhost:8000") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Execute a tool
        result = await client.call_tool("calculator", {
            "operation": "add",
            "a": 5,
            "b": 3
        })
        print(f"Result: {result.content}")
        
        # Access resources
        resources = await client.list_resources()
        content = await client.get_resource("file://data.json")
        
        # Use prompts
        prompt_content = await client.get_prompt("summarize", {
            "text": "Long text to summarize...",
            "max_words": 100
        })

asyncio.run(main())
```

### MCP Server

```python
from open_mcp import MCPServer
from open_mcp.models import Tool, ToolResult

# Create server instance
server = MCPServer("My MCP Server")

# Register a tool
@server.tool("calculator", "Perform basic calculations")
async def calculator(operation: str, a: float, b: float) -> ToolResult:
    operations = {
        "add": a + b,
        "subtract": a - b, 
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    
    result = operations.get(operation, "Unknown operation")
    return ToolResult(content=result)

# Register a resource
@server.resource("file://config.json", "Application configuration")
async def get_config():
    return {"setting1": "value1", "setting2": "value2"}

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server.app, host="0.0.0.0", port=8000)
```