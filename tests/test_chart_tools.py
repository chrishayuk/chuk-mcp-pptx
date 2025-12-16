"""
Comprehensive tests for chart_tools.py

Tests for the unified chart tool that supports all chart types.
Coverage target: 90%+
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest


class TestRegisterChartTools:
    """Tests for register_chart_tools function."""

    def test_register_returns_dict(self) -> None:
        """Test that register_chart_tools returns a dictionary of tools."""
        from chuk_mcp_pptx.chart_tools import register_chart_tools

        mock_mcp = MagicMock()
        mock_manager = MagicMock()

        result = register_chart_tools(mock_mcp, mock_manager)

        assert isinstance(result, dict)
        assert "pptx_add_chart" in result
        assert "pptx_get_chart_style" in result

    def test_tools_are_registered_with_mcp(self) -> None:
        """Test that tools are registered with the MCP server."""
        from chuk_mcp_pptx.chart_tools import register_chart_tools

        mock_mcp = MagicMock()
        mock_manager = MagicMock()

        register_chart_tools(mock_mcp, mock_manager)

        # Check that tool decorator was called
        assert mock_mcp.tool.called


class TestPptxAddChartBasics:
    """Tests for basic pptx_add_chart functionality."""

    @pytest.fixture
    def chart_tools(self):
        """Create chart tools with mocked dependencies."""
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_chart_no_presentation(self, chart_tools) -> None:
        """Test adding chart when no presentation exists."""
        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"Values": [1]}},
        )
        assert "No presentation found" in result

    @pytest.mark.asyncio
    async def test_add_chart_invalid_slide_index_string(self, chart_tools) -> None:
        """Test adding chart with invalid slide index (string)."""
        from chuk_mcp_pptx.async_server import pptx_create, manager

        manager.clear_all()
        await pptx_create(name="test")

        # We need to add a slide first
        from chuk_mcp_pptx.async_server import pptx_add_title_slide

        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index="invalid",  # type: ignore
            chart_type="column",
            data={"categories": ["A"], "series": {"Values": [1]}},
        )
        assert "slide_index must be a number" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_chart_slide_out_of_range(self, chart_tools) -> None:
        """Test adding chart with out-of-range slide index."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=99,
            chart_type="column",
            data={"categories": ["A"], "series": {"Values": [1]}},
        )
        assert "out of range" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_chart_invalid_chart_type(self, chart_tools) -> None:
        """Test adding chart with invalid chart type."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="invalid_chart_type",
            data={"categories": ["A"], "series": {"Values": [1]}},
        )
        assert "Invalid chart_type" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_chart_json_string_data(self, chart_tools) -> None:
        """Test adding chart with JSON string data (from MCP protocol)."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        # Pass data as JSON string (as MCP might send it)
        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data='{"categories": ["A", "B"], "series": {"Values": [1, 2]}}',
        )
        assert "Added column chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_chart_invalid_json_data(self, chart_tools) -> None:
        """Test adding chart with invalid JSON data."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data="not-valid-json{",
        )
        assert "valid JSON object" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_chart_json_string_options(self, chart_tools) -> None:
        """Test adding chart with JSON string options."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"Values": [1]}},
            options='{"show_legend": true}',
        )
        assert "Added column chart" in result

        manager.clear_all()


class TestColumnBarCharts:
    """Tests for column and bar chart types."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_column_chart(self, chart_tools) -> None:
        """Test adding a column chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={
                "categories": ["Q1", "Q2", "Q3", "Q4"],
                "series": {"Revenue": [100, 120, 140, 160]},
            },
            title="Revenue Chart",
        )
        assert "Added column chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_column_stacked_chart(self, chart_tools) -> None:
        """Test adding a stacked column chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column_stacked",
            data={"categories": ["Q1", "Q2"], "series": {"A": [10, 20], "B": [15, 25]}},
        )
        assert "Added column_stacked chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_bar_chart(self, chart_tools) -> None:
        """Test adding a horizontal bar chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="bar",
            data={"categories": ["A", "B", "C"], "series": {"Values": [10, 20, 30]}},
        )
        assert "Added bar chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_bar_stacked_chart(self, chart_tools) -> None:
        """Test adding a stacked bar chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="bar_stacked",
            data={"categories": ["A", "B"], "series": {"X": [5, 10], "Y": [8, 12]}},
        )
        assert "Added bar_stacked chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_column_chart_missing_categories(self, chart_tools) -> None:
        """Test column chart with missing categories."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"series": {"Values": [1, 2, 3]}},
        )
        assert "require 'categories' and 'series'" in result

        manager.clear_all()


