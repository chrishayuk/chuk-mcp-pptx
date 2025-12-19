# src/chuk_mcp_pptx/components/core/smart_art.py
"""
SmartArt-style diagram components for PowerPoint presentations.

Provides professional diagrams like process flows, cycles, hierarchies, etc.
"""

from typing import List, Optional, Dict, Any
import math

from ..base import Component
from ..registry import component, ComponentCategory, prop, example
from .shape import Shape
from .connector import Connector


class SmartArtBase(Component):
    """Base class for SmartArt-like diagram components."""

    def __init__(self, items: List[str], theme: Optional[Dict[str, Any]] = None):
        """
        Initialize SmartArt component.

        Args:
            items: List of text items for the diagram
            theme: Optional theme override
        """
        super().__init__(theme)
        self.items = items

    def _get_color(self, index: int, color_type: str = "primary") -> str:
        """Get alternating colors for items."""
        colors = ["primary.DEFAULT", "secondary.DEFAULT", "accent.DEFAULT"]
        if color_type == "alternating":
            return colors[index % len(colors)]
        return f"{color_type}.DEFAULT"


@component(
    name="ProcessFlow",
    category=ComponentCategory.UI,
    description="Process flow diagram with sequential steps",
    props=[
        prop("items", "array", "Process steps", required=True),
        prop("left", "number", "Left position in inches", required=True),
        prop("top", "number", "Top position in inches", required=True),
        prop("width", "number", "Width in inches", required=True),
        prop("height", "number", "Height in inches", required=True),
    ],
    examples=[
        example(
            "Development process",
            """
process = ProcessFlow(items=["Research", "Design", "Develop", "Test", "Deploy"])
process.render(slide, left=1, top=2, width=8, height=2)
            """,
            items=["Research", "Design", "Develop"],
        ),
    ],
    tags=["smartart", "process", "flow", "diagram"],
)
class ProcessFlow(SmartArtBase):
    """
    Process flow diagram component.

    Creates a horizontal sequential flow with connected shapes.

    Usage:
        process = ProcessFlow(items=["Plan", "Execute", "Review"])
        process.render(slide, left=1, top=2, width=8, height=2)
    """

    def render(
        self,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        placeholder: Optional[Any] = None,
    ) -> List[Any]:
        """Render process flow diagram."""
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        shapes = []
        num_items = len(self.items)

        if num_items == 0:
            return shapes

        # Calculate spacing
        min_spacing = 0.2
        total_spacing = min_spacing * (num_items - 1)
        available_width = width - total_spacing
        item_width = min(available_width / num_items, 1.5)

        # Adjust for centering if items are small
        if item_width < available_width / num_items:
            total_width = item_width * num_items + total_spacing
            start_offset = (width - total_width) / 2
        else:
            start_offset = 0

        for idx, item in enumerate(self.items):
            x = left + start_offset + idx * (item_width + min_spacing)

            # Create chevron shape (or rectangle for last item)
            shape_type = "chevron" if idx < num_items - 1 else "rounded_rectangle"
            fill_color = self._get_color(idx, "alternating")

            shape_comp = Shape(
                shape_type=shape_type, text=item, fill_color=fill_color, theme=self.theme
            )
            shape = shape_comp.render(slide, x, top, item_width, height * 0.8)
            shapes.append(shape)

        return shapes


