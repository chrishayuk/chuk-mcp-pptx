#!/usr/bin/env python3
"""
Beautiful Themes Demo - Showcasing automatic theme integration
with shapes, SmartArt, and code blocks
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_slide, pptx_save,
    pptx_apply_theme, pptx_add_shape, pptx_add_smart_art,
    pptx_add_code_block, pptx_add_arrow
)

async def create_beautiful_demo():
    """Create a beautiful presentation showcasing theme integration."""
    
    print("\n✨ Creating Beautiful Themed Presentation")
    print("="*70)
    
    await pptx_create("beautiful_themes_demo")
    
    # 1. Dark Purple - Tech Conference Style
    print("\n1. Creating Dark Purple tech slides...")
    await pptx_add_slide(
        title="Modern Tech Stack",
        content=[]
    )
    await pptx_apply_theme(slide_index=0, theme="dark_purple")
    
    # Add process flow - colors from theme
    await pptx_add_smart_art(
        slide_index=0,
        art_type="process",
        items=["Frontend", "API", "Backend", "Database", "Cache"],
        title="Architecture Flow",
        left=0.5, top=2.0, width=9.0, height=2.0
    )
    
    # Add code block
    code = """async def process_request(data):
    validated = await validate(data)
    result = await transform(validated)
    await cache.set(result.id, result)
    return result"""
    
    await pptx_add_code_block(
        slide_index=0,
        code=code,
        language="python",
        left=2.0, top=4.5, width=6.0, height=2.0,
        theme="dark_purple"
    )
    
    # 2. Cyberpunk - Futuristic Dashboard
    print("2. Creating Cyberpunk futuristic slides...")
    await pptx_add_slide(
        title="Neural Network Pipeline",
        content=[]
    )
    await pptx_apply_theme(slide_index=1, theme="cyberpunk")
    
    # Create network diagram
    await pptx_add_shape(
        slide_index=1,
        shape_type="hexagon",
        left=2.0, top=2.5, width=1.5, height=1.0,
        text="Input"
    )
    
    await pptx_add_shape(
        slide_index=1,
        shape_type="star",
        left=4.5, top=2.0, width=1.5, height=1.5,
        text="Neural"
    )
    
    await pptx_add_shape(
        slide_index=1,
        shape_type="hexagon",
        left=7.0, top=2.5, width=1.5, height=1.0,
        text="Output"
    )
    
    # Add neon connectors
    await pptx_add_arrow(
        slide_index=1,
        start_x=3.5, start_y=3.0,
        end_x=4.5, end_y=2.75,
        connector_type="curved",
        arrow_end=True
    )
    
    await pptx_add_arrow(
        slide_index=1,
        start_x=6.0, start_y=2.75,
        end_x=7.0, end_y=3.0,
        connector_type="curved",
        arrow_end=True
    )
    
    # Add cycle diagram
    await pptx_add_smart_art(
        slide_index=1,
        art_type="cycle",
        items=["Train", "Test", "Deploy", "Monitor"],
        title="",
        left=2.0, top=4.0, width=6.0, height=2.5
    )
    
    # 3. Dark Modern - Business Analytics
    print("3. Creating Dark Modern business slides...")
    await pptx_add_slide(
        title="Quarterly Business Review",
        content=[]
    )
    await pptx_apply_theme(slide_index=2, theme="dark_modern")
    
    # Add KPI shapes
    kpis = [
        ("Revenue", "↑ 45%", 1.5, 2.0),
        ("Users", "↑ 32%", 3.5, 2.0),
        ("Retention", "92%", 5.5, 2.0),
        ("NPS Score", "4.8", 7.5, 2.0)
    ]
    
    for title, value, x, y in kpis:
        await pptx_add_shape(
            slide_index=2,
            shape_type="rounded_rectangle",
            left=x, top=y, width=1.5, height=1.2,
            text=f"{title}\n{value}"
        )
    
    # Add hierarchy
    await pptx_add_smart_art(
        slide_index=2,
        art_type="hierarchy",
        items=["Strategy", "Execution", "Operations", "Delivery", "Support"],
        title="Organizational Focus",
        left=2.0, top=4.0, width=6.0, height=2.5
    )
    
    # 4. Light Minimal - Clean Design
    print("4. Creating Light Minimal design slides...")
    await pptx_add_slide(
        title="Minimalist Approach",
        content=[]
    )
    await pptx_apply_theme(slide_index=3, theme="light_minimal")
    
    # Simple shapes with clean design
    await pptx_add_shape(
        slide_index=3,
        shape_type="rectangle",
        left=2.0, top=2.5, width=6.0, height=0.5,
        text="Less is More"
    )
    
    # Add list
    await pptx_add_smart_art(
        slide_index=3,
        art_type="list",
        items=["Simplicity", "Clarity", "Focus", "Impact"],
        title="",
        left=2.5, top=3.5, width=5.0, height=2.5
    )
    
    # 5. Gradient Sunset - Creative
    print("5. Creating Gradient Sunset creative slides...")
    await pptx_add_slide(
        title="Creative Vision",
        content=[]
    )
    await pptx_apply_theme(slide_index=4, theme="gradient_sunset")
    
    # Relationship diagram
    await pptx_add_smart_art(
        slide_index=4,
        art_type="relationship",
        items=["Design", "Art", "Code", "Music", "Story"],
        title="Creative Elements",
        left=1.5, top=2.5, width=7.0, height=3.0
    )
    
    # Save
    await pptx_save("../outputs/beautiful_themes_demo.pptx")
    print("\n✅ Created beautiful_themes_demo.pptx")
    
    print("\n🎨 Features Demonstrated:")
    print("  • Automatic theme color application to shapes")
    print("  • SmartArt using theme palettes")
    print("  • Code blocks with theme backgrounds")
    print("  • Connectors with theme colors")
    print("  • Professional, cohesive design")
    print("\n💡 Each theme provides:")
    print("  • Consistent color scheme")
    print("  • Matching backgrounds and foregrounds")
    print("  • Professional typography")
    print("  • Automatic color coordination")

if __name__ == "__main__":
    asyncio.run(create_beautiful_demo())