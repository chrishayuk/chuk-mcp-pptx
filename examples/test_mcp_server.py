#!/usr/bin/env python3
"""
Test MCP Server Directly

Tests the MCP server by calling tools directly (without mcp-cli).
This helps isolate issues with the server itself vs mcp-cli integration.

Run from project root:
    uv run python examples/test_mcp_server.py
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_pptx import async_server


async def main():
    """Test MCP tools directly."""
    print("🧪 Testing MCP Server Tools Directly\n")

    # Test 1: Create presentation
    print("1. Testing pptx_create...")
    result = await async_server.pptx_create(name="test_deck", theme=None)
    response = json.loads(result)
    print(f"   Result: {response}")

    if "error" in response:
        print(f"   ❌ Error: {response['error']}")
        return
    else:
        print(f"   ✓ Created: {response['name']}\n")

    # Test 2: Add title slide
    print("2. Testing pptx_add_title_slide...")
    result = await async_server.pptx_add_title_slide(
        title="Test Presentation", subtitle="Created by MCP Server", presentation="test_deck"
    )
    response = json.loads(result)
    print(f"   Result: {response}")

    if "error" in response:
        print(f"   ❌ Error: {response['error']}")
        return
    else:
        print(f"   ✓ Slide added at index: {response.get('slide_index')}\n")

    # Test 3: Add content slide
    print("3. Testing pptx_add_slide...")
    result = await async_server.pptx_add_slide(
        title="Key Points", content=["Point 1", "Point 2", "Point 3"], presentation="test_deck"
    )
    response = json.loads(result)
    print(f"   Result: {response}")

    if "error" in response:
        print(f"   ❌ Error: {response['error']}")
        return
    else:
        print("   ✓ Slide added\n")

    # Test 4: List presentations
    print("4. Testing pptx_list...")
    result = await async_server.pptx_list()
    response = json.loads(result)
    print(f"   Result: {response}")

    if "error" in response:
        print(f"   ❌ Error: {response['error']}")
    else:
        count = len(response.get("presentations", []))
        print(f"   ✓ Found {count} presentation(s)\n")

    # Test 5: Get info
    print("5. Testing pptx_get_info...")
    result = await async_server.pptx_get_info(presentation="test_deck")
    response = json.loads(result)
    print(f"   Result: {response}")

    if "error" in response:
        print(f"   ❌ Error: {response['error']}")
    else:
        print(f"   ✓ Slides: {response.get('slide_count')}\n")

    # Test 6: Save to file
    print("6. Testing pptx_save...")
    result = await async_server.pptx_save(
        path="examples/output_mcp_test.pptx", presentation="test_deck"
    )
    response = json.loads(result)
    print(f"   Result: {response}")

    if "error" in response:
        print(f"   ❌ Error: {response['error']}")
    else:
        print(f"   ✓ Saved to: {response.get('path')}")
        print(f"   ✓ Size: {response.get('size_bytes'):,} bytes\n")

    print("✅ All MCP tools working correctly!")
    print("\n📄 Output file: examples/output_mcp_test.pptx")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
