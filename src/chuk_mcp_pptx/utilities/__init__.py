"""
Utilities module for reusable chart, text, and component helpers.
"""

from .chart_utils import (
    configure_legend,
    configure_axes,
    set_chart_title,
    apply_chart_colors
)
from .text_utils import (
    extract_slide_text,
    extract_presentation_text,
    format_text_frame,
    validate_text_fit,
    auto_fit_text,
)

__all__ = [
    # Chart utilities
    "configure_legend",
    "configure_axes",
    "set_chart_title",
    "apply_chart_colors",
    # Text utilities
    "extract_slide_text",
    "extract_presentation_text",
    "format_text_frame",
    "validate_text_fit",
    "auto_fit_text",
]
