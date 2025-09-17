#!/usr/bin/env python3
"""
Layout Inspection and Fix Demo for PowerPoint MCP Server

This example demonstrates how to:
1. Create slides with layout issues
2. Inspect slides to identify problems
3. Automatically fix layout issues
4. Analyze the entire presentation
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_create_title_slide, pptx_add_slide,
    pptx_add_chart, pptx_add_image, pptx_add_image_with_caption,
    pptx_inspect_slide, pptx_fix_slide_layout, 
    pptx_analyze_presentation_layout, pptx_save
)


def create_sample_image_base64(color='blue'):
    """Create a simple colored rectangle as base64 for demo purposes."""
    try:
        import io
        import base64
        from PIL import Image
        
        # Create a colored rectangle
        img = Image.new('RGB', (200, 150), color=color)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        
        # Convert to base64 data URL
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    except ImportError:
        return f"placeholder_{color}.png"


async def create_problematic_slide():
    """Create a slide with intentional layout issues."""
    print("\n📌 Creating slide with layout issues...")
    
    # Add a slide
    await pptx_add_slide(
        title="Problematic Layout Example",
        content=["This slide has intentional layout issues for demonstration"]
    )
    
    # Add overlapping images
    print("   Adding overlapping images...")
    demo_image_red = create_sample_image_base64('red')
    demo_image_blue = create_sample_image_base64('blue')
    demo_image_green = create_sample_image_base64('green')
    
    # These will overlap
    await pptx_add_image(
        slide_index=1,
        image_path=demo_image_red,
        left=2.0,
        top=2.0,
        width=4.0,
        height=3.0
    )
    
    await pptx_add_image(
        slide_index=1,
        image_path=demo_image_blue,
        left=4.0,  # Overlaps with red image
        top=2.5,
        width=4.0,
        height=3.0
    )
    
    # This one goes out of bounds
    await pptx_add_image(
        slide_index=1,
        image_path=demo_image_green,
        left=8.5,  # Too far right - will go off slide
        top=1.0,
        width=3.0,
        height=2.0
    )
    
    print("   ✅ Added problematic elements")


async def create_complex_slide():
    """Create a complex slide with multiple elements."""
    print("\n📊 Creating complex slide with charts and images...")
    
    await pptx_add_slide(
        title="Complex Multi-Element Slide",
        content=[]
    )
    
    # Add a chart
    await pptx_add_chart(
        slide_index=2,
        chart_type="column",
        data={
            "categories": ["Q1", "Q2", "Q3", "Q4"],
            "series": {
                "Revenue": [100, 120, 140, 160],
                "Costs": [80, 85, 90, 95]
            }
        },
        title="Quarterly Performance",
        left=0.5, top=1.5, width=5.0, height=3.0
    )
    
    # Add images that might overlap
    demo_image = create_sample_image_base64('orange')
    
    await pptx_add_image(
        slide_index=2,
        image_path=demo_image,
        left=5.0,
        top=1.8,
        width=2.5,
        height=2.0
    )
    
    await pptx_add_image_with_caption(
        slide_index=2,
        image_path=create_sample_image_base64('purple'),
        caption="Product Screenshot",
        left=7.5,
        top=2.0,
        image_width=2.5,
        image_height=2.0,
        caption_height=0.5
    )
    
    print("   ✅ Added multiple elements")


async def demonstrate_inspection():
    """Demonstrate the slide inspection capabilities."""
    print("\n🔍 DEMONSTRATING SLIDE INSPECTION")
    print("=" * 60)
    
    # Create presentation
    print("\n1. Creating presentation...")
    await pptx_create(name="layout_demo")
    print("   ✅ Created presentation")
    
    # Add title slide
    print("\n2. Adding title slide...")
    await pptx_create_title_slide(
        title="Layout Inspection & Fix Demo",
        subtitle="Automatic Layout Analysis and Correction",
        author="PowerPoint MCP Server",
        date="2024"
    )
    
    # Create problematic slides
    await create_problematic_slide()
    await create_complex_slide()
    
    # Inspect slide with issues
    print("\n" + "=" * 60)
    print("🔍 INSPECTING SLIDE 1 (with intentional issues)")
    print("=" * 60)
    
    inspection_result = await pptx_inspect_slide(
        slide_index=1,
        include_measurements=True,
        check_overlaps=True
    )
    print(inspection_result)
    
    # Inspect complex slide
    print("\n" + "=" * 60)
    print("🔍 INSPECTING SLIDE 2 (complex multi-element)")
    print("=" * 60)
    
    inspection_result = await pptx_inspect_slide(
        slide_index=2,
        include_measurements=True,
        check_overlaps=True
    )
    print(inspection_result)
    
    # Analyze entire presentation
    print("\n" + "=" * 60)
    print("📊 ANALYZING ENTIRE PRESENTATION")
    print("=" * 60)
    
    analysis = await pptx_analyze_presentation_layout()
    print(analysis)
    
    # Fix layout issues
    print("\n" + "=" * 60)
    print("🔧 FIXING LAYOUT ISSUES")
    print("=" * 60)
    
    print("\n📌 Fixing slide 1...")
    fix_result = await pptx_fix_slide_layout(
        slide_index=1,
        fix_overlaps=True,
        fix_bounds=True,
        fix_spacing=True
    )
    print(f"   {fix_result}")
    
    print("\n📌 Fixing slide 2...")
    fix_result = await pptx_fix_slide_layout(
        slide_index=2,
        fix_overlaps=True,
        fix_bounds=True,
        fix_spacing=True
    )
    print(f"   {fix_result}")
    
    # Re-inspect after fixes
    print("\n" + "=" * 60)
    print("✅ RE-INSPECTING AFTER FIXES")
    print("=" * 60)
    
    print("\n📌 Slide 1 after fixes:")
    inspection_result = await pptx_inspect_slide(
        slide_index=1,
        include_measurements=False,  # Less verbose
        check_overlaps=True
    )
    print(inspection_result)
    
    print("\n📌 Slide 2 after fixes:")
    inspection_result = await pptx_inspect_slide(
        slide_index=2,
        include_measurements=False,
        check_overlaps=True
    )
    print(inspection_result)
    
    # Final analysis
    print("\n" + "=" * 60)
    print("📊 FINAL PRESENTATION ANALYSIS")
    print("=" * 60)
    
    final_analysis = await pptx_analyze_presentation_layout()
    print(final_analysis)
    
    # Save presentation
    print("\n3. Saving presentation...")
    await pptx_save(path="../outputs/layout_demo.pptx")
    print("   ✅ Saved to outputs/layout_demo.pptx")


async def demonstrate_ai_workflow():
    """Show how AI could use these tools."""
    print("\n" + "=" * 60)
    print("🤖 AI WORKFLOW EXAMPLE")
    print("=" * 60)
    
    print("""
