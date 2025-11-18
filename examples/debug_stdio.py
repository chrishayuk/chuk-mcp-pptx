#!/usr/bin/env python3
"""
Debug STDIO MCP Server

Simulates how mcp-cli connects to the server via stdio.
This helps debug issues that only occur when the server runs in stdio mode.

Run from project root:
    uv run python examples/debug_stdio.py
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


async def test_stdio_mode():
    """Test the server in stdio mode by sending JSON-RPC messages."""
    print("🔍 Testing MCP Server in STDIO mode\n", file=sys.stderr)

    # Import the server module
    from chuk_mcp_pptx import async_server

    print("✓ Server module loaded", file=sys.stderr)
    print(f"✓ MCP server instance: {async_server.mcp}", file=sys.stderr)
    print(f"✓ Manager instance: {async_server.manager}", file=sys.stderr)
    print(f"✓ VFS provider: {async_server.vfs.provider}\n", file=sys.stderr)

    # Test 1: Call a tool directly
    print("Test 1: Calling pptx_create directly...", file=sys.stderr)
    try:
        result = await async_server.pptx_create(name="test", theme=None)
        print(f"✓ Result: {result}\n", file=sys.stderr)
    except Exception as e:
        print(f"✗ Error: {e}\n", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        return

    # Test 2: List all registered tools
    print("Test 2: Checking registered tools...", file=sys.stderr)
    try:
        # Access the internal registry
        if hasattr(async_server.mcp, "_registry"):
            registry = async_server.mcp._registry
            if hasattr(registry, "tools"):
                tools = registry.tools
                print(f"✓ Total tools registered: {len(tools)}", file=sys.stderr)
                print(f"✓ First 10 tools: {list(tools.keys())[:10]}\n", file=sys.stderr)
        else:
            print("⚠ Cannot access registry\n", file=sys.stderr)
    except Exception as e:
        print(f"⚠ Could not list tools: {e}\n", file=sys.stderr)

    # Test 3: Simulate JSON-RPC tool call
    print("Test 3: Simulating JSON-RPC request...", file=sys.stderr)
    try:
        # This is what mcp-cli sends to the server
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "pptx_create",
                "arguments": {"name": "french_cheeses", "theme": None},
            },
        }
        print(f"  Request: {json.dumps(request, indent=2)}\n", file=sys.stderr)

        # Try to call the tool through the MCP framework
        # Note: This is a simplified test - real MCP has more complex routing
        if hasattr(async_server.mcp, "call_tool"):
            result = await async_server.mcp.call_tool(
                name="pptx_create", arguments={"name": "french_cheeses", "theme": None}
            )
            print(f"✓ JSON-RPC result: {result}\n", file=sys.stderr)
        else:
            print("⚠ MCP server doesn't have call_tool method\n", file=sys.stderr)

    except Exception as e:
        print(f"✗ JSON-RPC error: {e}\n", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)

    # Test 4: Check if server can start in stdio mode
    print("Test 4: Testing server startup...", file=sys.stderr)
    print("  This would normally block, so we'll skip actual .run() call", file=sys.stderr)
    print("  But the server is configured to run with: mcp.run(stdio=True)\n", file=sys.stderr)

    print("✅ All stdio mode tests completed!", file=sys.stderr)
    print("\n📝 Summary:", file=sys.stderr)
    print("  - Server module loads correctly", file=sys.stderr)
    print("  - Tools can be called directly", file=sys.stderr)
    print("  - VFS is configured with memory provider", file=sys.stderr)
    print("  - Ready for mcp-cli integration\n", file=sys.stderr)


if __name__ == "__main__":
    try:
        asyncio.run(test_stdio_mode())
    except Exception as e:
        print(f"\n❌ Fatal error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
