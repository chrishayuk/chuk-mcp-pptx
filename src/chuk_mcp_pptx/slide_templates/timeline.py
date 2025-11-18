"""
Timeline slide templates.

Provides templates for timelines and roadmaps.
"""

from typing import List, Dict, Any, Optional

from .base import SlideTemplate
from .registry import template, TemplateCategory, TemplateProp


@template(
    name="TimelineSlide",
    category=TemplateCategory.TIMELINE,
    description="Timeline slide with events using Grid system",
    props=[
        TemplateProp(name="title", type="string", description="Slide title"),
        TemplateProp(
            name="events", type="array", description="List of events with date and description"
        ),
        TemplateProp(
            name="orientation",
            type="string",
            description="Timeline direction",
            required=False,
            options=["horizontal", "vertical"],
            default="horizontal",
        ),
        TemplateProp(name="theme", type="object", description="Theme dictionary", required=False),
    ],
    examples=[
        {
            "title": "Product Roadmap 2024",
            "events": [
                {"date": "Q1", "description": "Beta Launch"},
                {"date": "Q2", "description": "Public Release"},
                {"date": "Q3", "description": "Enterprise Features"},
                {"date": "Q4", "description": "Global Expansion"},
            ],
            "orientation": "horizontal",
        }
    ],
    tags=["timeline", "roadmap", "milestones", "schedule"],
)
class TimelineSlide(SlideTemplate):
    """
    Timeline slide template using Grid-based layout.

    Creates a slide with a timeline of events.
    Uses Grid system for consistent positioning.
    """

    def __init__(
        self,
        title: str,
        events: List[Dict[str, str]],
        orientation: str = "horizontal",
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize timeline template.

        Args:
            title: Slide title
            events: List of event dicts with date and description
            orientation: Timeline direction ("horizontal" or "vertical")
            theme: Optional theme dictionary
        """
        super().__init__(theme)
        self.title = title
        self.events = events
        self.orientation = orientation

    def render(self, prs) -> int:
        """Render timeline slide using Grid system."""
        from ..components.core import Timeline, TextBox

        # Add blank slide
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Add title
        title_text = TextBox(text=self.title, font_size=28, bold=True, theme=self.theme)
        title_text.render(slide, left=0.5, top=0.5, width=9.0, height=0.8)

        # Add timeline using Timeline component
        # Map orientation to style
        timeline_style = "line" if self.orientation == "horizontal" else "vertical"
        timeline = Timeline(events=self.events, style=timeline_style, theme=self.theme)
        # Timeline component handles its own positioning
        timeline.render(slide, left=1.0, top=2.5, width=8.0)

        return len(prs.slides) - 1
