#!/usr/bin/env python3
"""
Shapes Gallery Demo for PowerPoint MCP Server

Demonstrates all available shapes and their customization options.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_shape, pptx_add_arrow, pptx_save,
    pptx_get_info
)


async def create_shapes_gallery():
    """Create a comprehensive shapes gallery presentation."""
    
    print("\n🚀 PowerPoint MCP Server - Shapes Gallery")
    print("=" * 70)
    print("📐 Creating Shapes Gallery Presentation")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create("shapes_gallery")
    print(f"   ✅ {result}")
    
    # Title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="Shapes Gallery Showcase",
        subtitle="Comprehensive Shape Demonstrations",
        author="PowerPoint MCP Server",
        color_scheme="modern_blue"
    )
    print(f"   ✅ Created title slide at index 0")
    
    # ============================================
    # BASIC SHAPES
    # ============================================
    
    print("\n3. Adding Basic Shapes...")
    result = await pptx_add_slide(
        title="Basic Shapes Collection",
        content=[]
    )
    
    # Add various basic shapes
    basic_shapes = [
        ("rectangle", 1.0, 2.0, "#2E86AB"),
        ("rounded_rectangle", 3.5, 2.0, "#A23B72"),
        ("oval", 6.0, 2.0, "#F18F01"),
        ("diamond", 1.0, 4.0, "#C73E1D"),
        ("triangle", 3.5, 4.0, "#6A994E"),
        ("hexagon", 6.0, 4.0, "#BC4B51")
    ]
    
    for shape_type, left, top, color in basic_shapes:
        await pptx_add_shape(
            slide_index=1,
            shape_type=shape_type,
            left=left,
            top=top,
            width=2.0,
            height=1.5,
            text=shape_type.replace("_", " ").title(),
            fill_color=color,
            line_color="#333333",
            line_width=2.0
        )
    print(f"   ✅ Added {len(basic_shapes)} basic shapes")
    
    # ============================================
    # ARROWS AND CONNECTORS
    # ============================================
    
    print("\n4. Adding Arrows and Connectors...")
    result = await pptx_add_slide(
        title="Arrows and Connectors",
        content=[]
    )
    
    # Create pairs of shapes to connect with different arrow types
    
    # 1. Straight connector
    await pptx_add_shape(
        slide_index=2,
        shape_type="rectangle",
        left=1.0,
        top=1.5,
        width=1.2,
        height=0.8,
        text="A",
        fill_color="#FFE0E0",
        line_color="#FF0000"
    )
    await pptx_add_shape(
        slide_index=2,
        shape_type="rectangle",
        left=3.5,
        top=1.5,
        width=1.2,
        height=0.8,
        text="B",
        fill_color="#FFE0E0",
        line_color="#FF0000"
    )
    await pptx_add_arrow(
        slide_index=2,
        start_x=2.2,
        start_y=1.9,
        end_x=3.5,
        end_y=1.9,
        connector_type="straight",
        line_color="#FF0000",
        line_width=2.5,
        arrow_end=True
    )
    
    # 2. Elbow connector
    await pptx_add_shape(
        slide_index=2,
        shape_type="oval",
        left=5.5,
        top=1.5,
        width=1.2,
        height=0.8,
        text="C",
        fill_color="#E0FFE0",
        line_color="#00AA00"
    )
    await pptx_add_shape(
        slide_index=2,
        shape_type="oval",
        left=8.0,
        top=2.5,
        width=1.2,
        height=0.8,
        text="D",
        fill_color="#E0FFE0",
        line_color="#00AA00"
    )
    await pptx_add_arrow(
        slide_index=2,
        start_x=6.7,
        start_y=1.9,
        end_x=8.0,
        end_y=2.9,
        connector_type="elbow",
        line_color="#00AA00",
        line_width=2.5,
        arrow_end=True
    )
    
    # 3. Curved connector
    await pptx_add_shape(
        slide_index=2,
        shape_type="diamond",
        left=1.0,
        top=3.5,
        width=1.2,
        height=0.8,
        text="E",
        fill_color="#E0E0FF",
        line_color="#0000FF"
    )
    await pptx_add_shape(
        slide_index=2,
        shape_type="diamond",
        left=3.5,
        top=4.5,
        width=1.2,
        height=0.8,
        text="F",
        fill_color="#E0E0FF",
        line_color="#0000FF"
    )
    await pptx_add_arrow(
        slide_index=2,
        start_x=2.2,
        start_y=3.9,
        end_x=3.5,
        end_y=4.9,
        connector_type="curved",
        line_color="#0000FF",
        line_width=2.5,
        arrow_end=True
    )
    
    # 4. Bidirectional arrow
    await pptx_add_shape(
        slide_index=2,
        shape_type="hexagon",
        left=5.5,
        top=4.0,
        width=1.2,
        height=0.8,
        text="G",
        fill_color="#FFE0FF",
        line_color="#FF00FF"
    )
    await pptx_add_shape(
        slide_index=2,
        shape_type="hexagon",
        left=8.0,
        top=4.0,
        width=1.2,
        height=0.8,
        text="H",
        fill_color="#FFE0FF",
        line_color="#FF00FF"
    )
    await pptx_add_arrow(
        slide_index=2,
        start_x=6.7,
        start_y=4.4,
        end_x=8.0,
        end_y=4.4,
        connector_type="straight",
        line_color="#FF00FF",
        line_width=2.5,
        arrow_start=True,
        arrow_end=True
    )
    
    # Add type labels
    labels = [
        ("Straight", 2.25, 1.0),
        ("Elbow", 6.75, 1.0),
        ("Curved", 2.25, 3.0),
        ("Bidirectional", 6.75, 3.5)
    ]
    
    for text, left, top in labels:
        await pptx_add_shape(
            slide_index=2,
            shape_type="rounded_rectangle",
            left=left,
            top=top,
            width=1.5,
            height=0.3,
            text=text,
            fill_color="#FFFFCC",
            line_color="#999999",
            line_width=1.0
        )
    
    print(f"   ✅ Added 4 arrow types with connected shapes")
    
    # ============================================
    # SPECIAL SHAPES
    # ============================================
    
    print("\n5. Adding Special Shapes...")
    result = await pptx_add_slide(
        title="Special Shapes and Icons",
        content=[]
    )
    
    special_shapes = [
        ("star", 1.5, 2.0, "#FFD700", "Award"),
        ("plus", 4.0, 2.0, "#FF6B6B", "Medical"),
        ("chevron", 6.5, 2.0, "#4ECDC4", "Progress"),
        ("callout", 1.5, 4.0, "#95E77E", "Comment"),
        ("arrow", 4.0, 4.0, "#FFA500", "Direction"),
        ("rounded_rectangle", 6.5, 4.0, "#9B5DE5", "Button")
    ]
    
    for shape_type, left, top, color, label in special_shapes:
        await pptx_add_shape(
            slide_index=3,
            shape_type=shape_type,
            left=left,
            top=top,
            width=1.8,
            height=1.5,
            text=label,
            fill_color=color,
            line_color="#FFFFFF",
            line_width=2.0
        )
    print(f"   ✅ Added {len(special_shapes)} special shapes")
    
    # ============================================
    # SHAPE COMBINATIONS
    # ============================================
    
    print("\n6. Creating Shape Combinations...")
    result = await pptx_add_slide(
        title="Shape Combinations - Process Flow",
        content=[]
    )
    
    # Create a process flow with shapes and arrows
    process_steps = [
        ("Start", 0.5, 3.0, "oval", "#4CAF50"),
        ("Process", 2.5, 3.0, "rectangle", "#2196F3"),
        ("Decision", 4.5, 3.0, "diamond", "#FF9800"),
        ("End", 6.5, 3.0, "oval", "#F44336"),
    ]
    
    # Add shapes
    for text, left, top, shape, color in process_steps:
        await pptx_add_shape(
            slide_index=4,
            shape_type=shape,
            left=left,
            top=top,
            width=1.5,
            height=1.0,
            text=text,
            fill_color=color,
            line_color="#333333",
            line_width=2.0
        )
    
    # Add connecting arrows
    arrow_positions = [
        (2.0, 3.5, 2.5, 3.5),
        (4.0, 3.5, 4.5, 3.5),
        (6.0, 3.5, 6.5, 3.5),
    ]
    
    for start_x, start_y, end_x, end_y in arrow_positions:
        await pptx_add_arrow(
            slide_index=4,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            connector_type="straight",
            line_color="#666666",
            line_width=2.0,
            arrow_end=True
        )
    print(f"   ✅ Created process flow with {len(process_steps)} steps")
    
    # ============================================
    # COLOR VARIATIONS
    # ============================================
    
    print("\n7. Adding Color Variations...")
    result = await pptx_add_slide(
        title="Shape Color Variations",
        content=[]
    )
    
    # Show same shape with different colors
    colors = [
        ("#FF6B6B", "Red"),
        ("#4ECDC4", "Teal"),
        ("#45B7D1", "Blue"),
        ("#FFA07A", "Peach"),
        ("#98D8C8", "Mint"),
        ("#F7DC6F", "Yellow"),
        ("#BB8FCE", "Purple"),
        ("#85C88A", "Green"),
        ("#F8B739", "Orange")
    ]
    
    for idx, (color, name) in enumerate(colors):
        row = idx // 3
        col = idx % 3
        left = 1.5 + col * 2.5
        top = 2.0 + row * 1.5
        
        await pptx_add_shape(
            slide_index=5,
            shape_type="rounded_rectangle",
            left=left,
            top=top,
            width=2.0,
            height=1.0,
            text=name,
            fill_color=color,
            line_color="#FFFFFF",
            line_width=3.0
        )
    print(f"   ✅ Added {len(colors)} color variations")
    
    # ============================================
    # SHAPE SIZES
    # ============================================
    
    print("\n8. Demonstrating Shape Sizes...")
    result = await pptx_add_slide(
        title="Shape Size Variations",
        content=[]
    )
    
    # Different sizes of the same shape
    sizes = [
        (1.0, 0.75, "Small"),
        (1.5, 1.125, "Medium"),
        (2.0, 1.5, "Large"),
        (2.5, 1.875, "X-Large")
    ]
    
    left_pos = 1.0
    for width, height, label in sizes:
        await pptx_add_shape(
            slide_index=6,
            shape_type="star",
            left=left_pos,
            top=3.0 - height/2,  # Center vertically
            width=width,
            height=height,
            text=label,
            fill_color="#FFD700",
            line_color="#FFA500",
            line_width=2.0
        )
        left_pos += width + 0.5
    print(f"   ✅ Added {len(sizes)} size variations")
    
    # ============================================
    # SUMMARY SLIDE
    # ============================================
    
    print("\n9. Adding summary slide...")
    result = await pptx_add_slide(
        title="Shape Capabilities Summary",
        content=[
            "• 11+ shape types available",
            "• Customizable colors and borders",
            "• Text support in all shapes",
            "• Arrow and connector options",
            "• Process flow diagrams",
            "• Shape combinations for complex graphics",
            "• Full size and position control"
        ]
    )
    print(f"   ✅ Summary slide added")
    
    # ============================================
    # SAVE AND REPORT
    # ============================================
    
    print("\n10. Getting presentation info...")
    info = await pptx_get_info()
    print(f"   Total slides: 8")
    
    print("\n11. Saving presentation...")
    result = await pptx_save("../outputs/shapes_gallery.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "=" * 60)
    print("🎉 Shapes Gallery created successfully!")
    print("📁 File saved as: outputs/shapes_gallery.pptx")
    print("\n📐 Shapes demonstrated:")
    print("   • Basic shapes (rectangle, oval, triangle, etc.)")
    print("   • Arrows and connectors")
    print("   • Special shapes (star, chevron, callout)")
    print("   • Process flow diagrams")
    print("   • Color and size variations")
    print("\n💡 Open outputs/shapes_gallery.pptx to see all shape types!")


async def main():
    """Main execution function."""
    await create_shapes_gallery()
    
    print("\n" + "=" * 70)
    print("📝 Use cases for shapes:")
    print("   1. Process flow diagrams")
    print("   2. Organizational charts")
    print("   3. Icons and visual elements")
    print("   4. Callouts and annotations")
    print("   5. Custom graphics and designs")
    print("   6. Decision trees")
    print("   7. Timeline visualizations")
    print("\n💼 Perfect for:")
    print("   • Technical presentations")
    print("   • Business process documentation")
    print("   • Training materials")
    print("   • Infographics")
    print("   • Visual storytelling")


if __name__ == "__main__":
    asyncio.run(main())