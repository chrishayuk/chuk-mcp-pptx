"""
Column and Bar chart components.
"""

from typing import Dict, Any, List, Optional, Tuple
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION
from pptx.util import Pt

from .base import ChartComponent


class ColumnChart(ChartComponent):
    """
    Column chart component for vertical bar comparisons.
    
    Variants:
    - Regular (clustered)
    - Stacked
    - 100% Stacked
    - 3D
    """
    
    def __init__(self,
                 categories: List[str],
                 series: Dict[str, List[float]],
                 variant: str = "clustered",
                 **kwargs):
        """
        Initialize column chart.
        
        Args:
            categories: Category labels
            series: Dictionary of series names to values
            variant: Chart variant (clustered, stacked, stacked100, 3d)
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.series = series
        self.variant = variant
        
        # Set chart type based on variant
        variant_map = {
            "clustered": XL_CHART_TYPE.COLUMN_CLUSTERED,
            "stacked": XL_CHART_TYPE.COLUMN_STACKED,
            "stacked100": XL_CHART_TYPE.COLUMN_STACKED_100,
            "3d": XL_CHART_TYPE.COLUMN_CLUSTERED,  # Fallback to regular clustered
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
                return False, f"Series '{name}' has {len(values)} values, expected {expected_length}"
        
        return True, None
    
    def _prepare_chart_data(self) -> CategoryChartData:
        """Prepare column chart data."""
        chart_data = CategoryChartData()
        chart_data.categories = self.categories
        
        for series_name, values in self.series.items():
            chart_data.add_series(series_name, values)
        
        return chart_data
    
    def _render_sync(self, slide, **kwargs):
        """Render column chart with additional configuration."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Add data labels if requested
        if self.options.get("show_values", False):
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
        if hasattr(chart.plots[0], 'gap_width'):
            chart.plots[0].gap_width = self.options.get("gap_width", 150)
        
        # Configure overlap for stacked charts
        if "stacked" in self.variant and hasattr(chart.plots[0], 'overlap'):
            chart.plots[0].overlap = 100
        
        return chart


class BarChart(ColumnChart):
    """
    Bar chart component for horizontal bar comparisons.
    
    Inherits from ColumnChart but uses horizontal orientation.
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
            "3d": XL_CHART_TYPE.BAR_CLUSTERED,  # Fallback to regular clustered
        }
        self.chart_type = variant_map.get(variant, XL_CHART_TYPE.BAR_CLUSTERED)


class WaterfallChart(ChartComponent):
    """
    Waterfall chart for showing incremental changes.
    
    Note: PowerPoint doesn't have native waterfall support,
    so this uses a stacked column chart with formatting tricks.
    """
    
    def __init__(self,
                 categories: List[str],
                 values: List[float],
                 **kwargs):
        """
        Initialize waterfall chart.
        
        Args:
            categories: Category labels (e.g., ["Start", "Q1", "Q2", "End"])
            values: Values showing changes (positive/negative)
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.values = values
        self.chart_type = XL_CHART_TYPE.COLUMN_STACKED
    
    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate waterfall data."""
        if not self.categories:
            return False, "No categories provided"
        
        if not self.values:
            return False, "No values provided"
        
        if len(self.categories) != len(self.values):
            return False, f"Categories ({len(self.categories)}) and values ({len(self.values)}) must have same length"
        
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
    
    def _render_sync(self, slide, **kwargs):
        """Render waterfall chart with special formatting."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Make base series invisible
        if len(chart.series) >= 2:
            base_series = chart.series[0]
            fill = base_series.format.fill
            fill.background()  # Make transparent
            base_series.format.line.fill.background()  # Remove line
        
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
                        # Positive - use success color
                        fill.fore_color.rgb = self.get_color("success.DEFAULT")
                    else:
                        # Negative - use destructive color
                        fill.fore_color.rgb = self.get_color("destructive.DEFAULT")
        
        # Add data labels
        plot = chart.plots[0]
        plot.has_data_labels = True
        data_labels = plot.data_labels
        data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
        data_labels.font.size = Pt(9)
        
        # Set gap width to 0 for connected appearance
        if hasattr(chart.plots[0], 'gap_width'):
            chart.plots[0].gap_width = 0
        
        return chart