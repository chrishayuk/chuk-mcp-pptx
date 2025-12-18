"""
Scatter plot and Bubble chart components for correlation analysis.
"""

from typing import Dict, Any, List, Optional, Tuple, Union
from pptx.chart.data import XyChartData, BubbleChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_MARKER_STYLE
from pptx.util import Pt
from pptx.dml.color import RGBColor

from .base import ChartComponent


class ScatterChart(ChartComponent):
    """
    Scatter plot component for showing correlations between variables.

    Features:
    - Multiple data series
    - Custom marker styles
    - Trend lines
    - Outlier highlighting
    """

    def __init__(
        self,
        series_data: List[Dict[str, Any]],
        show_trendline: bool = False,
        marker_size: int = 8,
        variant: str = "default",
        **kwargs,
    ):
        """
        Initialize scatter chart.

        Args:
            series_data: List of series with x_values, y_values, and optional name
            show_trendline: Whether to show trend lines
            marker_size: Size of data point markers
            variant: Chart variant (default, smooth, smooth_markers)
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.series_data = series_data
        self.show_trendline = show_trendline
        self.marker_size = marker_size
        self.variant = variant

        # Validate data during initialization
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")

        # Set chart type based on variant
        variant_map = {
            "default": XL_CHART_TYPE.XY_SCATTER,
            "smooth": XL_CHART_TYPE.XY_SCATTER_SMOOTH,
            "smooth_markers": XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS,
            "lines": XL_CHART_TYPE.XY_SCATTER_LINES,
            "lines_markers": XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS,
        }
        self.chart_type = variant_map.get(variant, XL_CHART_TYPE.XY_SCATTER)

    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate scatter chart data."""
        if not self.series_data:
            return False, "No series data provided"

        for i, series in enumerate(self.series_data):
            if "x_values" not in series:
                return False, f"Series {i} missing x_values"

            if "y_values" not in series:
                return False, f"Series {i} missing y_values"

            x_values = series["x_values"]
            y_values = series["y_values"]

            if len(x_values) != len(y_values):
                return (
                    False,
                    f"Series {i}: x_values ({len(x_values)}) and y_values ({len(y_values)}) must have same length",
                )

            if len(x_values) == 0:
                return False, f"Series {i} has no data points"

        return True, None

    def _prepare_chart_data(self) -> XyChartData:
        """Prepare scatter chart data."""
        chart_data = XyChartData()

        for series in self.series_data:
            series_name = series.get("name", "Series")
            x_values = series["x_values"]
            y_values = series["y_values"]

            series_obj = chart_data.add_series(series_name)

            for x, y in zip(x_values, y_values):
                series_obj.add_data_point(x, y)

        return chart_data

    def render(self, slide, placeholder=None, **kwargs):
        """Render scatter chart with beautiful styling."""
        # Call base render to create chart
        chart_shape = super().render(slide, placeholder=placeholder, **kwargs)
        chart = chart_shape.chart  # Access the chart object from the shape

        # Get theme colors
        chart_colors = self.tokens.get("chart", [])

        # Style each series
        for idx, series in enumerate(chart.series):
            # Configure markers
            if hasattr(series, "marker"):
                series.marker.style = XL_MARKER_STYLE.CIRCLE
                series.marker.size = self.marker_size

                # Apply color
                if idx < len(chart_colors):
                    color_hex = chart_colors[idx]
                    if isinstance(color_hex, str):
                        rgb = self.hex_to_rgb(color_hex)

                        # Marker fill
                        fill = series.marker.format.fill
                        fill.solid()
                        fill.fore_color.rgb = RGBColor(*rgb)

                        # Marker border
                        line = series.marker.format.line
                        line.color.rgb = RGBColor(255, 255, 255)
                        line.width = Pt(1)

            # Configure lines if present
            if hasattr(series, "format") and hasattr(series.format, "line"):
                line = series.format.line
                if idx < len(chart_colors):
                    color_hex = chart_colors[idx]
                    if isinstance(color_hex, str):
                        rgb = self.hex_to_rgb(color_hex)
                        line.color.rgb = RGBColor(*rgb)
                        line.width = Pt(2)

        # Add trend lines if requested
        if self.show_trendline:
            for series in chart.series:
                if hasattr(series, "trendlines"):
                    # Note: PowerPoint trendline support varies
                    # This is a placeholder for trendline functionality
                    pass

        # Configure axes
        if hasattr(chart, "value_axis"):
            # Y-axis
            value_axis = chart.value_axis
            value_axis.has_major_gridlines = True

        if hasattr(chart, "category_axis"):
            # X-axis (for scatter, this is also a value axis)
            cat_axis = chart.category_axis
            cat_axis.has_major_gridlines = True

        return chart_shape


