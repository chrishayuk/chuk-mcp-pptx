# src/chuk_mcp_pptx/tokens/typography.py
"""
Typography design tokens for consistent text styling.
"""

from typing import Dict, Any

# Font stacks
FONT_FAMILIES = {
    "sans": ["Inter", "Segoe UI", "system-ui", "-apple-system", "sans-serif"],
    "serif": ["Playfair Display", "Georgia", "Times New Roman", "serif"],
    "mono": ["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas", "monospace"],
    "display": ["Poppins", "Montserrat", "Raleway", "sans-serif"],
}

# Font sizes (in points)
FONT_SIZES = {
    "xs": 10,
    "sm": 12,
    "base": 14,
    "lg": 16,
    "xl": 18,
    "2xl": 22,
    "3xl": 28,
    "4xl": 36,
    "5xl": 48,
    "6xl": 60,
    "7xl": 72,
    "8xl": 96,
    "9xl": 128,
}

# Line heights (multipliers)
LINE_HEIGHTS = {
    "none": 1,
    "tight": 1.25,
    "snug": 1.375,
    "normal": 1.5,
    "relaxed": 1.625,
    "loose": 2,
}

# Font weights
FONT_WEIGHTS = {
    "thin": 100,
    "extralight": 200,
    "light": 300,
    "normal": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
    "extrabold": 800,
    "black": 900,
}

# Letter spacing (em units)
LETTER_SPACING = {
    "tighter": -0.05,
    "tight": -0.025,
    "normal": 0,
    "wide": 0.025,
    "wider": 0.05,
    "widest": 0.1,
}

# Text transforms
TEXT_TRANSFORMS = {
    "uppercase": "uppercase",
    "lowercase": "lowercase",
    "capitalize": "capitalize",
    "normal": "none",
}

# Paragraph spacing (points)
PARAGRAPH_SPACING = {
    "xs": 4,
    "sm": 6,
    "base": 8,
    "lg": 12,
    "xl": 16,
    "2xl": 20,
    "3xl": 24,
}


def get_text_style(variant: str = "body") -> Dict[str, Any]:
    """
    Get predefined text styles for common use cases.

    Args:
        variant: Style variant (e.g., "body", "heading", "caption")

    Returns:
        Dictionary of text style properties
    """
    styles = {
        "h1": {
            "font_family": FONT_FAMILIES["display"][0],
            "font_size": FONT_SIZES["5xl"],
            "font_weight": FONT_WEIGHTS["bold"],
            "line_height": LINE_HEIGHTS["tight"],
            "letter_spacing": LETTER_SPACING["tight"],
        },
        "h2": {
            "font_family": FONT_FAMILIES["display"][0],
            "font_size": FONT_SIZES["4xl"],
            "font_weight": FONT_WEIGHTS["semibold"],
            "line_height": LINE_HEIGHTS["tight"],
            "letter_spacing": LETTER_SPACING["tight"],
        },
        "h3": {
            "font_family": FONT_FAMILIES["display"][0],
            "font_size": FONT_SIZES["3xl"],
            "font_weight": FONT_WEIGHTS["semibold"],
            "line_height": LINE_HEIGHTS["snug"],
        },
        "h4": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["2xl"],
            "font_weight": FONT_WEIGHTS["medium"],
            "line_height": LINE_HEIGHTS["snug"],
        },
        "h5": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["xl"],
            "font_weight": FONT_WEIGHTS["medium"],
            "line_height": LINE_HEIGHTS["normal"],
        },
        "h6": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["lg"],
            "font_weight": FONT_WEIGHTS["medium"],
            "line_height": LINE_HEIGHTS["normal"],
        },
        "body": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["base"],
            "font_weight": FONT_WEIGHTS["normal"],
            "line_height": LINE_HEIGHTS["relaxed"],
        },
        "body-lg": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["lg"],
            "font_weight": FONT_WEIGHTS["normal"],
            "line_height": LINE_HEIGHTS["relaxed"],
        },
        "body-sm": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["sm"],
            "font_weight": FONT_WEIGHTS["normal"],
            "line_height": LINE_HEIGHTS["relaxed"],
        },
        "caption": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["xs"],
            "font_weight": FONT_WEIGHTS["normal"],
            "line_height": LINE_HEIGHTS["normal"],
            "letter_spacing": LETTER_SPACING["wide"],
        },
        "overline": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["xs"],
            "font_weight": FONT_WEIGHTS["semibold"],
            "line_height": LINE_HEIGHTS["normal"],
            "letter_spacing": LETTER_SPACING["widest"],
            "text_transform": TEXT_TRANSFORMS["uppercase"],
        },
        "code": {
            "font_family": FONT_FAMILIES["mono"][0],
            "font_size": FONT_SIZES["sm"],
            "font_weight": FONT_WEIGHTS["normal"],
            "line_height": LINE_HEIGHTS["normal"],
        },
        "code-lg": {
            "font_family": FONT_FAMILIES["mono"][0],
            "font_size": FONT_SIZES["base"],
            "font_weight": FONT_WEIGHTS["normal"],
            "line_height": LINE_HEIGHTS["relaxed"],
        },
        "quote": {
            "font_family": FONT_FAMILIES["serif"][0],
            "font_size": FONT_SIZES["lg"],
            "font_weight": FONT_WEIGHTS["light"],
            "line_height": LINE_HEIGHTS["relaxed"],
            "letter_spacing": LETTER_SPACING["wide"],
        },
        "lead": {
            "font_family": FONT_FAMILIES["sans"][0],
            "font_size": FONT_SIZES["xl"],
            "font_weight": FONT_WEIGHTS["light"],
            "line_height": LINE_HEIGHTS["relaxed"],
        },
    }

    return styles.get(variant, styles["body"])


# Typography scale for responsive sizing
TYPOGRAPHY_SCALE = {
    "display": {
        "2xl": {"font_size": FONT_SIZES["9xl"], "line_height": LINE_HEIGHTS["none"]},
        "xl": {"font_size": FONT_SIZES["8xl"], "line_height": LINE_HEIGHTS["none"]},
        "lg": {"font_size": FONT_SIZES["7xl"], "line_height": LINE_HEIGHTS["tight"]},
        "md": {"font_size": FONT_SIZES["6xl"], "line_height": LINE_HEIGHTS["tight"]},
        "sm": {"font_size": FONT_SIZES["5xl"], "line_height": LINE_HEIGHTS["tight"]},
    },
    "heading": {
        "2xl": {"font_size": FONT_SIZES["5xl"], "line_height": LINE_HEIGHTS["tight"]},
        "xl": {"font_size": FONT_SIZES["4xl"], "line_height": LINE_HEIGHTS["tight"]},
        "lg": {"font_size": FONT_SIZES["3xl"], "line_height": LINE_HEIGHTS["snug"]},
        "md": {"font_size": FONT_SIZES["2xl"], "line_height": LINE_HEIGHTS["snug"]},
        "sm": {"font_size": FONT_SIZES["xl"], "line_height": LINE_HEIGHTS["normal"]},
    },
}
