#!/usr/bin/env python3
"""
SmartArt Gallery Demo for PowerPoint MCP Server

Demonstrates SmartArt-style diagrams using shapes.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_smart_art, pptx_save, pptx_get_info
)


async def create_smartart_gallery():
    """Create a comprehensive SmartArt gallery presentation."""
    
    print("\n🚀 PowerPoint MCP Server - SmartArt Gallery")
    print("=" * 70)
    print("🎨 Creating SmartArt Gallery Presentation")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating presentation...")
    result = await pptx_create("smartart_gallery")
    print(f"   ✅ {result}")
    
    # Title slide
    print("\n2. Creating title slide...")
    result = await pptx_create_title_slide(
        title="SmartArt Gallery Showcase",
        subtitle="Professional Diagrams and Visualizations",
        author="PowerPoint MCP Server",
        color_scheme="corporate_gray"
    )
    print(f"   ✅ Created title slide at index 0")
    
    # ============================================
    # PROCESS DIAGRAM
    # ============================================
    
    print("\n3. Adding Process Flow SmartArt...")
    result = await pptx_add_slide(
        title="Process Flow Diagram",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=1,
        art_type="process",
        items=["Research", "Design", "Develop", "Test", "Deploy", "Monitor"],
        title="Software Development Lifecycle",
        left=0.5,
        top=2.0,
        width=9.0,
        height=2.5,
        color_scheme="modern_blue"
    )
    print(f"   ✅ Process flow diagram added")
    
    # ============================================
    # CYCLE DIAGRAM
    # ============================================
    
    print("\n4. Adding Cycle SmartArt...")
    result = await pptx_add_slide(
        title="Continuous Improvement Cycle",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=2,
        art_type="cycle",
        items=["Plan", "Do", "Check", "Act"],
        title="PDCA Cycle",
        left=2.0,
        top=2.0,
        width=6.0,
        height=3.0,
        color_scheme="warm_orange"
    )
    print(f"   ✅ Cycle diagram added")
    
    # ============================================
    # HIERARCHY DIAGRAM
    # ============================================
    
    print("\n5. Adding Hierarchy SmartArt...")
    result = await pptx_add_slide(
        title="Organizational Structure",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=3,
        art_type="hierarchy",
        items=["CEO", "CTO", "CFO", "COO", "CMO"],
        title="Executive Team",
        left=1.5,
        top=2.0,
        width=7.0,
        height=3.0,
        color_scheme="corporate_gray"
    )
    print(f"   ✅ Hierarchy diagram added")
    
    # ============================================
    # LIST DIAGRAM
    # ============================================
    
    print("\n6. Adding List SmartArt...")
    result = await pptx_add_slide(
        title="Key Success Factors",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=4,
        art_type="list",
        items=[
            "Customer Focus",
            "Innovation",
            "Quality",
            "Teamwork",
            "Integrity"
        ],
        title="Core Values",
        left=2.0,
        top=2.0,
        width=6.0,
        height=3.0,
        color_scheme="modern_blue"
    )
    print(f"   ✅ List diagram added")
    
    # ============================================
    # RELATIONSHIP DIAGRAM
    # ============================================
    
    print("\n7. Adding Relationship SmartArt...")
    result = await pptx_add_slide(
        title="Strategic Partnerships",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=5,
        art_type="relationship",
        items=["Company", "Suppliers", "Customers", "Partners"],
        title="Business Ecosystem",
        left=1.5,
        top=2.0,
        width=7.0,
        height=3.0,
        color_scheme="warm_orange"
    )
    print(f"   ✅ Relationship diagram added")
    
    # ============================================
    # PYRAMID DIAGRAM
    # ============================================
    
    print("\n8. Adding Pyramid SmartArt...")
    result = await pptx_add_slide(
        title="Maslow's Hierarchy of Needs",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=6,
        art_type="pyramid",
        items=[
            "Self-Actualization",
            "Esteem",
            "Love/Belonging",
            "Safety",
            "Physiological"
        ],
        title="Human Motivation",
        left=2.5,
        top=1.8,
        width=5.0,
        height=3.2,
        color_scheme="corporate_gray"
    )
    print(f"   ✅ Pyramid diagram added")
    
    # ============================================
    # MULTI-COLOR PROCESS
    # ============================================
    
    print("\n9. Adding Multi-Color Process...")
    result = await pptx_add_slide(
        title="Project Phases",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=7,
        art_type="process",
        items=["Initiation", "Planning", "Execution", "Monitoring", "Closure"],
        title="Project Management Phases",
        left=1.0,
        top=2.0,
        width=8.0,
        height=2.5,
        color_scheme="modern_blue"
    )
    print(f"   ✅ Multi-color process added")
    
    # ============================================
    # COMPLEX CYCLE
    # ============================================
    
    print("\n10. Adding Complex Cycle...")
    result = await pptx_add_slide(
        title="Customer Journey",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=8,
        art_type="cycle",
        items=["Awareness", "Consideration", "Purchase", "Retention", "Advocacy"],
        title="Customer Lifecycle",
        left=2.0,
        top=2.0,
        width=6.0,
        height=3.0,
        color_scheme="warm_orange"
    )
    print(f"   ✅ Complex cycle added")
    
    # ============================================
    # STRATEGIC HIERARCHY
    # ============================================
    
    print("\n11. Adding Strategic Hierarchy...")
    result = await pptx_add_slide(
        title="Strategic Planning Framework",
        content=[]
    )
    
    await pptx_add_smart_art(
        slide_index=9,
        art_type="hierarchy",
        items=["Vision", "Mission", "Goals", "Objectives", "Tactics", "KPIs"],
        title="Strategy Cascade",
        left=1.5,
        top=2.0,
        width=7.0,
        height=3.0,
        color_scheme="corporate_gray"
    )
    print(f"   ✅ Strategic hierarchy added")
    
    # ============================================
    # SUMMARY SLIDE
    # ============================================
    
    print("\n12. Adding summary slide...")
    result = await pptx_add_slide(
        title="SmartArt Capabilities Summary",
        content=[
            "• Process flows for sequential steps",
            "• Cycles for continuous processes",
            "• Hierarchies for organizational structures",
            "• Lists for key points and values",
            "• Relationships for connections",
            "• Pyramids for layered concepts",
            "• Multiple color schemes available",
            "• Customizable positioning and sizing"
        ]
    )
    print(f"   ✅ Summary slide added")
    
    # ============================================
    # SAVE AND REPORT
    # ============================================
    
    print("\n13. Getting presentation info...")
    info = await pptx_get_info()
    print(f"   Total slides: 11")
    
    print("\n14. Saving presentation...")
    result = await pptx_save("../outputs/smartart_gallery.pptx")
    print(f"   ✅ {result}")
    
    print("\n" + "=" * 60)
    print("🎉 SmartArt Gallery created successfully!")
    print("📁 File saved as: outputs/smartart_gallery.pptx")
    print("\n🎨 SmartArt types demonstrated:")
    print("   • Process flows")
    print("   • Cycle diagrams")
    print("   • Organizational hierarchies")
    print("   • Lists and bullet points")
    print("   • Relationship diagrams")
    print("   • Pyramid structures")
    print("\n💡 Open outputs/smartart_gallery.pptx to see all SmartArt types!")


async def main():
    """Main execution function."""
    await create_smartart_gallery()
    
    print("\n" + "=" * 70)
    print("📝 Use cases for SmartArt:")
    print("   1. Business process documentation")
    print("   2. Organizational charts")
    print("   3. Strategic planning visuals")
    print("   4. Project management flows")
    print("   5. Decision trees")
    print("   6. Customer journey maps")
    print("   7. Value chain analysis")
    print("   8. SWOT analysis diagrams")
    print("\n💼 Perfect for:")
    print("   • Executive presentations")
    print("   • Strategy documents")
    print("   • Training materials")
    print("   • Process improvement")
    print("   • Change management")
    print("   • Business analysis")


if __name__ == "__main__":
    asyncio.run(main())