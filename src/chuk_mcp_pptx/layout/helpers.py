# src/chuk_mcp_pptx/layout/helpers.py
"""
Layout Helpers for PowerPoint MCP Server

Provides utilities for ensuring proper positioning and sizing of elements
within standard PowerPoint slide dimensions.
"""

from typing import Tuple, List, Dict, Optional


# Import boundary constants and utilities
from .boundaries import (
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    SLIDE_HEIGHT_4_3,
    MARGIN_TOP,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    validate_boundaries,
)

# Content area (safe zone)
CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT  # 9.0 inches
CONTENT_HEIGHT = SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM  # 4.125 inches
CONTENT_LEFT = MARGIN_LEFT
CONTENT_TOP = MARGIN_TOP


def validate_position(
    left: float,
    top: float,
    width: float,
    height: float,
    aspect_ratio: str = "16:9",
    auto_adjust: bool = True,
) -> Tuple[float, float, float, float]:
    """
    Validate and optionally adjust position to ensure element fits within slide.

    This is the main boundary handler that layout containers use.
    Individual components should generally not call this directly -
    instead, they should be placed within layout containers that
    handle boundaries automatically.

    Args:
        left: Left position in inches
        top: Top position in inches
        width: Width in inches
        height: Height in inches
        aspect_ratio: Slide aspect ratio ("16:9" or "4:3")
        auto_adjust: If True, automatically adjusts to fit. If False, just validates.

    Returns:
        Tuple of adjusted (left, top, width, height)

    Example:
        >>> # Layout container handles boundaries for all children
        >>> container = Container(size="lg")
        >>> bounds = container.render(slide, top=2.0)
        >>> # All components placed in container are auto-validated
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3

    if not auto_adjust:
        # Just validate without adjusting
        is_valid, error = validate_boundaries(left, top, width, height, aspect_ratio)
        if not is_valid:
            raise ValueError(f"Element doesn't fit: {error}")
        return left, top, width, height

    # Auto-adjust to fit
    # Ensure minimum size
    width = max(0.5, width)
    height = max(0.5, height)

    # Define max available content area
    max_content_bottom = slide_height - MARGIN_BOTTOM
    max_content_right = slide_width - MARGIN_RIGHT

    # First, ensure position is within valid range
    # Allow elements above MARGIN_TOP only if explicitly positioned there (e.g., logos)
    # but adjust elements that would exceed boundaries

    # Adjust if element goes beyond right edge
    if left + width > max_content_right:
        # First, try to move left
        new_left = max_content_right - width
        if new_left >= MARGIN_LEFT:
            left = new_left
        else:
            # Can't fit by moving, shrink width
            left = MARGIN_LEFT
            width = max_content_right - MARGIN_LEFT

    # Adjust if element goes beyond bottom edge
    if top + height > max_content_bottom:
        # First, try to reduce height to fit at current position
        available_height = max_content_bottom - top
        if available_height >= 0.5:  # Minimum useful height
            height = available_height
        else:
            # Position is too low - move up but not above title area
            top = max(MARGIN_TOP, max_content_bottom - height)
            # Recalculate height after moving
            available_height = max_content_bottom - top
            if available_height < height:
                height = max(0.5, available_height)

    # Ensure position doesn't start outside slide bounds
    if left < 0:
        left = MARGIN_LEFT
    if top < 0:
        top = MARGIN_TOP
    if top > max_content_bottom - 0.5:
        top = max(MARGIN_TOP, max_content_bottom - 0.5)
        height = max(0.5, max_content_bottom - top)

    # Final safety checks - ensure minimum sizes
    width = max(0.5, min(width, max_content_right - left))
    height = max(0.5, min(height, max_content_bottom - top))

    return left, top, width, height


def calculate_grid_layout(
    num_items: int,
    columns: Optional[int] = None,
    spacing: float = 0.2,
    container_left: float = CONTENT_LEFT,
    container_top: float = CONTENT_TOP,
    container_width: float = CONTENT_WIDTH,
    container_height: float = CONTENT_HEIGHT,
) -> List[Dict[str, float]]:
    """
    Calculate optimal grid layout for multiple items.

    Args:
        num_items: Number of items to arrange
        columns: Number of columns (auto-calculated if None)
        spacing: Spacing between items in inches
        container_left: Left position of container area
        container_top: Top position of container area
        container_width: Width of container area
        container_height: Height of container area

    Returns:
        List of position dictionaries with 'left', 'top', 'width', 'height'
    """
    if num_items == 0:
        return []

    # Auto-calculate columns if not specified
    if columns is None:
        if num_items <= 2:
            columns = num_items
        elif num_items <= 4:
            columns = 2
        elif num_items <= 9:
            columns = 3
        else:
            columns = 4

    # Calculate rows
    rows = (num_items + columns - 1) // columns

    # Calculate item dimensions
    total_h_spacing = spacing * (columns - 1)
    total_v_spacing = spacing * (rows - 1)

    item_width = (container_width - total_h_spacing) / columns
    item_height = (container_height - total_v_spacing) / rows

    # Ensure minimum item size
    item_width = max(1.0, item_width)
    item_height = max(0.75, item_height)

    positions = []
    for i in range(num_items):
        row = i // columns
        col = i % columns

        left = container_left + col * (item_width + spacing)
        top = container_top + row * (item_height + spacing)

        # Validate each position
        left, top, width, height = validate_position(left, top, item_width, item_height)

        positions.append({"left": left, "top": top, "width": width, "height": height})

    return positions


def get_logo_position(
    position: str, size: float = 1.0, margin: float = 0.5, aspect_ratio: str = "16:9"
) -> Dict[str, float]:
    """
    Get standard logo position coordinates.

    Args:
        position: Position name (e.g., "top-left", "bottom-right")
        size: Logo size in inches
        margin: Margin from edges in inches
        aspect_ratio: Slide aspect ratio

    Returns:
        Dictionary with 'left', 'top', 'width', 'height'
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3

    positions = {
        "top-left": (margin, margin),
        "top-center": ((slide_width - size) / 2, margin),
        "top-right": (slide_width - size - margin, margin),
        "center-left": (margin, (slide_height - size) / 2),
        "center": ((slide_width - size) / 2, (slide_height - size) / 2),
        "center-right": (slide_width - size - margin, (slide_height - size) / 2),
        "bottom-left": (margin, slide_height - size - margin),
        "bottom-center": ((slide_width - size) / 2, slide_height - size - margin),
        "bottom-right": (slide_width - size - margin, slide_height - size - margin),
    }

    # Default to top-right for invalid positions
    left, top = positions.get(position, positions["top-right"])

    # Validate position
    left, top, width, height = validate_position(left, top, size, size, aspect_ratio)

    return {"left": left, "top": top, "width": width, "height": height}


def get_safe_content_area(has_title: bool = True, aspect_ratio: str = "16:9") -> Dict[str, float]:
    """
    Get the safe content area for placing elements.

    Args:
        has_title: Whether the slide has a title
        aspect_ratio: Slide aspect ratio

    Returns:
        Dictionary with 'left', 'top', 'width', 'height'
    """
    top_margin = MARGIN_TOP if has_title else 0.5
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3

    return {
        "left": CONTENT_LEFT,
        "top": top_margin,
        "width": CONTENT_WIDTH,
        "height": slide_height - top_margin - MARGIN_BOTTOM,
    }
