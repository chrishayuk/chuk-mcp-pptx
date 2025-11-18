#!/usr/bin/env python3
"""
Simple Example for PowerPoint MCP Server

This example demonstrates basic functionality:
- Creating a presentation
- Adding slides
- Saving the presentation
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from chuk_mcp_pptx.server import (
    pptx_create,
    pptx_add_title_slide,
    pptx_add_slide,
    pptx_add_text_slide,
    pptx_save,
    pptx_get_info,
)
import json


async def main():
    """Create a simple presentation"""
    print("📝 Creating Simple Presentation")
    print("=" * 40)

    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create(name="simple_demo")
    print(f"   ✅ {result}")

    # Add title slide
    print("\n2. Adding title slide...")
    result = await pptx_add_title_slide(
        title="Welcome to PowerPoint MCP", subtitle="Simple demonstration of capabilities"
    )
    print(f"   ✅ {result}")

    # Add content slide with bullets
    print("\n3. Adding content slide...")
    result = await pptx_add_slide(
        title="Key Features",
        content=[
            "Create presentations programmatically",
            "Add various slide types",
            "Insert charts and images",
            "Export and import presentations",
            "Async/await support for better performance",
        ],
    )
    print(f"   ✅ {result}")

    # Add text slide
    print("\n4. Adding text slide...")
    result = await pptx_add_text_slide(
        title="About This Demo",
        text="This is a simple demonstration of the PowerPoint MCP Server. "
        "It shows how easy it is to create presentations programmatically "
        "using async Python functions. The server supports various slide types, "
        "charts, images, and professional formatting options.",
    )
    print(f"   ✅ {result}")

    # Get presentation info
    print("\n5. Getting presentation info...")
    info = await pptx_get_info()
    info_data = json.loads(info)
    print(f"   Total slides: {info_data['slides']}")
    for slide in info_data["slide_details"]:
        print(f"   - Slide {slide['index']}: {slide['title']}")

    # Save presentation
    print("\n6. Saving presentation...")
    result = await pptx_save(path="../outputs/simple_demo.pptx")
    print(f"   ✅ {result}")

    print("\n" + "=" * 40)
    print("✨ Simple demo completed!")
    print("📁 File saved as: outputs/simple_demo.pptx")


if __name__ == "__main__":
    print("🚀 PowerPoint MCP Server - Simple Example")
    print("=" * 50)

    # Run the async main function
    asyncio.run(main())
