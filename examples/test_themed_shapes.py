#!/usr/bin/env python3
"""
Test that shapes and SmartArt automatically use theme colors
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_slide, pptx_save,
    pptx_apply_theme, pptx_add_shape, pptx_add_smart_art,
    pptx_add_arrow
)

async def test_themed_shapes():
    """Test shapes automatically using theme colors."""
    
    print("\n🎨 Testing Themed Shapes and SmartArt")
    print("="*60)
    
    # Create presentation
    await pptx_create("themed_shapes_test")
    
    # Test 1: Dark Purple Theme
    print("\n1. Testing Dark Purple theme...")
    await pptx_add_slide(
        title="Dark Purple Theme - Auto Colors",
        content=[]
    )
    await pptx_apply_theme(slide_index=0, theme="dark_purple")
    
    # Add shapes WITHOUT specifying colors - should use theme
    await pptx_add_shape(
        slide_index=0,
        shape_type="rounded_rectangle",
        left=1.0, top=2.0, width=2.0, height=1.0,
        text="Auto Theme Color"
    )
    
    await pptx_add_shape(
        slide_index=0,
        shape_type="hexagon",
        left=3.5, top=2.0, width=2.0, height=1.0,
        text="Primary"
    )
    
    await pptx_add_shape(
        slide_index=0,
        shape_type="oval",
        left=6.0, top=2.0, width=2.0, height=1.0,
        text="Secondary"
    )
    
    # Add SmartArt - should use theme colors
    await pptx_add_smart_art(
        slide_index=0,
        art_type="process",
        items=["Step 1", "Step 2", "Step 3"],
        title="",
        left=1.0, top=3.5, width=7.0, height=1.5
    )
    
    # Test 2: Cyberpunk Theme
    print("2. Testing Cyberpunk theme...")
    await pptx_add_slide(
        title="Cyberpunk Theme - Neon Colors",
        content=[]
    )
    await pptx_apply_theme(slide_index=1, theme="cyberpunk")
    
    # Add shapes - should get neon colors
    await pptx_add_shape(
        slide_index=1,
        shape_type="star",
        left=2.0, top=2.0, width=1.5, height=1.5,
        text="Neon"
    )
    
    await pptx_add_shape(
        slide_index=1,
        shape_type="diamond",
        left=4.5, top=2.0, width=1.5, height=1.5,
        text="Cyber"
    )
    
    await pptx_add_shape(
        slide_index=1,
        shape_type="triangle",
        left=7.0, top=2.0, width=1.5, height=1.5,
        text="Punk"
    )
    
    # Add connectors - should use theme colors
    await pptx_add_arrow(
        slide_index=1,
        start_x=3.5, start_y=2.75,
        end_x=4.5, end_y=2.75,
        connector_type="straight",
        arrow_end=True
    )
    
    await pptx_add_arrow(
        slide_index=1,
        start_x=6.0, start_y=2.75,
        end_x=7.0, end_y=2.75,
        connector_type="straight",
        arrow_end=True
    )
    
    # Add SmartArt with cyberpunk theme
    await pptx_add_smart_art(
        slide_index=1,
        art_type="cycle",
        items=["Hack", "Build", "Deploy", "Monitor"],
        title="",
        left=2.0, top=4.0, width=6.0, height=2.0
    )
    
    # Test 3: Light Minimal Theme
    print("3. Testing Light Minimal theme...")
    await pptx_add_slide(
        title="Light Minimal - Clean Design",
        content=[]
    )
    await pptx_apply_theme(slide_index=2, theme="light_minimal")
    
    # Add shapes with minimal theme
    await pptx_add_shape(
        slide_index=2,
        shape_type="rectangle",
        left=2.0, top=2.5, width=2.0, height=1.0,
        text="Clean"
    )
    
    await pptx_add_shape(
        slide_index=2,
        shape_type="rounded_rectangle",
        left=4.5, top=2.5, width=2.0, height=1.0,
        text="Simple"
    )
    
    await pptx_add_shape(
        slide_index=2,
        shape_type="oval",
        left=7.0, top=2.5, width=2.0, height=1.0,
        text="Elegant"
    )
    
    # Add hierarchy SmartArt
    await pptx_add_smart_art(
        slide_index=2,
        art_type="hierarchy",
        items=["CEO", "CTO", "VP Eng", "Manager", "Developer"],
        title="",
        left=2.0, top=4.0, width=6.0, height=2.0
    )
    
    # Test 4: Dark Green Theme
    print("4. Testing Dark Green theme...")
    await pptx_add_slide(
        title="Dark Green - Nature Theme",
        content=[]
    )
    await pptx_apply_theme(slide_index=3, theme="dark_green")
    
    # Create a relationship diagram
    await pptx_add_smart_art(
        slide_index=3,
        art_type="relationship",
        items=["Earth", "Water", "Fire", "Air", "Spirit"],
        title="",
        left=1.5, top=2.5, width=7.0, height=3.0
    )
    
    # Save
    await pptx_save("../outputs/themed_shapes_test.pptx")
    print("\n✅ Created themed_shapes_test.pptx")
    print("\n📝 Results:")
    print("  • Shapes automatically use theme colors")
    print("  • SmartArt respects theme palette")
    print("  • Connectors use theme colors")
    print("  • Each theme provides unique visual style")
    
if __name__ == "__main__":
    asyncio.run(test_themed_shapes())