class TestLineAreaCharts:
    """Tests for line and area chart types."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_line_chart(self, chart_tools) -> None:
        """Test adding a line chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="line",
            data={
                "categories": ["Jan", "Feb", "Mar", "Apr"],
                "series": {"Sales": [100, 110, 120, 130]},
            },
            title="Sales Trend",
        )
        assert "Added line chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_line_markers_chart(self, chart_tools) -> None:
        """Test adding a line chart with markers."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="line_markers",
            data={"categories": ["A", "B", "C"], "series": {"Data": [1, 2, 3]}},
        )
        assert "Added line_markers chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_area_chart(self, chart_tools) -> None:
        """Test adding an area chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="area",
            data={"categories": ["2020", "2021", "2022"], "series": {"Growth": [100, 150, 200]}},
        )
        assert "Added area chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_area_stacked_chart(self, chart_tools) -> None:
        """Test adding a stacked area chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="area_stacked",
            data={"categories": ["Q1", "Q2"], "series": {"A": [10, 20], "B": [15, 25]}},
        )
        assert "Added area_stacked chart" in result

        manager.clear_all()


class TestPieCharts:
    """Tests for pie and doughnut chart types."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_pie_chart(self, chart_tools) -> None:
        """Test adding a pie chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="pie",
            data={"categories": ["Product A", "Product B", "Product C"], "values": [45, 30, 25]},
            title="Market Share",
        )
        assert "Added pie chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_pie_chart_with_percentages(self, chart_tools) -> None:
        """Test adding a pie chart with percentage labels."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="pie",
            data={"categories": ["A", "B"], "values": [60, 40]},
            options={"show_percentages": True},
        )
        assert "Added pie chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_doughnut_chart(self, chart_tools) -> None:
        """Test adding a doughnut chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="doughnut",
            data={"categories": ["A", "B", "C"], "values": [33, 33, 34]},
            title="Distribution",
        )
        assert "Added doughnut chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_pie_chart_missing_values(self, chart_tools) -> None:
        """Test pie chart with missing values."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="pie",
            data={"categories": ["A", "B", "C"]},
        )
        assert "require 'categories' and 'values'" in result

        manager.clear_all()


class TestScatterBubbleCharts:
    """Tests for scatter and bubble chart types."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_scatter_chart(self, chart_tools) -> None:
        """Test adding a scatter chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="scatter",
            data={
                "series": [
                    {"name": "Dataset 1", "x_values": [1, 2, 3, 4, 5], "y_values": [2, 4, 6, 8, 10]}
                ]
            },
            title="Correlation",
        )
        assert "Added scatter chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_scatter_chart_missing_series(self, chart_tools) -> None:
        """Test scatter chart with missing series."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="scatter",
            data={"categories": ["A", "B"]},
        )
        assert "Scatter charts require 'series'" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_bubble_chart(self, chart_tools) -> None:
        """Test adding a bubble chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="bubble",
            data={
                "series": [{"name": "Markets", "points": [[10, 20, 5], [15, 25, 8], [20, 30, 12]]}]
            },
            title="Bubble Analysis",
        )
        assert "Added bubble chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_bubble_chart_invalid_point(self, chart_tools) -> None:
        """Test bubble chart with invalid point format."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="bubble",
            data={
                "series": [
                    {
                        "name": "Invalid",
                        "points": [[10, 20]],  # Missing size value
                    }
                ]
            },
        )
        assert "Bubble chart points must be [x, y, size]" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_bubble_chart_missing_series(self, chart_tools) -> None:
        """Test bubble chart with missing series."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="bubble",
            data={"categories": ["A"]},
        )
        assert "Bubble charts require 'series'" in result

        manager.clear_all()


