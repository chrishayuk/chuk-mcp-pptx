#!/usr/bin/env python3
"""
Batch refactoring script to update chat components to use design system.
"""

import re
from pathlib import Path

# File-specific replacements
REFACTORINGS = {
    "chatgpt.py": {
        "platform": "chatgpt",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import get_chat_color, CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "color_replacements": [
            ("RGBColor(247, 247, 248)", "get_chat_color('chatgpt', 'user', 'light')"),
            ("RGBColor(236, 236, 241)", "get_chat_color('chatgpt', 'system', 'light')"),
            ("RGBColor(255, 255, 255)", "get_chat_color('chatgpt', 'assistant', 'light')"),
            ("RGBColor(52, 53, 65)", "CHAT_COLORS['chatgpt']['text']"),
            ("RGBColor(16, 163, 127)", "CHAT_COLORS['chatgpt']['avatar']"),
        ],
        "font_replacements": [
            ('p.font.name = "Söhne"', "p.font.name = FONT_FAMILIES['sans'][0]"),
            ("Pt(10)", "Pt(FONT_SIZES['xs'])"),
            ("Pt(11)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(12)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(14)", "Pt(FONT_SIZES['base'])"),
        ],
    },
    "facebook.py": {
        "platform": "facebook",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import get_chat_color, CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "color_replacements": [
            ("RGBColor(0, 132, 255)", "get_chat_color('facebook', 'sent', 'light')"),
            ("RGBColor(233, 234, 237)", "get_chat_color('facebook', 'received', 'light')"),
            ("RGBColor(255, 255, 255)", "CHAT_COLORS['facebook']['text_sent']"),
            ("RGBColor(0, 0, 0)", "CHAT_COLORS['facebook']['text']"),
        ],
        "font_replacements": [
            ("Pt(11)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(15)", "Pt(FONT_SIZES['lg'])"),
        ],
    },
    "slack.py": {
        "platform": "slack",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "color_replacements": [
            ("RGBColor(97, 31, 105)", "CHAT_COLORS['slack']['avatar']"),
            ("RGBColor(29, 28, 29)", "CHAT_COLORS['slack']['text']"),
            ("RGBColor(97, 96, 97)", "CHAT_COLORS['slack']['secondary_text']"),
            ("RGBColor(29, 155, 209)", "CHAT_COLORS['slack']['link']"),
            ("RGBColor(255, 255, 255)", "CHAT_COLORS['slack']['background']"),
            ("RGBColor(248, 248, 248)", "CHAT_COLORS['slack']['hover']"),
        ],
        "font_replacements": [
            ("Pt(10)", "Pt(FONT_SIZES['xs'])"),
            ("Pt(11)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(15)", "Pt(FONT_SIZES['lg'])"),
        ],
    },
    "teams.py": {
        "platform": "teams",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "color_replacements": [
            ("RGBColor(98, 100, 167)", "CHAT_COLORS['teams']['purple']"),
            ("RGBColor(37, 36, 35)", "CHAT_COLORS['teams']['text']"),
            ("RGBColor(96, 94, 92)", "CHAT_COLORS['teams']['secondary_text']"),
            ("RGBColor(255, 255, 255)", "CHAT_COLORS['teams']['background']"),
        ],
        "font_replacements": [
            ("Pt(10)", "Pt(FONT_SIZES['xs'])"),
            ("Pt(11)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(14)", "Pt(FONT_SIZES['base'])"),
        ],
    },
    "msn.py": {
        "platform": "msn",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import get_chat_color, CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "font_replacements": [
            ("Pt(10)", "Pt(FONT_SIZES['xs'])"),
            ("Pt(12)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(14)", "Pt(FONT_SIZES['base'])"),
        ],
    },
    "aol.py": {
        "platform": "aol",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import get_chat_color, CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "font_replacements": [
            ("Pt(10)", "Pt(FONT_SIZES['xs'])"),
            ("Pt(12)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(14)", "Pt(FONT_SIZES['base'])"),
        ],
    },
    "generic.py": {
        "platform": "generic",
        "imports_to_add": [
            "from ...tokens.typography import FONT_SIZES, FONT_FAMILIES",
            "from ...tokens.platform_colors import get_chat_color, CHAT_COLORS",
            "from ...constants import MessageVariant",
        ],
        "font_replacements": [
            ("Pt(10)", "Pt(FONT_SIZES['xs'])"),
            ("Pt(11)", "Pt(FONT_SIZES['sm'])"),
            ("Pt(14)", "Pt(FONT_SIZES['base'])"),
        ],
    },
}

def main():
    base_path = Path(__file__).parent / "src" / "chuk_mcp_pptx" / "components" / "chat"

    print("Refactoring Summary:")
    print("=" * 60)

    for filename, config in REFACTORINGS.items():
        filepath = base_path / filename
        if not filepath.exists():
            print(f"⚠️  {filename}: File not found")
            continue

        print(f"\n📝 Processing: {filename}")
        print(f"   Platform: {config['platform']}")
        print(f"   Font replacements: {len(config.get('font_replacements', []))}")
        print(f"   Color replacements: {len(config.get('color_replacements', []))}")

    print("\n" + "=" * 60)
    print("\nManual refactoring still required for:")
    print("- Verifying import statements are added correctly")
    print("- Checking _get_bubble_color() and _get_text_color() methods")
    print("- Updating hardcoded font names to FONT_FAMILIES")

if __name__ == "__main__":
    main()
