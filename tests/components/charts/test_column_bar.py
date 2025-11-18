"""Tests for column and bar chart components."""

import pytest
from pptx.enum.chart import XL_CHART_TYPE
from chuk_mcp_pptx.components.charts.column_bar import ColumnChart, BarChart, WaterfallChart


class TestColumnChart:
    """Test the ColumnChart class."""

    @pytest.fixture
    def column_chart(self):
        """Create a column chart instance."""
        return ColumnChart(
            categories=["Q1", "Q2", "Q3", "Q4"],
            series={"Sales": [100, 150, 200, 175]},
            title="Quarterly Sales",
            variant="clustered",
        )

    def test_initialization(self, column_chart):
        """Test column chart initialization."""
        assert column_chart.categories == ["Q1", "Q2", "Q3", "Q4"]
        assert column_chart.series == {"Sales": [100, 150, 200, 175]}
        assert column_chart.title == "Quarterly Sales"
        assert column_chart.variant == "clustered"
        assert column_chart.chart_type == XL_CHART_TYPE.COLUMN_CLUSTERED

    def test_validate_data_valid(self, column_chart):
        """Test validation with valid data."""
        is_valid, error = column_chart.validate_data()
        assert is_valid is True
        assert error is None

    def test_validate_data_no_categories(self):
        """Test validation with no categories."""
        with pytest.raises(ValueError, match="No categories provided"):
            ColumnChart(categories=[], series={"Sales": [100]})

    def test_validate_data_no_series(self):
        """Test validation with no series data."""
        with pytest.raises(ValueError, match="No data series provided"):
            ColumnChart(categories=["Q1"], series={})

    def test_validate_data_mismatched_lengths(self):
        """Test validation with mismatched data lengths."""
        with pytest.raises(ValueError, match="has 3 values, expected 2"):
            ColumnChart(
                categories=["Q1", "Q2"],
                series={"Sales": [100, 150, 200]},  # 3 values for 2 categories
            )

    def test_variant_stacked(self):
        """Test stacked column chart variant."""
        chart = ColumnChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="stacked")
        assert chart.chart_type == XL_CHART_TYPE.COLUMN_STACKED

    def test_variant_stacked100(self):
        """Test 100% stacked column chart variant."""
        chart = ColumnChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="stacked100")
        assert chart.chart_type == XL_CHART_TYPE.COLUMN_STACKED_100

    def test_variant_3d(self):
        """Test 3D column chart variant."""
        chart = ColumnChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="3d")
        assert chart.chart_type == XL_CHART_TYPE.THREE_D_COLUMN

    def test_multiple_series(self):
        """Test column chart with multiple series."""
        chart = ColumnChart(
            categories=["Q1", "Q2"], series={"Sales": [100, 150], "Costs": [80, 90]}
        )
        assert len(chart.series) == 2
        assert "Sales" in chart.series
        assert "Costs" in chart.series


class TestBarChart:
    """Test the BarChart class."""

    @pytest.fixture
    def bar_chart(self):
        """Create a bar chart instance."""
        return BarChart(
            categories=["Product A", "Product B", "Product C"], series={"Sales": [300, 450, 250]}
        )

    def test_initialization(self, bar_chart):
        """Test bar chart initialization."""
        assert bar_chart.categories == ["Product A", "Product B", "Product C"]
        assert bar_chart.series == {"Sales": [300, 450, 250]}
        # Bar chart inherits from ColumnChart but changes orientation
        assert bar_chart.chart_type == XL_CHART_TYPE.BAR_CLUSTERED

    def test_variant_stacked(self):
        """Test stacked bar chart variant."""
        chart = BarChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="stacked")
        assert chart.chart_type == XL_CHART_TYPE.BAR_STACKED

    def test_variant_3d(self):
        """Test 3D bar chart variant."""
        chart = BarChart(categories=["A", "B"], series={"Test": [1, 2]}, variant="3d")
        assert chart.chart_type == XL_CHART_TYPE.THREE_D_BAR_CLUSTERED


class TestWaterfallChart:
    """Test the WaterfallChart class."""

    @pytest.fixture
    def waterfall_chart(self):
        """Create a waterfall chart instance."""
        return WaterfallChart(
            categories=["Start", "Q1", "Q2", "Q3", "Q4", "End"],
            values=[100, 30, -20, 45, -10, None],
            title="Quarterly Performance",
        )

    def test_initialization(self, waterfall_chart):
        """Test waterfall chart initialization."""
        assert waterfall_chart.categories == ["Start", "Q1", "Q2", "Q3", "Q4", "End"]
        assert waterfall_chart.values == [100, 30, -20, 45, -10, None]
        assert waterfall_chart.title == "Quarterly Performance"

    def test_validate_data_valid(self, waterfall_chart):
        """Test validation with valid data."""
        is_valid, error = waterfall_chart.validate_data()
        assert is_valid is True
        assert error is None

    def test_validate_data_empty_categories(self):
        """Test validation with empty categories."""
        with pytest.raises(ValueError, match="No categories provided"):
            WaterfallChart(categories=[], values=[100])

    def test_validate_data_mismatched_lengths(self):
        """Test validation with mismatched data lengths."""
        with pytest.raises(ValueError, match="must have same length"):
            WaterfallChart(
                categories=["A", "B"],
                values=[100, 50, 25],  # 3 values for 2 categories
            )

    def test_negative_values(self):
        """Test waterfall chart with negative values."""
        chart = WaterfallChart(
            categories=["Start", "Loss", "Gain", "End"], values=[100, -30, 50, None]
        )
        assert chart.values[1] == -30  # Negative value preserved
        assert chart.values[3] is None  # Total value preserved as None
