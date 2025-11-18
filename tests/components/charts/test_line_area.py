"""Tests for line and area chart components."""

import pytest
from pptx.enum.chart import XL_CHART_TYPE
from chuk_mcp_pptx.components.charts.line_area import LineChart, AreaChart, SparklineChart


class TestLineChart:
    """Test the LineChart class."""

    @pytest.fixture
    def line_chart(self):
        """Create a line chart instance."""
        return LineChart(
            categories=["Jan", "Feb", "Mar", "Apr", "May"],
            series={"Revenue": [100, 120, 140, 135, 160], "Costs": [80, 85, 90, 88, 95]},
            title="Monthly Performance",
        )

    def test_initialization(self, line_chart):
        """Test line chart initialization."""
        assert line_chart.categories == ["Jan", "Feb", "Mar", "Apr", "May"]
        assert "Revenue" in line_chart.series
        assert "Costs" in line_chart.series
        assert line_chart.title == "Monthly Performance"
        assert line_chart.variant == "line"  # Updated API
        assert line_chart.style == "default"

    def test_initialization_with_options(self):
        """Test line chart with custom options."""
        chart = LineChart(
            categories=["Q1", "Q2", "Q3", "Q4"],
            series={"Sales": [100, 110, 120, 115]},
            variant="smooth",  # Use variant instead of smooth param
            style="minimal",
        )
        assert chart.variant == "smooth"
        assert chart.style == "minimal"

    def test_validate_data_valid(self, line_chart):
        """Test validation with valid data."""
        is_valid, error = line_chart.validate_data()
        assert is_valid is True
        assert error is None

    def test_validate_data_empty_categories(self):
        """Test validation with empty categories."""
        with pytest.raises(ValueError, match="No categories provided"):
            LineChart(categories=[], series={"Sales": [100]})

    def test_validate_data_empty_series(self):
        """Test validation with empty series data."""
        with pytest.raises(ValueError, match="No data series provided"):
            LineChart(categories=["Q1"], series={})

    def test_validate_data_mismatched_lengths(self):
        """Test validation with mismatched data lengths."""
        with pytest.raises(ValueError, match="has 3 values, expected 2"):
            LineChart(
                categories=["Q1", "Q2"],
                series={"Sales": [100, 110, 120]},  # 3 values for 2 categories
            )

    def test_chart_type_default(self, line_chart):
        """Test default line chart type."""
        # Default has markers=True, so type is LINE_MARKERS
        assert line_chart.chart_type == XL_CHART_TYPE.LINE_MARKERS

    def test_chart_type_markers(self):
        """Test line chart with markers type."""
        chart = LineChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="markers")
        assert chart.chart_type == XL_CHART_TYPE.LINE_MARKERS

    def test_chart_type_3d(self):
        """Test 3D line chart type - removed in new API."""
        # 3D variant removed, use standard line
        chart = LineChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="line")
        assert chart.chart_type == XL_CHART_TYPE.LINE_MARKERS

    def test_smooth_lines(self):
        """Test smooth lines option."""
        chart = LineChart(
            categories=["A", "B", "C"],
            series={"Test": [1, 2, 3]},
            variant="smooth",  # Use variant instead
        )
        assert chart.variant == "smooth"
        assert chart.variant_props.get("smooth") is True

    def test_no_markers(self):
        """Test line chart without markers."""
        chart = LineChart(
            categories=["A", "B", "C"],
            series={"Test": [1, 2, 3]},
            style="minimal",  # Minimal style hides markers
        )
        assert chart.style == "minimal"
        assert chart.variant_props.get("show_markers") is False


class TestAreaChart:
    """Test the AreaChart class."""

    @pytest.fixture
    def area_chart(self):
        """Create an area chart instance."""
        return AreaChart(
            categories=["2020", "2021", "2022", "2023"],
            series={"Growth": [100, 150, 200, 180]},
            title="Growth Trend",
        )

    def test_initialization(self, area_chart):
        """Test area chart initialization."""
        assert area_chart.categories == ["2020", "2021", "2022", "2023"]
        assert area_chart.series == {"Growth": [100, 150, 200, 180]}
        assert area_chart.title == "Growth Trend"
        assert area_chart.variant == "area"

    def test_chart_type_default(self, area_chart):
        """Test default area chart type."""
        assert area_chart.chart_type == XL_CHART_TYPE.AREA

    def test_chart_type_stacked(self):
        """Test stacked area chart type."""
        chart = AreaChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="stacked")
        assert chart.chart_type == XL_CHART_TYPE.AREA_STACKED

    def test_chart_type_stacked100(self):
        """Test 100% stacked area chart type."""
        chart = AreaChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="stacked100")
        assert chart.chart_type == XL_CHART_TYPE.AREA_STACKED_100

    def test_chart_type_3d(self):
        """Test 3D area chart type."""
        chart = AreaChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="3d")
        assert chart.chart_type == XL_CHART_TYPE.THREE_D_AREA

    def test_transparency_option(self):
        """Test transparency option - removed from new API."""
        # Options parameter removed - use style variants instead
        chart = AreaChart(categories=["A", "B"], series={"Test": [1, 2]}, style="default")
        # Verify chart was created successfully
        assert chart.style == "default"


class TestSparklineChart:
    """Test the SparklineChart class."""

    @pytest.fixture
    def sparkline_chart(self):
        """Create a sparkline chart instance."""
        return SparklineChart(values=[10, 15, 12, 18, 20, 17, 22, 25], title="Trend")

    def test_initialization(self, sparkline_chart):
        """Test sparkline chart initialization."""
        assert sparkline_chart.series["Value"] == [10, 15, 12, 18, 20, 17, 22, 25]
        assert sparkline_chart.title == "Trend"
        # Sparkline auto-generates categories
        assert len(sparkline_chart.categories) == 8

    def test_initialization_with_categories(self):
        """Test sparkline with explicit categories."""
        chart = SparklineChart(values=[10, 20, 30], categories=["A", "B", "C"])
        assert chart.series["Value"] == [10, 20, 30]
        assert chart.categories == ["A", "B", "C"]

    def test_minimal_styling(self, sparkline_chart):
        """Test that sparklines use minimal style by default."""
        assert sparkline_chart.style == "minimal"
        assert sparkline_chart.legend == "none"

    def test_default_variant(self):
        """Test sparkline uses line variant by default."""
        chart = SparklineChart(values=[1, 2, 3, 4, 5])
        # Sparklines use line variant with minimal styling
        assert chart.variant == "line"
        assert chart.style == "minimal"
        assert chart.variant_props.get("show_markers") is False
