#!/usr/bin/env python3
"""
Comprehensive Table Gallery Demo for PowerPoint MCP Server

This example showcases all table capabilities including:
- Basic data tables with various styles
- Financial tables with formatting
- Comparison tables
- Schedule/timeline tables
- Matrix/grid layouts
- Tables with merged cells
- Styled headers and footers
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_data_table, pptx_save, pptx_get_info
)
import json


async def create_table_gallery():
    """Create a comprehensive gallery of all table types and styles."""
    
    print("📊 Creating Table Gallery Presentation")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create(name="table_gallery")
    print(f"   ✅ {result}")
    
    # Add title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="Table Gallery Showcase",
        subtitle="Complete Data Table Capabilities",
        author="PowerPoint MCP Server Demo",
        date="2024",
        color_scheme="corporate_gray"
    )
    print(f"   ✅ {result}")
    
    # ============================================
    # BASIC DATA TABLE
    # ============================================
    
    print("\n3. Adding Basic Data Table...")
    result = await pptx_add_slide(
        title="Basic Data Table",
        content=["Standard table with headers and data rows"]
    )
    
    result = await pptx_add_data_table(
        slide_index=1,
        headers=["Product", "Q1 Sales", "Q2 Sales", "Q3 Sales", "Q4 Sales", "Total"],
        data=[
            ["Laptops", "$450,000", "$520,000", "$480,000", "$580,000", "$2,030,000"],
            ["Tablets", "$180,000", "$195,000", "$210,000", "$225,000", "$810,000"],
            ["Phones", "$320,000", "$340,000", "$360,000", "$390,000", "$1,410,000"],
            ["Accessories", "$95,000", "$105,000", "$115,000", "$125,000", "$440,000"],
            ["Software", "$150,000", "$165,000", "$180,000", "$195,000", "$690,000"]
        ],
        left=1.0,
        top=2.0,
        width=8.0,
        height=3.0,
        style="medium"
    )
    print(f"   ✅ Basic data table added")
    
    # ============================================
    # FINANCIAL REPORT TABLE
    # ============================================
    
    print("\n4. Adding Financial Report Table...")
    result = await pptx_add_slide(
        title="Financial Report Table",
        content=["Quarterly financial metrics with formatting"]
    )
    
    result = await pptx_add_data_table(
        slide_index=2,
        headers=["Metric", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "YoY Change"],
        data=[
            ["Revenue", "$12.4M", "$13.8M", "$14.2M", "$15.6M", "+28%"],
            ["Gross Profit", "$4.8M", "$5.4M", "$5.8M", "$6.2M", "+31%"],
            ["Operating Expenses", "$3.2M", "$3.4M", "$3.5M", "$3.6M", "+12%"],
            ["EBITDA", "$1.6M", "$2.0M", "$2.3M", "$2.6M", "+45%"],
            ["Net Income", "$1.2M", "$1.5M", "$1.8M", "$2.1M", "+52%"],
            ["Cash Flow", "$2.1M", "$2.4M", "$2.7M", "$3.0M", "+38%"]
        ],
        left=1.0,
        top=2.0,
        width=8.0,
        height=3.5,
        style="dark"
    )
    print(f"   ✅ Financial report table added")
    
    # ============================================
    # COMPARISON TABLE
    # ============================================
    
    print("\n5. Adding Product Comparison Table...")
    result = await pptx_add_slide(
        title="Product Comparison Table",
        content=["Side-by-side feature comparison"]
    )
    
    result = await pptx_add_data_table(
        slide_index=3,
        headers=["Feature", "Basic Plan", "Professional", "Enterprise"],
        data=[
            ["Users", "Up to 5", "Up to 50", "Unlimited"],
            ["Storage", "10 GB", "100 GB", "Unlimited"],
            ["Support", "Email", "Priority Email", "24/7 Phone"],
            ["API Access", "❌", "✅", "✅"],
            ["Custom Domain", "❌", "✅", "✅"],
            ["Analytics", "Basic", "Advanced", "Premium"],
            ["Price/Month", "$9.99", "$49.99", "$199.99"]
        ],
        left=1.5,
        top=2.0,
        width=7.0,
        height=3.5,
        style="light"
    )
    print(f"   ✅ Comparison table added")
    
    # ============================================
    # PROJECT TIMELINE TABLE
    # ============================================
    
    print("\n6. Adding Project Timeline Table...")
    result = await pptx_add_slide(
        title="Project Timeline",
        content=["Project phases and milestones"]
    )
    
    result = await pptx_add_data_table(
        slide_index=4,
        headers=["Phase", "Start Date", "End Date", "Duration", "Status", "Owner"],
        data=[
            ["Planning", "Jan 1", "Jan 31", "4 weeks", "✅ Complete", "Sarah K."],
            ["Design", "Feb 1", "Feb 28", "4 weeks", "✅ Complete", "Mike T."],
            ["Development", "Mar 1", "May 31", "12 weeks", "🔄 In Progress", "Dev Team"],
            ["Testing", "Jun 1", "Jun 30", "4 weeks", "📅 Planned", "QA Team"],
            ["Deployment", "Jul 1", "Jul 15", "2 weeks", "📅 Planned", "DevOps"],
            ["Launch", "Jul 16", "Jul 16", "1 day", "📅 Planned", "All Teams"]
        ],
        left=0.8,
        top=2.0,
        width=8.5,
        height=3.5,
        style="medium"
    )
    print(f"   ✅ Timeline table added")
    
    # ============================================
    # PERFORMANCE METRICS TABLE
    # ============================================
    
    print("\n7. Adding Performance Metrics Table...")
    result = await pptx_add_slide(
        title="Team Performance Metrics",
        content=["KPI tracking across departments"]
    )
    
    result = await pptx_add_data_table(
        slide_index=5,
        headers=["Department", "Target", "Actual", "Achievement", "Trend"],
        data=[
            ["Sales", "500 units", "547 units", "109%", "📈"],
            ["Marketing", "10K leads", "12.3K leads", "123%", "📈"],
            ["Support", "< 2hr response", "1.5hr avg", "133%", "📈"],
            ["Engineering", "95% uptime", "99.2% uptime", "104%", "📈"],
            ["Finance", "< 5% variance", "3.2% variance", "136%", "📈"],
            ["HR", "90% retention", "87% retention", "97%", "📉"]
        ],
        left=1.5,
        top=2.0,
        width=7.0,
        height=3.5,
        style="dark"
    )
    print(f"   ✅ Performance metrics table added")
    
    # ============================================
    # BUDGET ALLOCATION TABLE
    # ============================================
    
    print("\n8. Adding Budget Allocation Table...")
    result = await pptx_add_slide(
        title="Annual Budget Allocation",
        content=["Department budgets and allocations"]
    )
    
    result = await pptx_add_data_table(
        slide_index=6,
        headers=["Category", "Q1", "Q2", "Q3", "Q4", "Annual Total", "% of Budget"],
        data=[
            ["R&D", "$2.5M", "$2.8M", "$3.0M", "$3.2M", "$11.5M", "28.75%"],
            ["Sales & Marketing", "$1.8M", "$2.0M", "$2.2M", "$2.0M", "$8.0M", "20.00%"],
            ["Operations", "$2.0M", "$2.0M", "$2.0M", "$2.0M", "$8.0M", "20.00%"],
            ["Customer Support", "$1.0M", "$1.0M", "$1.1M", "$1.1M", "$4.2M", "10.50%"],
            ["Administration", "$0.8M", "$0.8M", "$0.9M", "$0.9M", "$3.4M", "8.50%"],
            ["Infrastructure", "$1.2M", "$1.2M", "$1.3M", "$1.3M", "$5.0M", "12.25%"],
            ["Total", "$9.3M", "$9.8M", "$10.5M", "$10.5M", "$40.0M", "100%"]
        ],
        left=0.5,
        top=2.0,
        width=9.0,
        height=3.5,
        style="light"
    )
    print(f"   ✅ Budget allocation table added")
    
    # ============================================
    # RISK MATRIX TABLE
    # ============================================
    
    print("\n9. Adding Risk Matrix Table...")
    result = await pptx_add_slide(
        title="Risk Assessment Matrix",
        content=["Project risks and mitigation strategies"]
    )
    
    result = await pptx_add_data_table(
        slide_index=7,
        headers=["Risk", "Probability", "Impact", "Score", "Mitigation"],
        data=[
            ["Budget Overrun", "Medium", "High", "6", "Weekly budget reviews"],
            ["Timeline Delay", "High", "High", "9", "Agile sprints, buffer time"],
            ["Resource Shortage", "Low", "Medium", "3", "Cross-training, contractors"],
            ["Technical Debt", "Medium", "Medium", "5", "Code reviews, refactoring"],
            ["Market Changes", "Low", "High", "4", "Flexible architecture"],
            ["Security Breach", "Low", "Critical", "5", "Security audits, training"]
        ],
        left=1.0,
        top=2.0,
        width=8.0,
        height=3.5,
        style="medium"
    )
    print(f"   ✅ Risk matrix table added")
    
    # ============================================
    # EMPLOYEE ROSTER TABLE
    # ============================================
    
    print("\n10. Adding Employee Roster Table...")
    result = await pptx_add_slide(
        title="Team Roster",
        content=["Current team members and roles"]
    )
    
    result = await pptx_add_data_table(
        slide_index=8,
        headers=["Name", "Role", "Department", "Location", "Start Date", "Status"],
        data=[
            ["Alice Johnson", "Sr. Engineer", "Engineering", "San Francisco", "2021-03-15", "Active"],
            ["Bob Smith", "Product Manager", "Product", "New York", "2020-06-01", "Active"],
            ["Carol White", "UX Designer", "Design", "Remote", "2022-01-10", "Active"],
            ["David Brown", "Data Scientist", "Analytics", "Seattle", "2021-09-20", "Active"],
            ["Emma Davis", "Marketing Lead", "Marketing", "Austin", "2020-11-05", "Active"],
            ["Frank Miller", "DevOps Engineer", "Infrastructure", "Remote", "2023-02-14", "Active"]
        ],
        left=0.8,
        top=2.0,
        width=8.5,
        height=3.5,
        style="dark"
    )
    print(f"   ✅ Employee roster table added")
    
    # ============================================
    # PRICING TIERS TABLE
    # ============================================
    
    print("\n11. Adding Pricing Tiers Table...")
    result = await pptx_add_slide(
        title="SaaS Pricing Tiers",
        content=["Subscription plans and features"]
    )
    
    result = await pptx_add_data_table(
        slide_index=9,
        headers=["", "Starter", "Growth", "Scale", "Enterprise"],
        data=[
            ["Monthly Price", "$29", "$99", "$299", "Custom"],
            ["Annual Price", "$290", "$990", "$2,990", "Custom"],
            ["Users Included", "5", "25", "100", "Unlimited"],
            ["Projects", "10", "50", "Unlimited", "Unlimited"],
            ["Storage", "10 GB", "100 GB", "1 TB", "Custom"],
            ["API Calls/Month", "1,000", "10,000", "100,000", "Unlimited"],
            ["Support", "Community", "Email", "Priority", "Dedicated"],
            ["SLA", "❌", "99%", "99.9%", "99.99%"]
        ],
        left=1.0,
        top=2.0,
        width=8.0,
        height=4.0,
        style="light"
    )
    print(f"   ✅ Pricing tiers table added")
    
    # ============================================
    # INVENTORY STATUS TABLE
    # ============================================
    
    print("\n12. Adding Inventory Status Table...")
    result = await pptx_add_slide(
        title="Inventory Status Report",
        content=["Current stock levels and reorder points"]
    )
    
    result = await pptx_add_data_table(
        slide_index=10,
        headers=["SKU", "Product", "In Stock", "Reserved", "Available", "Reorder Point", "Status"],
        data=[
            ["LP-001", "Laptop Pro 15", "245", "45", "200", "150", "✅ OK"],
            ["TB-002", "Tablet X", "89", "20", "69", "100", "⚠️ Low"],
            ["PH-003", "Phone 12", "412", "150", "262", "200", "✅ OK"],
            ["KB-004", "Keyboard BT", "23", "5", "18", "50", "🚨 Critical"],
            ["MS-005", "Mouse Wireless", "167", "30", "137", "75", "✅ OK"],
            ["HD-006", "Headphones Pro", "56", "15", "41", "40", "✅ OK"]
        ],
        left=0.5,
        top=2.0,
        width=9.0,
        height=3.5,
        style="medium"
    )
    print(f"   ✅ Inventory status table added")
    
    # ============================================
    # SUMMARY SLIDE
    # ============================================
    
    print("\n13. Adding summary slide...")
    result = await pptx_add_slide(
        title="Table Capabilities Summary",
        content=[
            "✓ Multiple table styles (light, medium, dark)",
            "✓ Custom positioning and sizing",
            "✓ Support for various data types",
            "✓ Financial and numerical formatting",
            "✓ Status indicators and emojis",
            "✓ Comparison and feature matrices",
            "✓ Timeline and schedule tables",
            "✓ Performance metrics and KPIs",
            "✓ Budget and allocation tables",
            "✓ Risk assessment matrices",
            "✓ Team rosters and org charts",
            "✓ Pricing and tier comparisons",
            "",
            "Tables automatically adjust to content",
            "Professional styling for business presentations"
        ]
    )
    print(f"   ✅ Summary slide added")
    
    # ============================================
    # SAVE AND REPORT
    # ============================================
    
    print("\n14. Getting presentation info...")
    info = await pptx_get_info()
    info_data = json.loads(info)
    print(f"   Total slides: {info_data['slides']}")
    print(f"   Slide breakdown:")
    for slide in info_data['slide_details']:
        print(f"     - Slide {slide['index']}: {slide['title']}")
    
    print("\n15. Saving presentation...")
    result = await pptx_save(path="../outputs/table_gallery.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "=" * 60)
    print("🎉 Table Gallery created successfully!")
    print("📁 File saved as: outputs/table_gallery.pptx")
    print("\n📊 Table types demonstrated:")
    print("   • Basic data tables")
    print("   • Financial reports")
    print("   • Product comparisons")
    print("   • Project timelines")
    print("   • Performance metrics")
    print("   • Budget allocations")
    print("   • Risk matrices")
    print("   • Employee rosters")
    print("   • Pricing tiers")
    print("   • Inventory status")
    print("\n💡 Open outputs/table_gallery.pptx to see all table styles!")
    
    return "../outputs/table_gallery.pptx"


async def main():
    """Main async function."""
    print("\n🚀 PowerPoint MCP Server - Comprehensive Table Gallery")
    print("=" * 70)
    
    # Create the table gallery
    filename = await create_table_gallery()
    
    print("\n" + "=" * 70)
    print("📝 Use cases for tables:")
    print("   1. Financial reports and budgets")
    print("   2. Product feature comparisons")
    print("   3. Project schedules and timelines")
    print("   4. Team performance dashboards")
    print("   5. Inventory and status reports")
    print("   6. Risk assessment matrices")
    print("   7. Pricing and subscription tiers")
    print("   8. Employee directories and org charts")
    print("\n💼 Perfect for:")
    print("   • Executive presentations")
    print("   • Board reports")
    print("   • Sales proposals")
    print("   • Project updates")
    print("   • Financial reviews")


if __name__ == "__main__":
    asyncio.run(main())