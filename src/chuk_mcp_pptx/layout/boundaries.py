# src/chuk_mcp_pptx/layout/boundaries.py
"""
Boundary validation and adjustment for PowerPoint elements.

Provides utilities to ensure elements fit within slide dimensions
and handle overflow scenarios gracefully.
"""

from typing import Tuple, Optional

# Standard PowerPoint slide dimensions (16:9 aspect ratio)
SLIDE_WIDTH = 10.0  # inches
SLIDE_HEIGHT = 5.625  # inches (16:9 ratio)

# Alternative 4:3 dimensions
SLIDE_WIDTH_4_3 = 10.0  # inches
SLIDE_HEIGHT_4_3 = 7.5  # inches

# Safe margins from edges
MARGIN_TOP = 1.0  # inches - accounts for typical title area
MARGIN_BOTTOM = 0.5  # inches
MARGIN_LEFT = 0.5  # inches
MARGIN_RIGHT = 0.5  # inches


def validate_boundaries(
    left: float, top: float, width: float, height: float, aspect_ratio: str = "16:9"
) -> Tuple[bool, Optional[str]]:
    """
    Validate element boundaries against slide dimensions.

    Useful for checking if elements will fit before rendering.

    Args:
        left: Left position in inches
        top: Top position in inches
        width: Width in inches
        height: Height in inches
        aspect_ratio: Slide aspect ratio ("16:9" or "4:3")

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> is_valid, error = validate_boundaries(1.0, 2.0, 8.0, 4.0)
        >>> if not is_valid:
        ...     print(f"Element won't fit: {error}")
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3

    # Check if element exceeds slide boundaries
    if left + width > slide_width:
        return False, f"Element exceeds slide width (max: {slide_width} inches)"
    if top + height > slide_height:
        return False, f"Element exceeds slide height (max: {slide_height} inches)"
    if left < 0 or top < 0:
        return False, "Element position cannot be negative"
    if width <= 0 or height <= 0:
        return False, "Element dimensions must be positive"

    return True, None


def adjust_to_boundaries(
    left: float, top: float, width: float, height: float, aspect_ratio: str = "16:9"
) -> Tuple[float, float, float, float]:
    """
    Adjust element dimensions to fit within slide boundaries.

    Unlike validate_position (in helpers.py) which tries to preserve size,
    this method will shrink elements if needed to fit.

    Args:
        left: Left position in inches
        top: Top position in inches
        width: Width in inches
        height: Height in inches
        aspect_ratio: Slide aspect ratio

    Returns:
        Tuple of adjusted (left, top, width, height)

    Example:
        >>> # Element that's too wide
        >>> left, top, width, height = adjust_to_boundaries(8.0, 1.0, 5.0, 3.0)
        >>> # Returns adjusted position/size that fits
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3

    # Adjust left if needed
    if left + width > slide_width:
        left = max(MARGIN_LEFT, slide_width - width)

    # Adjust top if needed
    if top + height > slide_height:
        top = max(MARGIN_TOP, slide_height - height)

    # Ensure non-negative position
    left = max(left, MARGIN_LEFT)
    top = max(top, MARGIN_TOP)

    # Adjust dimensions if still exceeding
    width = min(width, slide_width - MARGIN_LEFT - MARGIN_RIGHT)
    height = min(height, slide_height - MARGIN_TOP - MARGIN_BOTTOM)

    return left, top, width, height


def check_overlap(
    left1: float,
    top1: float,
    width1: float,
    height1: float,
    left2: float,
    top2: float,
    width2: float,
    height2: float,
) -> bool:
    """
    Check if two elements overlap.

    Args:
        left1, top1, width1, height1: First element bounds
        left2, top2, width2, height2: Second element bounds

    Returns:
        True if elements overlap, False otherwise

    Example:
        >>> overlaps = check_overlap(1.0, 1.0, 3.0, 2.0, 2.0, 1.5, 3.0, 2.0)
        >>> if overlaps:
        ...     print("Elements overlap!")
    """
    # Calculate boundaries
    right1 = left1 + width1
    bottom1 = top1 + height1
    right2 = left2 + width2
    bottom2 = top2 + height2

    # Check for no overlap (easier to reason about)
    no_overlap = right1 < left2 or right2 < left1 or bottom1 < top2 or bottom2 < top1

    return not no_overlap


def get_available_space(left: float, top: float, aspect_ratio: str = "16:9") -> Tuple[float, float]:
    """
    Get available width and height from a given position to slide edge.

    Args:
        left: Starting left position
        top: Starting top position
        aspect_ratio: Slide aspect ratio

    Returns:
        Tuple of (available_width, available_height)

    Example:
        >>> width, height = get_available_space(1.0, 2.0)
        >>> # Returns remaining space to right and bottom edges
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3

    available_width = max(0, slide_width - left - MARGIN_RIGHT)
    available_height = max(0, slide_height - top - MARGIN_BOTTOM)

    return available_width, available_height
