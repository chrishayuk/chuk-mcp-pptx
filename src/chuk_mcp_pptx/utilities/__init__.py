"""
Utilities module for reusable chart, text, and component helpers.
"""

from .chart_utils import (
    # Modern utilities
    configure_legend,
    configure_axes,
    set_chart_title,
    apply_chart_colors,
    # Legacy API functions
    add_chart,
    add_scatter_chart,
    add_pie_chart,
    add_data_table,
    CHART_TYPES,
)
from .text_utils import (
    extract_slide_text,
    extract_presentation_text,
    format_text_frame,
    validate_text_fit,
    auto_fit_text,
)

__all__ = [
    # Chart utilities (modern)
    "configure_legend",
    "configure_axes",
    "set_chart_title",
    "apply_chart_colors",
    # Chart utilities (legacy API)
    "add_chart",
    "add_scatter_chart",
    "add_pie_chart",
    "add_data_table",
    "CHART_TYPES",
    # Text utilities
    "extract_slide_text",
    "extract_presentation_text",
    "format_text_frame",
    "validate_text_fit",
    "auto_fit_text",
]
