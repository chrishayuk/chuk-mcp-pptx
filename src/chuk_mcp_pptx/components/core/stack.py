# src/chuk_mcp_pptx/components/core/stack.py
"""
Stack component for vertical and horizontal layouts.
"""

from typing import Optional, Dict, Any, List, Literal

from ..base import Component
from ...tokens.spacing import GAPS
from ...layout.helpers import SLIDE_WIDTH, SLIDE_HEIGHT, CONTENT_WIDTH
from ..registry import component, ComponentCategory, prop, example


@component(
    name="Stack",
    category=ComponentCategory.LAYOUT,
    description="Stack elements vertically or horizontally with consistent spacing",
    props=[
        prop(
            "direction",
            "string",
            "Stack direction",
            options=["vertical", "horizontal"],
            default="vertical",
        ),
        prop(
            "gap",
            "string",
            "Gap between items",
            options=["none", "xs", "sm", "md", "lg", "xl"],
            default="md",
        ),
        prop(
            "align",
            "string",
            "Alignment",
            options=["start", "center", "end", "stretch"],
            default="start",
        ),
    ],
    examples=[
        example(
            "Vertical stack",
            """
stack = Stack(direction="vertical", gap="md")
positions = stack.distribute(3, item_height=1.0, top=2.0)
            """,
            direction="vertical",
            gap="md",
        )
    ],
    tags=["layout", "stack", "flexbox"],
)
class Stack(Component):
    """
    Stack component for arranging items (like CSS Flexbox).

    Usage:
        # Vertical stack
        stack = Stack(direction="vertical", gap="lg")
        positions = stack.distribute(
            num_items=3,
            item_height=1.0,
            top=2.0
        )

        for pos in positions:
            component.render(slide, **pos)
    """

    def __init__(
        self,
        direction: Literal["vertical", "horizontal"] = "vertical",
        gap: Literal["none", "xs", "sm", "md", "lg", "xl"] = "md",
        align: Literal["start", "center", "end", "stretch"] = "start",
        theme: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(theme)
        self.direction = direction
        self.gap = GAPS.get(gap, GAPS["md"])
        self.align = align
        # Store bounds for composition
        self.bounds = None

    def render(
        self,
        slide,
        left: float,
        top: float,
        width: float,
        height: float,
        placeholder: Optional[Any] = None,
    ) -> Dict[str, float]:
        """
        Render stack (initializes bounds for child positioning).

        Args:
            slide: PowerPoint slide object
            left: Left position in inches
            top: Top position in inches
            width: Width in inches
            height: Height in inches
            placeholder: Optional placeholder to replace

        Returns:
            Bounds dict for composition
        """
        # Delete placeholder if provided
        self._delete_placeholder_if_needed(placeholder)

        # Store bounds for composition
        self.bounds = {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
        }

        return self.bounds

    def distribute(
        self,
        num_items: int,
        item_width: Optional[float] = None,
        item_height: Optional[float] = None,
        left: float = 0.5,
        top: float = 1.5,
        container_width: Optional[float] = None,
        container_height: Optional[float] = None,
    ) -> List[Dict[str, float]]:
        """
        Distribute items in stack.

        Returns:
            List of position dicts for each item
        """
        positions = []

        if self.direction == "vertical":
            # Vertical stack
            current_top = top
            width = item_width or container_width or CONTENT_WIDTH

            for i in range(num_items):
                height = item_height or 1.0

                # Handle alignment
                if self.align == "center":
                    item_left = (SLIDE_WIDTH - width) / 2
                elif self.align == "end":
                    item_left = SLIDE_WIDTH - width - 0.5
                else:  # start or stretch
                    item_left = left

                positions.append(
                    {"left": item_left, "top": current_top, "width": width, "height": height}
                )

                current_top += height + self.gap

        else:  # horizontal
            # Horizontal stack
            current_left = left
            height = item_height or container_height or 1.0

            for i in range(num_items):
                width = item_width or 2.0

                # Handle alignment
                if self.align == "center":
                    item_top = (SLIDE_HEIGHT - height) / 2
                elif self.align == "end":
                    item_top = SLIDE_HEIGHT - height - 0.5
                else:  # start or stretch
                    item_top = top

                positions.append(
                    {"left": current_left, "top": item_top, "width": width, "height": height}
                )

                current_left += width + self.gap

        return positions

    def render_children(
        self,
        slide,
        children: List[Any],
        left: float = 0.5,
        top: float = 1.5,
        item_width: Optional[float] = None,
        item_height: Optional[float] = None,
    ) -> List[Any]:
        """
        Render a list of components in a stack layout.

        This is a convenience method that handles positioning automatically.

        Args:
            slide: PowerPoint slide
            children: List of component instances to render
            left: Starting left position
            top: Starting top position
            item_width: Width for all items (optional)
            item_height: Height for all items (optional)

        Returns:
            List of rendered shapes

        Example:
            stack = Stack(direction="vertical", gap="md")
            buttons = [
                Button("Save", "default"),
                Button("Cancel", "ghost")
            ]
            stack.render_children(slide, buttons, left=1, top=2)
        """
        positions = self.distribute(
            num_items=len(children),
            item_width=item_width,
            item_height=item_height,
            left=left,
            top=top,
        )

        shapes = []
        for child, pos in zip(children, positions):
            # Render each child at its calculated position
            if hasattr(child, "render"):
                shape = child.render(slide, **pos)
                shapes.append(shape)

        return shapes
