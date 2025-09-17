"""
Design tokens for PowerPoint presentations.
"""

from .colors import PALETTE, get_semantic_tokens, GRADIENTS
from .typography import (
    FONT_FAMILIES, FONT_SIZES, FONT_WEIGHTS,
    LINE_HEIGHTS, LETTER_SPACING, get_text_style
)
from .spacing import (
    SPACING, MARGINS, PADDING, GAPS, 
    RADIUS, BORDER_WIDTH, get_layout_spacing
)

__all__ = [
    # Colors
    'PALETTE',
    'get_semantic_tokens',
    'GRADIENTS',
    
    # Typography
    'FONT_FAMILIES',
    'FONT_SIZES',
    'FONT_WEIGHTS',
    'LINE_HEIGHTS',
    'LETTER_SPACING',
    'get_text_style',
    
    # Spacing
    'SPACING',
    'MARGINS',
    'PADDING',
    'GAPS',
    'RADIUS',
    'BORDER_WIDTH',
    'get_layout_spacing',
]