class BubbleChart(ChartComponent):
    """
    Bubble chart component for 3D data visualization.

    Features:
    - Variable bubble sizes
    - Custom colors per bubble
    - Size scaling
    - Transparent bubbles
    """

    def __init__(
        self,
        series_data: List[Dict[str, Any]],
        size_scale: float = 1.0,
        transparency: int = 20,
        **kwargs,
    ):
        """
        Initialize bubble chart.

        Args:
            series_data: List of series with name and points [[x, y, size], ...]
            size_scale: Scale factor for bubble sizes
            transparency: Bubble transparency (0-100)
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.series_data = series_data
        self.size_scale = size_scale
        self.transparency = max(0, min(100, transparency))
        self.chart_type = XL_CHART_TYPE.BUBBLE

        # Validate data during initialization
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")

    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate bubble chart data."""
        if not self.series_data:
            return False, "No series data provided"

        for i, series in enumerate(self.series_data):
            if "points" not in series:
                return False, f"Series {i} missing points data"

            points = series["points"]
            if not points:
                return False, f"Series {i} has no data points"

            for j, point in enumerate(points):
                if not isinstance(point, (list, tuple)) or len(point) != 3:
                    return False, f"Series {i}, point {j}: must be [x, y, size] format"

                x, y, size = point
                if (
                    not isinstance(x, (int, float))
                    or not isinstance(y, (int, float))
                    or not isinstance(size, (int, float))
                ):
                    return False, f"Series {i}, point {j}: x, y, size must be numeric"

                if size <= 0:
                    return False, f"Series {i}, point {j}: size must be positive"

        return True, None

    def _prepare_chart_data(self) -> BubbleChartData:
        """Prepare bubble chart data."""
        chart_data = BubbleChartData()

        for series in self.series_data:
            series_name = series.get("name", "Series")
            points = series["points"]

            series_obj = chart_data.add_series(series_name)

            for point in points:
                x, y, size = point
                # Apply size scaling
                scaled_size = size * self.size_scale
                series_obj.add_data_point(x, y, scaled_size)

        return chart_data

    def render(self, slide, placeholder=None, **kwargs):
        """Render bubble chart with beautiful styling."""
        # Call base render to create chart
        chart_shape = super().render(slide, placeholder=placeholder, **kwargs)
        chart = chart_shape.chart  # Access the chart object from the shape

        # Get theme colors
        chart_colors = self.tokens.get("chart", [])

        # Style each series
        for idx, series in enumerate(chart.series):
            if idx < len(chart_colors):
                color_hex = chart_colors[idx]
                if isinstance(color_hex, str):
                    rgb = self.hex_to_rgb(color_hex)

                    # Apply fill color to bubbles
                    fill = series.format.fill
                    fill.solid()
                    fill.fore_color.rgb = RGBColor(*rgb)

                    # Set transparency for modern look
                    if hasattr(fill, "transparency"):
                        fill.transparency = self.transparency / 100.0

                    # Subtle border
                    line = series.format.line
                    line.color.rgb = RGBColor(*rgb)
                    line.width = Pt(1)

        # Configure axes with appropriate scaling
        if hasattr(chart, "value_axis"):
            value_axis = chart.value_axis
            value_axis.has_major_gridlines = True

        return chart_shape


class Matrix3DChart(BubbleChart):
    """
    3D Matrix chart for multi-dimensional data visualization.

    Uses bubble chart with size and color encoding for 4+ dimensions.
    """

    def __init__(
        self,
        data_points: List[Dict[str, Union[float, str]]],
        x_field: str,
        y_field: str,
        size_field: str,
        color_field: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize matrix 3D chart.

        Args:
            data_points: List of data records
            x_field: Field name for x-axis
            y_field: Field name for y-axis
            size_field: Field name for bubble size
            color_field: Field name for color grouping
            **kwargs: Additional chart parameters
        """
        self.data_points = data_points
        self.x_field = x_field
        self.y_field = y_field
        self.size_field = size_field
        self.color_field = color_field

        # Convert to bubble chart format
        series_data = self._convert_to_series()

        # Initialize BubbleChart with converted data
        super().__init__(series_data=series_data, **kwargs)

    def _convert_to_series(self) -> List[Dict[str, Any]]:
        """Convert matrix data to series format."""
        if self.color_field:
            # Group by color field
            groups = {}
            for point in self.data_points:
                group_key = point.get(self.color_field, "Unknown")
                if group_key not in groups:
                    groups[group_key] = []

                x = point.get(self.x_field, 0)
                y = point.get(self.y_field, 0)
                size = point.get(self.size_field, 1)
                groups[group_key].append([x, y, size])

            # Convert to series format
            series_data = []
            for group_name, points in groups.items():
                series_data.append({"name": str(group_name), "points": points})
        else:
            # Single series
            points = []
            for point in self.data_points:
                x = point.get(self.x_field, 0)
                y = point.get(self.y_field, 0)
                size = point.get(self.size_field, 1)
                points.append([x, y, size])

            series_data = [{"name": "Data", "points": points}]

        return series_data
