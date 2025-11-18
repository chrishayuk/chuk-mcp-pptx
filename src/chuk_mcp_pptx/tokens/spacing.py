# src/chuk_mcp_pptx/tokens/spacing.py
"""
Spacing design tokens for consistent layout.
"""

from typing import Dict

# Base spacing unit (in inches for PowerPoint)
SPACING_BASE = 0.25  # 0.25 inches

# Spacing scale
SPACING = {
    "0": 0,
    "px": 0.01,  # 1 pixel equivalent
    "0.5": SPACING_BASE * 0.125,  # 0.03125"
    "1": SPACING_BASE * 0.25,  # 0.0625"
    "1.5": SPACING_BASE * 0.375,  # 0.09375"
    "2": SPACING_BASE * 0.5,  # 0.125"
    "2.5": SPACING_BASE * 0.625,  # 0.15625"
    "3": SPACING_BASE * 0.75,  # 0.1875"
    "3.5": SPACING_BASE * 0.875,  # 0.21875"
    "4": SPACING_BASE,  # 0.25"
    "5": SPACING_BASE * 1.25,  # 0.3125"
    "6": SPACING_BASE * 1.5,  # 0.375"
    "7": SPACING_BASE * 1.75,  # 0.4375"
    "8": SPACING_BASE * 2,  # 0.5"
    "9": SPACING_BASE * 2.25,  # 0.5625"
    "10": SPACING_BASE * 2.5,  # 0.625"
    "11": SPACING_BASE * 2.75,  # 0.6875"
    "12": SPACING_BASE * 3,  # 0.75"
    "14": SPACING_BASE * 3.5,  # 0.875"
    "16": SPACING_BASE * 4,  # 1"
    "20": SPACING_BASE * 5,  # 1.25"
    "24": SPACING_BASE * 6,  # 1.5"
    "28": SPACING_BASE * 7,  # 1.75"
    "32": SPACING_BASE * 8,  # 2"
    "36": SPACING_BASE * 9,  # 2.25"
    "40": SPACING_BASE * 10,  # 2.5"
    "44": SPACING_BASE * 11,  # 2.75"
    "48": SPACING_BASE * 12,  # 3"
    "52": SPACING_BASE * 13,  # 3.25"
    "56": SPACING_BASE * 14,  # 3.5"
    "60": SPACING_BASE * 15,  # 3.75"
    "64": SPACING_BASE * 16,  # 4"
    "72": SPACING_BASE * 18,  # 4.5"
    "80": SPACING_BASE * 20,  # 5"
    "96": SPACING_BASE * 24,  # 6"
}

# Margin presets
MARGINS = {
    "none": 0,
    "xs": SPACING["2"],
    "sm": SPACING["4"],
    "md": SPACING["6"],
    "lg": SPACING["8"],
    "xl": SPACING["12"],
    "2xl": SPACING["16"],
    "3xl": SPACING["24"],
}

# Padding presets
PADDING = {
    "none": 0,
    "xs": SPACING["2"],
    "sm": SPACING["3"],
    "md": SPACING["4"],
    "lg": SPACING["6"],
    "xl": SPACING["8"],
    "2xl": SPACING["12"],
    "3xl": SPACING["16"],
}

# Gap presets (for spacing between elements)
GAPS = {
    "none": 0,
    "xs": SPACING["1"],
    "sm": SPACING["2"],
    "md": SPACING["4"],
    "lg": SPACING["6"],
    "xl": SPACING["8"],
    "2xl": SPACING["12"],
    "3xl": SPACING["16"],
}

# Border radius (in points)
RADIUS = {
    "none": 0,
    "sm": 2,
    "md": 4,
    "lg": 6,
    "xl": 8,
    "2xl": 12,
    "3xl": 16,
    "full": 9999,  # Effectively full rounded
}

# Border widths (in points)
BORDER_WIDTH = {
    "0": 0,
    "1": 0.5,
    "2": 1,
    "3": 1.5,
    "4": 2,
    "8": 4,
}