class TestRadarCharts:
    """Tests for radar chart types."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_radar_chart(self, chart_tools) -> None:
        """Test adding a radar chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="radar",
            data={
                "categories": ["Speed", "Reliability", "Comfort", "Design"],
                "series": {"Model A": [8, 7, 9, 8], "Model B": [7, 9, 7, 6]},
            },
            title="Product Comparison",
        )
        assert "Added radar chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_radar_filled_chart(self, chart_tools) -> None:
        """Test adding a filled radar chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="radar_filled",
            data={"categories": ["A", "B", "C", "D"], "series": {"Test": [5, 6, 7, 8]}},
        )
        assert "Added radar_filled chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_radar_chart_missing_data(self, chart_tools) -> None:
        """Test radar chart with missing data."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="radar",
            data={"series": {"Test": [1, 2, 3]}},
        )
        assert "Radar charts require 'categories' and 'series'" in result

        manager.clear_all()


class TestWaterfallCharts:
    """Tests for waterfall chart type."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_add_waterfall_chart(self, chart_tools) -> None:
        """Test adding a waterfall chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="waterfall",
            data={
                "categories": ["Start", "Sales", "Costs", "Tax", "End"],
                "values": [100, 50, -30, -10, 110],
            },
            title="Financial Flow",
        )
        assert "Added waterfall chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_waterfall_chart_missing_values(self, chart_tools) -> None:
        """Test waterfall chart with missing values."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="waterfall",
            data={"categories": ["A", "B", "C"]},
        )
        assert "Waterfall charts require 'categories' and 'values'" in result

        manager.clear_all()


class TestChartOptions:
    """Tests for chart options."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_chart_with_legend_options(self, chart_tools) -> None:
        """Test chart with legend options."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A", "B"], "series": {"X": [1, 2], "Y": [3, 4]}},
            options={"show_legend": True, "legend_position": "bottom"},
        )
        assert "Added column chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_chart_without_legend(self, chart_tools) -> None:
        """Test chart with legend disabled."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
            options={"show_legend": False},
        )
        assert "Added column chart" in result

        manager.clear_all()


