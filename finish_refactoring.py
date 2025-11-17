#!/usr/bin/env python3
"""
Final batch refactoring script for all remaining components.
"""

import re
from pathlib import Path

def add_imports_if_missing(content: str, file_type: str) -> str:
    """Add necessary imports based on file type."""
    base_import = "from ..base import Component"

    if file_type == "container":
        imports = [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import MACOS_CONTROLS, WINDOWS_CONTROLS, DEVICE_COLORS",
            "from ...constants import ContainerPlatform",
        ]
    elif file_type == "core":
        imports = [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.spacing import SPACING",
            "from ...constants import ComponentSizing",
        ]
    else:
        return content

    # Check if imports already exist
    if imports[0] not in content:
        content = content.replace(
            base_import,
            base_import + "\n" + "\n".join(imports)
        )

    return content

def refactor_file(filepath: Path, file_type: str) -> tuple:
    """Refactor a single file."""
    if not filepath.exists():
        return (str(filepath), "NOT_FOUND", [])

    content = filepath.read_text()
    original = content
    changes = []

    # Add imports
    content = add_imports_if_missing(content, file_type)
    if content != original:
        changes.append("Added imports")

    # Replace hardcoded font sizes
    font_replacements = [
        (r'\bPt\(9\)', 'Pt(FONT_SIZES["xs"])'),
        (r'\bPt\(10\)', 'Pt(FONT_SIZES["xs"])'),
        (r'\bPt\(11\)', 'Pt(FONT_SIZES["sm"])'),
        (r'\bPt\(12\)', 'Pt(FONT_SIZES["sm"])'),
    ]

    for pattern, replacement in font_replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes.append(f"Replaced {pattern}")
            content = new_content

    # Container-specific replacements
    if file_type == "container":
        # macOS controls
        macos_replacements = [
            ('RGBColor(255, 95, 86)', 'RGBColor(*self.hex_to_rgb(MACOS_CONTROLS["close"]))'),
            ('RGBColor(255, 189, 46)', 'RGBColor(*self.hex_to_rgb(MACOS_CONTROLS["minimize"]))'),
            ('RGBColor(40, 201, 64)', 'RGBColor(*self.hex_to_rgb(MACOS_CONTROLS["maximize"]))'),
        ]

        # Windows controls
        windows_replacements = [
            ('RGBColor(232, 17, 35)', 'RGBColor(*self.hex_to_rgb(WINDOWS_CONTROLS["close"]))'),
        ]

        for old, new in macos_replacements + windows_replacements:
            if old in content:
                content = content.replace(old, new)
                changes.append(f"Replaced {old[:30]}...")

    # Core component replacements
    elif file_type == "core":
        # Button sizing
        if "button" in str(filepath).lower():
            button_replacements = [
                ('"sm": 1.5', 'ComponentSizing.BUTTON_BASE_WIDTH_SM'),
                ('"md": 2.0', 'ComponentSizing.BUTTON_BASE_WIDTH_MD'),
                ('"lg": 2.5', 'ComponentSizing.BUTTON_BASE_WIDTH_LG'),
                ('"sm": 0.06', 'ComponentSizing.CHAR_WIDTH_SM'),
                ('"md": 0.07', 'ComponentSizing.CHAR_WIDTH_MD'),
                ('"lg": 0.08', 'ComponentSizing.CHAR_WIDTH_LG'),
            ]

            for old, new in button_replacements:
                if old in content:
                    content = content.replace(old, new)
                    changes.append(f"Replaced button sizing")

        # Badge sizing
        if "badge" in str(filepath).lower():
            if "0.08" in content and "char_width" in content.lower():
                content = re.sub(r'char_width\s*=\s*0\.08', 'char_width = ComponentSizing.BADGE_CHAR_WIDTH', content)
                changes.append("Replaced badge char_width")
            if "0.5" in content and "padding" in content.lower():
                content = re.sub(r'padding\s*=\s*0\.5', 'padding = ComponentSizing.BADGE_PADDING', content)
                changes.append("Replaced badge padding")

    # Write back if changed
    if content != original:
        filepath.write_text(content)
        return (str(filepath), "UPDATED", changes)
    else:
        return (str(filepath), "NO_CHANGE", changes)

def main():
    print("=" * 70)
    print("FINAL REFACTORING BATCH PROCESS")
    print("=" * 70)

    # Container components
    container_files = [
        "windows.py",
        "macos.py",
        "iphone.py",
        "samsung.py",
    ]

    # Core components
    core_files = [
        "button.py",
        "card.py",
        "badge.py",
    ]

    container_path = Path("src/chuk_mcp_pptx/components/containers")
    core_path = Path("src/chuk_mcp_pptx/components/core")

    results = []

    print("\n📦 Processing Container Components...")
    for filename in container_files:
        filepath = container_path / filename
        result = refactor_file(filepath, "container")
        results.append(result)
        status_icon = "✅" if result[1] == "UPDATED" else "ℹ️"
        print(f"  {status_icon} {filename}: {result[1]}")
        if result[2]:
            for change in result[2]:
                print(f"     - {change}")

    print("\n🎨 Processing Core Components...")
    for filename in core_files:
        filepath = core_path / filename
        result = refactor_file(filepath, "core")
        results.append(result)
        status_icon = "✅" if result[1] == "UPDATED" else "ℹ️"
        print(f"  {status_icon} {filename}: {result[1]}")
        if result[2]:
            for change in result[2]:
                print(f"     - {change}")

    print("\n" + "=" * 70)
    updated = sum(1 for r in results if r[1] == "UPDATED")
    print(f"✅ COMPLETE: {updated}/{len(results)} files updated")
    print("=" * 70)

    print("\n📋 SUMMARY:")
    print(f"  - Container components: {len(container_files)} files")
    print(f"  - Core components: {len(core_files)} files")
    print(f"  - Total changes made: {updated} files")

    print("\n🎯 NEXT STEPS:")
    print("  1. Test imports: python -c 'from src.chuk_mcp_pptx.components.containers.windows import *'")
    print("  2. Check for remaining hardcoded values: grep -r 'RGBColor([0-9]' src/")
    print("  3. Run demos to verify visual output")

if __name__ == "__main__":
    main()
