#!/usr/bin/env python3
"""
Theme Gallery Demo for PowerPoint MCP Server

Demonstrates all available beautiful themes with dark and light modes.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_slide, pptx_save,
    pptx_apply_theme, pptx_list_themes,
    pptx_add_shape, pptx_add_smart_art,
    pptx_add_code_block
)


async def create_theme_showcase(theme_name: str):
    """Create a showcase presentation for a specific theme."""
    
    print(f"\n{'='*60}")
    print(f"Creating showcase for: {theme_name}")
    print(f"{'='*60}")
    
    # Create presentation
    await pptx_create(f"theme_{theme_name}")
    
    # Slide 1: Title slide (apply theme after adding content)
    await pptx_add_slide(
        title=f"{theme_name.replace('_', ' ').title()} Theme",
        content=[
            "Beautiful presentation design",
            "Modern color schemes",
            "Professional typography"
        ]
    )
    await pptx_apply_theme(slide_index=0, theme=theme_name)
    
    # Slide 2: Shapes and Colors
    await pptx_add_slide(
        title="Color Palette & Shapes",
        content=[]
    )
    
    # Add various shapes to show theme colors
    shapes = [
        ("rectangle", 1.0, 2.5, "Primary"),
        ("rounded_rectangle", 3.0, 2.5, "Secondary"),
        ("oval", 5.0, 2.5, "Accent"),
        ("hexagon", 7.0, 2.5, "Muted")
    ]
    
    for shape_type, left, top, label in shapes:
        await pptx_add_shape(
            slide_index=1,
            shape_type=shape_type,
            left=left,
            top=top,
            width=1.5,
            height=1.2,
            text=label
        )
    await pptx_apply_theme(slide_index=1, theme=theme_name)
    
    # Slide 3: SmartArt
    await pptx_add_slide(
        title="Process Flow",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=2,
        art_type="process",
        items=["Analyze", "Design", "Implement", "Test", "Deploy"],
        title="Development Workflow",
        left=1.0,
        top=2.0,
        width=8.0,
        height=2.5
    )
    await pptx_apply_theme(slide_index=2, theme=theme_name)
    
    # Slide 4: Code Example
    await pptx_add_slide(
        title="Code Example",
        content=[]
    )
    
    code_sample = """# Example function with theme colors
def process_data(items):
    results = []
    for item in items:
        if validate(item):
            results.append(transform(item))
    return results"""
    
    await pptx_add_code_block(
        slide_index=3,
        code=code_sample,
        language="python",
        left=1.5,
        top=2.0,
        width=7.0,
        height=3.0,
        theme=theme_name
    )
    await pptx_apply_theme(slide_index=3, theme=theme_name)
    
    # Save
    output_path = f"../outputs/theme_{theme_name}.pptx"
    await pptx_save(output_path)
    print(f"✅ Saved: {output_path}")


async def create_all_themes_gallery():
    """Create a single presentation showcasing all themes."""
    
    print("\n🎨 Creating All Themes Gallery")
    print("="*70)
    
    await pptx_create("all_themes_gallery")
    
    # List of all themes to showcase
    themes = [
        "dark_modern",
        "dark_blue", 
        "dark_purple",
        "dark_green",
        "light_minimal",
        "light_warm",
        "cyberpunk",
        "gradient_sunset"
    ]
    
    slide_index = 0
    
    for theme in themes:
        print(f"\nAdding {theme} theme slides...")
        
        # Title slide for this theme
        await pptx_add_slide(
            title=f"{theme.replace('_', ' ').title()} Theme",
            content=[
                "Professional design system",
                "Consistent color palette",
                "Modern typography"
            ]
        )
        await pptx_apply_theme(slide_index=slide_index, theme=theme)
        slide_index += 1
        
        # Content slide with shapes
        await pptx_add_slide(
            title=f"{theme.replace('_', ' ').title()} - Elements",
            content=[]
        )
        
        # Add shapes to show colors
        await pptx_add_shape(
            slide_index=slide_index,
            shape_type="rounded_rectangle",
            left=1.0, top=2.0, width=2.0, height=1.0,
            text="Primary"
        )
        await pptx_add_shape(
            slide_index=slide_index,
            shape_type="rounded_rectangle",
            left=3.5, top=2.0, width=2.0, height=1.0,
            text="Secondary"
        )
        await pptx_add_shape(
            slide_index=slide_index,
            shape_type="rounded_rectangle",
            left=6.0, top=2.0, width=2.0, height=1.0,
            text="Accent"
        )
        
        # Add a process flow
        await pptx_add_smart_art(
            slide_index=slide_index,
            art_type="process",
            items=["Step 1", "Step 2", "Step 3"],
            title="Process Example",
            left=1.5, top=3.5, width=7.0, height=1.5
        )
        
        await pptx_apply_theme(slide_index=slide_index, theme=theme)
        slide_index += 1
    
    # Save gallery
    await pptx_save("../outputs/all_themes_gallery.pptx")
    print("\n✅ Created all_themes_gallery.pptx with all theme variations!")


async def main():
    """Main execution function."""
    
    print("\n🎨 PowerPoint MCP Server - Theme Gallery")
    print("="*70)
    
    # List available themes
    themes_list = await pptx_list_themes()
    print("\n" + themes_list)
    
    # Create individual theme showcases for key themes
    key_themes = ["dark_modern", "dark_purple", "cyberpunk", "light_minimal"]
    
    print("\n📁 Creating individual theme showcases...")
    for theme in key_themes:
        await create_theme_showcase(theme)
    
    # Create comprehensive gallery
    print("\n📁 Creating comprehensive theme gallery...")
    await create_all_themes_gallery()
    
    print("\n" + "="*70)
    print("🎉 Theme Gallery Complete!")
    print("\n📁 Files created:")
    print("  • outputs/theme_dark_modern.pptx")
    print("  • outputs/theme_dark_purple.pptx") 
    print("  • outputs/theme_cyberpunk.pptx")
    print("  • outputs/theme_light_minimal.pptx")
    print("  • outputs/all_themes_gallery.pptx")
    print("\n💡 Each file demonstrates:")
    print("  • Beautiful dark and light themes")
    print("  • Consistent color palettes")
    print("  • Professional typography")
    print("  • Theme applied to shapes, charts, and SmartArt")


if __name__ == "__main__":
    asyncio.run(main())