class TestChartPositioning:
    """Tests for chart positioning and validation."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_chart_custom_position(self, chart_tools) -> None:
        """Test chart with custom position."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
            left=2.0,
            top=3.0,
            width=6.0,
            height=4.0,
        )
        assert "Added column chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_chart_invalid_position_values(self, chart_tools) -> None:
        """Test chart with invalid position values."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
            left="invalid",  # type: ignore
            top=2.0,
            width=6.0,
            height=4.0,
        )
        assert "Position/size parameters must be numbers" in result

        manager.clear_all()


class TestChartWithTheme:
    """Tests for chart with theme applied."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_chart_with_theme(self, chart_tools) -> None:
        """Test adding chart to themed presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="themed", theme="dark-violet")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A", "B"], "series": {"Values": [10, 20]}},
            title="Themed Chart",
        )
        assert "Added column chart" in result

        manager.clear_all()


class TestPptxGetChartStyle:
    """Tests for pptx_get_chart_style tool."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_get_corporate_style(self, chart_tools) -> None:
        """Test getting corporate chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="corporate")
        data = json.loads(result)

        assert "colors" in data
        assert "description" in data
        assert "corporate" in data["description"].lower() or data["preset_name"] == "corporate"

    @pytest.mark.asyncio
    async def test_get_vibrant_style(self, chart_tools) -> None:
        """Test getting vibrant chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="vibrant")
        data = json.loads(result)

        assert "colors" in data
        assert len(data["colors"]) > 0

    @pytest.mark.asyncio
    async def test_get_pastel_style(self, chart_tools) -> None:
        """Test getting pastel chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="pastel")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_monochrome_blue_style(self, chart_tools) -> None:
        """Test getting monochrome blue chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="monochrome_blue")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_monochrome_green_style(self, chart_tools) -> None:
        """Test getting monochrome green chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="monochrome_green")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_earthy_style(self, chart_tools) -> None:
        """Test getting earthy chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="earthy")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_cool_style(self, chart_tools) -> None:
        """Test getting cool chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="cool")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_warm_style(self, chart_tools) -> None:
        """Test getting warm chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="warm")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_rainbow_style(self, chart_tools) -> None:
        """Test getting rainbow chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="rainbow")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_status_style(self, chart_tools) -> None:
        """Test getting status chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="status")
        data = json.loads(result)

        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_invalid_style(self, chart_tools) -> None:
        """Test getting invalid chart style."""
        result = await chart_tools["pptx_get_chart_style"](style_preset="nonexistent")
        data = json.loads(result)

        assert "error" in data
        assert "Invalid style_preset" in data["error"]


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_chart_invalid_json_options(self, chart_tools) -> None:
        """Test chart with invalid JSON options string."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        # Pass invalid JSON options string - should be handled gracefully
        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
            options="not-valid-json{",
        )
        # Should still succeed with default options
        assert "Added column chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_chart_overlap_detection(self, chart_tools) -> None:
        """Test chart overlap warning detection."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        # Add first chart
        result1 = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
            left=1.0,
            top=2.0,
            width=4.0,
            height=3.0,
        )
        assert "Added column chart" in result1

        # Add second chart that overlaps
        result2 = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="pie",
            data={"categories": ["A"], "values": [100]},
            left=2.0,  # Overlapping position
            top=2.5,
            width=4.0,
            height=3.0,
        )
        # May contain overlap warning
        assert "Added pie chart" in result2

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_chart_position_adjustment(self, chart_tools) -> None:
        """Test chart position adjustment for out-of-bounds values."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        # Use extreme position values that will be adjusted
        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
            left=15.0,  # Too far right
            top=10.0,  # Too far down
            width=12.0,  # Too wide
            height=10.0,  # Too tall
        )
        # Should succeed with position adjustment note
        assert "Added column chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_radar_chart_with_legend_options(self, chart_tools) -> None:
        """Test radar chart with legend options."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="radar",
            data={"categories": ["A", "B", "C", "D"], "series": {"Test": [5, 6, 7, 8]}},
            title="Radar with Legend",
            options={"show_legend": False},
        )
        assert "Added radar chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_bubble_chart_without_title(self, chart_tools) -> None:
        """Test bubble chart without title."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="bubble",
            data={"series": [{"name": "Data", "points": [[1, 2, 3], [4, 5, 6]]}]},
            # No title
        )
        assert "Added bubble chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_waterfall_chart_with_zero_values(self, chart_tools) -> None:
        """Test waterfall chart with zero values."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="waterfall",
            data={
                "categories": ["Start", "No Change", "Up", "Down", "End"],
                "values": [100, 0, 50, -30, 120],
            },
            title="Waterfall with Zeros",
        )
        assert "Added waterfall chart" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_chart_negative_slide_index(self, chart_tools) -> None:
        """Test chart with negative slide index."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await chart_tools["pptx_add_chart"](
            slide_index=-1,
            chart_type="column",
            data={"categories": ["A"], "series": {"X": [1]}},
        )
        assert "out of range" in result

        manager.clear_all()


class TestIntegration:
    """Integration tests for chart tools."""

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_multiple_charts_on_different_slides(self, chart_tools) -> None:
        """Test adding multiple charts on different slides."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_add_title_slide,
            pptx_add_slide,
            manager,
        )

        manager.clear_all()
        await pptx_create(name="multi_chart")
        await pptx_add_title_slide(title="Chart Presentation")
        await pptx_add_slide(title="Slide 2", content=["Content"])
        await pptx_add_slide(title="Slide 3", content=["Content"])

        # Add different chart types
        result1 = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A", "B"], "series": {"X": [1, 2]}},
        )
        assert "Added column chart" in result1

        result2 = await chart_tools["pptx_add_chart"](
            slide_index=1,
            chart_type="pie",
            data={"categories": ["A", "B"], "values": [60, 40]},
        )
        assert "Added pie chart" in result2

        result3 = await chart_tools["pptx_add_chart"](
            slide_index=2,
            chart_type="line",
            data={"categories": ["Q1", "Q2"], "series": {"Trend": [10, 20]}},
        )
        assert "Added line chart" in result3

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_chart_with_style_preset(self, chart_tools) -> None:
        """Test using chart style preset with chart creation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="styled_chart")
        await pptx_add_title_slide(title="Styled Chart")

        # Get style preset
        style_result = await chart_tools["pptx_get_chart_style"](style_preset="corporate")
        style_data = json.loads(style_result)

        # Create chart with colors from preset
        result = await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A", "B", "C"], "series": {"Values": [10, 20, 30]}},
            options={"colors": style_data["colors"]},
        )
        assert "Added column chart" in result

        manager.clear_all()
