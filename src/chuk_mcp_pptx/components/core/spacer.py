# src/chuk_mcp_pptx/components/core/spacer.py
"""
Spacer component for adding spacing between elements.
"""

from typing import Optional, Dict, Any, Literal

from ..base import Component
from ...tokens.spacing import SPACING
from ..registry import component, ComponentCategory, prop


@component(
    name="Spacer",
    category=ComponentCategory.LAYOUT,
    description="Invisible spacer for adding spacing between elements",
    props=[
        prop(
            "size",
            "string",
            "Spacer size",
            options=["xs", "sm", "md", "lg", "xl", "2xl"],
            default="md",
        ),
        prop(
            "direction",
            "string",
            "Spacer direction",
            options=["vertical", "horizontal"],
            default="vertical",
        ),
    ],
    tags=["layout", "spacer", "margin"],
)
class Spacer(Component):
    """
    Spacer component for adding space (like SwiftUI Spacer).

    Usage:
        # Get spacer height
        spacer = Spacer(size="lg", direction="vertical")
        spacing = spacer.get_size()
    """

    def __init__(
        self,
        size: Literal["xs", "sm", "md", "lg", "xl", "2xl"] = "md",
        direction: Literal["vertical", "horizontal"] = "vertical",
        theme: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(theme)
        self.size = size
        self.direction = direction

    def get_size(self) -> float:
        """Get the spacer size in inches."""
        size_map = {
            "xs": SPACING["4"],
            "sm": SPACING["6"],
            "md": SPACING["8"],
            "lg": SPACING["12"],
            "xl": SPACING["16"],
            "2xl": SPACING["24"],
        }
        return size_map.get(self.size, SPACING["8"])

    def render(self, slide, left: float = 0, top: float = 0, placeholder: Optional[Any] = None):
        """Spacer doesn't render anything, just returns size."""
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        size = self.get_size()
        if self.direction == "vertical":
            return {"height": size, "width": 0}
        else:
            return {"width": size, "height": 0}
