"""
Pie and Doughnut chart components with modern styling.
"""

from typing import Dict, Any, List, Optional, Tuple
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION
from pptx.util import Pt
from pptx.dml.color import RGBColor

from .base import ChartComponent


class PieChart(ChartComponent):
    """
    Pie chart component for showing proportions.
    
    Features:
    - Exploded slices
    - Data labels with percentages
    - Custom colors
    - 3D variants
    """
    
    def __init__(self,
                 categories: List[str],
                 values: List[float],
                 explode_slice: Optional[int] = None,
                 variant: str = "default",
                 show_percentages: bool = True,
                 **kwargs):
        """
        Initialize pie chart.
        
        Args:
            categories: Category labels
            values: Data values
            explode_slice: Index of slice to explode (optional)
            variant: Chart variant (default, 3d, exploded)
            show_percentages: Whether to show percentages
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.values = values
        self.explode_slice = explode_slice
        self.variant = variant
        self.show_percentages = show_percentages
        
        # Validate data during initialization
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")
        
        # Set chart type based on variant
        if variant == "3d":
            self.chart_type = XL_CHART_TYPE.THREE_D_PIE
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
            return False, f"Categories ({len(self.categories)}) and values ({len(self.values)}) must have same length"
        
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
    
    def _render_sync(self, slide, **kwargs):
        """Render pie chart with beautiful styling."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Get theme colors
        chart_colors = self.tokens.get("chart", [])
        
        # Apply colors to slices
        if len(chart.series) > 0:
            series = chart.series[0]
            
            for idx, point in enumerate(series.points):
                if idx < len(chart_colors):
                    color_hex = chart_colors[idx]
                    if isinstance(color_hex, str):
                        rgb = self.hex_to_rgb(color_hex)
                        fill = point.format.fill
                        fill.solid()
                        fill.fore_color.rgb = RGBColor(*rgb)
                
                # Add subtle border for definition
                line = point.format.line
                line.color.rgb = RGBColor(255, 255, 255)
                line.width = Pt(0.5)
        
        # Explode slice if specified
        if self.explode_slice is not None and len(chart.series) > 0:
            series = chart.series[0]
            if 0 <= self.explode_slice < len(series.points):
                series.points[self.explode_slice].explosion = 10
        
        # Add data labels
        plot = chart.plots[0]
        plot.has_data_labels = True
        data_labels = plot.data_labels
        
        # Show percentages and categories
        opts = self._computed_options if hasattr(self, '_computed_options') else {}
        if opts.get("show_percentages", self.show_percentages):
            data_labels.show_percentage = True
        
        if opts.get("show_categories", True):
            data_labels.show_category_name = True
        
        if opts.get("show_values", False):
            data_labels.show_value = True
        
        # Configure label appearance
        data_labels.font.size = Pt(10)
        data_labels.font.color.rgb = RGBColor(255, 255, 255)
        data_labels.position = XL_DATA_LABEL_POSITION.CENTER
        
        # Add leader lines for outside labels
        if opts.get("labels_outside", False):
            data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
            data_labels.font.color.rgb = self.get_color("foreground.DEFAULT")
            if hasattr(data_labels, 'show_leader_lines'):
                data_labels.show_leader_lines = True
        
        return chart


class DoughnutChart(PieChart):
    """
    Doughnut chart component - pie chart with hollow center.
    
    Features:
    - Adjustable hole size
    - Center text capability
    - Modern flat design
    """
    
    def __init__(self,
                 hole_size: int = 50,
                 center_text: Optional[str] = None,
                 variant: str = "default",
                 **kwargs):
        """
        Initialize doughnut chart.
        
        Args:
            hole_size: Size of center hole (0-90)
            center_text: Text to display in the center
            variant: Chart variant (default, exploded)
            **kwargs: Additional chart parameters
        """
        super().__init__(variant=variant, **kwargs)
        self.hole_size = max(10, min(90, hole_size))
        self.center_text = center_text
        
        # Set chart type
        if variant == "exploded":
            self.chart_type = XL_CHART_TYPE.DOUGHNUT_EXPLODED
        else:
            self.chart_type = XL_CHART_TYPE.DOUGHNUT
    
    def _render_sync(self, slide, **kwargs):
        """Render doughnut chart with modern styling."""
        chart = super()._render_sync(slide, **kwargs)
        
        # Configure hole size (if python-pptx supports it)
        # Note: Direct hole size configuration may require XML manipulation
        # For now, we rely on the default doughnut appearance
        
        # Adjust label position for doughnut
        plot = chart.plots[0]
        if plot.has_data_labels:
            data_labels = plot.data_labels
            
            # Position labels outside for doughnut
            opts = self._computed_options if hasattr(self, '_computed_options') else {}
            if not opts.get("labels_inside", False):
                data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
                data_labels.font.color.rgb = self.get_color("foreground.DEFAULT")
                if hasattr(data_labels, 'show_leader_lines'):
                    data_labels.show_leader_lines = True
        
        return chart


class SunburstChart(ChartComponent):
    """
    Sunburst chart for hierarchical data.
    
    Note: PowerPoint may have limited support for sunburst charts.
    This creates a multi-level doughnut chart as approximation.
    """
    
    def __init__(self,
                 data: Dict[str, Any],
                 max_levels: Optional[int] = None,
                 color_scheme: Optional[str] = None,
                 **kwargs):
        """
        Initialize sunburst chart.
        
        Args:
            data: Hierarchical data structure
            max_levels: Maximum depth levels to display
            color_scheme: Color scheme for the chart
            **kwargs: Additional chart parameters
        """
        super().__init__(**kwargs)
        self.data = data  # Store as data for test compatibility
        self.max_levels = max_levels
        self.color_scheme = color_scheme
        self.chart_type = XL_CHART_TYPE.DOUGHNUT
        
        # Convert hierarchical data to flat structure
        self._flatten_data()
        
        # Validate data after flattening
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Invalid chart data: {error}")
    
    def _flatten_data(self):
        """Flatten hierarchical data for doughnut representation."""
        # This is a simplified approach
        # In practice, you'd need more complex logic for true sunburst
        self.categories = []
        self.values = []
        
        def traverse(node, level=0):
            # Skip if max_levels is set and we're too deep
            if self.max_levels and level >= self.max_levels:
                return
                
            if isinstance(node, dict):
                # Handle both 'name'/'value' structure and generic dict
                if 'name' in node and 'value' in node:
                    self.categories.append(node['name'])
                    self.values.append(node['value'])
                    # Traverse children if present
                    if 'children' in node:
                        for child in node['children']:
                            traverse(child, level + 1)
                else:
                    # Generic dict traversal
                    for key, value in node.items():
                        if isinstance(value, (int, float)):
                            self.categories.append(key)
                            self.values.append(value)
                        else:
                            traverse(value, level + 1)
        
        traverse(self.data)
    
    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """Validate sunburst data."""
        if not self.categories:
            return False, "No data could be extracted from hierarchical structure"
        
        return True, None
    
    def _prepare_chart_data(self) -> CategoryChartData:
        """Prepare sunburst data as doughnut."""
        chart_data = CategoryChartData()
        chart_data.categories = self.categories
        chart_data.add_series("Values", self.values)
        return chart_data