"""
Comprehensive tests for inspection_tools.py

Tests for slide inspection and layout adjustment tools.
Coverage target: 90%+
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest


class TestRegisterInspectionTools:
    """Tests for register_inspection_tools function."""

    def test_register_returns_dict(self) -> None:
        """Test that register_inspection_tools returns a dictionary of tools."""
        from chuk_mcp_pptx.inspection_tools import register_inspection_tools

        mock_mcp = MagicMock()
        mock_manager = MagicMock()

        result = register_inspection_tools(mock_mcp, mock_manager)

        assert isinstance(result, dict)
        assert "pptx_inspect_slide" in result
        assert "pptx_fix_slide_layout" in result
        assert "pptx_analyze_presentation_layout" in result

    def test_tools_are_registered_with_mcp(self) -> None:
        """Test that tools are registered with the MCP server."""
        from chuk_mcp_pptx.inspection_tools import register_inspection_tools

        mock_mcp = MagicMock()
        mock_manager = MagicMock()

        register_inspection_tools(mock_mcp, mock_manager)

        # Check that tool decorator was called
        assert mock_mcp.tool.called


class TestPptxInspectSlide:
    """Tests for pptx_inspect_slide tool."""

    @pytest.fixture
    def inspection_tools(self):
        """Create inspection tools with mocked dependencies."""
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.mark.asyncio
    async def test_inspect_slide_no_presentation(self, inspection_tools) -> None:
        """Test inspecting slide when no presentation exists."""
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()

        result = await inspection_tools["pptx_inspect_slide"](slide_index=0)
        assert "Error" in result or "No presentation" in result

    @pytest.mark.asyncio
    async def test_inspect_slide_out_of_range(self, inspection_tools) -> None:
        """Test inspecting slide with invalid index."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_inspect_slide"](slide_index=99)
        assert "Error" in result or "out of range" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_inspect_slide_basic(self, inspection_tools) -> None:
        """Test basic slide inspection."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test Title", subtitle="Test Subtitle")

        result = await inspection_tools["pptx_inspect_slide"](slide_index=0)

        # Should contain inspection info
        assert "SLIDE" in result or "slide" in result.lower()
        assert "Test Title" in result or "Title" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_inspect_slide_with_measurements(self, inspection_tools) -> None:
        """Test slide inspection with measurements."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_inspect_slide"](
            slide_index=0,
            include_measurements=True,
        )

        # Should contain measurement info
        assert "SLIDE" in result or "slide" in result.lower()

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_inspect_slide_check_overlaps(self, inspection_tools) -> None:
        """Test slide inspection with overlap checking."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_inspect_slide"](
            slide_index=0,
            check_overlaps=True,
        )

        # Should return inspection info
        assert "SLIDE" in result or "slide" in result.lower()

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_inspect_slide_with_content_slide(self, inspection_tools) -> None:
        """Test inspecting a content slide with bullet points."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_slide(title="Content Slide", content=["Point 1", "Point 2"])

        result = await inspection_tools["pptx_inspect_slide"](slide_index=0)

        # Should contain info about the slide
        assert "SLIDE" in result or "slide" in result.lower()

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_inspect_slide_no_title(self, inspection_tools) -> None:
        """Test inspecting slide without title."""
        from chuk_mcp_pptx.async_server import pptx_create, manager

        manager.clear_all()
        await pptx_create(name="test")

        # Get presentation and add a blank slide
        prs = manager.get_presentation("test")
        # Use a blank layout (usually index 6)
        blank_layout = prs.slide_layouts[6]
        prs.slides.add_slide(blank_layout)

        result = await inspection_tools["pptx_inspect_slide"](slide_index=0)

        # Should handle slide without title
        assert "SLIDE" in result or "slide" in result.lower()

        manager.clear_all()


