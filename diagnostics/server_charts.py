#!/usr/bin/env python3
"""
Test server chart functions directly
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from chuk_mcp_pptx.server import (
    pptx_create,
    pptx_add_slide,
    pptx_add_chart,
    pptx_add_pie_chart,
    pptx_save,
    pptx_get_info,
)
import json


def test_server_charts():
    """Test server chart functions"""
    print("Testing Server Chart Functions")
    print("=" * 50)

    # Create presentation
    print("\n1. Creating presentation...")
    result = pptx_create(name="test_charts_server")
    print(f"   {result}")

    # Add a slide for the chart
    print("\n2. Adding slide for chart...")
    result = pptx_add_slide(title="Sales Chart", content=["This slide will have a chart below"])
    print(f"   {result}")

    # Get presentation info to check slide count
    print("\n3. Checking presentation state...")
    info = json.loads(pptx_get_info())
    print(f"   Total slides: {info['slides']}")
    print("   Slide details:")
    for slide in info["slide_details"]:
        print(f"     - Slide {slide['index']}: {slide['title']} ({slide['shapes']} shapes)")

    # Add chart to slide 0 (the only slide)
    print("\n4. Adding chart to slide 0...")
    result = pptx_add_chart(
        slide_index=0,
        chart_type="column",
        categories=["Q1", "Q2", "Q3", "Q4"],
        series_data={"Revenue": [100, 120, 140, 160], "Profit": [20, 25, 30, 35]},
        title="Quarterly Results",
        left=1.0,
        top=2.5,  # Lower to avoid overlapping with title
        width=8.0,
        height=4.0,
    )
    print(f"   {result}")

    # Check slide shapes after adding chart
    print("\n5. Checking slide shapes after chart...")
    info = json.loads(pptx_get_info())
    for slide in info["slide_details"]:
        print(f"   Slide {slide['index']}: {slide['shapes']} shapes")

    # Add another slide for pie chart
    print("\n6. Adding another slide...")
    result = pptx_add_slide(title="Market Share", content=[])
    print(f"   {result}")

    # Add pie chart
    print("\n7. Adding pie chart to slide 1...")
    result = pptx_add_pie_chart(
        slide_index=1,
        categories=["Product A", "Product B", "Product C"],
        values=[45, 30, 25],
        title="Market Distribution",
    )
    print(f"   {result}")

    # Final check
    print("\n8. Final presentation state...")
    info = json.loads(pptx_get_info())
    print(f"   Total slides: {info['slides']}")
    for slide in info["slide_details"]:
        print(f"   Slide {slide['index']}: {slide['title']} ({slide['shapes']} shapes)")

    # Save
    print("\n9. Saving presentation...")
    result = pptx_save(path="test_server_charts.pptx")
    print(f"   {result}")

    print("\n" + "=" * 50)
    print("✅ Test completed! Check test_server_charts.pptx")


if __name__ == "__main__":
    test_server_charts()
