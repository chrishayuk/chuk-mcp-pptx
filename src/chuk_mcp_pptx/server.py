#!/usr/bin/env python3
"""
PowerPoint MCP Server - Async-native implementation

This module provides the async MCP server for PowerPoint operations.
Supports both stdio (for Claude Desktop) and HTTP (for API access) transports.
"""

import sys
import os

# Import mcp instance and all registered tools from async server
from .async_server import mcp  # noqa: F401

# The tools are registered via decorators in their respective modules
# They become available as soon as the modules are imported by async_server


def main():
    """Main entry point for the MCP server.

    Automatically detects transport mode:
    - stdio: When stdin is piped or MCP_STDIO is set (for Claude Desktop)
    - HTTP: Default mode for API access
    """
    import argparse

    parser = argparse.ArgumentParser(description="PowerPoint MCP Server")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["stdio", "http"],
        default=None,
        help="Transport mode (stdio for Claude Desktop, http for API)",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP mode (default: localhost)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP mode (default: 8000)")

    args = parser.parse_args()

    # Determine transport mode
    if args.mode == "stdio":
        # Explicitly requested stdio mode
        print("PowerPoint MCP Server starting in STDIO mode", file=sys.stderr)
        mcp.run(stdio=True)
    elif args.mode == "http":
        # Explicitly requested HTTP mode
        print(
            f"PowerPoint MCP Server starting in HTTP mode on {args.host}:{args.port}",
            file=sys.stderr,
        )
        mcp.run(host=args.host, port=args.port, stdio=False)
    else:
        # Auto-detect mode based on environment
        if os.environ.get("MCP_STDIO") or (not sys.stdin.isatty()):
            print("PowerPoint MCP Server starting in STDIO mode (auto-detected)", file=sys.stderr)
            mcp.run(stdio=True)
        else:
            print(
                f"PowerPoint MCP Server starting in HTTP mode on {args.host}:{args.port}",
                file=sys.stderr,
            )
            mcp.run(host=args.host, port=args.port, stdio=False)


if __name__ == "__main__":
    main()
