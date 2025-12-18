"""
Column and Bar chart components with variants and registry integration.
"""

from typing import Dict, List, Optional, Tuple
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION
from pptx.util import Pt
from pptx.dml.color import RGBColor

from .base import ChartComponent
from ..variants import COLUMN_CHART_VARIANTS
from ..registry import component, ComponentCategory, prop, example


@component(
    name="ColumnChart",
    category=ComponentCategory.CHART,
    description="Column chart component for vertical bar comparisons with multiple variants",
    props=[
        prop(
            "categories",
            "array",
            "Category labels for x-axis",
            required=True,
            example=["Q1", "Q2", "Q3", "Q4"],
        ),
        prop(
            "series",
            "object",
            "Dictionary of series names to values",
            required=True,
            example={"Revenue": [100, 120, 130, 150], "Costs": [80, 90, 85, 95]},
        ),
        prop(
            "variant",
            "string",
            "Chart variant style",
            options=["clustered", "stacked", "stacked100", "3d"],
            default="clustered",
            example="clustered",
        ),
        prop(
            "style",
            "string",
            "Visual style preset",
            options=["default", "minimal", "detailed"],
            default="default",
            example="default",
        ),
        prop("title", "string", "Chart title", example="Quarterly Revenue"),
        prop(
            "legend",
            "string",
            "Legend position",
            options=["right", "bottom", "top", "none"],
            default="right",
            example="right",
        ),
        prop("left", "number", "Left position in inches", example=1.0),
        prop("top", "number", "Top position in inches", example=2.0),
        prop("width", "number", "Width in inches", example=8.0),
        prop("height", "number", "Height in inches", example=4.5),
    ],
    variants={
        "variant": ["clustered", "stacked", "stacked100", "3d"],
        "style": ["default", "minimal", "detailed"],
        "legend": ["right", "bottom", "top", "none"],
    },
    examples=[
        example(
            "Clustered column chart",
            """
chart = ColumnChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    series={"Revenue": [100, 120, 130, 150], "Costs": [80, 90, 85, 95]},
    title="Quarterly Performance",
    variant="clustered"
)
chart.render(slide, left=1, top=2)
            """,
            categories=["Q1", "Q2", "Q3", "Q4"],
            series={"Revenue": [100, 120, 130, 150]},
            variant="clustered",
        ),
        example(
            "Stacked column chart",
            """
chart = ColumnChart(
    categories=["Jan", "Feb", "Mar"],
    series={"Product A": [50, 60, 70], "Product B": [30, 40, 50]},
    title="Sales by Product",
    variant="stacked",
    style="detailed"
)
chart.render(slide)
            """,
            categories=["Jan", "Feb", "Mar"],
            series={"Product A": [50, 60, 70], "Product B": [30, 40, 50]},
            variant="stacked",
            style="detailed",
        ),
    ],
    tags=["chart", "column", "bar", "data", "visualization"],
)
class ColumnChart(ChartComponent):
    """
    Column chart component for vertical bar comparisons.

    Features:
    - Multiple variants (clustered, stacked, stacked100, 3d)
    - Theme-aware styling
    - Data validation
    - Customizable legend and styling

    Variants:
    - clustered: Side-by-side columns for each category
    - stacked: Stacked columns showing total with breakdown
    - stacked100: Percentage-based stacked columns
    - 3d: Three-dimensional column chart

    Styles:
    - default: Standard appearance with legend
    - minimal: Clean look without grid or values
    - detailed: Shows values on columns with full grid
    """

    def __init__(
        self,
        categories: List[str],
        series: Dict[str, List[float]],
        variant: str = "clustered",
        style: str = "default",
        **kwargs,
    ):
        """
        Initialize column chart.

        Args:
            categories: Category labels
            series: Dictionary of series names to values
            variant: Chart variant (clustered, stacked, stacked100, 3d)
            style: Visual style (default, minimal, detailed)
            **kwargs: Additional chart parameters (title, theme, legend, etc.)
        """
        super().__init__(style=style, **kwargs)
        self.categories = categories
        self.series = series
        self.variant = variant

        # Validate data during initialization
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")

        # Update variant props to include column-specific variants
        self.variant_props = COLUMN_CHART_VARIANTS.build(variant=variant, style=style)

        # Set chart type based on variant
        variant_map = {
            "clustered": XL_CHART_TYPE.COLUMN_CLUSTERED,
            "stacked": XL_CHART_TYPE.COLUMN_STACKED,
            "stacked100": XL_CHART_TYPE.COLUMN_STACKED_100,
            "3d": XL_CHART_TYPE.THREE_D_COLUMN,
        }
        self.chart_type = variant_map.get(variant, XL_CHART_TYPE.COLUMN_CLUSTERED)

    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate column chart data."""
        if not self.categories:
            return False, "No categories provided"

        if not self.series:
            return False, "No data series provided"

        # Check all series have same length as categories
        expected_length = len(self.categories)
        for name, values in self.series.items():
            if len(values) != expected_length:
                return (
                    False,
                    f"Series '{name}' has {len(values)} values, expected {expected_length}",
                )

        return True, None

    def _prepare_chart_data(self) -> CategoryChartData:
        """Prepare column chart data."""
        chart_data = CategoryChartData()
        chart_data.categories = self.categories

        for series_name, values in self.series.items():
            chart_data.add_series(series_name, values)

        return chart_data

    def render(self, slide, placeholder=None, **kwargs):
        """Render column chart with additional configuration."""
        chart_shape = super().render(slide, placeholder=placeholder, **kwargs)
        chart = chart_shape.chart  # Access the chart object from the shape

        # Add data labels if requested
        if self.variant_props.get("show_values", False):
            plot = chart.plots[0]
            plot.has_data_labels = True
            data_labels = plot.data_labels

            # Position labels based on variant
            if "stacked" in self.variant:
                data_labels.position = XL_DATA_LABEL_POSITION.CENTER
            else:
                data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END

            data_labels.font.size = Pt(9)
            data_labels.font.color.rgb = self.get_color("muted.foreground")

        # Configure gap width
        if hasattr(chart.plots[0], "gap_width"):
            chart.plots[0].gap_width = self.variant_props.get("gap_width", 150)

        # Configure overlap for stacked charts
        if "stacked" in self.variant and hasattr(chart.plots[0], "overlap"):
            chart.plots[0].overlap = self.variant_props.get("overlap", 100)

        return chart_shape


@component(
    name="BarChart",
    category=ComponentCategory.CHART,
    description="Bar chart component for horizontal bar comparisons",
    props=[
        prop(
            "categories",
            "array",
            "Category labels for y-axis",
            required=True,
            example=["Product A", "Product B", "Product C"],
        ),
        prop(
            "series",
            "object",
            "Dictionary of series names to values",
            required=True,
            example={"Sales": [100, 120, 90]},
        ),
        prop(
            "variant",
            "string",
            "Chart variant style",
            options=["clustered", "stacked", "stacked100", "3d"],
            default="clustered",
            example="clustered",
        ),
        prop(
            "style",
            "string",
            "Visual style preset",
            options=["default", "minimal", "detailed"],
            default="default",
            example="default",
        ),
        prop("title", "string", "Chart title", example="Product Sales"),
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
        "variant": ["clustered", "stacked", "stacked100", "3d"],
        "style": ["default", "minimal", "detailed"],
    },
    examples=[
        example(
            "Horizontal bar chart",
            """
