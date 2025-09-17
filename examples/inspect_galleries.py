#!/usr/bin/env python3
"""
Inspector for Shapes and SmartArt galleries to check text placement.
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import pptx_inspect_slide, pptx_analyze_presentation_layout

async def inspect_gallery(file_path: str, gallery_name: str):
    """Inspect a gallery presentation for issues."""
    print(f"\n{'='*70}")
    print(f"🔍 INSPECTING {gallery_name}")
    print(f"{'='*70}")
    
    # Get overall presentation analysis
    print("\n📊 Presentation Overview:")
    analysis = await pptx_analyze_presentation_layout(file_path)
    print(analysis)
    
    # For shapes gallery, check specific slides
    if "shapes" in gallery_name.lower():
        slides_to_check = [
            (1, "Basic Shapes Collection"),
            (2, "Arrows and Connectors"),
            (3, "Special Shapes and Icons"),
            (4, "Shape Combinations - Process Flow"),
            (5, "Shape Color Variations"),
            (6, "Shape Size Variations")
        ]
    else:  # SmartArt gallery
        slides_to_check = [
            (1, "Process Flow Diagram"),
            (2, "Continuous Improvement Cycle"),
            (3, "Organizational Structure"),
            (4, "Key Success Factors"),
            (5, "Strategic Partnerships"),
            (6, "Maslow's Hierarchy"),
            (7, "Project Phases"),
            (8, "Customer Journey"),
            (9, "Strategic Planning Framework")
        ]
    
    # Inspect each slide
    for slide_idx, slide_name in slides_to_check:
        print(f"\n{'='*50}")
        print(f"📌 Slide {slide_idx}: {slide_name}")
        print(f"{'='*50}")
        
        inspection = await pptx_inspect_slide(slide_idx, file_path)
        
        # Parse inspection results for issues
        if "OVERLAPPING ELEMENTS" in inspection:
            print("⚠️  OVERLAPPING ELEMENTS DETECTED")
        if "OUT OF BOUNDS" in inspection:
            print("⚠️  OUT OF BOUNDS ELEMENTS DETECTED")
        
        # Show the full inspection
        print(inspection)
        
        # Check for text placement specifically
        if "text:" in inspection or "Text" in inspection:
            print("\n📝 Text elements found - checking placement...")
            # Extract text positions from the inspection
            lines = inspection.split('\n')
            for line in lines:
                if 'text:' in line or 'TextBox' in line:
                    print(f"   {line.strip()}")

async def main():
    """Main function to inspect both galleries."""
    
    # Check if files exist
    shapes_path = "../outputs/shapes_gallery.pptx"
    smartart_path = "../outputs/smartart_gallery.pptx"
    
    if os.path.exists(shapes_path):
        await inspect_gallery(shapes_path, "SHAPES GALLERY")
    else:
        print(f"❌ Shapes gallery not found at {shapes_path}")
    
    if os.path.exists(smartart_path):
        await inspect_gallery(smartart_path, "SMARTART GALLERY")
    else:
        print(f"❌ SmartArt gallery not found at {smartart_path}")
    
    print("\n" + "="*70)
    print("✅ Inspection complete!")
    print("\n💡 Recommendations:")
    print("   • Check for overlapping text and shapes")
    print("   • Verify text is centered in shapes")
    print("   • Ensure adequate margins for readability")
    print("   • Look for any out-of-bounds elements")

if __name__ == "__main__":
    asyncio.run(main())