# src/chuk_mcp_pptx/tokens/__init__.py
"""
Design tokens for PowerPoint presentations.

Design tokens are the foundation of the design system, providing consistent
values for colors, typography, spacing, and other design properties.

Similar to CSS variables in web design, these tokens can be referenced
throughout components to maintain consistency and enable theming.

Usage:
    from chuk_mcp_pptx.tokens import PALETTE, FONT_SIZES, SPACING

    # Access raw values
    primary_color = PALETTE["blue"][500]
    heading_size = FONT_SIZES["3xl"]
    padding = SPACING["4"]

    # Get semantic tokens (theme-aware)
    from chuk_mcp_pptx.tokens import get_semantic_tokens
    tokens = get_semantic_tokens("blue", "dark")
    bg_color = tokens["background"]["DEFAULT"]
"""

from typing import Dict, Any
from .colors import PALETTE, get_semantic_tokens, GRADIENTS
from .typography import (
    FONT_FAMILIES,
    FONT_SIZES,
    FONT_WEIGHTS,
    LINE_HEIGHTS,
    LETTER_SPACING,
    get_text_style,
    TYPOGRAPHY_SCALE,
)
from .spacing import (
    SPACING,
    MARGINS,
    PADDING,
    GAPS,
    RADIUS,
    BORDER_WIDTH,
    SHADOWS,
    get_layout_spacing,
    GRID,
    CONTAINERS,
    ASPECT_RATIOS,
)

__all__ = [
    # Colors
    "PALETTE",
    "get_semantic_tokens",
    "GRADIENTS",
    # Typography
    "FONT_FAMILIES",
    "FONT_SIZES",
    "FONT_WEIGHTS",
    "LINE_HEIGHTS",
    "LETTER_SPACING",
    "TYPOGRAPHY_SCALE",
    "get_text_style",
    # Spacing
    "SPACING",
    "MARGINS",
    "PADDING",
    "GAPS",
    "RADIUS",
    "BORDER_WIDTH",
    "SHADOWS",
    "GRID",
    "CONTAINERS",
    "ASPECT_RATIOS",
    "get_layout_spacing",
    # Utilities
    "get_all_tokens",
    "export_tokens_json",
]


def get_all_tokens(primary_hue: str = "blue", mode: str = "dark") -> Dict[str, Any]:
    """
    Get all design tokens as a single dictionary.

    Args:
        primary_hue: Primary color hue
        mode: Color mode (dark/light)

    Returns:
        Dictionary containing all token categories
    """
    return {
        "colors": {
            "palette": PALETTE,
            "semantic": get_semantic_tokens(primary_hue, mode),
            "gradients": GRADIENTS,
        },
        "typography": {
            "families": FONT_FAMILIES,
            "sizes": FONT_SIZES,
            "weights": FONT_WEIGHTS,
            "lineHeights": LINE_HEIGHTS,
            "letterSpacing": LETTER_SPACING,
            "scale": TYPOGRAPHY_SCALE,
        },
        "spacing": {
            "scale": SPACING,
            "margins": MARGINS,
            "padding": PADDING,
            "gaps": GAPS,
        },
        "borders": {
            "radius": RADIUS,
            "width": BORDER_WIDTH,
        },
        "shadows": SHADOWS,
        "layout": {
            "grid": GRID,
            "containers": CONTAINERS,
            "aspectRatios": ASPECT_RATIOS,
        },
    }


def export_tokens_json(primary_hue: str = "blue", mode: str = "dark") -> str:
    """
    Export all tokens as JSON string for LLM consumption or external tools.

    Args:
        primary_hue: Primary color hue
        mode: Color mode (dark/light)

    Returns:
        JSON string with all tokens
    """
    import json

    tokens = get_all_tokens(primary_hue, mode)
    return json.dumps(tokens, indent=2)