# Shadow definitions
SHADOWS = {
    "none": None,
    "sm": {
        "offset_x": 0,
        "offset_y": 1,
        "blur": 2,
        "color": "rgba(0, 0, 0, 0.05)",
    },
    "md": {
        "offset_x": 0,
        "offset_y": 4,
        "blur": 6,
        "color": "rgba(0, 0, 0, 0.1)",
    },
    "lg": {
        "offset_x": 0,
        "offset_y": 10,
        "blur": 15,
        "color": "rgba(0, 0, 0, 0.1)",
    },
    "xl": {
        "offset_x": 0,
        "offset_y": 20,
        "blur": 25,
        "color": "rgba(0, 0, 0, 0.1)",
    },
    "2xl": {
        "offset_x": 0,
        "offset_y": 25,
        "blur": 50,
        "color": "rgba(0, 0, 0, 0.25)",
    },
    "inner": {
        "offset_x": 0,
        "offset_y": 2,
        "blur": 4,
        "color": "rgba(0, 0, 0, 0.06)",
        "inset": True,
    },
}

# Grid system
GRID = {
    "cols": 12,  # 12-column grid
    "gutter": SPACING["4"],  # Space between columns
    "margin": SPACING["8"],  # Outer margin
}

# Container widths (in inches)
CONTAINERS = {
    "sm": 8,  # Small container
    "md": 9,  # Medium container
    "lg": 10,  # Large container (standard slide width)
    "xl": 11,  # Extra large
    "2xl": 12,  # Full width with margins
    "full": 13.333,  # Full slide width
}

# Aspect ratios for media
ASPECT_RATIOS = {
    "square": "1:1",
    "video": "16:9",
    "photo": "4:3",
    "portrait": "3:4",
    "widescreen": "21:9",
    "golden": "1.618:1",
}

# Font sizes (in points)
FONT_SIZES = {
    "xs": 8,
    "sm": 10,
    "base": 12,
    "md": 14,
    "lg": 16,
    "xl": 18,
    "2xl": 20,
    "3xl": 24,
    "4xl": 28,
    "5xl": 32,
    "6xl": 36,
    "7xl": 48,
    "8xl": 60,
    "9xl": 72,
}

# Line widths (in points) - for borders, chart lines, etc.
LINE_WIDTHS = {
    "hairline": 0.25,
    "thin": 0.5,
    "normal": 1,
    "medium": 1.5,
    "thick": 2,
    "heavy": 3,
    "bold": 4,
}

# Common dimension presets (in inches)
DIMENSIONS = {
    # Common icon/button sizes
    "icon_xs": 0.15,
    "icon_sm": 0.2,
    "icon_md": 0.25,
    "icon_lg": 0.3,
    "icon_xl": 0.4,
    # Common chart gaps
    "chart_gap_narrow": 50,
    "chart_gap_default": 100,
    "chart_gap_medium": 150,
    "chart_gap_wide": 200,
}


def get_layout_spacing(layout_type: str = "default") -> Dict[str, float]:
    """
    Get spacing configuration for different layout types.

    Args:
        layout_type: Type of layout (e.g., "default", "compact", "comfortable")

    Returns:
        Dictionary of spacing values
    """
    layouts = {
        "compact": {
            "margin": MARGINS["sm"],
            "padding": PADDING["sm"],
            "gap": GAPS["sm"],
        },
        "default": {
            "margin": MARGINS["md"],
            "padding": PADDING["md"],
            "gap": GAPS["md"],
        },
        "comfortable": {
            "margin": MARGINS["lg"],
            "padding": PADDING["lg"],
            "gap": GAPS["lg"],
        },
        "spacious": {
            "margin": MARGINS["xl"],
            "padding": PADDING["xl"],
            "gap": GAPS["xl"],
        },
    }

    return layouts.get(layout_type, layouts["default"])
