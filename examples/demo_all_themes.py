#!/usr/bin/env python3
"""
Demo All Themes - Quick script to showcase all theme galleries.
Opens each theme gallery to demonstrate the design system.
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def demo_theme_galleries():
    """Demo all theme galleries."""
    
    print("\n🎨 PowerPoint Chart Gallery Theme Demo")
    print("=" * 60)
    print("This demo shows the same chart components with different themes,")
    print("demonstrating our 'shadcn for PowerPoint' design system.")
    print()
    
    # Find all theme gallery files
    current_dir = Path(__file__).parent
    gallery_files = list(current_dir.glob("chart_gallery_*.pptx"))
    
    if not gallery_files:
        # Check in outputs directory
        outputs_dir = current_dir.parent / "outputs"
        gallery_files = list(outputs_dir.glob("chart_gallery_*.pptx"))
        
        if not gallery_files:
            # Check in theme_galleries subdirectory
            theme_dir = outputs_dir / "theme_galleries"
            gallery_files = list(theme_dir.glob("chart_gallery_*.pptx"))
    
    if not gallery_files:
        print("❌ No theme gallery files found!")
        print("   Run 'python examples/theme_chart_galleries.py' first.")
        return
    
    # Sort files for better presentation
    gallery_files.sort()
    
    print(f"📊 Found {len(gallery_files)} theme galleries:")
    print()
    
    # Group themes for better presentation
    theme_groups = {
        "🌑 Dark Themes": [],
        "🌅 Light Themes": [], 
        "✨ Special Themes": []
    }
    
    for file in gallery_files:
        theme_name = file.stem.replace("chart_gallery_", "").replace("_", "-")
        
        if theme_name.startswith("dark"):
            theme_groups["🌑 Dark Themes"].append((theme_name, file))
        elif theme_name in ["light", "corporate", "light-warm"]:
            theme_groups["🌅 Light Themes"].append((theme_name, file))
        else:
            theme_groups["✨ Special Themes"].append((theme_name, file))
    
    # Display grouped themes
    for group_name, themes in theme_groups.items():
        if themes:
            print(f"{group_name}:")
            for theme_name, file_path in themes:
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  • {theme_name:<15} - {file_path.name} ({size_mb:.1f}MB)")
            print()
    
    print("🎯 What each gallery demonstrates:")
    print("  • Column & Bar Charts (clustered, stacked, waterfall)")
    print("  • Line & Area Charts (smooth, markers, sparklines)")
    print("  • Pie & Doughnut Charts (exploded, modern)")
    print("  • Scatter & Bubble Analysis (correlations, 3D data)")
    print("  • Radar & Performance Charts (multi-criteria, KPIs)")
    print("  • Theme-specific styling and colors")
    print("  • Consistent component behavior across themes")
    print()
    
    print("🚀 Key Features Showcased:")
    print("  ✓ Component-based architecture")
    print("  ✓ Design token system") 
    print("  ✓ Theme-aware color schemes")
    print("  ✓ Boundary detection and validation")
    print("  ✓ Beautiful default styling")
    print("  ✓ Professional chart quality")
    print()
    
    # Interactive demo option
    while True:
        choice = input("🎪 Would you like to open galleries for viewing? (y/n/specific): ").lower().strip()
        
        if choice in ['n', 'no', 'exit', 'quit']:
            break
        elif choice in ['y', 'yes']:
            print("\n🔍 Opening all theme galleries...")
            open_all_galleries(gallery_files)
            break
        elif choice == "specific":
            print("\n📋 Available themes:")
            for i, (theme_name, file_path) in enumerate([(f.stem.replace("chart_gallery_", "").replace("_", "-"), f) for f in gallery_files], 1):
                print(f"  {i:2d}. {theme_name}")
            
            try:
                selection = input("\nEnter theme number(s) (comma-separated) or 'all': ").strip()
                if selection.lower() == 'all':
                    open_all_galleries(gallery_files)
                else:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    selected_files = [gallery_files[i] for i in indices if 0 <= i < len(gallery_files)]
                    if selected_files:
                        open_all_galleries(selected_files)
                    else:
                        print("❌ Invalid selection")
            except (ValueError, IndexError):
                print("❌ Invalid input")
            break
        else:
            print("Please enter 'y' for yes, 'n' for no, or 'specific' to choose themes")
    
    print("\n💡 Pro tip: Compare galleries side by side to see how the same")
    print("    chart components look completely different with various themes!")
    print("\n🎨 This demonstrates the power of design systems - one codebase,")
    print("    infinite visual possibilities!")


def open_all_galleries(gallery_files):
    """Open gallery files for viewing."""
    print(f"\n🔄 Opening {len(gallery_files)} galleries...")
    
    for i, file_path in enumerate(gallery_files, 1):
        theme_name = file_path.stem.replace("chart_gallery_", "").replace("_", "-")
        print(f"  {i:2d}. Opening {theme_name} gallery...")
        
        try:
            # Open file with default application
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(file_path)], check=True)
            elif sys.platform == "win32":  # Windows
                os.startfile(str(file_path))
            else:  # Linux
                subprocess.run(["xdg-open", str(file_path)], check=True)
            
            # Small delay to prevent overwhelming the system
            if i < len(gallery_files):
                time.sleep(0.5)
                
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            print(f"     ⚠️  Could not open {file_path.name}: {e}")
    
    print(f"\n✅ Opened {len(gallery_files)} theme galleries!")
    print("📖 Each gallery shows the same charts with different themes.")


def main():
    """Main function."""
    demo_theme_galleries()


if __name__ == "__main__":
    main()