@component(
    name="CycleDiagram",
    category=ComponentCategory.UI,
    description="Circular cycle diagram",
    props=[
        prop("items", "array", "Cycle items", required=True),
        prop("left", "number", "Left position in inches", required=True),
        prop("top", "number", "Top position in inches", required=True),
        prop("width", "number", "Width in inches", required=True),
        prop("height", "number", "Height in inches", required=True),
    ],
    examples=[
        example(
            "PDCA Cycle",
            """
cycle = CycleDiagram(items=["Plan", "Do", "Check", "Act"])
cycle.render(slide, left=1, top=1, width=6, height=5)
            """,
            items=["Plan", "Do", "Check", "Act"],
        ),
    ],
    tags=["smartart", "cycle", "circular", "diagram"],
)
class CycleDiagram(SmartArtBase):
    """
    Cycle diagram component.

    Creates a circular diagram with connected items.

    Usage:
        cycle = CycleDiagram(items=["Plan", "Do", "Check", "Act"])
        cycle.render(slide, left=1, top=1, width=6, height=5)
    """

    def render(
        self,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        placeholder: Optional[Any] = None,
    ) -> List[Any]:
        """Render cycle diagram."""
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        shapes = []
        num_items = len(self.items)

        if num_items == 0:
            return shapes

        center_x = left + width / 2
        center_y = top + height / 2

        # Adjust radius and shape size based on number of items
        if num_items <= 4:
            radius = min(width, height) / 2.5
            shape_width = 1.2
            shape_height = 0.8
        elif num_items <= 6:
            radius = min(width, height) / 2.2
            shape_width = 1.0
            shape_height = 0.7
        else:
            radius = min(width, height) / 2.0
            shape_width = 0.9
            shape_height = 0.6

        for idx, item in enumerate(self.items):
            angle = 2 * math.pi * idx / num_items - math.pi / 2
            x = center_x + radius * math.cos(angle) - shape_width / 2
            y = center_y + radius * math.sin(angle) - shape_height / 2

            fill_color = self._get_color(idx, "alternating")

            shape_comp = Shape(
                shape_type="rounded_rectangle", text=item, fill_color=fill_color, theme=self.theme
            )
            shape = shape_comp.render(slide, x, y, shape_width, shape_height)
            shapes.append(shape)

            # Add curved connector to next item
            next_idx = (idx + 1) % num_items
            next_angle = 2 * math.pi * next_idx / num_items - math.pi / 2
            next_x = center_x + radius * math.cos(next_angle) - shape_width / 2
            next_y = center_y + radius * math.sin(next_angle) - shape_height / 2

            # Calculate edge points for connector
            curr_cx = x + shape_width / 2
            curr_cy = y + shape_height / 2
            next_cx = next_x + shape_width / 2
            next_cy = next_y + shape_height / 2

            dx = next_cx - curr_cx
            dy = next_cy - curr_cy
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 0:
                dx /= dist
                dy /= dist

                start_x = curr_cx + dx * shape_width * 0.5
                start_y = curr_cy + dy * shape_height * 0.5
                end_x = next_cx - dx * shape_width * 0.5
                end_y = next_cy - dy * shape_height * 0.5

                connector_comp = Connector(
                    start_x=start_x,
                    start_y=start_y,
                    end_x=end_x,
                    end_y=end_y,
                    connector_type="curved",
                    line_color="muted.foreground",
                    arrow_end=True,
                    theme=self.theme,
                )
                connector = connector_comp.render(slide)
                shapes.append(connector)

        return shapes


@component(
    name="HierarchyDiagram",
    category=ComponentCategory.UI,
    description="Organizational hierarchy diagram",
    props=[
        prop("items", "array", "Hierarchy items (first is root)", required=True),
        prop("left", "number", "Left position in inches", required=True),
        prop("top", "number", "Top position in inches", required=True),
        prop("width", "number", "Width in inches", required=True),
        prop("height", "number", "Height in inches", required=True),
    ],
    examples=[
        example(
            "Org chart",
            """
hierarchy = HierarchyDiagram(items=["CEO", "CTO", "CFO", "COO"])
hierarchy.render(slide, left=1, top=1, width=8, height=3)
            """,
            items=["CEO", "CTO", "CFO"],
        ),
    ],
    tags=["smartart", "hierarchy", "org", "chart", "diagram"],
)
class HierarchyDiagram(SmartArtBase):
    """
    Hierarchy diagram component.

    Creates an organizational chart with root and child items.

    Usage:
        hierarchy = HierarchyDiagram(items=["CEO", "CTO", "CFO", "COO"])
        hierarchy.render(slide, left=1, top=1, width=8, height=3)
    """

    def render(
        self,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        placeholder: Optional[Any] = None,
    ) -> List[Any]:
        """Render hierarchy diagram."""
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        shapes = []

        if len(self.items) == 0:
            return shapes

        # Top level (root)
        top_x = left + width / 2 - 1.5
        top_y = top

        root_shape_comp = Shape(
            shape_type="rounded_rectangle",
            text=self.items[0],
            fill_color="primary.DEFAULT",
            theme=self.theme,
        )
        root_shape = root_shape_comp.render(slide, top_x, top_y, 3.0, 0.8)
        shapes.append(root_shape)

        # Second level items
        if len(self.items) > 1:
            remaining = self.items[1:]
            num_items = len(remaining)
            item_width = min(1.8, (width - 0.3 * (num_items - 1)) / num_items)

            total_width = num_items * item_width + (num_items - 1) * 0.3
            start_x = left + (width - total_width) / 2

            for idx, item in enumerate(remaining):
                x = start_x + idx * (item_width + 0.3)
                y = top + 2.0

                child_shape_comp = Shape(
                    shape_type="rectangle",
                    text=item,
                    fill_color="secondary.DEFAULT",
                    theme=self.theme,
                )
                child_shape = child_shape_comp.render(slide, x, y, item_width, 0.8)
                shapes.append(child_shape)

                # Add connector from root to child
                connector_comp = Connector(
                    start_x=top_x + 1.5,  # Center of root
                    start_y=top_y + 0.8,  # Bottom of root
                    end_x=x + item_width / 2,  # Center of child
                    end_y=y,  # Top of child
                    connector_type="straight",
                    line_color="border.DEFAULT",
                    arrow_end=True,
                    theme=self.theme,
                )
                connector = connector_comp.render(slide)
                shapes.append(connector)

        return shapes
