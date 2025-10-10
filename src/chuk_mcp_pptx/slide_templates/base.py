"""
Base Slide Template

Provides abstract base class for all slide templates.
"""

from typing import Any, Optional, Dict
from abc import ABC, abstractmethod


class SlideTemplate(ABC):
    """
    Base class for slide templates.

    All templates should:
    - Use Grid-based positioning (no hardcoded inches)
    - Accept optional theme parameter
    - Return slide index from render()
    - Be self-documenting via @template decorator
    """

    def __init__(self, theme: Optional[Dict[str, Any]] = None):
        """
        Initialize template.

        Args:
            theme: Optional theme dictionary
        """
        self.theme = theme

    @abstractmethod
    def render(self, prs) -> int:
        """
        Render template to a presentation.

        This method should:
        1. Add a new slide to the presentation
        2. Use Grid component for positioning
        3. Use design system components for content
        4. Apply theme if provided
        5. Return the index of the created slide

        Args:
            prs: python-pptx Presentation object

        Returns:
            Index of the created slide (0-based)

        Example:
            def render(self, prs):
                from ..components.core import Grid, Card
                from ..layout.patterns import get_dashboard_positions

                slide = prs.slides.add_slide(prs.slide_layouts[6])

                # Use grid-based positioning
                grid = Grid(columns=12, rows=2, gap="md")
                pos = grid.get_cell(col_span=6, col_start=0)
                card = Card(variant="default", theme=self.theme)
                card.render(slide, **pos)

                return len(prs.slides) - 1
        """
        raise NotImplementedError("Subclasses must implement render()")
