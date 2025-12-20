"""
Base chart component with validation, theming, and composition support.
"""

from typing import Dict, Any, Optional, Tuple, Union
from pptx.chart.data import CategoryChartData, XyChartData, BubbleChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches
from pptx.dml.color import RGBColor

from ..composition import ComposableComponent
from ..variants import CHART_VARIANTS
from ...layout.helpers import (
    validate_position,
)
from ...utilities.chart_utils import (
    configure_legend,
    configure_axes,
    set_chart_title,
    apply_chart_colors,
)


class ChartComponent(ComposableComponent):
    """
    Base chart component with theming, validation, and composition support.

    Features:
    - Data validation
    - Layout integration
    - Theme integration
    - Variant system support
    - Error handling
    - Composition support
    - Smart aspect ratio handling for square charts (pie/doughnut)

    Usage:
        # Extend this class for specific chart types
        class ColumnChart(ChartComponent):
            def __init__(self, categories, series, variant="clustered", **kwargs):
                super().__init__(**kwargs)
                self.categories = categories
                self.series = series
                self.variant = variant
                self.variant_props = COLUMN_CHART_VARIANTS.build(
                    variant=variant,
                    style=kwargs.get("style", "default")
                )
    """

    # Default chart dimensions
    # Note: DEFAULT_TOP=2.0 leaves 1.0" for title, and with SLIDE_HEIGHT=5.625 and MARGIN_BOTTOM=0.5,
    # the available height is 5.625 - 2.0 - 0.5 = 3.125 inches
    DEFAULT_WIDTH = 8.0
    DEFAULT_HEIGHT = 3.0  # Fits comfortably below title area
    DEFAULT_LEFT = 1.0
    DEFAULT_TOP = 2.0

    # Chart types that prefer square aspect ratio (pie, doughnut)
    SQUARE_CHART_TYPES = {
        XL_CHART_TYPE.PIE,
        XL_CHART_TYPE.PIE_EXPLODED,
        XL_CHART_TYPE.DOUGHNUT,
        XL_CHART_TYPE.DOUGHNUT_EXPLODED,
    }

    def __init__(
        self,
        title: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        theme: Optional[Dict[str, Any]] = None,
        style: str = "default",
        legend: str = "right",
    ):
        """
        Initialize chart component.

        Args:
            title: Chart title
            data: Chart data
            theme: Theme configuration
            style: Chart style variant (default, minimal, detailed)
            legend: Legend position (right, bottom, top, none)
        """
        super().__init__(theme)
        self.title = title
        self.data = data
        self.style = style
        self.legend = legend
        self.chart_type = XL_CHART_TYPE.COLUMN_CLUSTERED

        # Get variant props
        self.variant_props = CHART_VARIANTS.build(style=style, legend=legend)

    def validate(self) -> Tuple[bool, Optional[str]]:
        """
        Public validation method for complete chart configuration.
        Validates data, options, and other settings.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # First validate data
        valid, error = self.validate_data()
        if not valid:
            return False, error

        # Could add more validation here (options, theme, etc.)
        return True, None

    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """
        Internal method to validate chart data specifically.
        Override in subclasses for specific data validation.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Base implementation - subclasses should override
        return True, None

    def apply_theme_colors(self, chart):
        """
        Apply theme colors to chart.

        Args:
            chart: PowerPoint chart object
        """
        # Get theme chart colors
        chart_colors = self.tokens.get("chart", [])

        # Convert hex colors to RGBColor objects
        rgb_colors = []
        for color_hex in chart_colors:
            if isinstance(color_hex, str):
                rgb = self.hex_to_rgb(color_hex)
                rgb_colors.append(RGBColor(*rgb))

        # Apply using utility function
        if rgb_colors:
            apply_chart_colors(chart, rgb_colors)

    def _get_font_family(self) -> str:
        """Get font family from theme."""
        return self.get_theme_attr("font_family", "Inter")

    def _prepare_chart_data(self) -> Union[CategoryChartData, XyChartData, BubbleChartData]:
        """
        Prepare chart data (override in subclasses).

        Returns:
            Chart data object
        """
        raise NotImplementedError("Subclasses must implement _prepare_chart_data")

    def _optimize_bounds_for_square_chart(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
    ) -> Tuple[float, float, float, float]:
        """
        Optimize bounds for square charts (pie/doughnut).

        Note: Pie chart sizing is now handled via XML plot area manipulation
        in the PieChart class, so we don't need to constrain bounds here.

        Args:
            left: Original left position in inches
            top: Original top position in inches
            width: Available width in inches
            height: Available height in inches

        Returns:
            Original bounds unchanged
        """
        # Pie/doughnut chart sizing is handled via _expand_plot_area() in PieChart
        return left, top, width, height

    def render(
        self,
        slide,
        left: Optional[float] = None,
        top: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        placeholder: Optional[Any] = None,
    ) -> Any:
        """
        Render chart to slide or replace a placeholder.

        Args:
            slide: PowerPoint slide
            left: Left position in inches
            top: Top position in inches
            width: Chart width in inches
            height: Chart height in inches
            placeholder: Optional placeholder shape to replace

        Returns:
            Chart object
        """
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds
            import logging

            logger = logging.getLogger(__name__)
            logger.info(
                f"Chart targeting placeholder - using bounds: ({left:.2f}, {top:.2f}, {width:.2f}, {height:.2f})"
            )

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        # Use defaults if not provided
        left = left if left is not None else self.DEFAULT_LEFT
        top = top if top is not None else self.DEFAULT_TOP
        width = width if width is not None else self.DEFAULT_WIDTH
        height = height if height is not None else self.DEFAULT_HEIGHT

        # Optimize bounds for square charts (pie/doughnut)
        left, top, width, height = self._optimize_bounds_for_square_chart(left, top, width, height)

        # Validate data
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Chart data validation failed: {error}")

        # Validate and adjust position using layout helpers
        left, top, width, height = validate_position(left, top, width, height)

        # Prepare data
        chart_data = self._prepare_chart_data()

        # Add chart to slide
        chart_shape = slide.shapes.add_chart(
            self.chart_type, Inches(left), Inches(top), Inches(width), Inches(height), chart_data
        )

        chart = chart_shape.chart

        # Apply styling using utilities
        font_family = self._get_font_family()

        # Set title
        if self.title:
            set_chart_title(
                chart,
                self.title,
                font_family=font_family,
                font_color=self.get_color("foreground.DEFAULT"),
            )

        # Apply theme colors
        self.apply_theme_colors(chart)

        # Configure legend from variant props
        configure_legend(
            chart,
            position=self.variant_props.get("legend_position", "right"),
            show=self.variant_props.get("show_legend", True),
            font_family=font_family,
        )

        # Configure axes from variant props
        configure_axes(
            chart,
            gridline_color=self.get_color("border.secondary"),
            label_font_family=font_family,
            label_color=self.get_color("muted.foreground"),
        )

        # Return chart_shape (not chart) so position attributes are accessible
        return chart_shape
