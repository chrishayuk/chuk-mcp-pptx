"""
Base chart component with validation and boundary detection.
"""

from typing import Dict, Any, List, Optional, Tuple, Union
from pptx.chart.data import CategoryChartData, XyChartData, BubbleChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_MARK, XL_TICK_LABEL_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import asyncio

from ..base import AsyncComponent


class ChartComponent(AsyncComponent):
    """
    Base chart component with validation and boundary detection.
    
    Features:
    - Data validation
    - Boundary detection
    - Theme integration
    - Error handling
    """
    
    # Default chart dimensions
    DEFAULT_WIDTH = 8.0
    DEFAULT_HEIGHT = 4.5
    DEFAULT_LEFT = 1.0
    DEFAULT_TOP = 2.0
    
    # Slide dimensions (standard 16:9)
    SLIDE_WIDTH = 10.0
    SLIDE_HEIGHT = 7.5
    
    # Safe margins
    MARGIN_TOP = 1.5  # Leave space for title
    MARGIN_BOTTOM = 0.5
    MARGIN_LEFT = 0.5
    MARGIN_RIGHT = 0.5
    
    def __init__(self,
                 title: Optional[str] = None,
                 data: Optional[Dict[str, Any]] = None,
                 theme: Optional[Dict[str, Any]] = None,
                 options: Optional[Dict[str, Any]] = None):
        """
        Initialize chart component.
        
        Args:
            title: Chart title
            data: Chart data
            theme: Theme configuration
            options: Chart-specific options
        """
        super().__init__(theme)
        self.title = title
        self.data = data or {}
        self.options = options or {}
        self.chart_type = XL_CHART_TYPE.COLUMN_CLUSTERED
    
    def validate_data(self) -> Tuple[bool, Optional[str]]:
        """
        Validate chart data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.data:
            return False, "No data provided for chart"
        
        # Override in subclasses for specific validation
        return True, None
    
    def validate_position(self, left: float, top: float, 
                         width: float, height: float,
                         has_title: bool = False) -> Tuple[float, float, float, float]:
        """
        Validate and adjust chart position to fit within slide bounds.
        
        Args:
            left: Left position in inches
            top: Top position in inches
            width: Width in inches
            height: Height in inches
            has_title: Whether slide has a title
        
        Returns:
            Tuple of adjusted (left, top, width, height)
        """
        # Adjust top margin if slide has title
        min_top = self.MARGIN_TOP if has_title else self.MARGIN_TOP / 2
        
        # Calculate maximum dimensions
        max_width = self.SLIDE_WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT
        max_height = self.SLIDE_HEIGHT - min_top - self.MARGIN_BOTTOM
        
        # Validate and adjust left position
        if left < self.MARGIN_LEFT:
            left = self.MARGIN_LEFT
        if left + width > self.SLIDE_WIDTH - self.MARGIN_RIGHT:
            # Try to fit by adjusting left position
            left = max(self.MARGIN_LEFT, self.SLIDE_WIDTH - self.MARGIN_RIGHT - width)
            if left < self.MARGIN_LEFT:
                # Still doesn't fit, reduce width
                left = self.MARGIN_LEFT
                width = max_width
        
        # Validate and adjust top position
        if top < min_top:
            top = min_top
        if top + height > self.SLIDE_HEIGHT - self.MARGIN_BOTTOM:
            # Try to fit by adjusting top position
            top = max(min_top, self.SLIDE_HEIGHT - self.MARGIN_BOTTOM - height)
            if top < min_top:
                # Still doesn't fit, reduce height
                top = min_top
                height = max_height
        
        # Final validation of dimensions
        width = min(width, max_width)
        height = min(height, max_height)
        
        return left, top, width, height
    
    def get_safe_content_area(self, has_title: bool = False) -> Dict[str, float]:
        """
        Get safe content area for chart placement.
        
        Args:
            has_title: Whether slide has a title
        
        Returns:
            Dictionary with safe area boundaries
        """
        return {
            'left': self.MARGIN_LEFT,
            'top': self.MARGIN_TOP if has_title else self.MARGIN_TOP / 2,
            'right': self.SLIDE_WIDTH - self.MARGIN_RIGHT,
            'bottom': self.SLIDE_HEIGHT - self.MARGIN_BOTTOM,
            'width': self.SLIDE_WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT,
            'height': self.SLIDE_HEIGHT - (self.MARGIN_TOP if has_title else self.MARGIN_TOP / 2) - self.MARGIN_BOTTOM
        }
    
    def apply_theme_colors(self, chart):
        """
        Apply theme colors to chart.
        
        Args:
            chart: PowerPoint chart object
        """
        # Get theme chart colors
        chart_colors = self.tokens.get("chart", [])
        
        # Apply colors to series
        for idx, series in enumerate(chart.series):
            if idx < len(chart_colors):
                # Get color for this series
                color_hex = chart_colors[idx]
                if isinstance(color_hex, str):
                    rgb = self.hex_to_rgb(color_hex)
                    fill = series.format.fill
                    fill.solid()
                    fill.fore_color.rgb = RGBColor(*rgb)
    
    def configure_legend(self, chart, position: str = "right", show: bool = True):
        """
        Configure chart legend.
        
        Args:
            chart: PowerPoint chart object
            position: Legend position
            show: Whether to show legend
        """
        chart.has_legend = show
        
        if show:
            position_map = {
                "right": XL_LEGEND_POSITION.RIGHT,
                "left": XL_LEGEND_POSITION.LEFT,
                "top": XL_LEGEND_POSITION.TOP,
                "bottom": XL_LEGEND_POSITION.BOTTOM,
                "corner": XL_LEGEND_POSITION.CORNER,
            }
            
            chart.legend.position = position_map.get(position.lower(), XL_LEGEND_POSITION.RIGHT)
            chart.legend.include_in_layout = False
            
            # Apply theme font
            if hasattr(chart.legend, 'font'):
                chart.legend.font.name = self.theme.get("font_family", "Inter")
                chart.legend.font.size = Pt(10)
    
    def configure_axes(self, chart):
        """
        Configure chart axes with theme styling.
        
        Args:
            chart: PowerPoint chart object
        """
        # Skip axis configuration for pie and doughnut charts
        try:
            # Configure value axis
            if hasattr(chart, 'value_axis'):
                value_axis = chart.value_axis
                value_axis.has_major_gridlines = True
                value_axis.major_gridlines.format.line.color.rgb = self.get_color("border.secondary")
                value_axis.major_gridlines.format.line.width = Pt(0.5)
                
                # Format axis labels
                if hasattr(value_axis, 'tick_labels'):
                    value_axis.tick_labels.font.name = self.theme.get("font_family", "Inter")
                    value_axis.tick_labels.font.size = Pt(9)
                    value_axis.tick_labels.font.color.rgb = self.get_color("muted.foreground")
            
            # Configure category axis
            if hasattr(chart, 'category_axis'):
                cat_axis = chart.category_axis
                if hasattr(cat_axis, 'tick_labels'):
                    cat_axis.tick_labels.font.name = self.theme.get("font_family", "Inter")
                    cat_axis.tick_labels.font.size = Pt(9)
                    cat_axis.tick_labels.font.color.rgb = self.get_color("muted.foreground")
        except ValueError:
            # Chart type doesn't have axes (e.g., pie charts)
            pass
    
    def set_chart_title(self, chart):
        """
        Set and style chart title.
        
        Args:
            chart: PowerPoint chart object
        """
        if self.title:
            chart.has_title = True
            title = chart.chart_title
            title.text_frame.text = self.title
            
            # Style the title
            para = title.text_frame.paragraphs[0]
            para.font.name = self.theme.get("font_family", "Inter")
            para.font.size = Pt(16)
            para.font.bold = True
            para.font.color.rgb = self.get_color("foreground.DEFAULT")
    
    def _prepare_chart_data(self) -> Union[CategoryChartData, XyChartData, BubbleChartData]:
        """
        Prepare chart data (override in subclasses).
        
        Returns:
            Chart data object
        """
        raise NotImplementedError("Subclasses must implement _prepare_chart_data")
    
    def _render_sync(self, slide,
                     left: Optional[float] = None,
                     top: Optional[float] = None,
                     width: Optional[float] = None,
                     height: Optional[float] = None) -> Any:
        """
        Synchronous render implementation.
        
        Args:
            slide: PowerPoint slide
            left: Left position in inches
            top: Top position in inches
            width: Chart width in inches
            height: Chart height in inches
        
        Returns:
            Chart object
        """
        # Use defaults if not provided
        left = left or self.DEFAULT_LEFT
        top = top or self.DEFAULT_TOP
        width = width or self.DEFAULT_WIDTH
        height = height or self.DEFAULT_HEIGHT
        
        # Validate data
        is_valid, error = self.validate_data()
        if not is_valid:
            raise ValueError(f"Chart data validation failed: {error}")
        
        # Check if slide has title
        has_title = bool(slide.shapes.title)
        
        # Validate and adjust position
        left, top, width, height = self.validate_position(left, top, width, height, has_title)
        
        # Prepare data
        chart_data = self._prepare_chart_data()
        
        # Add chart to slide
        chart_shape = slide.shapes.add_chart(
            self.chart_type,
            Inches(left), Inches(top),
            Inches(width), Inches(height),
            chart_data
        )
        
        chart = chart_shape.chart
        
        # Apply styling
        self.set_chart_title(chart)
        self.apply_theme_colors(chart)
        self.configure_legend(
            chart,
            position=self.options.get("legend_position", "right"),
            show=self.options.get("show_legend", True)
        )
        self.configure_axes(chart)
        
        return chart