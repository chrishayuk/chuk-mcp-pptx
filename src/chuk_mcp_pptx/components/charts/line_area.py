"""
Line and Area chart components with beautiful styling.
"""

from typing import Dict, Any, List, Optional, Tuple
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_MARKER_STYLE
from pptx.util import Pt
from pptx.dml.color import RGBColor

from .base import ChartComponent


class LineChart(ChartComponent):
    """
    Line chart component for showing trends over time.
    
    Features:
    - Smooth or straight lines
    - Data markers
    - Multiple series
    - Gradient fills (area under line)
    """
    
    def __init__(self,
                 categories: List[str],
                 series: Dict[str, List[float]],
                 smooth: bool = True,
                 markers: bool = True,
                 variant: str = "default",
                 **kwargs):
        """
        Initialize line chart.
        
        Args:
            categories: Category labels (x-axis)
            series: Dictionary of series names to values
            smooth: Whether to smooth lines
            markers: Whether to show data point markers
            variant: Chart variant (default, markers, stacked)
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.series = series
        self.smooth = smooth
        self.markers = markers
        self.variant = variant
        
        # Set chart type based on options
        if variant == "stacked":
            self.chart_type = XL_CHART_TYPE.LINE_STACKED
        elif markers:
            self.chart_type = XL_CHART_TYPE.LINE_MARKERS
        else:
            self.chart_type = XL_CHART_TYPE.LINE
    
    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate line chart data."""
        if not self.categories:
            return False, "No categories provided"
        
        if not self.series:
            return False, "No data series provided"
        
        expected_length = len(self.categories)
        for name, values in self.series.items():
            if len(values) != expected_length:
                return False, f"Series '{name}' has {len(values)} values, expected {expected_length}"
        
        return True, None
    
    def _prepare_chart_data(self) -> CategoryChartData:
        """Prepare line chart data."""
        chart_data = CategoryChartData()
        chart_data.categories = self.categories
        
        for series_name, values in self.series.items():
            chart_data.add_series(series_name, values)
        
        return chart_data
    
    def _render_sync(self, slide, **kwargs):
        """Render line chart with beautiful styling."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Get theme colors
        chart_colors = self.tokens.get("chart", [])
        
        # Style each series
        for idx, series in enumerate(chart.series):
            # Smooth lines if requested
            if hasattr(series, 'smooth'):
                series.smooth = self.smooth
            
            # Configure line style
            line = series.format.line
            line.width = Pt(2.5)  # Thicker lines for visibility
            
            # Apply color with gradient effect
            if idx < len(chart_colors):
                color_hex = chart_colors[idx]
                if isinstance(color_hex, str):
                    rgb = self.hex_to_rgb(color_hex)
                    line.color.rgb = RGBColor(*rgb)
            
            # Configure markers
            if self.markers and hasattr(series, 'marker'):
                series.marker.style = XL_MARKER_STYLE.CIRCLE
                series.marker.size = 8
                
                # Marker fill matches line color
                if idx < len(chart_colors):
                    fill = series.marker.format.fill
                    fill.solid()
                    fill.fore_color.rgb = RGBColor(*rgb)
                    
                    # White border on markers
                    marker_line = series.marker.format.line
                    marker_line.color.rgb = RGBColor(255, 255, 255)
                    marker_line.width = Pt(1)
        
        # Add data labels if requested
        if self.options.get("show_values", False):
            plot = chart.plots[0]
            plot.has_data_labels = True
            data_labels = plot.data_labels
            data_labels.font.size = Pt(9)
            data_labels.font.color.rgb = self.get_color("muted.foreground")
            data_labels.number_format = '0'
        
        # Configure grid lines for cleaner look
        if hasattr(chart, 'value_axis'):
            value_axis = chart.value_axis
            value_axis.has_major_gridlines = True
            gridlines = value_axis.major_gridlines.format.line
            gridlines.color.rgb = self.get_color("border.secondary")
            gridlines.width = Pt(0.5)
            # gridlines.dash_style = "dash"  # Simplified dash style
        
        return chart


class AreaChart(ChartComponent):
    """
    Area chart component for showing magnitude over time.
    
    Features:
    - Semi-transparent fills
    - Stacked variants
    - Gradient effects
    """
    
    def __init__(self,
                 categories: List[str],
                 series: Dict[str, List[float]],
                 variant: str = "default",
                 transparency: int = 30,
                 **kwargs):
        """
        Initialize area chart.
        
        Args:
            categories: Category labels
            series: Dictionary of series names to values
            variant: Chart variant (default, stacked, stacked100)
            transparency: Fill transparency (0-100)
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.series = series
        self.variant = variant
        self.transparency = max(0, min(100, transparency))
        
        # Set chart type based on variant
        variant_map = {
            "default": XL_CHART_TYPE.AREA,
            "stacked": XL_CHART_TYPE.AREA_STACKED,
            "stacked100": XL_CHART_TYPE.AREA_STACKED_100,
            "3d": XL_CHART_TYPE.AREA,  # Fallback to regular area
        }
        self.chart_type = variant_map.get(variant, XL_CHART_TYPE.AREA)
    
    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate area chart data."""
        if not self.categories:
            return False, "No categories provided"
        
        if not self.series:
            return False, "No data series provided"
        
        expected_length = len(self.categories)
        for name, values in self.series.items():
            if len(values) != expected_length:
                return False, f"Series '{name}' has {len(values)} values, expected {expected_length}"
        
        return True, None
    
    def _prepare_chart_data(self) -> CategoryChartData:
        """Prepare area chart data."""
        chart_data = CategoryChartData()
        chart_data.categories = self.categories
        
        for series_name, values in self.series.items():
            chart_data.add_series(series_name, values)
        
        return chart_data
    
    def _render_sync(self, slide, **kwargs):
        """Render area chart with beautiful styling."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Get theme colors
        chart_colors = self.tokens.get("chart", [])
        
        # Style each series with semi-transparent fills
        for idx, series in enumerate(chart.series):
            if idx < len(chart_colors):
                color_hex = chart_colors[idx]
                if isinstance(color_hex, str):
                    rgb = self.hex_to_rgb(color_hex)
                    
                    # Apply fill color
                    fill = series.format.fill
                    fill.solid()
                    fill.fore_color.rgb = RGBColor(*rgb)
                    
                    # Set transparency for modern look
                    if hasattr(fill, 'transparency'):
                        fill.transparency = self.transparency / 100.0
                    
                    # Style the line
                    line = series.format.line
                    line.color.rgb = RGBColor(*rgb)
                    line.width = Pt(2)
        
        # Clean gridlines
        if hasattr(chart, 'value_axis'):
            value_axis = chart.value_axis
            value_axis.has_major_gridlines = True
            gridlines = value_axis.major_gridlines.format.line
            gridlines.color.rgb = self.get_color("border.secondary")
            gridlines.width = Pt(0.5)
            # gridlines.dash_style = "dash"  # Simplified dash style
        
        return chart


