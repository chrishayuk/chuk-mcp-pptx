"""
Pie and Doughnut chart components with variants and registry integration.
"""

from typing import List, Optional, Tuple
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.dml.color import RGBColor

from .base import ChartComponent
from ..variants import PIE_CHART_VARIANTS
from ..registry import component, ComponentCategory, prop, example


@component(
    name="PieChart",
    category=ComponentCategory.CHART,
    description="Pie chart component for showing proportions and percentages",
    props=[
        prop(
            "categories",
            "array",
            "Category labels",
            required=True,
            example=["Q1", "Q2", "Q3", "Q4"],
        ),
        prop(
            "values",
            "array",
            "Data values (must be positive)",
            required=True,
            example=[30, 25, 25, 20],
        ),
        prop(
            "variant",
            "string",
            "Chart variant",
            options=["pie", "doughnut", "exploded"],
            default="pie",
            example="pie",
        ),
        prop(
            "style",
            "string",
            "Visual style preset",
            options=["default", "detailed", "minimal"],
            default="default",
            example="default",
        ),
        prop("title", "string", "Chart title", example="Market Share"),
        prop("explode_slice", "number", "Index of slice to explode (0-based)", example=0),
        prop(
            "legend",
            "string",
            "Legend position",
            options=["right", "bottom", "top", "none"],
            default="right",
            example="right",
        ),
    ],
    variants={
        "variant": ["pie", "doughnut", "exploded"],
        "style": ["default", "detailed", "minimal"],
    },
    examples=[
        example(
            "Basic pie chart",
            """
chart = PieChart(
    categories=["Product A", "Product B", "Product C"],
    values=[45, 30, 25],
    title="Market Share",
    variant="pie"
)
chart.render(slide, left=1, top=2)
            """,
            categories=["Product A", "Product B", "Product C"],
            values=[45, 30, 25],
            variant="pie",
        ),
        example(
            "Doughnut chart with detailed style",
            """
chart = PieChart(
    categories=["Sales", "Marketing", "R&D", "Operations"],
    values=[40, 25, 20, 15],
    title="Budget Allocation",
    variant="doughnut",
    style="detailed"
)
chart.render(slide)
            """,
            categories=["Sales", "Marketing", "R&D", "Operations"],
            values=[40, 25, 20, 15],
            variant="doughnut",
            style="detailed",
        ),
    ],
    tags=["chart", "pie", "doughnut", "proportions", "percentages"],
)
class PieChart(ChartComponent):
    """
    Pie chart component for showing proportions.

    Features:
    - Multiple variants (pie, doughnut, exploded)
    - Automatic percentage calculation
    - Theme-aware coloring
    - Data validation
    - Exploded slices

    Variants:
    - pie: Classic circular pie chart
    - doughnut: Pie chart with hollow center
    - exploded: Pie chart with separated slices

    Styles:
    - default: Shows percentages
    - detailed: Shows percentages and values
    - minimal: No labels
    """

    def __init__(
        self,
        categories: List[str],
        values: List[float],
        variant: str = "pie",
        style: str = "default",
        explode_slice: Optional[int] = None,
        **kwargs,
    ):
        """
        Initialize pie chart.

        Args:
            categories: Category labels
            values: Data values (must be positive)
            variant: Chart variant (pie, doughnut, exploded)
            style: Visual style (default, detailed, minimal)
            explode_slice: Index of slice to explode (optional)
            **kwargs: Additional chart parameters (title, theme, legend, etc.)
        """
        super().__init__(style=style, **kwargs)
        self.categories = categories
        self.values = values
        self.variant = variant
        self.explode_slice = explode_slice

        # Validate data during initialization
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")

        # Update variant props to include pie-specific variants
        self.variant_props = PIE_CHART_VARIANTS.build(variant=variant, style=style)

        # Set chart type based on variant
        if variant == "doughnut":
            self.chart_type = XL_CHART_TYPE.DOUGHNUT
        elif variant == "exploded":
            self.chart_type = XL_CHART_TYPE.PIE_EXPLODED
        else:
            self.chart_type = XL_CHART_TYPE.PIE

    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate pie chart data."""
        if not self.categories:
            return False, "No categories provided"

        if not self.values:
            return False, "No values provided"

        if len(self.categories) != len(self.values):
            return (
                False,
                f"Categories ({len(self.categories)}) and values ({len(self.values)}) must have same length",
            )

        # Check for negative values
        if any(v < 0 for v in self.values):
            return False, "Pie chart cannot have negative values"

        # Check if all values are zero
        if sum(self.values) == 0:
            return False, "Pie chart must have at least one non-zero value"

        return True, None

    def _prepare_chart_data(self) -> CategoryChartData:
        """Prepare pie chart data."""
        chart_data = CategoryChartData()
        chart_data.categories = self.categories
        chart_data.add_series("Values", self.values)
        return chart_data

    def render(self, slide, placeholder=None, **kwargs):
        """Render pie chart with theme styling."""
        chart_shape = super().render(slide, placeholder=placeholder, **kwargs)
        chart = chart_shape.chart  # Access the chart object from the shape

        # Get theme colors
        chart_colors = self.tokens.get("chart", [])

        # Apply colors to slices
        if len(chart.series) > 0:
            series = chart.series[0]

            for i, point in enumerate(series.points):
                if i < len(chart_colors):
                    color_hex = chart_colors[i]
                    if isinstance(color_hex, str) and color_hex.startswith("#"):
                        rgb = self.hex_to_rgb(color_hex)
                        fill = point.format.fill
                        fill.solid()
                        fill.fore_color.rgb = RGBColor(*rgb)

                # Explode specific slice if requested
                if self.explode_slice is not None and i == self.explode_slice:
                    point.explosion = 20

        # Configure data labels - minimal to avoid corruption
        try:
            plot = chart.plots[0]
            show_labels = self.variant_props.get("show_labels", True)

            if show_labels:
                plot.has_data_labels = True
        except Exception:
            # Skip data labels if they cause issues
            pass

        return chart_shape


@component(
    name="DoughnutChart",
    category=ComponentCategory.CHART,
    description="Doughnut chart (pie chart with hollow center) for showing proportions",
    props=[
        prop(
            "categories",
            "array",
            "Category labels",
            required=True,
            example=["Category A", "Category B", "Category C"],
        ),
        prop(
            "values", "array", "Data values (must be positive)", required=True, example=[40, 35, 25]
        ),
        prop(
            "style",
            "string",
            "Visual style preset",
            options=["default", "detailed", "minimal"],
            default="default",
            example="default",
        ),
        prop("title", "string", "Chart title", example="Distribution"),
        prop("hole_size", "number", "Size of center hole (0-1)", default=0.5, example=0.5),
    ],
    variants={"style": ["default", "detailed", "minimal"]},
    examples=[
        example(
            "Doughnut chart",
            """
