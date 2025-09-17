#!/usr/bin/env python3
"""Test connector implementation to identify issues."""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_slide, pptx_add_shape, 
    pptx_add_arrow, pptx_save
)

async def test_connectors():
    """Test various connector scenarios."""
    print("🔍 Testing Connector Implementation")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating test presentation...")
    await pptx_create("connector_test")
    
    # Test 1: Basic straight connectors
    print("\n2. Testing straight connectors...")
    await pptx_add_slide(
        title="Straight Connectors Test",
        content=[]
    )
    
    # Add two shapes to connect
    await pptx_add_shape(
        slide_index=0,
        shape_type="rectangle",
        left=2.0,
        top=2.0,
        width=1.5,
        height=1.0,
        text="Start",
        fill_color="#4CAF50"
    )
    
    await pptx_add_shape(
        slide_index=0,
        shape_type="rectangle",
        left=6.0,
        top=2.0,
        width=1.5,
        height=1.0,
        text="End",
        fill_color="#2196F3"
    )
    
    # Try to connect them
    result = await pptx_add_arrow(
        slide_index=0,
        start_x=3.5,  # Right edge of first shape
        start_y=2.5,  # Middle of first shape
        end_x=6.0,    # Left edge of second shape
        end_y=2.5,    # Middle of second shape
        connector_type="straight",
        arrow_end=True
    )
    print(f"   Straight connector: {result}")
    
    # Test 2: Elbow connectors
    print("\n3. Testing elbow connectors...")
    await pptx_add_slide(
        title="Elbow Connectors Test",
        content=[]
    )
    
    # Add shapes at different heights
    await pptx_add_shape(
        slide_index=1,
        shape_type="oval",
        left=2.0,
        top=2.0,
        width=1.5,
        height=1.0,
        text="A",
        fill_color="#FF9800"
    )
    
    await pptx_add_shape(
        slide_index=1,
        shape_type="oval",
        left=6.0,
        top=4.0,
        width=1.5,
        height=1.0,
        text="B",
        fill_color="#9C27B0"
    )
    
    result = await pptx_add_arrow(
        slide_index=1,
        start_x=3.5,
        start_y=2.5,
        end_x=6.0,
        end_y=4.5,
        connector_type="elbow",
        arrow_end=True
    )
    print(f"   Elbow connector: {result}")
    
    # Test 3: Curved connectors
    print("\n4. Testing curved connectors...")
    await pptx_add_slide(
        title="Curved Connectors Test",
        content=[]
    )
    
    # Add shapes in a circular pattern
    positions = [
        (4.0, 2.0, "Top"),
        (5.5, 3.0, "Right"),
        (4.0, 4.0, "Bottom"),
        (2.5, 3.0, "Left")
    ]
    
    for x, y, text in positions:
        await pptx_add_shape(
            slide_index=2,
            shape_type="diamond",
            left=x,
            top=y,
            width=1.0,
            height=1.0,
            text=text,
            fill_color="#00BCD4"
        )
    
    # Connect them in a circle
    for i in range(4):
        start_x, start_y, _ = positions[i]
        end_x, end_y, _ = positions[(i + 1) % 4]
        
        result = await pptx_add_arrow(
            slide_index=2,
            start_x=start_x + 0.5,
            start_y=start_y + 0.5,
            end_x=end_x + 0.5,
            end_y=end_y + 0.5,
            connector_type="curved",
            arrow_end=True
        )
        print(f"   Curved connector {i+1}: {result}")
    
    # Test 4: Bidirectional arrows
    print("\n5. Testing bidirectional arrows...")
    await pptx_add_slide(
        title="Bidirectional Arrows Test",
        content=[]
    )
    
    await pptx_add_shape(
        slide_index=3,
        shape_type="hexagon",
        left=2.0,
        top=3.0,
        width=2.0,
        height=1.5,
        text="Process A",
        fill_color="#8BC34A"
    )
    
    await pptx_add_shape(
        slide_index=3,
        shape_type="hexagon",
        left=6.0,
        top=3.0,
        width=2.0,
        height=1.5,
        text="Process B",
        fill_color="#FFC107"
    )
    
    result = await pptx_add_arrow(
        slide_index=3,
        start_x=4.0,
        start_y=3.75,
        end_x=6.0,
        end_y=3.75,
        connector_type="straight",
        arrow_start=True,
        arrow_end=True
    )
    print(f"   Bidirectional arrow: {result}")
    
    # Save
    print("\n6. Saving test presentation...")
    await pptx_save("../outputs/connector_test.pptx")
    print("   ✅ Saved to outputs/connector_test.pptx")
    
    print("\n" + "=" * 60)
    print("✅ Connector tests complete!")
    print("\n💡 Check the output file to see:")
    print("   • If connectors are visible")
    print("   • If they connect to the right positions")
    print("   • If arrow heads are showing")
    print("   • If different connector types work")

if __name__ == "__main__":
    asyncio.run(test_connectors())