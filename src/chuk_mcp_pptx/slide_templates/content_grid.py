"""
Content grid slide templates.

Provides templates for slides with grid layouts of cards, tiles, or buttons.
"""

from typing import List, Dict, Any, Optional

from .base import SlideTemplate
from .registry import template, TemplateCategory, TemplateProp


@template(
    name="ContentGridSlide",
    category=TemplateCategory.CONTENT,
    description="Slide with grid of content items (cards, tiles, buttons) using Grid system",
    props=[
        TemplateProp(name="title", type="string", description="Slide title"),
        TemplateProp(name="items", type="array", description="List of items to display"),
        TemplateProp(
            name="item_type",
            type="string",
            description="Type of items",
            required=False,
            options=["card", "tile", "button"],
            default="card",
        ),
        TemplateProp(
            name="columns",
            type="number",
            description="Number of columns",
            required=False,
            default=2,
        ),
        TemplateProp(name="theme", type="object", description="Theme dictionary", required=False),
    ],
    examples=[
        {
            "title": "Key Features",
            "items": [
                {"title": "Fast", "description": "Lightning quick performance"},
                {"title": "Secure", "description": "Enterprise-grade security"},
                {"title": "Scalable", "description": "Grows with your needs"},
                {"title": "Reliable", "description": "99.9% uptime guarantee"},
            ],
            "item_type": "card",
            "columns": 2,
        }
    ],
    tags=["grid", "cards", "features", "content", "layout"],
)
class ContentGridSlide(SlideTemplate):
    """
    Content grid slide template using ContentGrid component.

    Creates a complete slide with title and ContentGrid component.
    The ContentGrid component can be reused independently.
    """

    def __init__(
        self,
        title: str,
        items: List[Dict[str, Any]],
        item_type: str = "card",
        columns: int = 2,
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize content grid slide template.

        Args:
            title: Slide title
            items: List of item dicts (structure depends on item_type)
            item_type: Type of items ("card", "tile", "button")
            columns: Number of columns in grid (2-4)
            theme: Optional theme dictionary
        """
        super().__init__(theme)
        self.title = title
        self.items = items
        self.item_type = item_type
        self.columns = columns

    def render(self, prs) -> int:
        """Render content grid slide using ContentGrid component."""
        from ..components.core import ContentGrid, TextBox

        # Add blank slide
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Add title
        title_text = TextBox(text=self.title, font_size=28, bold=True, theme=self.theme)
        title_text.render(slide, left=0.5, top=0.5, width=9.0, height=0.8)

        # Use ContentGrid component to render the grid
        content_grid = ContentGrid(
            items=self.items, item_type=self.item_type, columns=self.columns, theme=self.theme
        )
        content_grid.render(slide, left=0.5, top=1.8, width=9.0, height=5.5)

        return len(prs.slides) - 1