chart = BarChart(
    categories=["Product A", "Product B", "Product C"],
    series={"Q1": [100, 120, 90], "Q2": [110, 130, 95]},
    title="Product Performance",
    variant="clustered"
)
chart.render(slide, left=1, top=2)
            """,
            categories=["Product A", "Product B", "Product C"],
            series={"Q1": [100, 120, 90]},
            variant="clustered",
        )
    ],
    tags=["chart", "bar", "horizontal", "data", "visualization"],
)
class BarChart(ColumnChart):
    """
    Bar chart component for horizontal bar comparisons.

    Inherits from ColumnChart but uses horizontal orientation.
    Perfect for comparing items, especially when category labels are long.
    """

    def __init__(self, variant: str = "clustered", **kwargs):
        """
        Initialize bar chart.

        Args:
            variant: Chart variant (clustered, stacked, stacked100, 3d)
            **kwargs: Additional chart parameters
        """
        super().__init__(variant=variant, **kwargs)

        # Override with bar chart types
        variant_map = {
            "clustered": XL_CHART_TYPE.BAR_CLUSTERED,
            "stacked": XL_CHART_TYPE.BAR_STACKED,
            "stacked100": XL_CHART_TYPE.BAR_STACKED_100,
            "3d": XL_CHART_TYPE.THREE_D_BAR_CLUSTERED,
        }
        self.chart_type = variant_map.get(variant, XL_CHART_TYPE.BAR_CLUSTERED)


@component(
    name="WaterfallChart",
    category=ComponentCategory.CHART,
    description="Waterfall chart for showing incremental changes and cumulative effects",
    props=[
        prop(
            "categories",
            "array",
            "Category labels",
            required=True,
            example=["Start", "Q1", "Q2", "Q3", "Q4", "End"],
        ),
        prop(
            "values",
            "array",
            "Values showing changes (positive/negative)",
            required=True,
            example=[100, 20, -10, 15, -5, 120],
        ),
        prop("title", "string", "Chart title", example="Waterfall Analysis"),
        prop("show_connectors", "boolean", "Show connector lines", default=False),
    ],
    examples=[
        example(
            "Waterfall chart showing profit changes",
            """
