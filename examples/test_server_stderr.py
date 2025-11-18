#!/usr/bin/env python3
"""
Capture Server STDERR Output

Runs the MCP server and captures all stderr output to help debug crashes.
This script runs the actual server.py that mcp-cli uses.

Run from project root:
    uv run python examples/test_server_stderr.py
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set up detailed logging to stderr
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

print("🚀 Starting MCP Server with debug logging enabled", file=sys.stderr)
print("=" * 60, file=sys.stderr)
print("", file=sys.stderr)

try:
    # Import and run the server
    from chuk_mcp_pptx import async_server

    print("✓ Server module loaded successfully", file=sys.stderr)
    print(f"✓ MCP instance: {async_server.mcp}", file=sys.stderr)
    print(f"✓ Manager instance: {async_server.manager}", file=sys.stderr)
    print(f"✓ VFS instance: {async_server.vfs}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Starting server in STDIO mode...", file=sys.stderr)
    print("(Server will communicate via stdin/stdout, logs go to stderr)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("", file=sys.stderr)

    # Run the server
    async_server.mcp.run(stdio=True)

except KeyboardInterrupt:
    print("\n\n" + "=" * 60, file=sys.stderr)
    print("✓ Server stopped by user (Ctrl+C)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
except Exception as e:
    print("\n\n" + "=" * 60, file=sys.stderr)
    print("❌ Server crashed with error:", file=sys.stderr)
    print(f"   {type(e).__name__}: {e}", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("", file=sys.stderr)
    import traceback

    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
