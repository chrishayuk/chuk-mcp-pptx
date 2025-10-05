#!/usr/bin/env python3
"""
Quick test of theme functionality
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_slide, pptx_save,
    pptx_apply_theme, pptx_add_shape, pptx_add_code_block
)

async def test_themes():
    """Test theme and code block functionality."""
    
    print("Testing themes and code blocks...")
    
    # Create presentation
    await pptx_create("theme_test")
    
    # Add slide with dark theme
    await pptx_add_slide(
        title="Dark Purple Theme Test",
        content=["Beautiful dark theme", "Modern design"]
    )
    await pptx_apply_theme(slide_index=0, theme="dark_purple")
    
    # Add code block
    await pptx_add_slide(title="Code Example", content=[])
    code = """def hello_world():
    print("Hello from dark theme!")
    return True"""
    
    await pptx_add_code_block(
        slide_index=1,
        code=code,
        language="python",
        theme="dark_purple"
    )
    await pptx_apply_theme(slide_index=1, theme="dark_purple")
    
    # Add cyberpunk theme slide
    await pptx_add_slide(title="Cyberpunk Style", content=["Neon colors", "Futuristic design"])
    await pptx_apply_theme(slide_index=2, theme="cyberpunk")
    
    # Save
    await pptx_save("../outputs/theme_test.pptx")
    print("✅ Created theme_test.pptx")
    
if __name__ == "__main__":
    asyncio.run(test_themes())