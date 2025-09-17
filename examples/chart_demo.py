#!/usr/bin/env python3
"""
Comprehensive Chart and Visualization Demo for PowerPoint MCP Server

This example demonstrates creating a complete data-driven presentation
with various chart types, templates, and professional formatting.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_chart, pptx_create_comparison_slide, pptx_create_metrics_slide,
    pptx_save, pptx_list_templates
)
import json


async def create_sales_presentation():
    """Create a comprehensive sales presentation with charts and data."""
    
    print("📊 Creating Sales Analytics Presentation")
    print("==" * 25)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create(name="sales_analytics_2024")
    print(f"   ✅ {result}")
    
    # Add professional title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="Sales Analytics Report",
        subtitle="Q4 2024 Performance Review",
        author="Analytics Team",
        date="December 2024",
        color_scheme="corporate_gray"
    )
    print(f"   ✅ {result}")
    
    # Add key metrics dashboard
    print("\n3. Creating key metrics dashboard...")
    result = await pptx_create_metrics_slide(
        title="Executive Summary",
        metrics=[
            {"value": "$12.4M", "label": "Total Revenue"},
            {"value": "94%", "label": "Target Achievement"},
            {"value": "+28%", "label": "YoY Growth"},
            {"value": "247", "label": "New Customers"}
        ],
        color_scheme="corporate_gray"
    )
    print(f"   ✅ {result}")
    
    # Add quarterly revenue chart slide
    print("\n4. Adding quarterly revenue chart...")
    result = await pptx_add_slide(title="Quarterly Revenue Trend", content=[])
    print(f"   ✅ {result}")
    
    result = await pptx_add_chart(
        slide_index=2,
        chart_type="column",
        data={
            "categories": ["Q1", "Q2", "Q3", "Q4"],
            "series": {
                "2023": [2.1, 2.4, 2.8, 3.2],
                "2024": [2.8, 3.1, 3.4, 3.1]
            }
        },
        title="Quarterly Revenue (in millions)"
    )
    print(f"   ✅ {result}")
    
    # Add product mix pie chart
    print("\n5. Adding product mix pie chart...")
    result = await pptx_add_slide(title="Product Revenue Distribution", content=[])
    print(f"   ✅ {result}")
    
    result = await pptx_add_chart(
        slide_index=3,
        chart_type="pie",
        data={
            "categories": ["Enterprise", "Professional", "Standard", "Basic"],
            "values": [45, 30, 20, 5]
        },
        title="Revenue by Product Tier",
        options={"show_percentages": True}
    )
    print(f"   ✅ {result}")
    
    # Save the presentation
    print("\n6. Saving presentation...")
    result = await pptx_save(path="../outputs/sales_analytics_2024.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "==" * 25)
    print("✨ Sales presentation created successfully!")
    print("📁 File saved as: outputs/sales_analytics_2024.pptx")


async def test_templates():
    """Test listing available templates."""
    
    print("\n🎨 Available Templates and Color Schemes")
    print("==" * 25)
    
    try:
        result = await pptx_list_templates()
        if isinstance(result, dict):
            data = result
        else:
            data = json.loads(result)
        
        print("\n📋 Slide Templates:")
        if 'templates' in data:
            for template in data['templates'][:3]:  # Show first 3
                print(f"   • {template['name']}: {template['description']}")
        
        print("\n🎨 Color Schemes:")
        if 'color_schemes' in data:
            for scheme in data['color_schemes']:
                print(f"   • {scheme}")
    except Exception as e:
        print(f"   Note: Template listing not available ({e})")


async def main():
    """Main async function"""
    print("\n🚀 PowerPoint MCP Server - Chart Demo")
    print("=" * 60)
    
    # Create sales presentation with charts
    await create_sales_presentation()
    
    # Test templates
    await test_templates()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("\n📊 Created presentation:")
    print("   • outputs/sales_analytics_2024.pptx - Sales report with charts")
    print("\n💡 Open the file in PowerPoint to see the results!")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())