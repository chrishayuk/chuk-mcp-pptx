"""
Comprehensive chart components for PowerPoint presentations.
Beautiful, theme-aware charts similar to modern design systems.
"""

from .base import ChartComponent
from .column_bar import ColumnChart, BarChart, WaterfallChart
from .pie_doughnut import PieChart, DoughnutChart

# Line and Area charts - refactored
from .line_area import LineChart, AreaChart, SparklineChart

try:
    from .scatter_bubble import ScatterChart, BubbleChart, Matrix3DChart
except ImportError:
    ScatterChart = None  # type: ignore[misc, assignment]
    BubbleChart = None  # type: ignore[misc, assignment]
    Matrix3DChart = None  # type: ignore[misc, assignment]

try:
    from .radar_combo import RadarChart, ComboChart, GaugeChart
except ImportError:
    RadarChart = None  # type: ignore[misc, assignment]
    ComboChart = None  # type: ignore[misc, assignment]
    GaugeChart = None  # type: ignore[misc, assignment]

try:
    from .funnel import FunnelChart, GanttChart, HeatmapChart
except ImportError:
    FunnelChart = None  # type: ignore[misc, assignment]
    GanttChart = None  # type: ignore[misc, assignment]
    HeatmapChart = None  # type: ignore[misc, assignment]

# Legacy chart component (for backward compatibility)
try:
    from ..chart import (
        Chart,
        BarChart as LegacyBarChart,
        LineChart as LegacyLineChart,
        PieChart as LegacyPieChart,
    )
except ImportError:
    # Fallback if legacy chart module doesn't exist
    Chart = None
    LegacyBarChart = None
    LegacyLineChart = None
    LegacyPieChart = None

__all__ = [
    # Base
    "ChartComponent",
    # Column & Bar Charts
    "ColumnChart",
    "BarChart",
    "WaterfallChart",
    # Line & Area Charts
    "LineChart",
    "AreaChart",
    "SparklineChart",
    # Pie & Doughnut Charts
    "PieChart",
    "DoughnutChart",
    # Scatter & Bubble Charts
    "ScatterChart",
    "BubbleChart",
    "Matrix3DChart",
    # Specialized Charts
    "RadarChart",
    "ComboChart",
    "GaugeChart",
    # Business Charts
    "FunnelChart",
    "GanttChart",
    "HeatmapChart",
    # Legacy (backward compatibility)
    "Chart",
    "LegacyBarChart",
    "LegacyLineChart",
    "LegacyPieChart",
]