class SparklineChart(LineChart):
    """
    Sparkline chart - minimal line chart for inline data visualization.
    
    Features:
    - No axes or labels
    - Minimal styling
    - Small size optimized
    """
    
    def __init__(self,
                 values: List[float],
                 color: Optional[str] = None,
                 **kwargs):
        """
        Initialize sparkline chart.
        
        Args:
            values: Data values
            color: Line color (hex)
            **kwargs: Additional parameters
        """
        # Create minimal categories
        categories = list(range(len(values)))
        series = {"": values}  # Single unnamed series
        
        super().__init__(
            categories=categories,
            series=series,
            smooth=True,
            markers=False,
            **kwargs
        )
        self.color = color
        
        # Override defaults for sparklines
        self.DEFAULT_WIDTH = 2.0
        self.DEFAULT_HEIGHT = 0.5
    
    def _render_sync(self, slide, **kwargs):
        """Render minimal sparkline."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Remove all chrome
        chart.has_title = False
        chart.has_legend = False
        
        # Hide axes
        if hasattr(chart, 'value_axis'):
            chart.value_axis.visible = False
        if hasattr(chart, 'category_axis'):
            chart.category_axis.visible = False
        
        # Remove gridlines
        if hasattr(chart, 'value_axis'):
            chart.value_axis.has_major_gridlines = False
            chart.value_axis.has_minor_gridlines = False
        
        # Apply custom color if provided
        if self.color and len(chart.series) > 0:
            series = chart.series[0]
            line = series.format.line
            
            if self.color.startswith('#'):
                rgb = self.hex_to_rgb(self.color)
                line.color.rgb = RGBColor(*rgb)
            
            line.width = Pt(1.5)
        
        return chart