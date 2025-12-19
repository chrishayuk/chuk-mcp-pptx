"""
Dashboard slide templates.

Provides templates for metric dashboards and KPI displays.
"""

from typing import List, Dict, Any, Optional

from .base import SlideTemplate
from .registry import template, TemplateCategory, TemplateProp


@template(
    name="MetricsDashboard",
    category=TemplateCategory.DASHBOARD,
    description="Dashboard slide with metric cards in grid layout using Grid system",
    props=[
        TemplateProp(name="title", type="string", description="Slide title"),
        TemplateProp(
            name="metrics",
            type="array",
            description="List of metrics with label, value, optional change and trend",
        ),
        TemplateProp(
            name="layout",
            type="string",
            description="Layout style",
            required=False,
            options=["grid", "row"],
            default="grid",
        ),
        TemplateProp(name="theme", type="object", description="Theme dictionary", required=False),
    ],
    examples=[
        {
            "title": "Q4 Performance Metrics",
            "metrics": [
                {"label": "Revenue", "value": "$2.5M", "change": "+12%", "trend": "up"},
                {"label": "Users", "value": "45K", "change": "+8%", "trend": "up"},
                {"label": "NPS Score", "value": "72", "change": "+5pts", "trend": "up"},
            ],
            "layout": "grid",
        }
    ],
    tags=["dashboard", "metrics", "kpi", "grid", "performance"],
)
class MetricsDashboard(SlideTemplate):
    """
    Metrics dashboard template using Grid-based layout.

    Creates a slide with title and metric cards automatically positioned
    using the Grid system and layout patterns.
    """

    def __init__(
        self,
        title: str,
        metrics: List[Dict[str, str]],
        layout: str = "grid",
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize dashboard template.

        Args:
            title: Slide title
            metrics: List of metric dicts with label, value, change, trend
            layout: Layout style ("grid" or "row")
            theme: Optional theme dictionary
        """
        super().__init__(theme)
        self.title = title
        self.metrics = metrics
        self.layout = layout

    def render(self, prs) -> int:
        """Render dashboard slide using Grid system."""
        from ..components.core import MetricCard, TextBox
        from ..layout.patterns import get_dashboard_positions

        # Add blank slide
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Add title using TextBox component
        title_text = TextBox(text=self.title, font_size=32, bold=True, theme=self.theme)
        title_text.render(slide, left=0.5, top=0.5, width=9.0, height=0.8)

        # Use grid-based dashboard positions
        if self.layout == "grid":
            positions = get_dashboard_positions(gap="md", left=0.5, top=1.8, width=9.0, height=5.5)

            # Render metrics using grid positions
            for i, metric_data in enumerate(self.metrics[:3]):  # Top 3 metrics row
                pos = positions["metrics"][i]
                card = MetricCard(
                    label=metric_data["label"],
                    value=metric_data["value"],
                    change=metric_data.get("change"),
                    trend=metric_data.get("trend"),
                    theme=self.theme,
                )
                card.render(slide, **pos)

        else:  # row layout
            from ..components.core import Grid

            # Use Grid component directly for row layout
            grid = Grid(columns=len(self.metrics), rows=1, gap="md")

            for i, metric_data in enumerate(self.metrics):
                pos = grid.get_cell(
                    col_span=1,
                    col_start=i,
                    left=0.5,
                    top=2.5,
                    width=9.0,
                    height=2.5,
                    auto_height=False,
                )
                card = MetricCard(
                    label=metric_data["label"],
                    value=metric_data["value"],
                    change=metric_data.get("change"),
                    trend=metric_data.get("trend"),
                    theme=self.theme,
                )
                card.render(slide, **pos)

        return len(prs.slides) - 1