chart = WaterfallChart(
    categories=["Start", "Q1 Sales", "Q2 Sales", "Q3 Costs", "End"],
    values=[100, 50, 30, -20, 160],
    title="Profit Waterfall"
)
chart.render(slide)
            """,
            categories=["Start", "Q1", "Q2", "End"],
            values=[100, 50, 30, 180],
        )
    ],
    tags=["chart", "waterfall", "cumulative", "data", "visualization"],
)
class WaterfallChart(ChartComponent):
    """
    Waterfall chart for showing incremental changes.

    Note: PowerPoint doesn't have native waterfall support,
    so this uses a stacked column chart with formatting tricks.

    Features:
    - Shows cumulative effect of sequential values
    - Automatically colors positive (success) and negative (destructive) changes
    - Displays data labels for each segment
    """

    def __init__(
        self, categories: List[str], values: List[float], show_connectors: bool = False, **kwargs
    ):
        """
        Initialize waterfall chart.

        Args:
            categories: Category labels (e.g., ["Start", "Q1", "Q2", "End"])
            values: Values showing changes (positive/negative)
            show_connectors: Whether to show connector lines
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.values = values
        self.show_connectors = show_connectors
        self.chart_type = XL_CHART_TYPE.COLUMN_STACKED

        # Validate data during initialization
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")

    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate waterfall data."""
        if not self.categories:
            return False, "No categories provided"

        if not self.values:
            return False, "No values provided"

        if len(self.categories) != len(self.values):
            return (
                False,
                f"Categories ({len(self.categories)}) and values ({len(self.values)}) must have same length",
            )

        return True, None

    def _prepare_chart_data(self) -> CategoryChartData:
        """
        Prepare waterfall chart data using stacked column approach.

        Creates invisible base series and visible value series.
        """
        chart_data = CategoryChartData()
        chart_data.categories = self.categories

        # Calculate cumulative values and bases
        bases = []
        values = []
        cumulative = 0

        for i, val in enumerate(self.values):
            if i == 0:
                # First bar starts at 0
                bases.append(0)
                values.append(val)
                cumulative = val
            else:
                if val >= 0:
                    # Positive value
                    bases.append(cumulative)
                    values.append(val)
                    cumulative += val
                else:
                    # Negative value
                    bases.append(cumulative + val)
                    values.append(-val)
                    cumulative += val

        # Add series for waterfall effect
        chart_data.add_series("Base", bases)  # Will be made invisible
        chart_data.add_series("Values", values)

        return chart_data

    def render(self, slide, placeholder=None, **kwargs):
        """Render waterfall chart with special formatting."""
        chart_shape = super().render(slide, placeholder=placeholder, **kwargs)
        chart = chart_shape.chart  # Access the chart object from the shape

        try:
            # Make base series invisible
            if len(chart.series) >= 2:
                base_series = chart.series[0]
                fill = base_series.format.fill
                fill.background()  # Make transparent

            # Color positive and negative values differently
            if len(chart.series) >= 2:
                value_series = chart.series[1]

                # Apply colors based on positive/negative
                for i, val in enumerate(self.values):
                    if i < len(value_series.points):
                        point = value_series.points[i]
                        fill = point.format.fill
                        fill.solid()

                        if val >= 0:
                            # Positive - green
                            fill.fore_color.rgb = RGBColor(16, 185, 129)
                        else:
                            # Negative - red
                            fill.fore_color.rgb = RGBColor(239, 68, 68)

            # Set gap width to 0 for connected appearance
            if hasattr(chart.plots[0], "gap_width"):
                chart.plots[0].gap_width = 0

        except Exception:
            # If any formatting fails, return the basic chart
            pass

        return chart_shape