chart = DoughnutChart(
    categories=["Sales", "Marketing", "Operations"],
    values=[50, 30, 20],
    title="Department Allocation"
)
chart.render(slide, left=1, top=2)
            """,
            categories=["Sales", "Marketing", "Operations"],
            values=[50, 30, 20],
        )
    ],
    tags=["chart", "doughnut", "donut", "proportions"],
)
class DoughnutChart(PieChart):
    """
    Doughnut chart component (pie with hollow center).

    Inherits from PieChart but uses doughnut chart type.
    Perfect for showing proportions with a modern look.
    """

    def __init__(self, hole_size: float = 0.5, **kwargs):
        """
        Initialize doughnut chart.

        Args:
            hole_size: Size of center hole (0-1, default 0.5)
            **kwargs: Additional chart parameters
        """
        # Force variant to doughnut
        kwargs["variant"] = "doughnut"
        super().__init__(**kwargs)
        self.hole_size = hole_size

    def render(self, slide, placeholder=None, **kwargs):
        """Render doughnut chart."""
        chart_shape = super().render(slide, placeholder=placeholder, **kwargs)
        chart = chart_shape.chart  # Access the chart object from the shape

        # Set hole size if supported
        if hasattr(chart.plots[0], "doughnut_hole_size"):
            chart.plots[0].doughnut_hole_size = int(self.hole_size * 100)

        return chart_shape
