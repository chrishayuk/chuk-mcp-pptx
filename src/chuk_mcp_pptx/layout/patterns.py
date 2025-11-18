"""
Common slide layout patterns.

Provides pre-calculated position sets for common slide layouts like
dashboards, comparisons, hero sections, and galleries.
"""

from typing import Dict, Any
from ..tokens.spacing import GAPS


def _calculate_cell_position(
    col_span: int,
    col_start: int,
    row_start: int,
    col_width: float,
    row_height: float,
    gap_value: float,
    left: float,
    top: float,
    auto_height: bool = True,
) -> Dict[str, float]:
    """
    Calculate position for a grid cell.

    Internal helper function for layout patterns.
    """
    cell_left = left + (col_start * (col_width + gap_value))
    cell_top = top + (row_start * (row_height + gap_value))
    cell_width = (col_span * col_width) + ((col_span - 1) * gap_value)
    cell_height = row_height

    pos = {"left": round(cell_left, 3), "top": round(cell_top, 3), "width": round(cell_width, 3)}

    if not auto_height:
        pos["height"] = round(cell_height, 3)

    return pos


def get_dashboard_positions(
    gap: str = "md", left: float = 0.5, top: float = 1.8, width: float = 9.0, height: float = 5.5
) -> Dict[str, Any]:
    """
    Get positions for a dashboard layout.

    Layout:
    - 3 metric cards in top row (4 columns each)
    - Main content area (8 columns)
    - Sidebar (4 columns)

    Args:
        gap: Gap size
        left: Left edge of grid
        top: Top edge of grid
        width: Total width
        height: Total height

    Returns:
        Dictionary with positions for metrics, main, and sidebar
    """
    gap_value = GAPS.get(gap, GAPS["md"])
    columns = 12
    rows = 2

    # Calculate cell dimensions
    total_gap_width = (columns - 1) * gap_value
    col_width = (width - total_gap_width) / columns

    total_gap_height = (rows - 1) * gap_value
    row_height = (height - total_gap_height) / rows

    def calc_cell(col_span, col_start, row_start, auto_height=True):
        return _calculate_cell_position(
            col_span, col_start, row_start, col_width, row_height, gap_value, left, top, auto_height
        )

    return {
        "metrics": [
            calc_cell(4, 0, 0, auto_height=False),  # Metric 1: cols 0-3
            calc_cell(4, 4, 0, auto_height=False),  # Metric 2: cols 4-7
            calc_cell(4, 8, 0, auto_height=False),  # Metric 3: cols 8-11
        ],
        "main": calc_cell(8, 0, 1, auto_height=False),  # Main: cols 0-7, row 1
        "sidebar": calc_cell(4, 8, 1, auto_height=False),  # Sidebar: cols 8-11, row 1
        "description": "Dashboard layout with 3 metrics (top row) + main content (8 cols) + sidebar (4 cols)",
    }


def get_comparison_positions(
    gap: str = "md",
    left: float = 0.5,
    top: float = 1.8,
    width: float = 9.0,
    height: float = 5.5,
    include_header: bool = False,
) -> Dict[str, Any]:
    """
    Get positions for a two-column comparison layout.

    Layout:
    - Optional header row (full width)
    - Left column (6 columns)
    - Right column (6 columns)

    Args:
        gap: Gap size
        left: Left edge
        top: Top edge
        width: Total width
        height: Total height
        include_header: Whether to include header row

    Returns:
        Dictionary with positions for header (optional), left, and right
    """
    gap_value = GAPS.get(gap, GAPS["md"])
    columns = 12
    rows = 2 if include_header else 1

    # Calculate cell dimensions
    total_gap_width = (columns - 1) * gap_value
    col_width = (width - total_gap_width) / columns

    total_gap_height = (rows - 1) * gap_value if rows > 1 else 0
    row_height = (height - total_gap_height) / rows

    def calc_cell(col_span, col_start, row_start, auto_height=True):
        return _calculate_cell_position(
            col_span, col_start, row_start, col_width, row_height, gap_value, left, top, auto_height
        )

    layout = {"description": "Two-column comparison layout"}

    if include_header:
        layout["header"] = calc_cell(12, 0, 0, auto_height=False)  # Full width header
        layout["left"] = calc_cell(6, 0, 1, auto_height=False)  # Left column, row 1
        layout["right"] = calc_cell(6, 6, 1, auto_height=False)  # Right column, row 1
    else:
        layout["left"] = calc_cell(6, 0, 0, auto_height=False)  # Left column, row 0
        layout["right"] = calc_cell(6, 6, 0, auto_height=False)  # Right column, row 0

    return layout


