"""Tests for pie and doughnut chart components."""

import pytest
from pptx.enum.chart import XL_CHART_TYPE
from chuk_mcp_pptx.components.charts.pie_doughnut import PieChart, DoughnutChart


class TestPieChart:
    """Test the PieChart class."""

    @pytest.fixture
    def pie_chart(self):
        """Create a pie chart instance."""
        return PieChart(
            categories=["North", "South", "East", "West"],
            values=[30, 25, 20, 25],
            title="Sales by Region",
        )

    def test_initialization(self, pie_chart):
        """Test pie chart initialization."""
        assert pie_chart.categories == ["North", "South", "East", "West"]
        assert pie_chart.values == [30, 25, 20, 25]
        assert pie_chart.title == "Sales by Region"
        assert pie_chart.explode_slice is None
        assert pie_chart.variant == "pie"  # Updated to match new API
        assert pie_chart.style == "default"  # Check style instead

    def test_initialization_with_explode(self):
        """Test pie chart with exploded slice."""
        chart = PieChart(categories=["A", "B", "C"], values=[50, 30, 20], explode_slice=0)
        assert chart.explode_slice == 0

    def test_validate_data_valid(self, pie_chart):
        """Test validation with valid data."""
        is_valid, error = pie_chart.validate_data()
        assert is_valid is True
        assert error is None

    def test_validate_data_empty_categories(self):
        """Test validation with empty categories."""
        with pytest.raises(ValueError, match="No categories provided"):
            PieChart(categories=[], values=[10])

    def test_validate_data_empty_values(self):
        """Test validation with empty values."""
        with pytest.raises(ValueError, match="No values provided"):
            PieChart(categories=["A"], values=[])

    def test_validate_data_mismatched_lengths(self):
        """Test validation with mismatched data lengths."""
        with pytest.raises(ValueError, match="must have same length"):
            PieChart(
                categories=["A", "B"],
                values=[10, 20, 30],  # 3 values for 2 categories
            )

    def test_validate_data_negative_values(self):
        """Test validation with negative values."""
        with pytest.raises(ValueError, match="cannot have negative values"):
            PieChart(categories=["A", "B"], values=[10, -5])

    def test_validate_data_all_zeros(self):
        """Test validation with all zero values."""
        with pytest.raises(ValueError, match="must have at least one non-zero value"):
            PieChart(categories=["A", "B", "C"], values=[0, 0, 0])

    def test_chart_type(self, pie_chart):
        """Test pie chart type."""
        assert pie_chart.chart_type == XL_CHART_TYPE.PIE

    def test_variant_3d(self):
        """Test 3D pie chart variant - removed in new API."""
        # 3D variant removed - pie only supports: pie, doughnut, exploded
        chart = PieChart(categories=["A"], values=[100], variant="pie")
        assert chart.chart_type == XL_CHART_TYPE.PIE

    def test_variant_exploded(self):
        """Test exploded pie chart variant."""
        chart = PieChart(categories=["A", "B"], values=[60, 40], variant="exploded")
        assert chart.chart_type == XL_CHART_TYPE.PIE_EXPLODED

    def test_show_percentages_option(self):
        """Test show_percentages option - now controlled by style variant."""
        # Use minimal style to hide percentages
        chart = PieChart(categories=["A", "B"], values=[60, 40], style="minimal")
        # Verify variant props control percentages
        assert chart.variant_props.get("show_percentages") is False


class TestDoughnutChart:
    """Test the DoughnutChart class."""

    @pytest.fixture
    def doughnut_chart(self):
        """Create a doughnut chart instance."""
        return DoughnutChart(
            categories=["Desktop", "Mobile", "Tablet"],
            values=[60, 30, 10],
            title="Device Usage",
            hole_size=50,
        )

    def test_initialization(self, doughnut_chart):
        """Test doughnut chart initialization."""
        assert doughnut_chart.categories == ["Desktop", "Mobile", "Tablet"]
        assert doughnut_chart.values == [60, 30, 10]
        assert doughnut_chart.title == "Device Usage"
        assert doughnut_chart.hole_size == 50

    def test_initialization_default_hole_size(self):
        """Test doughnut chart with default hole size."""
        chart = DoughnutChart(categories=["A", "B"], values=[70, 30])
        assert chart.hole_size == 0.5  # Default value (0-1 scale, not percentage)

    def test_chart_type(self, doughnut_chart):
        """Test doughnut chart type."""
        assert doughnut_chart.chart_type == XL_CHART_TYPE.DOUGHNUT

    def test_variant_exploded(self):
        """Test exploded doughnut chart - uses explode_slice parameter instead."""
        # Doughnut doesn't support exploded variant in new API
        # Use explode_slice parameter on PieChart instead
        chart = DoughnutChart(categories=["A", "B"], values=[70, 30])
        # Doughnut always uses DOUGHNUT type
        assert chart.chart_type == XL_CHART_TYPE.DOUGHNUT

    def test_validate_data_all_zeros(self):
        """Test validation with all zero values."""
        with pytest.raises(ValueError, match="must have at least one non-zero value"):
            DoughnutChart(categories=["A", "B", "C"], values=[0, 0, 0])

    def test_hole_size_bounds(self):
        """Test hole size boundaries."""
        # Test minimum hole size
        chart = DoughnutChart(categories=["A", "B"], values=[60, 40], hole_size=10)
        assert chart.hole_size == 10

        # Test maximum hole size
        chart = DoughnutChart(categories=["A", "B"], values=[60, 40], hole_size=90)
        assert chart.hole_size == 90