This demonstrates how an AI assistant could use these tools:

1. User: "Add a chart and two images to slide 3"
   
2. AI adds the requested elements:
   - await pptx_add_chart(...)
   - await pptx_add_image(...)
   - await pptx_add_image(...)
   
3. AI proactively inspects the slide:
   - result = await pptx_inspect_slide(slide_index=3)
   - Detects: "WARNING: 2 overlapping elements detected"
   
4. AI automatically fixes the issues:
   - await pptx_fix_slide_layout(slide_index=3)
   - Reports: "Fixed 2 overlapping elements"
   
5. AI confirms the fix:
   - result = await pptx_inspect_slide(slide_index=3)
   - Confirms: "✅ No layout issues detected"

This ensures professional, well-laid-out slides every time!
""")


async def main():
    """Main async function."""
    print("\n🚀 PowerPoint MCP Server - Layout Inspection & Fix Demo")
    print("=" * 70)
    
    # Demonstrate inspection and fixes
    await demonstrate_inspection()
    
    # Show AI workflow
    await demonstrate_ai_workflow()
    
    print("\n" + "=" * 70)
    print("🎉 Demo completed successfully!")
    print("\n📝 Key features demonstrated:")
    print("   • Detailed slide inspection with measurements")
    print("   • Overlap detection between elements")
    print("   • Out-of-bounds element detection")
    print("   • Automatic layout fixes")
    print("   • Presentation-wide analysis")
    print("   • AI-friendly workflow for quality assurance")
    print("\n💡 Open outputs/layout_demo.pptx to see the corrected layouts!")


if __name__ == "__main__":
    asyncio.run(main())