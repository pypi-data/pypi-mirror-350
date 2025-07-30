"""Command line interface for Open-MCP."""

import argparse
import sys
from typing import List, Optional

from .. import __version__


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Open-MCP: Model Context Protocol CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Open-MCP {__version__}",
        help="Show version and exit",
    )
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Server command
    server_parser = subparsers.add_parser("server", help="Start MCP server")
    server_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)",
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )
    
    # Client command
    client_parser = subparsers.add_parser("client", help="Run MCP client")
    client_parser.add_argument(
        "server_url",
        help="MCP server URL",
    )
    client_parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds (default: 30.0)",
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    
    if not parsed_args.command:
        print("Error: No command specified. Use --help for usage information.")
        return 1
        
    try:
        if parsed_args.command == "server":
            from ..server import MCPServer
            import uvicorn
            
            server = MCPServer()
            uvicorn.run(
                server.app,
                host=parsed_args.host,
                port=parsed_args.port,
            )
        elif parsed_args.command == "client":
            import asyncio
            from ..client import MCPClient
            
            async def run_client():
                async with MCPClient(
                    parsed_args.server_url,
                    timeout=parsed_args.timeout,
                ) as client:
                    tools = await client.list_tools()
                    print(f"Available tools: {[tool.name for tool in tools]}")
            
            asyncio.run(run_client())
            
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
