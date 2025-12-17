# src/chuk_mcp_pptx/components/core/grid.py
"""
Grid layout component.

12-column grid system for flexible layouts, inspired by Bootstrap/Tailwind.
"""

from typing import Optional, Dict, Any, List, Literal

from ..base import Component
from ...tokens.spacing import GAPS
from ...layout.helpers import CONTENT_WIDTH, CONTENT_HEIGHT
from ..registry import component, ComponentCategory, prop, example


@component(
    name="Grid",
    category=ComponentCategory.LAYOUT,
    description="12-column grid system for flexible layouts",
    props=[
        prop("columns", "number", "Number of columns", default=12),
        prop(
            "gap",
            "string",
            "Gap between columns",
            options=["none", "xs", "sm", "md", "lg", "xl"],
            default="md",
        ),
        prop("rows", "number", "Number of rows", default=1),
    ],
    examples=[
        example(
            "Three column grid",
            """
grid = Grid(columns=3, gap="md")
positions = grid.get_cell_positions(slide, top=2.0, height=3.0)
            """,
            columns=3,
            gap="md",
        )
    ],
    tags=["layout", "grid", "columns"],
)
class Grid(Component):
    """
    12-column grid system (like Bootstrap/Tailwind).

    Usage:
        # 3-column grid
        grid = Grid(columns=3, gap="md")
        cells = grid.get_cell_positions(slide, top=2.0, height=3.0)

        for i, cell in enumerate(cells):
            # Render content in each cell
            card.render(slide, **cell)

        # Use with bounds from a container
        container = Container(size="lg")
        bounds = container.render(slide, top=1.5)
        grid = Grid(columns=12, rows=2, bounds=bounds)

        # Get specific cell position
        pos = grid.get_cell(col_span=8, col_start=0, row_start=1)
        card.render(slide, **pos)
    """

    def __init__(
        self,
        columns: int = 12,
        gap: Literal["none", "xs", "sm", "md", "lg", "xl"] = "md",
        rows: int = 1,
        bounds: Optional[Dict[str, float]] = None,
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize grid.

        Args:
            columns: Number of columns
            gap: Gap between cells
            rows: Number of rows
            bounds: Optional container bounds dict with 'left', 'top', 'width', 'height'
                   If provided, grid will use these as defaults for all cell calculations
            theme: Optional theme
        """
        super().__init__(theme)
        self.columns = columns
        self.gap = gap
        self.gap_inches = GAPS.get(gap, GAPS["md"])
        self.rows = rows
        self.bounds = bounds or {}

    def get_cell_positions(
        self,
        slide,
        left: float = 0.5,
        top: float = 1.5,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> List[Dict[str, float]]:
        """
        Calculate positions for all grid cells.

        Returns:
            List of dicts with 'left', 'top', 'width', 'height' for each cell
        """
        grid_width = width or CONTENT_WIDTH
        grid_height = height or CONTENT_HEIGHT

        # Calculate cell dimensions
        total_h_gap = self.gap_inches * (self.columns - 1)
        total_v_gap = self.gap_inches * (self.rows - 1)

        cell_width = (grid_width - total_h_gap) / self.columns
        cell_height = (grid_height - total_v_gap) / self.rows

        positions = []
        for row in range(self.rows):
            for col in range(self.columns):
                cell_left = left + col * (cell_width + self.gap_inches)
                cell_top = top + row * (cell_height + self.gap_inches)

                positions.append(
                    {
                        "left": cell_left,
                        "top": cell_top,
                        "width": cell_width,
                        "height": cell_height,
                        "row": row,
                        "col": col,
                    }
                )

        return positions

    def get_span(
        self,
        col_span: int = 1,
        row_span: int = 1,
        col_start: int = 0,
        row_start: int = 0,
        left: float = 0.5,
        top: float = 1.5,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> Dict[str, float]:
        """
        Get position for a cell that spans multiple columns/rows.

        Args:
            col_span: Number of columns to span
            row_span: Number of rows to span
            col_start: Starting column (0-indexed)
            row_start: Starting row (0-indexed)

        Returns:
            Dict with position and dimensions
        """
        grid_width = width or CONTENT_WIDTH
        grid_height = height or CONTENT_HEIGHT

        # Calculate cell dimensions
        total_h_gap = self.gap_inches * (self.columns - 1)
        total_v_gap = self.gap_inches * (self.rows - 1)

        cell_width = (grid_width - total_h_gap) / self.columns
        cell_height = (grid_height - total_v_gap) / self.rows

        # Calculate span dimensions
        span_width = cell_width * col_span + self.gap_inches * (col_span - 1)
        span_height = cell_height * row_span + self.gap_inches * (row_span - 1)

        # Calculate position
        cell_left = left + col_start * (cell_width + self.gap_inches)
        cell_top = top + row_start * (cell_height + self.gap_inches)

        return {"left": cell_left, "top": cell_top, "width": span_width, "height": span_height}

    def get_cell(
        self,
        col_span: int = 1,
        row_span: int = 1,
        col_start: int = 0,
        row_start: int = 0,
        left: Optional[float] = None,
        top: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        auto_height: bool = True,
    ) -> Dict[str, float]:
        """
        Get position for a cell with optional auto-height for components.

        This is the preferred method for laying out components in a grid.
        Use auto_height=True (default) for components that calculate their own height.
        Use auto_height=False when you need fixed-height cells.

        Args:
            col_span: Number of columns to span
            row_span: Number of rows to span
            col_start: Starting column (0-indexed)
            row_start: Starting row (0-indexed)
            left: Grid left position (uses bounds if not provided)
            top: Grid top position (uses bounds if not provided)
            width: Grid total width (uses bounds if not provided)
            height: Grid total height (uses bounds if not provided)
            auto_height: If True, omit height from result (for auto-sizing components)

        Returns:
            Dict with 'left', 'top', 'width' and optionally 'height'

        Example:
            # With bounds set on grid
            grid = Grid(columns=12, rows=2, bounds=container_bounds)
            pos = grid.get_cell(col_span=8, col_start=0, row_start=1)
            card.render(slide, **pos)

            # Without bounds (manual positioning)
            grid = Grid(columns=12, rows=2)
            pos = grid.get_cell(col_span=8, col_start=0, row_start=1,
                               left=0.5, top=2.0, width=9.0, height=4.0)
            card.render(slide, **pos)
        """
        # Use bounds as defaults if available
        grid_left = left if left is not None else self.bounds.get("left", 0.5)
        grid_top = top if top is not None else self.bounds.get("top", 1.5)
        grid_width = width if width is not None else self.bounds.get("width", CONTENT_WIDTH)
        grid_height = height if height is not None else self.bounds.get("height", CONTENT_HEIGHT)

        # Calculate column and row sizes
        total_gap_width = (self.columns - 1) * self.gap_inches
        col_width = (grid_width - total_gap_width) / self.columns

        total_gap_height = (self.rows - 1) * self.gap_inches
        row_height = (grid_height - total_gap_height) / self.rows

        # Calculate cell position
        cell_left = grid_left + (col_start * (col_width + self.gap_inches))
        cell_top = grid_top + (row_start * (row_height + self.gap_inches))
        cell_width = (col_span * col_width) + ((col_span - 1) * self.gap_inches)
        cell_height = (row_span * row_height) + ((row_span - 1) * self.gap_inches)

        # Build position dictionary
        position = {
            "left": round(cell_left, 3),
            "top": round(cell_top, 3),
            "width": round(cell_width, 3),
        }

        if not auto_height:
            position["height"] = round(cell_height, 3)

        return position

    def create_layout(
        self,
        left: Optional[float] = None,
        top: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Create a grid layout configuration with metadata.

        Returns grid configuration including cell sizes, bounds, and usage examples.
        Useful for understanding the grid structure and available patterns.

        Args:
            left: Grid left position (uses bounds if not provided)
            top: Grid top position (uses bounds if not provided)
            width: Grid total width (uses bounds if not provided)
            height: Grid total height (uses bounds if not provided)

        Returns:
            Dict with grid metadata including columns, rows, gap, cell_size, bounds, and usage examples

        Example:
            grid = Grid(columns=12, rows=2, gap="md")
            config = grid.create_layout(left=0.5, top=1.8, width=9.0, height=5.5)
            # Returns: {
            #   "columns": 12,
            #   "rows": 2,
            #   "gap": "md",
            #   "gap_inches": 0.1,
            #   "bounds": {...},
            #   "cell_size": {...},
            #   "usage": {...}
            # }
        """
        # Use bounds as defaults if available
        grid_left = left if left is not None else self.bounds.get("left", 0.5)
        grid_top = top if top is not None else self.bounds.get("top", 1.8)
        grid_width = width if width is not None else self.bounds.get("width", 9.0)
        grid_height = height if height is not None else self.bounds.get("height", 5.5)

        # Calculate cell dimensions
        total_gap_width = (self.columns - 1) * self.gap_inches
        col_width = (grid_width - total_gap_width) / self.columns

        total_gap_height = (self.rows - 1) * self.gap_inches
        row_height = (grid_height - total_gap_height) / self.rows

        return {
            "columns": self.columns,
            "rows": self.rows,
            "gap": self.gap,
            "gap_inches": self.gap_inches,
            "bounds": {
                "left": grid_left,
                "top": grid_top,
                "width": grid_width,
                "height": grid_height,
            },
            "cell_size": {"col_width": round(col_width, 3), "row_height": round(row_height, 3)},
            "usage": {
                "description": "Use get_cell() method to get cell positions",
                "example_patterns": {
                    "full_width": f'col_span=12, col_start=0 (width: {round(grid_width, 1)}")',
                    "half_width": f'col_span=6, col_start=0 or 6 (width: {round(col_width * 6 + self.gap_inches * 5, 1)}")',
                    "third_width": f'col_span=4, col_start=0/4/8 (width: {round(col_width * 4 + self.gap_inches * 3, 1)}")',
                    "quarter_width": f'col_span=3, col_start=0/3/6/9 (width: {round(col_width * 3 + self.gap_inches * 2, 1)}")',
                },
            },
        }