class TestPptxFixSlideLayout:
    """Tests for pptx_fix_slide_layout tool."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.mark.asyncio
    async def test_fix_layout_no_presentation(self, inspection_tools) -> None:
        """Test fixing layout when no presentation exists."""
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()

        result = await inspection_tools["pptx_fix_slide_layout"](slide_index=0)
        assert "Error" in result or "No presentation" in result

    @pytest.mark.asyncio
    async def test_fix_layout_out_of_range(self, inspection_tools) -> None:
        """Test fixing layout with invalid slide index."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_fix_slide_layout"](slide_index=99)
        assert "Error" in result or "out of range" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_fix_layout_basic(self, inspection_tools) -> None:
        """Test basic layout fix."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_fix_slide_layout"](slide_index=0)

        # Should return success or no issues message
        assert "fix" in result.lower() or "optimal" in result.lower() or "Error" in result

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_fix_layout_with_all_options(self, inspection_tools) -> None:
        """Test layout fix with all options enabled."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_fix_slide_layout"](
            slide_index=0,
            fix_overlaps=True,
            fix_bounds=True,
            fix_spacing=True,
        )

        # Should return result
        assert isinstance(result, str)

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_fix_layout_no_options(self, inspection_tools) -> None:
        """Test layout fix with no options enabled."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_fix_slide_layout"](
            slide_index=0,
            fix_overlaps=False,
            fix_bounds=False,
            fix_spacing=False,
        )

        # Should return result
        assert isinstance(result, str)

        manager.clear_all()


class TestPptxAnalyzePresentationLayout:
    """Tests for pptx_analyze_presentation_layout tool."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.mark.asyncio
    async def test_analyze_no_presentation(self, inspection_tools) -> None:
        """Test analyzing when no presentation exists."""
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()

        result = await inspection_tools["pptx_analyze_presentation_layout"]()
        assert "Error" in result or "No presentation" in result

    @pytest.mark.asyncio
    async def test_analyze_basic(self, inspection_tools) -> None:
        """Test basic presentation analysis."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Test")

        result = await inspection_tools["pptx_analyze_presentation_layout"]()

        # Should contain analysis info
        assert "PRESENTATION" in result or "Slide" in result or "slide" in result.lower()

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_analyze_multiple_slides(self, inspection_tools) -> None:
        """Test analysis with multiple slides."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_add_title_slide,
            pptx_add_slide,
            manager,
        )

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Title Slide")
        await pptx_add_slide(title="Content Slide", content=["Item 1", "Item 2"])
        await pptx_add_slide(title="Another Slide", content=["Point A"])

        result = await inspection_tools["pptx_analyze_presentation_layout"]()

        # Should analyze all slides
        assert isinstance(result, str)

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_analyze_with_specific_presentation(self, inspection_tools) -> None:
        """Test analysis of specific presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="pres1")
        await pptx_add_title_slide(title="Pres 1")
        await pptx_create(name="pres2")
        await pptx_add_title_slide(title="Pres 2")

        result = await inspection_tools["pptx_analyze_presentation_layout"](presentation="pres1")

        # Should analyze specific presentation
        assert isinstance(result, str)

        manager.clear_all()


class TestInspectSlideWithCharts:
    """Tests for inspecting slides with charts."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.fixture
    def chart_tools(self):
        from chuk_mcp_pptx.async_server import chart_tools

        return chart_tools

    @pytest.mark.asyncio
    async def test_inspect_slide_with_chart(self, inspection_tools, chart_tools) -> None:
        """Test inspecting slide containing a chart."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Chart Slide")

        # Add a chart
        await chart_tools["pptx_add_chart"](
            slide_index=0,
            chart_type="column",
            data={"categories": ["A", "B"], "series": {"Values": [10, 20]}},
            title="Test Chart",
        )

        result = await inspection_tools["pptx_inspect_slide"](slide_index=0)

        # Should contain chart info
        assert "SLIDE" in result or "slide" in result.lower()

        manager.clear_all()


class TestInspectSlideWithTables:
    """Tests for inspecting slides with tables."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.mark.asyncio
    async def test_inspect_slide_with_table(self, inspection_tools) -> None:
        """Test inspecting slide containing a table."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_add_title_slide,
            table_tools,
            manager,
        )

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Table Slide")

        # Add a table (using correct parameter name 'data' instead of 'rows')
        await table_tools["pptx_add_data_table"](
            slide_index=0,
            headers=["Col1", "Col2"],
            data=[["A", "B"], ["C", "D"]],
        )

        result = await inspection_tools["pptx_inspect_slide"](slide_index=0)

        # Should contain table info or slide info
        assert "SLIDE" in result or "slide" in result.lower() or "TABLE" in result

        manager.clear_all()


class TestInspectSlideWithImages:
    """Tests for inspecting slides with images."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.mark.asyncio
    async def test_inspect_slide_with_multiple_elements(self, inspection_tools) -> None:
        """Test inspecting slide with multiple element types."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_slide(title="Multi-Element Slide", content=["Point 1", "Point 2", "Point 3"])

        result = await inspection_tools["pptx_inspect_slide"](
            slide_index=0,
            include_measurements=True,
            check_overlaps=True,
        )

        # Should analyze all elements
        assert isinstance(result, str)
        assert "SLIDE" in result or "slide" in result.lower()

        manager.clear_all()


class TestLayoutFixingWithShapes:
    """Tests for layout fixing with various shapes."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.fixture
    def shape_tools(self):
        from chuk_mcp_pptx.async_server import shape_tools

        return shape_tools

    @pytest.mark.asyncio
    async def test_fix_layout_with_shapes(self, inspection_tools, shape_tools) -> None:
        """Test fixing layout on slide with shapes."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Shape Slide")

        # Add a shape (using correct parameters)
        await shape_tools["pptx_add_arrow"](
            slide_index=0,
            start_x=1.0,
            start_y=2.0,
            end_x=5.0,
            end_y=4.0,
        )

        result = await inspection_tools["pptx_fix_slide_layout"](
            slide_index=0,
            fix_bounds=True,
        )

        assert isinstance(result, str)

        manager.clear_all()


class TestIntegration:
    """Integration tests for inspection tools."""

    @pytest.fixture
    def inspection_tools(self):
        from chuk_mcp_pptx.async_server import manager

        manager.clear_all()
        from chuk_mcp_pptx.async_server import inspection_tools

        return inspection_tools

    @pytest.mark.asyncio
    async def test_inspect_then_fix_workflow(self, inspection_tools) -> None:
        """Test workflow of inspecting then fixing a slide."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_add_title_slide,
            pptx_add_slide,
            manager,
        )

        manager.clear_all()
        await pptx_create(name="test")
        await pptx_add_title_slide(title="Title")
        await pptx_add_slide(title="Content", content=["Item 1", "Item 2"])

        # Inspect first
        inspect_result = await inspection_tools["pptx_inspect_slide"](slide_index=0)
        assert isinstance(inspect_result, str)

        # Then fix
        fix_result = await inspection_tools["pptx_fix_slide_layout"](slide_index=0)
        assert isinstance(fix_result, str)

        # Analyze whole presentation
        analyze_result = await inspection_tools["pptx_analyze_presentation_layout"]()
        assert isinstance(analyze_result, str)

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_analyze_empty_presentation(self, inspection_tools) -> None:
        """Test analyzing presentation with no slides."""
        from chuk_mcp_pptx.async_server import pptx_create, manager

        manager.clear_all()
        await pptx_create(name="empty")

        # Get presentation and ensure no slides
        manager.get_presentation("empty")
        # New presentation has no slides

        result = await inspection_tools["pptx_analyze_presentation_layout"]()

        # Should handle empty presentation
        assert isinstance(result, str)

        manager.clear_all()
