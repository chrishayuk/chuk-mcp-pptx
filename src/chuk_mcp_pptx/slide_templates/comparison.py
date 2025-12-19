"""
Comparison slide templates.

Provides templates for side-by-side comparisons.
"""

from typing import List, Dict, Any, Optional

from .base import SlideTemplate
from .registry import template, TemplateCategory, TemplateProp


@template(
    name="ComparisonSlide",
    category=TemplateCategory.COMPARISON,
    description="Two-column comparison slide using Grid system",
    props=[
        TemplateProp(name="title", type="string", description="Slide title"),
        TemplateProp(name="left_title", type="string", description="Title for left column"),
        TemplateProp(name="left_items", type="array", description="Items for left column"),
        TemplateProp(name="right_title", type="string", description="Title for right column"),
        TemplateProp(name="right_items", type="array", description="Items for right column"),
        TemplateProp(name="theme", type="object", description="Theme dictionary", required=False),
    ],
    examples=[
        {
            "title": "Build vs Buy",
            "left_title": "Build In-House",
            "left_items": ["Full control", "Custom features", "Higher cost", "Longer timeline"],
            "right_title": "Buy Solution",
            "right_items": [
                "Quick deployment",
                "Proven reliability",
                "Lower initial cost",
                "Less customization",
            ],
        }
    ],
    tags=["comparison", "versus", "side-by-side", "options"],
)
class ComparisonSlide(SlideTemplate):
    """
    Comparison slide template using Grid-based layout.

    Creates a slide with two columns for comparing options, features, or approaches.
    Uses Grid system for consistent positioning.
    """

    def __init__(
        self,
        title: str,
        left_title: str,
        left_items: List[str],
        right_title: str,
        right_items: List[str],
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize comparison template.

        Args:
            title: Slide title
            left_title: Title for left column
            left_items: Items for left column
            right_title: Title for right column
            right_items: Items for right column
            theme: Optional theme dictionary
        """
        super().__init__(theme)
        self.title = title
        self.left_title = left_title
        self.left_items = left_items
        self.right_title = right_title
        self.right_items = right_items

    def render(self, prs) -> int:
        """Render comparison slide using Grid system."""
        from ..components.core import Card, BulletList, TextBox
        from ..layout.patterns import get_comparison_positions

        # Add blank slide
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Add title
        title_text = TextBox(text=self.title, font_size=28, bold=True, theme=self.theme)
        title_text.render(slide, left=0.5, top=0.5, width=9.0, height=0.8)

        # Use grid-based comparison positions
        positions = get_comparison_positions(
            gap="md", left=0.5, top=1.8, width=9.0, height=5.5, include_header=False
        )

        # Left column
        left_pos = positions["left"]
        left_card = Card(variant="default", theme=self.theme)
        # Ensure card gets explicit dimensions including height
        left_card.render(
            slide,
            left=left_pos["left"],
            top=left_pos["top"],
            width=left_pos["width"],
            height=left_pos["height"],
        )

        # Left title
        left_title_text = TextBox(text=self.left_title, font_size=16, bold=True, theme=self.theme)
        left_title_text.render(
            slide,
            left=left_pos["left"] + 0.2,
            top=left_pos["top"] + 0.2,
            width=left_pos["width"] - 0.4,
            height=0.4,
        )

        # Left bullet list
        left_bullets = BulletList(items=self.left_items, theme=self.theme)
        left_bullets.render(
            slide,
            left=left_pos["left"] + 0.3,
            top=left_pos["top"] + 0.7,
            width=left_pos["width"] - 0.6,
            height=left_pos["height"] - 1.0,  # Use actual height from position
        )

        # Right column
        right_pos = positions["right"]
        right_card = Card(variant="default", theme=self.theme)
        # Ensure card gets explicit dimensions including height
        right_card.render(
            slide,
            left=right_pos["left"],
            top=right_pos["top"],
            width=right_pos["width"],
            height=right_pos["height"],
        )

        # Right title
        right_title_text = TextBox(text=self.right_title, font_size=16, bold=True, theme=self.theme)
        right_title_text.render(
            slide,
            left=right_pos["left"] + 0.2,
            top=right_pos["top"] + 0.2,
            width=right_pos["width"] - 0.4,
            height=0.4,
        )

        # Right bullet list
        right_bullets = BulletList(items=self.right_items, theme=self.theme)
        right_bullets.render(
            slide,
            left=right_pos["left"] + 0.3,
            top=right_pos["top"] + 0.7,
            width=right_pos["width"] - 0.6,
            height=right_pos["height"] - 1.0,  # Use actual height from position
        )

        return len(prs.slides) - 1
