#!/usr/bin/env python3
"""
Comprehensive Image Gallery Demo for PowerPoint MCP Server

This example showcases all image handling capabilities including
galleries, backgrounds, replacements, and various positioning options.
"""
import asyncio
import sys
import os
import base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_image_slide, pptx_add_image, pptx_add_background_image,
    pptx_add_image_gallery, pptx_add_image_with_caption, pptx_add_logo,
    pptx_replace_image, pptx_save, pptx_get_info
)
import json


def create_colored_image_base64(color, size=(200, 150)):
    """Create a colored rectangle as base64 for demo purposes."""
    try:
        import io
        from PIL import Image
        
        # Create a colored rectangle
        img = Image.new('RGB', size, color=color)
        
        # Add some variation - draw a diagonal line
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.line([(0, 0), size], fill='white', width=3)
        draw.line([(0, size[1]), (size[0], 0)], fill='white', width=3)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        
        # Convert to base64 data URL
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    except ImportError:
        # Return placeholder if PIL not available
        return f"placeholder_{color}.png"


async def create_image_gallery():
    """Create a comprehensive gallery showcasing all image features."""
    
    print("🖼️ Creating Image Gallery Presentation")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create(name="image_gallery")
    print(f"   ✅ {result}")
    
    # Add title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="Image Gallery Showcase",
        subtitle="Complete Image Handling Capabilities",
        author="PowerPoint MCP Server Demo",
        date="2024",
        color_scheme="modern_blue"
    )
    print(f"   ✅ {result}")
    
    # Generate sample images for demo
    print("\n3. Generating demo images...")
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']
    demo_images = {}
    
    for color in colors:
        demo_images[color] = create_colored_image_base64(color)
    
    if demo_images['red'].startswith("data:"):
        print(f"   ✅ Generated {len(demo_images)} demo images")
        demo_mode = True
    else:
        print("   ⚠️ PIL not available - using placeholder paths")
        demo_mode = False
    
    # ============================================
    # BASIC IMAGE SLIDE
    # ============================================
    
    print("\n4. Adding basic image slide...")
    result = await pptx_add_image_slide(
        title="Basic Image Slide",
        image_path=demo_images['blue']
    )
    print(f"   ✅ Basic image slide added")
    
    # ============================================
    # IMAGE WITH CUSTOM POSITIONING
    # ============================================
    
    print("\n5. Adding custom positioned images...")
    result = await pptx_add_slide(
        title="Custom Image Positioning",
        content=[]  # No bullets - the positioned images demonstrate the feature
    )
    
    # Add images in different positions - adjusted for better slide layout
    positions = [
        ('red', 1.0, 1.8, 2.0, 1.5),
        ('green', 3.5, 1.8, 2.0, 1.5),
        ('blue', 6.0, 1.8, 2.0, 1.5),
        ('orange', 1.0, 3.5, 2.0, 1.5),
        ('purple', 3.5, 3.5, 2.0, 1.5),
        ('yellow', 6.0, 3.5, 2.0, 1.5),
    ]
    
    for color, left, top, width, height in positions:
        if demo_mode:
            result = await pptx_add_image(
                slide_index=2,
                image_path=demo_images[color],
                left=left,
                top=top,
                width=width,
                height=height
            )
    print(f"   ✅ Added {len(positions)} positioned images")
    
    # ============================================
    # IMAGE GALLERY GRID
    # ============================================
    
    print("\n6. Adding image gallery grid...")
    result = await pptx_add_slide(
        title="Image Gallery - Grid Layout",
        content=[]  # No bullets needed - the grid demonstrates the layout
    )
    
    if demo_mode:
        gallery_images = [demo_images[color] for color in colors[:6]]
        result = await pptx_add_image_gallery(
            slide_index=3,
            image_paths=gallery_images,
            columns=3,
            spacing=0.2,
            start_left=0.8,
            start_top=1.8,  # Content placeholder will be removed by the function
            image_width=2.8,
            image_height=1.6
        )
        print(f"   ✅ Created 3x2 image gallery grid")
    
    # ============================================
    # IMAGES WITH CAPTIONS
    # ============================================
    
    print("\n7. Adding images with captions...")
    result = await pptx_add_slide(
        title="Images with Captions",
        content=[]  # No bullets needed - images will show the captions
    )
    
    caption_examples = [
        ('red', "Figure 1: Primary Color", 1.0, 2.0),
        ('blue', "Figure 2: Secondary Color", 4.0, 2.0),
        ('green', "Figure 3: Tertiary Color", 7.0, 2.0)
    ]
    
    for color, caption, left, top in caption_examples:
        if demo_mode:
            result = await pptx_add_image_with_caption(
                slide_index=4,
                image_path=demo_images[color],
                caption=caption,
                left=left,
                top=top,
                image_width=2.0,
                image_height=1.5,
                caption_height=0.5
            )
    print(f"   ✅ Added {len(caption_examples)} images with captions")
    
    # ============================================
    # LOGO POSITIONING
    # ============================================
    
    print("\n8. Adding logos in standard positions...")
    result = await pptx_add_slide(
        title="Logo Positioning Options",
        content=[
            "Logos can be placed in standard positions:",
            "• Top-left, Top-center, Top-right",
            "• Bottom-left, Bottom-center, Bottom-right",
            "• Center of slide"
        ]
    )
    
    logo_positions = [
        "top-left", "top-right", 
        "bottom-left", "bottom-right"
    ]
    
    for position in logo_positions:
        if demo_mode:
            result = await pptx_add_logo(
                slide_index=5,
                logo_path=demo_images['cyan'],
                position=position,
                size=0.8,
                margin=0.3
            )
    print(f"   ✅ Added logos in {len(logo_positions)} positions")
    
    # ============================================
    # BACKGROUND IMAGE
    # ============================================
    
    print("\n9. Adding slide with background image...")
    result = await pptx_add_slide(
        title="Background Image Example",
        content=["This slide has a background image"]
    )
    
    if demo_mode:
        # Create a lighter background image
        bg_image = create_colored_image_base64('lightgray', size=(800, 600))
        result = await pptx_add_background_image(
            slide_index=6,
            image_path=bg_image
        )
        print(f"   ✅ Added background image to slide")
    
    # ============================================
    # IMAGE REPLACEMENT DEMO
    # ============================================
    
    print("\n10. Demonstrating image replacement...")
    result = await pptx_add_slide(
        title="Image Replacement",
        content=["Images can be replaced while maintaining position"]
    )
    
    # First add an image
    if demo_mode:
        result = await pptx_add_image(
            slide_index=7,
            image_path=demo_images['red'],
            left=4.0,
            top=3.0,
            width=2.0,
            height=2.0
        )
        
        # Then replace it with another
        result = await pptx_replace_image(
            slide_index=7,
            old_image_index=0,
            new_image_path=demo_images['green'],
            maintain_position=True,
            maintain_size=True
        )
        print(f"   ✅ Demonstrated image replacement")
    
    # ============================================
    # MIXED LAYOUT
    # ============================================
    
    print("\n11. Adding mixed image layout...")
    result = await pptx_add_slide(
        title="Mixed Image Layout",
        content=[]
    )
    
    if demo_mode:
        # Large featured image - adjusted for better layout
        result = await pptx_add_image(
            slide_index=8,
            image_path=demo_images['blue'],
            left=0.8,
            top=1.5,
            width=4.0,
            height=2.8
        )
        
        # Smaller supporting images - better positioned
        small_positions = [
            ('red', 5.2, 1.5, 1.8, 1.3),
            ('green', 7.2, 1.5, 1.8, 1.3),
            ('orange', 5.2, 3.0, 1.8, 1.3),
            ('purple', 7.2, 3.0, 1.8, 1.3),
        ]
        
        for color, left, top, width, height in small_positions:
            result = await pptx_add_image(
                slide_index=8,
                image_path=demo_images[color],
                left=left,
                top=top,
                width=width,
                height=height
            )
        
        print(f"   ✅ Created mixed layout with featured and supporting images")
    
    # ============================================
    # SUMMARY SLIDE
    # ============================================
    
    print("\n12. Adding summary slide...")
    result = await pptx_add_slide(
        title="Image Handling Summary",
        content=[
            "✓ Basic image slides with titles",
            "✓ Custom positioning and sizing",
            "✓ Automatic gallery grids",
            "✓ Images with captions",
            "✓ Logo positioning (7 standard positions)",
            "✓ Background images for slides",
            "✓ Image replacement with position retention",
            "✓ Mixed layouts with multiple images",
            "",
            "Supported formats:",
            "• File paths: PNG, JPG, GIF, BMP, TIFF",
            "• Base64 data URLs for embedded images",
            "• Automatic aspect ratio maintenance",
            "• Precise inch-based positioning"
        ]
    )
    print(f"   ✅ Summary slide added")
    
    # ============================================
    # SAVE AND REPORT
    # ============================================
    
    print("\n13. Getting presentation info...")
    info = await pptx_get_info()
    info_data = json.loads(info)
    print(f"   Total slides: {info_data['slides']}")
    
    print("\n14. Saving presentation...")
    result = await pptx_save(path="../outputs/image_gallery.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "=" * 60)
    print("🎉 Image Gallery created successfully!")
    print("📁 File saved as: outputs/image_gallery.pptx")
    print("\n📸 Features demonstrated:")
    print("   • Basic image slides")
    print("   • Custom positioning")
    print("   • Gallery grids")
    print("   • Images with captions")
    print("   • Logo positioning")
    print("   • Background images")
    print("   • Image replacement")
    print("\n💡 Open outputs/image_gallery.pptx to see all image features!")
    
    return "../outputs/image_gallery.pptx"


async def main():
    """Main async function."""
    print("\n🚀 PowerPoint MCP Server - Comprehensive Image Gallery")
    print("=" * 70)
    
    # Create the image gallery
    filename = await create_image_gallery()
    
    print("\n" + "=" * 70)
    print("📝 For production use:")
    print("   1. Replace demo images with actual photos/graphics")
    print("   2. Use company logos for branding")
    print("   3. Add product screenshots")
    print("   4. Include data visualizations exported as images")
    print("   5. Mix images with charts for rich presentations")


if __name__ == "__main__":
    asyncio.run(main())