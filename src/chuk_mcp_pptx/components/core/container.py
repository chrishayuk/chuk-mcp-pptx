# src/chuk_mcp_pptx/components/core/container.py
"""
Container component for centering and constraining content.
"""

from typing import Optional, Dict, Any, Literal

from ..base import Component
from ...tokens.spacing import PADDING, CONTAINERS
from ...layout.helpers import SLIDE_WIDTH, SLIDE_HEIGHT
from ..registry import component, ComponentCategory, prop, example


@component(
    name="Container",
    category=ComponentCategory.LAYOUT,
    description="Responsive container for centering and constraining content width",
    props=[
        prop(
            "size",
            "string",
            "Container size",
            options=["sm", "md", "lg", "xl", "2xl", "full"],
            default="lg",
        ),
        prop(
            "padding",
            "string",
            "Internal padding",
            options=["none", "sm", "md", "lg", "xl"],
            default="md",
        ),
        prop("center", "boolean", "Center horizontally", default=True),
    ],
    examples=[
        example(
            "Centered content container",
            """
container = Container(size="lg", padding="md")
container.render(slide, top=1.5)
            """,
            size="lg",
            padding="md",
        )
    ],
    tags=["layout", "container", "responsive"],
)
class Container(Component):
    """
    Container component for centering and constraining content.

    Usage:
        # Standard container
        container = Container(size="lg")
        container.render(slide, top=1.5)

        # Full width
        container = Container(size="full", padding="none")
        container.render(slide, top=0)
    """

    def __init__(
        self,
        size: Literal["sm", "md", "lg", "xl", "2xl", "full"] = "lg",
        padding: Literal["none", "sm", "md", "lg", "xl"] = "md",
        center: bool = True,
        theme: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(theme)
        self.size = size
        self.padding = padding
        self.center = center

    def render(
        self,
        slide,
        top: float = 0,
        height: Optional[float] = None,
        placeholder: Optional[Any] = None,
    ):
        """
        Render container and return its bounds.

        Args:
            slide: PowerPoint slide object
            top: Top position in inches
            height: Optional height in inches
            placeholder: Optional placeholder to replace

        Returns:
            Dict with container dimensions for child rendering
        """
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds
        else:
            left = None
            width = None

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        container_width = (
            width if width is not None else CONTAINERS.get(self.size, CONTAINERS["lg"])
        )
        padding_value = PADDING.get(self.padding, PADDING["md"])

        # Center horizontally if requested (only if not using placeholder bounds)
        if left is None:
            if self.center:
                left = (SLIDE_WIDTH - container_width) / 2
            else:
                left = 0.5

        # Container doesn't render a visual element, just returns bounds
        return {
            "left": left + padding_value,
            "top": top + padding_value,
            "width": container_width - (2 * padding_value),
            "height": (height or SLIDE_HEIGHT - top) - (2 * padding_value),
        }
