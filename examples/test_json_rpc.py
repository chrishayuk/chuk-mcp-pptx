#!/usr/bin/env python3
"""
Test JSON-RPC Communication

Sends actual JSON-RPC messages to the server via stdin/stdout
to test if the MCP protocol is working correctly.
"""

import subprocess
import json
import sys
import time
from pathlib import Path


def send_jsonrpc_request(proc, method, params=None, id=1):
    """Send a JSON-RPC request to the server."""
    request = {
        "jsonrpc": "2.0",
        "id": id,
        "method": method,
    }
    if params:
        request["params"] = params

    message = json.dumps(request) + "\n"
    print(f"→ Sending: {message.strip()}", file=sys.stderr)
    proc.stdin.write(message)
    proc.stdin.flush()

    # Read response
    response_line = proc.stdout.readline()
    if response_line:
        print(f"← Received: {response_line.strip()}", file=sys.stderr)
        return json.loads(response_line)
    return None


def main():
    print("🧪 Testing JSON-RPC Communication with MCP Server\n", file=sys.stderr)

    # Start the server
    server_path = Path(__file__).parent.parent / "src" / "chuk_mcp_pptx" / "async_server.py"

    print(f"Starting server: {server_path}\n", file=sys.stderr)

    proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "chuk_mcp_pptx.async_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Give server time to start
    time.sleep(2)

    try:
        # Test 1: Initialize
        print("Test 1: Sending initialize request...", file=sys.stderr)
        response = send_jsonrpc_request(
            proc,
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        )

        if response:
            print("✓ Initialize response received\n", file=sys.stderr)
        else:
            print("✗ No response to initialize\n", file=sys.stderr)
            return

        # Test 2: List tools
        print("Test 2: Listing tools...", file=sys.stderr)
        response = send_jsonrpc_request(proc, "tools/list", {}, id=2)

        if response and "result" in response:
            tools = response["result"].get("tools", [])
            print(f"✓ Found {len(tools)} tools\n", file=sys.stderr)
        else:
            print("✗ No tools list received\n", file=sys.stderr)

        # Test 3: Call a tool
        print("Test 3: Calling pptx_create...", file=sys.stderr)
        response = send_jsonrpc_request(
            proc,
            "tools/call",
            {"name": "pptx_create", "arguments": {"name": "test_presentation", "theme": None}},
            id=3,
        )

        if response:
            print(f"✓ Tool call response: {json.dumps(response, indent=2)}\n", file=sys.stderr)
        else:
            print("✗ No response from tool call\n", file=sys.stderr)

        print("✅ JSON-RPC test complete!", file=sys.stderr)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    main()
