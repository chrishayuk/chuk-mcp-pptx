"""
Layout system for PowerPoint presentations.

Provides:
- Grid system (12-column like Bootstrap/Tailwind)
- Layout components (Container, Stack, Spacer, Divider)
- Helper utilities for positioning and spacing
- Responsive layout patterns
"""

from .components import Container, Grid, Stack, Spacer, Divider
from .helpers import (
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    SLIDE_WIDTH_4_3,
    SLIDE_HEIGHT_4_3,
    CONTENT_WIDTH,
    CONTENT_HEIGHT,
    CONTENT_LEFT,
    CONTENT_TOP,
    validate_position,
    calculate_grid_layout,
    get_logo_position,
    get_safe_content_area,
    distribute_horizontally,
    center_element,
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
    "calculate_grid_layout",
    "get_logo_position",
    "get_safe_content_area",
    "distribute_horizontally",
    "center_element",
]
