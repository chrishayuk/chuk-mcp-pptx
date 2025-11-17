#!/usr/bin/env python3
"""
Apply design system refactoring to remaining chat components.
"""

import re
from pathlib import Path

def refactor_imports(content: str) -> str:
    """Add design system imports if not present."""
    imports_to_add = [
        "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
        "from ...tokens.platform_colors import get_chat_color, CHAT_COLORS",
        "from ...constants import MessageVariant",
    ]

    # Find the base import line
    base_import = "from ..base import Component"
    if base_import in content and imports_to_add[0] not in content:
        # Add imports after the base import
        content = content.replace(
            base_import,
            base_import + "\n" + "\n".join(imports_to_add)
        )

    return content

def refactor_fonts(content: str) -> str:
    """Replace hardcoded fonts with FONT_FAMILIES and FONT_SIZES."""
    replacements = [
        # Font sizes
        (r'Pt\(10\)', 'Pt(FONT_SIZES["xs"])'),
        (r'Pt\(11\)', 'Pt(FONT_SIZES["sm"])'),
        (r'Pt\(12\)', 'Pt(FONT_SIZES["sm"])'),
        (r'Pt\(13\)', 'Pt(FONT_SIZES["sm"])'),
        (r'Pt\(14\)', 'Pt(FONT_SIZES["base"])'),
        (r'Pt\(15\)', 'Pt(FONT_SIZES["lg"])'),
        (r'Pt\(16\)', 'Pt(FONT_SIZES["lg"])'),

        # Font families (common ones)
        (r'p\.font\.name = "Roboto"', 'p.font.name = FONT_FAMILIES["sans"][0]'),
        (r'p\.font\.name = "Segoe UI"', 'p.font.name = FONT_FAMILIES["sans"][0]'),
        (r'p\.font\.name = "Helvetica"', 'p.font.name = FONT_FAMILIES["sans"][0]'),
        (r'p\.font\.name = "Arial"', 'p.font.name = FONT_FAMILIES["sans"][0]'),
        (r'font\.name = "Roboto"', 'font.name = FONT_FAMILIES["sans"][0]'),
        (r'font\.name = "Segoe UI"', 'font.name = FONT_FAMILIES["sans"][0]'),
        (r'font\.name = "Helvetica"', 'font.name = FONT_FAMILIES["sans"][0]'),
        (r'font\.name = "Arial"', 'font.name = FONT_FAMILIES["sans"][0]'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    return content

def main():
    base_path = Path("src/chuk_mcp_pptx/components/chat")
    files_to_refactor = ["slack.py", "teams.py", "msn.py", "aol.py", "generic.py"]

    print("Applying automatic refactoring...")
    print("=" * 60)

    for filename in files_to_refactor:
        filepath = base_path / filename
        if not filepath.exists():
            print(f"⚠️  {filename}: Not found")
            continue

        print(f"\n📝 Processing: {filename}")

        # Read file
        content = filepath.read_text()
        original_content = content

        # Apply refactorings
        content = refactor_imports(content)
        content = refactor_fonts(content)

        # Write back if changed
        if content != original_content:
            filepath.write_text(content)
            print(f"   ✅ Updated imports and fonts")
        else:
            print(f"   ℹ️  No changes needed")

    print("\n" + "=" * 60)
    print("✅ Automatic refactoring complete!")
    print("\nManual steps still required:")
    print("- Update _get_bubble_color() methods to use get_chat_color()")
    print("- Update _get_text_color() methods to use CHAT_COLORS")
    print("- Replace any remaining hardcoded RGBColor() calls")

if __name__ == "__main__":
    main()
