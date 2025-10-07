#!/usr/bin/env python3
"""
Image Demo for PowerPoint MCP Server

This example demonstrates basic image handling capabilities including
adding images to slides, creating photo galleries, and using logos.
"""
import asyncio
import sys
import os
import base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_image_slide, pptx_add_image, pptx_add_logo,
    pptx_add_image_with_caption, pptx_save
)


def create_sample_image_base64():
    """Create a simple colored rectangle as base64 for demo purposes."""
    # This creates a simple 100x100 blue square PNG
    import io
    from PIL import Image
    
    # Create a simple blue square
    img = Image.new('RGB', (100, 100), color='blue')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    
    # Convert to base64 data URL
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


async def create_image_demo():
    """Create a presentation demonstrating image capabilities."""
    
    print("🖼️ Creating Image Demo Presentation")
    print("=" * 50)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create(name="image_demo")
    print(f"   ✅ {result}")
    
    # Add title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="Image Handling Demo",
        subtitle="PowerPoint MCP Server Image Capabilities",
        author="Demo Application",
        date="2024"
    )
    print(f"   ✅ {result}")
    
    # Note: For this demo, we'll use base64 images since we don't have actual image files
    # In real usage, you would use file paths to actual images
    
    try:
        # Create a sample base64 image for demo
        sample_image = create_sample_image_base64()
        demo_note = "Note: Using generated base64 images for demo"
    except ImportError:
        # If PIL is not available, use a placeholder
        sample_image = "placeholder.png"
        demo_note = "Note: Using placeholder paths (actual images needed for real use)"
    
    print(f"\n   ℹ️ {demo_note}")
    
    # Example 1: Image slide
    print("\n3. Adding image slide...")
    if sample_image.startswith("data:"):
        result = await pptx_add_image_slide(
            title="Product Screenshot",
            image_path=sample_image
        )
        print(f"   ✅ Added image slide with base64 data")
    else:
        print(f"   ⚠️ Skipping - needs actual image file")
    
    # Example 2: Image with caption
    print("\n4. Adding image with caption...")
    result = await pptx_add_slide(
        title="Image with Caption Example",
        content=["Images can have descriptive captions"]
    )
    
    if sample_image.startswith("data:"):
        result = await pptx_add_image_with_caption(
            slide_index=2,
            image_path=sample_image,
            caption="Figure 1: Product Interface Screenshot",
            left=2.0,
            top=2.0,
            image_width=6.0,
            image_height=3.0
        )
        print(f"   ✅ Added image with caption")
    else:
        print(f"   ⚠️ Skipping - needs actual image file")
    
    # Example 3: Logo positioning
    print("\n5. Adding logos in different positions...")
    result = await pptx_add_slide(
        title="Logo Positioning Examples",
        content=["Logos can be placed in standard positions"]
    )
    
    if sample_image.startswith("data:"):
        # Add logos in corners
        positions = ["top-right", "bottom-left"]
        for position in positions:
            result = await pptx_add_logo(
                slide_index=3,
                logo_path=sample_image,
                position=position,
                size=1.0,
                margin=0.5
            )
            print(f"   ✅ Added logo at {position}")
    else:
        print(f"   ⚠️ Skipping - needs actual image file")
    
    # Example 4: Multiple images on one slide
    print("\n6. Adding multiple images...")
    result = await pptx_add_slide(
        title="Multiple Images Layout",
        content=["Multiple images can be arranged on a single slide"]
    )
    
    if sample_image.startswith("data:"):
        # Add multiple images in different positions
        positions = [
            (1.0, 2.5, 2.0, 2.0),  # left, top, width, height
            (4.0, 2.5, 2.0, 2.0),
            (7.0, 2.5, 2.0, 2.0)
        ]
        
        for i, (left, top, width, height) in enumerate(positions):
            result = await pptx_add_image(
                slide_index=4,
                image_path=sample_image,
                left=left,
                top=top,
                width=width,
                height=height
            )
        print(f"   ✅ Added {len(positions)} images to slide")
    else:
        print(f"   ⚠️ Skipping - needs actual image files")
    
    # Summary slide
    print("\n7. Adding summary slide...")
    result = await pptx_add_slide(
        title="Image Capabilities Summary",
        content=[
            "✓ Add images from file paths or base64 data",
            "✓ Create image slides with titles",
            "✓ Add captions to images",
            "✓ Position logos in standard locations",
            "✓ Create image galleries with grid layouts",
            "✓ Set background images for slides",
            "✓ Replace existing images",
            "✓ Control image size and position precisely",
            "",
            "Supported formats: PNG, JPG, GIF, BMP, and more"
        ]
    )
    print(f"   ✅ Summary slide added")
    
    # Save presentation
    print("\n8. Saving presentation...")
    result = await pptx_save(path="../outputs/image_demo.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "=" * 50)
    print("✨ Image demo completed!")
    print("📁 File saved as: outputs/image_demo.pptx")
    print("\n💡 For better results, use actual image files:")
    print("   - Product screenshots")
    print("   - Company logos")
    print("   - Charts exported as images")
    print("   - Photos from events")


async def main():
    """Main async function."""
    print("\n🚀 PowerPoint MCP Server - Image Demo")
    print("=" * 60)
    
    await create_image_demo()
    
    print("\n" + "=" * 60)
    print("📝 Next steps:")
    print("   1. Open outputs/image_demo.pptx in PowerPoint")
    print("   2. Replace demo images with actual files")
    print("   3. Try different image formats and sizes")


if __name__ == "__main__":
    asyncio.run(main())