def get_hero_positions(
    gap: str = "md",
    left: float = 0.5,
    top: float = 1.8,
    width: float = 9.0,
    height: float = 5.5,
    image_side: str = "left",
) -> Dict[str, Any]:
    """
    Get positions for a hero section layout.

    Layout:
    - Large hero image (7 columns)
    - Text content area (5 columns) with:
      - Title (full text area width)
      - Subtitle (full text area width)
      - Body (full text area width)

    Args:
        gap: Gap size
        left: Left edge
        top: Top edge
        width: Total width
        height: Total height
        image_side: Which side for image ("left" or "right")

    Returns:
        Dictionary with positions for hero_image, title, subtitle, and body
    """
    gap_value = GAPS.get(gap, GAPS["md"])
    columns = 12
    rows = 3  # For title, subtitle, body

    # Calculate cell dimensions
    total_gap_width = (columns - 1) * gap_value
    col_width = (width - total_gap_width) / columns

    total_gap_height = (rows - 1) * gap_value
    row_height = (height - total_gap_height) / rows

    def calc_cell(col_span, col_start, row_start, row_span=1, auto_height=True):
        cell_left = left + (col_start * (col_width + gap_value))
        cell_top = top + (row_start * (row_height + gap_value))
        cell_width = (col_span * col_width) + ((col_span - 1) * gap_value)
        cell_height = (row_span * row_height) + ((row_span - 1) * gap_value)

        pos = {
            "left": round(cell_left, 3),
            "top": round(cell_top, 3),
            "width": round(cell_width, 3),
        }

        if not auto_height:
            pos["height"] = round(cell_height, 3)

        return pos

    # Hero layout
    if image_side == "left":
        layout = {
            "hero_image": calc_cell(7, 0, 0, row_span=3, auto_height=False),  # Full height, left
            "title": calc_cell(5, 7, 0),  # Title in text area
            "subtitle": calc_cell(5, 7, 1),  # Subtitle in text area
            "body": calc_cell(5, 7, 2),  # Body in text area
        }
    else:  # image_side == "right"
        layout = {
            "title": calc_cell(5, 0, 0),  # Title in text area
            "subtitle": calc_cell(5, 0, 1),  # Subtitle in text area
            "body": calc_cell(5, 0, 2),  # Body in text area
            "hero_image": calc_cell(7, 5, 0, row_span=3, auto_height=False),  # Full height, right
        }

    layout["description"] = f"Hero section with image on {image_side}"

    return layout


def get_gallery_positions(
    gap: str = "md",
    left: float = 0.5,
    top: float = 1.8,
    width: float = 9.0,
    height: float = 5.5,
    layout_style: str = "2x2",
) -> Dict[str, Any]:
    """
    Get positions for a photo gallery grid layout.

    Supports multiple grid patterns:
    - "2x2": 4 items (6 cols x 2 rows each)
    - "3x2": 6 items (4 cols x 2 rows each)
    - "3x3": 9 items (4 cols x 3 rows each)
    - "4x2": 8 items (3 cols x 2 rows each)

    Args:
        gap: Gap size
        left: Left edge
        top: Top edge
        width: Total width
        height: Total height
        layout_style: Gallery pattern

    Returns:
        Dictionary with array of positions for gallery items
    """
    gap_value = GAPS.get(gap, GAPS["md"])

    # Define grid patterns
    patterns = {
        "2x2": {"cols": 2, "rows": 2, "col_span": 6},
        "3x2": {"cols": 3, "rows": 2, "col_span": 4},
        "3x3": {"cols": 3, "rows": 3, "col_span": 4},
        "4x2": {"cols": 4, "rows": 2, "col_span": 3},
    }

    if layout_style not in patterns:
        return {
            "error": f"Invalid layout_style '{layout_style}'. Supported: {', '.join(patterns.keys())}"
        }

    pattern = patterns[layout_style]
    grid_cols = pattern["cols"]
    grid_rows = pattern["rows"]
    col_span = pattern["col_span"]

    columns = 12
    total_gap_width = (columns - 1) * gap_value
    col_width = (width - total_gap_width) / columns

    total_gap_height = (grid_rows - 1) * gap_value
    row_height = (height - total_gap_height) / grid_rows

    def calc_cell(col_start, row_start):
        cell_left = left + (col_start * col_span * (col_width + gap_value))
        cell_top = top + (row_start * (row_height + gap_value))
        cell_width = (col_span * col_width) + ((col_span - 1) * gap_value)

        return {
            "left": round(cell_left, 3),
            "top": round(cell_top, 3),
            "width": round(cell_width, 3),
            "height": round(row_height, 3),
        }

    # Build gallery items
    items = []
    for row in range(grid_rows):
        for col in range(grid_cols):
            items.append(calc_cell(col, row))

    return {
        "items": items,
        "pattern": layout_style,
        "count": len(items),
        "description": f"Gallery with {len(items)} equal-sized items ({layout_style})",
    }
