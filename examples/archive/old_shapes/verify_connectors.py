#!/usr/bin/env python3
"""Verify that connectors are properly implemented with arrows."""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_slide, pptx_add_shape, 
    pptx_add_arrow, pptx_save
)

async def verify_connectors():
    """Create comprehensive connector tests."""
    print("🔧 CONNECTOR VERIFICATION TEST")
    print("=" * 60)
    
    # Create presentation
    await pptx_create("connector_verify")
    
    # Test 1: Flow diagram with proper connectors
    print("\n1. Creating flow diagram...")
    await pptx_add_slide(
        title="Flow Diagram with Connectors",
        content=[]
    )
    
    # Create a flow: Start -> Process -> Decision -> End
    shapes = [
        ("oval", "Start", 1.0, 3.0, "#4CAF50"),
        ("rectangle", "Process", 3.0, 3.0, "#2196F3"),
        ("diamond", "Decision", 5.0, 3.0, "#FF9800"),
        ("oval", "End", 7.0, 3.0, "#F44336")
    ]
    
    for shape_type, text, x, y, color in shapes:
        await pptx_add_shape(
            slide_index=0,
            shape_type=shape_type,
            left=x,
            top=y,
            width=1.2,
            height=0.8,
            text=text,
            fill_color=color,
            line_color="#333333",
            line_width=2.0
        )
    
    # Connect them with arrows
    connections = [
        (2.2, 3.4, 3.0, 3.4, "Start to Process"),
        (4.2, 3.4, 5.0, 3.4, "Process to Decision"),
        (6.2, 3.4, 7.0, 3.4, "Decision to End")
    ]
    
    for start_x, start_y, end_x, end_y, label in connections:
        result = await pptx_add_arrow(
            slide_index=0,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            connector_type="straight",
            line_color="#333333",
            line_width=2.0,
            arrow_end=True
        )
        print(f"   ✓ {label}: {result}")
    
    # Test 2: Network diagram with curved connectors
    print("\n2. Creating network diagram...")
    await pptx_add_slide(
        title="Network Diagram",
        content=[]
    )
    
    # Create hub and spoke layout
    # Central hub
    await pptx_add_shape(
        slide_index=1,
        shape_type="hexagon",
        left=4.0,
        top=3.0,
        width=2.0,
        height=1.5,
        text="HUB",
        fill_color="#9C27B0",
        line_color="#FFFFFF",
        line_width=3.0
    )
    
    # Surrounding nodes
    nodes = [
        (2.0, 1.5, "Node A"),
        (6.0, 1.5, "Node B"),
        (6.0, 4.5, "Node C"),
        (2.0, 4.5, "Node D")
    ]
    
    for x, y, text in nodes:
        await pptx_add_shape(
            slide_index=1,
            shape_type="rounded_rectangle",
            left=x,
            top=y,
            width=1.5,
            height=0.8,
            text=text,
            fill_color="#00BCD4",
            line_color="#006064",
            line_width=1.5
        )
    
    # Connect hub to nodes with curved connectors
    hub_connections = [
        (4.0, 3.2, 2.8, 2.3, "Hub to A"),
        (6.0, 3.2, 6.8, 2.3, "Hub to B"),
        (6.0, 3.8, 6.8, 4.9, "Hub to C"),
        (4.0, 3.8, 2.8, 4.9, "Hub to D")
    ]
    
    for start_x, start_y, end_x, end_y, label in hub_connections:
        result = await pptx_add_arrow(
            slide_index=1,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            connector_type="curved",
            line_color="#673AB7",
            line_width=2.5,
            arrow_end=True
        )
        print(f"   ✓ {label}: {result}")
    
    # Test 3: Bidirectional data flow
    print("\n3. Creating bidirectional flow...")
    await pptx_add_slide(
        title="Bidirectional Data Flow",
        content=[]
    )
    
    # Create two systems
    await pptx_add_shape(
        slide_index=2,
        shape_type="rectangle",
        left=2.0,
        top=3.0,
        width=2.0,
        height=1.5,
        text="System A",
        fill_color="#4CAF50",
        line_color="#1B5E20",
        line_width=2.0
    )
    
    await pptx_add_shape(
        slide_index=2,
        shape_type="rectangle",
        left=6.0,
        top=3.0,
        width=2.0,
        height=1.5,
        text="System B",
        fill_color="#FF5722",
        line_color="#BF360C",
        line_width=2.0
    )
    
    # Bidirectional arrow
    result = await pptx_add_arrow(
        slide_index=2,
        start_x=4.0,
        start_y=3.5,
        end_x=6.0,
        end_y=3.5,
        connector_type="straight",
        line_color="#333333",
        line_width=3.0,
        arrow_start=True,
        arrow_end=True
    )
    print(f"   ✓ Bidirectional: {result}")
    
    # Add label above arrow
    await pptx_add_shape(
        slide_index=2,
        shape_type="rectangle",
        left=4.5,
        top=2.8,
        width=1.0,
        height=0.4,
        text="Data",
        fill_color="#FFFFCC",
        line_color="#999999",
        line_width=0.5
    )
    
    # Save
    print("\n4. Saving verification presentation...")
    await pptx_save("../outputs/connector_verify.pptx")
    print("   ✅ Saved to outputs/connector_verify.pptx")
    
    print("\n" + "=" * 60)
    print("✅ CONNECTOR VERIFICATION COMPLETE!")
    print("\nExpected results:")
    print("  ✓ Flow diagram: Arrows pointing from left to right")
    print("  ✓ Network diagram: Curved arrows from hub to nodes")
    print("  ✓ Data flow: Bidirectional arrow between systems")
    print("\n💡 Open the file to verify:")
    print("  • Arrow heads are visible")
    print("  • Different connector types work (straight, curved)")
    print("  • Bidirectional arrows show heads on both ends")

if __name__ == "__main__":
    asyncio.run(verify_connectors())