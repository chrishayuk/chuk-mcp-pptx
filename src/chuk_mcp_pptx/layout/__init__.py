# src/chuk_mcp_pptx/layout/__init__.py
"""
Layout system for PowerPoint presentations.

Provides:
- Grid system (12-column like Bootstrap/Tailwind)
- Layout components (Container, Stack, Spacer, Divider)
- Helper utilities for positioning and spacing
- Responsive layout patterns
"""

# Layout components are available from components package directly
from .boundaries import (
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    SLIDE_WIDTH_4_3,
    SLIDE_HEIGHT_4_3,
    adjust_to_boundaries,
    validate_boundaries,
)
from .helpers import (
    CONTENT_WIDTH,
    CONTENT_HEIGHT,
    CONTENT_LEFT,
    CONTENT_TOP,
    validate_position,
    calculate_grid_layout,
    get_logo_position,
    get_safe_content_area,
)

__all__ = [
    # Components
    "Container",
    "Grid",
    "Stack",
    "Spacer",
    "Divider",
    # Constants
    "SLIDE_WIDTH",
    "SLIDE_HEIGHT",
    "SLIDE_WIDTH_4_3",
    "SLIDE_HEIGHT_4_3",
    "CONTENT_WIDTH",
    "CONTENT_HEIGHT",
    "CONTENT_LEFT",
    "CONTENT_TOP",
    # Helper functions
    "validate_position",
    "validate_boundaries",
    "adjust_to_boundaries",
    "calculate_grid_layout",
    "get_logo_position",
    "get_safe_content_area",
]
