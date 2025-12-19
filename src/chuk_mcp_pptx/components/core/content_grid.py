# src/chuk_mcp_pptx/components/core/content_grid.py
"""
Content grid component for arranging items in a grid layout.
"""

from typing import List, Dict, Any, Optional, Literal

from ..base import Component
from ..registry import component, ComponentCategory, prop, example


@component(
    name="ContentGrid",
    category=ComponentCategory.LAYOUT,
    description="Grid of content items (cards, tiles, buttons) using Grid system",
    props=[
        prop("items", "array", "List of items to display"),
        prop(
            "item_type",
            "string",
            "Type of items",
            options=["card", "tile", "button"],
            default="card",
        ),
        prop("columns", "number", "Number of columns", default=2),
    ],
    examples=[
        example(
            "Card grid",
            """
grid = ContentGrid(
    items=[
        {"title": "Feature 1", "description": "Description"},
        {"title": "Feature 2", "description": "Description"}
    ],
    item_type="card",
    columns=2
)
grid.render(slide, left=0.5, top=2.0, width=9.0, height=5.0)
            """,
            items=[{"title": "Feature 1"}, {"title": "Feature 2"}],
            item_type="card",
            columns=2,
        )
    ],
    tags=["grid", "cards", "layout", "content"],
)
class ContentGrid(Component):
    """
    Content grid component using Grid-based layout.

    Arranges items (cards, tiles, buttons) in a responsive grid.
    This is a reusable component that can be used anywhere, not just in slides.

    Usage:
        # Create a grid of cards
        grid = ContentGrid(
            items=[
                {"title": "Fast", "description": "Lightning quick"},
                {"title": "Secure", "description": "Enterprise-grade"}
            ],
            item_type="card",
            columns=2,
            theme=theme
        )
        grid.render(slide, left=0.5, top=2.0, width=9.0, height=5.0)
    """

    def __init__(
        self,
        items: List[Dict[str, Any]],
        item_type: Literal["card", "tile", "button"] = "card",
        columns: int = 2,
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize content grid.

        Args:
            items: List of item dicts (structure depends on item_type)
            item_type: Type of items ("card", "tile", "button")
            columns: Number of columns in grid (2-4)
            theme: Optional theme dictionary
        """
        super().__init__(theme)
        self.items = items
        self.item_type = item_type
        self.columns = min(max(columns, 2), 4)  # Clamp to 2-4

    def render(
        self,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        placeholder: Optional[Any] = None,
    ):
        """
        Render content grid using Grid system.

        Args:
            slide: PowerPoint slide
            left: Left position in inches
            top: Top position in inches
            width: Total width in inches
            height: Total height in inches
            placeholder: Optional placeholder to replace

        Returns:
            List of rendered shapes
        """
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        from .card import Card
        from .tile import Tile
        from .button import Button
        from .text import TextBox
        from .grid import Grid

        # Calculate grid layout
        rows = (len(self.items) + self.columns - 1) // self.columns
        grid = Grid(columns=self.columns, rows=rows, gap="md")

        shapes = []

        # Add items using Grid positioning
        for i, item_data in enumerate(self.items):
            row = i // self.columns
            col = i % self.columns

            pos = grid.get_cell(
                col_span=1,
                col_start=col,
                row_span=1,
                row_start=row,
                left=left,
                top=top,
                width=width,
                height=height,
                auto_height=False,
            )

            if self.item_type == "card":
                # Create card background
                card = Card(variant=item_data.get("variant", "default"), theme=self.theme)
                shape = card.render(slide, **pos)
                shapes.append(shape)

                # Add title text on top of card
                if "title" in item_data:
                    title_text = TextBox(
                        text=item_data["title"], font_size=14, bold=True, theme=self.theme
                    )
                    title_shape = title_text.render(
                        slide,
                        left=pos["left"] + 0.2,
                        top=pos["top"] + 0.2,
                        width=pos["width"] - 0.4,
                        height=0.5,
                    )
                    shapes.append(title_shape)

                # Add description if present
                if "description" in item_data:
                    desc_text = TextBox(
                        text=item_data["description"], font_size=11, theme=self.theme
                    )
                    desc_shape = desc_text.render(
                        slide,
                        left=pos["left"] + 0.2,
                        top=pos["top"] + 0.8,
                        width=pos["width"] - 0.4,
                        height=pos["height"] - 1.0,
                    )
                    shapes.append(desc_shape)

            elif self.item_type == "tile":
                tile = Tile(
                    label=item_data.get("label", item_data.get("title", "")),
                    text=item_data.get("value", ""),
                    variant=item_data.get("variant", "default"),
                    theme=self.theme,
                )
                shape = tile.render(slide, **pos)
                shapes.append(shape)

            else:  # button
                button = Button(
                    text=item_data.get("text", item_data.get("title", "")),
                    variant=item_data.get("variant", "default"),
                    size="md",
                    theme=self.theme,
                )
                shape = button.render(slide, **pos)
                shapes.append(shape)

        return shapes
