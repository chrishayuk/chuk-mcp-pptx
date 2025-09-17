#!/usr/bin/env python3
"""
Comprehensive Chart Gallery Demo for PowerPoint MCP Server

This example creates a presentation showcasing all supported chart types
using the unified chart API.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_chart, pptx_save, pptx_get_info
)
import json


async def create_chart_gallery():
    """Create a comprehensive gallery of all supported chart types."""
    
    print("📊 Creating Chart Gallery Presentation")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create(name="chart_gallery")
    print(f"   ✅ {result}")
    
    # Add title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="Chart Gallery Showcase",
        subtitle="All Supported Chart Types with Unified API",
        author="PowerPoint MCP Server Demo",
        date="2024",
        color_scheme="modern_blue"
    )
    print(f"   ✅ {result}")
    
    # ============================================
    # COLUMN CHARTS
    # ============================================
    
    print("\n3. Adding Column Chart...")
    result = await pptx_add_slide(
        title="Column Chart - Quarterly Sales",
        content=["Standard column chart showing quarterly data"]
    )
    result = await pptx_add_chart(
        slide_index=1,
        chart_type="column",
        data={
            "categories": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"],
            "series": {
                "Product A": [45, 52, 48, 58],
                "Product B": [38, 41, 44, 49],
                "Product C": [22, 28, 31, 35]
            }
        },
        title="Quarterly Sales Performance"
    )
    print(f"   ✅ Column chart added")
    
    print("\n4. Adding Stacked Column Chart...")
    result = await pptx_add_slide(
        title="Stacked Column Chart - Regional Sales",
        content=["Shows cumulative values across categories"]
    )
    result = await pptx_add_chart(
        slide_index=2,
        chart_type="column_stacked",
        data={
            "categories": ["North", "South", "East", "West"],
            "series": {
                "Online": [120, 95, 110, 105],
                "Retail": [80, 105, 90, 95],
                "Wholesale": [45, 60, 55, 50]
            }
        },
        title="Sales by Region and Channel"
    )
    print(f"   ✅ Stacked column chart added")
    
    # ============================================
    # BAR CHARTS
    # ============================================
    
    print("\n5. Adding Bar Chart...")
    result = await pptx_add_slide(
        title="Bar Chart - Product Comparison",
        content=["Horizontal bars for better label readability"]
    )
    result = await pptx_add_chart(
        slide_index=3,
        chart_type="bar",
        data={
            "categories": ["Smartphones", "Laptops", "Tablets", "Accessories", "Software"],
            "series": {
                "2023 Sales": [450, 320, 180, 290, 150],
                "2024 Target": [500, 350, 200, 320, 180]
            }
        },
        title="Product Line Performance"
    )
    print(f"   ✅ Bar chart added")
    
    # ============================================
    # LINE CHARTS
    # ============================================
    
    print("\n6. Adding Line Chart...")
    result = await pptx_add_slide(
        title="Line Chart - Growth Trends",
        content=["Shows trends over time"]
    )
    result = await pptx_add_chart(
        slide_index=4,
        chart_type="line_markers",
        data={
            "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "series": {
                "Revenue": [42, 45, 48, 52, 58, 65],
                "Profit": [8, 9, 11, 12, 14, 17],
                "Expenses": [34, 36, 37, 40, 44, 48]
            }
        },
        title="Six Month Financial Trends"
    )
    print(f"   ✅ Line chart added")
    
    # ============================================
    # PIE & DOUGHNUT CHARTS
    # ============================================
    
    print("\n7. Adding Pie Chart...")
    result = await pptx_add_slide(
        title="Pie Chart - Market Share",
        content=["Shows proportional distribution"]
    )
    result = await pptx_add_chart(
        slide_index=5,
        chart_type="pie",
        data={
            "categories": ["Company A", "Company B", "Company C", "Company D", "Others"],
            "values": [35, 28, 20, 12, 5]
        },
        title="Market Share Distribution",
        options={"show_percentages": True}
    )
    print(f"   ✅ Pie chart added")
    
    print("\n8. Adding Doughnut Chart...")
    result = await pptx_add_slide(
        title="Doughnut Chart - Budget Allocation",
        content=["Similar to pie chart with hollow center"]
    )
    result = await pptx_add_chart(
        slide_index=6,
        chart_type="doughnut",
        data={
            "categories": ["R&D", "Marketing", "Operations", "Sales", "Admin"],
            "values": [25, 20, 30, 15, 10]
        },
        title="Budget Distribution 2024"
    )
    print(f"   ✅ Doughnut chart added")
    
    # ============================================
    # AREA CHARTS
    # ============================================
    
    print("\n9. Adding Area Chart...")
    result = await pptx_add_slide(
        title="Area Chart - Cumulative Growth",
        content=["Shows magnitude of change over time"]
    )
    result = await pptx_add_chart(
        slide_index=7,
        chart_type="area",
        data={
            "categories": ["2019", "2020", "2021", "2022", "2023", "2024"],
            "series": {
                "Users (millions)": [1.2, 2.1, 3.5, 5.2, 7.8, 11.5],
                "Revenue (millions)": [10, 18, 32, 48, 72, 95]
            }
        },
        title="Platform Growth Metrics"
    )
    print(f"   ✅ Area chart added")
    
    # ============================================
    # SCATTER CHART
    # ============================================
    
    print("\n10. Adding Scatter Chart...")
    result = await pptx_add_slide(
        title="Scatter Chart - Price vs Sales",
        content=["Shows correlation between two variables"]
    )
    result = await pptx_add_chart(
        slide_index=8,
        chart_type="scatter",
        data={
            "series": [
                {
                    "name": "Product Analysis",
                    "x_values": [10, 15, 20, 25, 30, 35, 40],
                    "y_values": [85, 95, 110, 108, 125, 135, 130]
                }
            ]
        },
        title="Price vs Sales Volume Correlation"
    )
    print(f"   ✅ Scatter chart added")
    
    # ============================================
    # BUBBLE CHART
    # ============================================
    
    print("\n11. Adding Bubble Chart...")
    result = await pptx_add_slide(
        title="Bubble Chart - Market Positioning",
        content=["Three dimensions: X=Price, Y=Quality, Size=Market Share"]
    )
    result = await pptx_add_chart(
        slide_index=9,
        chart_type="bubble",
        data={
            "series": [
                {
                    "name": "Product Portfolio",
                    "points": [
                        [10, 20, 5],   # Low price, low quality, small share
                        [25, 35, 12],  # Mid price, mid quality, medium share
                        [40, 45, 18],  # High price, high quality, large share
                        [15, 30, 8],   # Low price, good quality, small share
                        [35, 40, 15]   # High price, good quality, medium share
                    ]
                }
            ]
        },
        title="Market Positioning Analysis"
    )
    print(f"   ✅ Bubble chart added")
    
    # ============================================
    # RADAR CHART
    # ============================================
    
    print("\n12. Adding Radar Chart...")
    result = await pptx_add_slide(
        title="Radar Chart - Product Comparison",
        content=["Multi-criteria comparison across products"]
    )
    result = await pptx_add_chart(
        slide_index=10,
        chart_type="radar_filled",
        data={
            "categories": ["Speed", "Reliability", "Comfort", "Design", "Economy"],
            "series": {
                "Model A": [8, 7, 9, 8, 6],
                "Model B": [7, 9, 7, 6, 8],
                "Competitor": [6, 8, 6, 7, 9]
            }
        },
        title="Product Feature Comparison"
    )
    print(f"   ✅ Radar chart added")
    
    # ============================================
    # WATERFALL CHART
    # ============================================
    
    print("\n13. Adding Waterfall Chart...")
    result = await pptx_add_slide(
        title="Waterfall Chart - Profit Analysis",
        content=["Shows incremental positive and negative changes"]
    )
    result = await pptx_add_chart(
        slide_index=11,
        chart_type="waterfall",
        data={
            "categories": ["Start", "Sales", "Services", "Costs", "Tax", "Net Profit"],
            "values": [0, 150, 40, -80, -20, 90]
        },
        title="Profit Waterfall Analysis"
    )
    print(f"   ✅ Waterfall chart added")
    
    # ============================================
    # SUMMARY SLIDE
    # ============================================
    
    print("\n14. Adding summary slide...")
    result = await pptx_add_slide(
        title="Chart Types Summary",
        content=[
            "✓ Column & Bar Charts (Regular & Stacked)",
            "✓ Line Charts (With and Without Markers)",
            "✓ Pie & Doughnut Charts",
            "✓ Area Charts (Regular & Stacked)",
            "✓ Scatter (XY) Charts for Correlations",
            "✓ Bubble Charts for 3D Data",
            "✓ Radar Charts for Multi-Criteria",
            "✓ Waterfall Charts for Financial Analysis",
            "",
            "All charts created with unified pptx_add_chart() API",
            "• Single tool for all chart types",
            "• Automatic data validation",
            "• Clear error messages for AI/LLM usage"
        ]
    )
    print(f"   ✅ Summary slide added")
    
    # ============================================
    # SAVE AND REPORT
    # ============================================
    
    print("\n15. Getting presentation info...")
    info = await pptx_get_info()
    info_data = json.loads(info)
    print(f"   Total slides: {info_data['slides']}")
    print(f"   Slide breakdown:")
    for slide in info_data['slide_details']:
        print(f"     - Slide {slide['index']}: {slide['title']}")
    
    print("\n16. Saving presentation...")
    result = await pptx_save(path="../outputs/chart_gallery.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "=" * 60)
    print("🎉 Chart Gallery created successfully!")
    print("📁 File saved as: outputs/chart_gallery.pptx")
    print("\n📊 Chart types demonstrated:")
    print("   • Column, Bar, Line, Area (with variants)")
    print("   • Pie & Doughnut")
    print("   • Scatter, Bubble, Radar, Waterfall")
    print("\n💡 Open outputs/chart_gallery.pptx to see all chart types!")
    
    return "../outputs/chart_gallery.pptx"


async def main():
    """Main async function"""
    print("\n🚀 PowerPoint MCP Server - Comprehensive Chart Gallery")
    print("=" * 70)
    
    # Create the chart gallery
    filename = await create_chart_gallery()
    
    print("\n" + "=" * 70)
    print("📝 Next steps:")
    print("   1. Open outputs/chart_gallery.pptx in PowerPoint")
    print("   2. Review all chart types and their formatting")
    print("   3. Note the unified API usage for all charts")
    print("   4. Each chart demonstrates the new simplified data structure")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())