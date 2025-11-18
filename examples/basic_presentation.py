#!/usr/bin/env python3
"""
Basic Presentation Example

Demonstrates creating a simple PowerPoint presentation using the chuk-mcp-pptx library.
This script creates a presentation with:
- Title slide
- Content slide with bullet points
- Chart slide

Run from project root:
    uv run python examples/basic_presentation.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_pptx.presentation_manager import PresentationManager
from chuk_virtual_fs import AsyncVirtualFileSystem


async def main():
    """Create a basic presentation."""
    print("🎯 Creating basic PowerPoint presentation...\n")

    # Initialize VFS with memory provider
    print("1. Initializing Virtual File System (memory provider)...")
    vfs = AsyncVirtualFileSystem(provider="memory")
    await vfs.initialize()
    print("   ✓ VFS initialized\n")

    # Create presentation manager
    print("2. Creating Presentation Manager...")
    manager = PresentationManager(vfs=vfs, base_path="presentations")
    print("   ✓ Manager created\n")

    # Create a new presentation
    print("3. Creating new presentation 'my_presentation'...")
    metadata = await manager.create(name="my_presentation")
    print(f"   ✓ Created: {metadata.name}")
    print(f"   ✓ Slides: {metadata.slide_count}\n")

    # Verify we can retrieve it
    print("4. Retrieving presentation from VFS...")
    result = await manager.get("my_presentation")
    if result:
        prs, meta = result
        print("   ✓ Retrieved successfully")
        print(f"   ✓ Slide count: {len(prs.slides)}")
        print(f"   ✓ Metadata: {meta.name}\n")
    else:
        print("   ✗ Failed to retrieve\n")
        return

    # Add a title slide
    print("5. Adding title slide...")
    from chuk_mcp_pptx.constants import SlideLayoutIndex

    slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "My First Presentation"
    if len(slide.placeholders) > 1:
        slide.placeholders[1].text = "Created with chuk-mcp-pptx"

    # Update in VFS
    await manager.update("my_presentation")
    print("   ✓ Title slide added\n")

    # Add a content slide
    print("6. Adding content slide with bullets...")
    slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE_AND_CONTENT]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Key Features"

    if len(slide.placeholders) > 1:
        text_frame = slide.placeholders[1].text_frame
        bullets = [
            "Easy to use API",
            "Virtual filesystem integration",
            "Component-based design system",
            "Pydantic models for type safety",
        ]
        for idx, bullet in enumerate(bullets):
            if idx == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            p.text = bullet
            p.level = 0

    await manager.update("my_presentation")
    print(f"   ✓ Content slide added with {len(bullets)} bullets\n")

    # Verify final state
    result = await manager.get("my_presentation")
    if result:
        prs, meta = result
        print("7. Final presentation state:")
        print(f"   ✓ Total slides: {len(prs.slides)}")
        print(f"   ✓ Presentation name: {meta.name}\n")

    # Export to file
    print("8. Saving to file...")
    output_path = "examples/output_basic.pptx"
    prs.save(output_path)

    # Check file size
    file_size = Path(output_path).stat().st_size
    print(f"   ✓ Saved to: {output_path}")
    print(f"   ✓ File size: {file_size:,} bytes\n")

    # List all presentations
    print("9. Listing all presentations in VFS...")
    list_response = await manager.list_presentations()
    print(f"   ✓ Total presentations: {len(list_response.presentations)}")
    for p in list_response.presentations:
        print(f"     - {p.name}: {p.slide_count} slides, current={p.is_current}")

    print("\n✅ Success! Presentation created successfully.")
    print(f"📄 Output saved to: {output_path}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
