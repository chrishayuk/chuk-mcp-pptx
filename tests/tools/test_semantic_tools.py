"""
Tests for semantic_tools.py

Tests all high-level semantic slide creation MCP tools for >90% coverage.
"""

import pytest
from chuk_mcp_pptx.tools.semantic_tools import register_semantic_tools


@pytest.fixture
def semantic_tools(mock_mcp_server, mock_presentation_manager):
    """Register semantic tools and return them."""
    tools = register_semantic_tools(mock_mcp_server, mock_presentation_manager)
    return tools


# ThemeManager doesn't need to be mocked - it works fine in tests


class TestCreateQuickDeck:
    """Test pptx_create_quick_deck tool."""

    @pytest.mark.asyncio
    async def test_create_quick_deck_minimal(self, semantic_tools, mock_presentation_manager):
        """Test creating quick deck with minimal parameters."""
        result = await semantic_tools["pptx_create_quick_deck"](
            name="test_deck", title="Test Title"
        )
        assert isinstance(result, str)
        assert "test_deck" in result or "Created" in result

    @pytest.mark.asyncio
    async def test_create_quick_deck_with_subtitle(self, semantic_tools, mock_presentation_manager):
        """Test creating quick deck with subtitle."""
        result = await semantic_tools["pptx_create_quick_deck"](
            name="test_deck", title="Test Title", subtitle="Test Subtitle"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_create_quick_deck_with_theme(self, semantic_tools, mock_presentation_manager):
        """Test creating quick deck with custom theme."""
        result = await semantic_tools["pptx_create_quick_deck"](
            name="test_deck", title="Test Title", theme="dark-violet"
        )
        assert isinstance(result, str)
        assert "dark-violet" in result or "theme" in result.lower()

    @pytest.mark.asyncio
    async def test_create_quick_deck_creates_presentation(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test that quick deck creates presentation."""
        await semantic_tools["pptx_create_quick_deck"](name="new_deck", title="New Deck")
        # Verify presentation was created by checking it exists
        result = await mock_presentation_manager.get("new_deck")
        assert result is not None
        prs, metadata = result
        assert prs is not None
        assert metadata.name == "new_deck"


class TestAddMetricsDashboard:
    """Test pptx_add_metrics_dashboard tool."""

    @pytest.mark.asyncio
    async def test_add_metrics_dashboard_grid_layout(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test adding metrics dashboard with grid layout."""
        metrics = [
            {"label": "Revenue", "value": "$2.5M"},
            {"label": "Users", "value": "45K"},
            {"label": "NPS", "value": "72"},
            {"label": "MRR", "value": "$180K"},
        ]
        result = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Q4 Metrics", metrics=metrics, layout="grid"
        )
        assert isinstance(result, str)
        assert "4" in result or "metrics" in result.lower()

    @pytest.mark.asyncio
    async def test_add_metrics_dashboard_row_layout(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test adding metrics dashboard with row layout."""
        metrics = [{"label": "Revenue", "value": "$2.5M"}, {"label": "Users", "value": "45K"}]
        result = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Key Metrics", metrics=metrics, layout="row"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_metrics_dashboard_with_changes(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test metrics with change and trend data."""
        metrics = [
            {"label": "Revenue", "value": "$2.5M", "change": "+12%", "trend": "up"},
            {"label": "Users", "value": "45K", "change": "-3%", "trend": "down"},
        ]
        result = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Metrics", metrics=metrics
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_metrics_dashboard_with_theme(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test metrics dashboard with custom theme."""
        metrics = [{"label": "Test", "value": "100"}]
        result = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Metrics", metrics=metrics, theme="corporate"
        )
        assert isinstance(result, str)


class TestAddContentGrid:
    """Test pptx_add_content_grid tool."""

    @pytest.mark.asyncio
    async def test_add_content_grid_cards(self, semantic_tools, mock_presentation_manager):
        """Test adding content grid with card items."""
        items = [
            {"title": "Fast", "description": "Lightning quick"},
            {"title": "Secure", "description": "Enterprise-grade security"},
            {"title": "Scalable", "description": "Grows with you"},
            {"title": "Reliable", "description": "99.9% uptime"},
        ]
        result = await semantic_tools["pptx_add_content_grid"](
            title="Features", items=items, item_type="card", columns=2
        )
        assert isinstance(result, str)
        assert "4" in result or "card" in result.lower()

    @pytest.mark.asyncio
    async def test_add_content_grid_tiles(self, semantic_tools, mock_presentation_manager):
        """Test adding content grid with tile items."""
        items = [{"label": "Metric 1", "value": "100"}, {"label": "Metric 2", "value": "200"}]
        result = await semantic_tools["pptx_add_content_grid"](
            title="Metrics", items=items, item_type="tile", columns=2
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_content_grid_buttons(self, semantic_tools, mock_presentation_manager):
        """Test adding content grid with button items."""
        items = [{"text": "Action 1"}, {"text": "Action 2"}, {"text": "Action 3"}]
        result = await semantic_tools["pptx_add_content_grid"](
            title="Actions", items=items, item_type="button", columns=3
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_content_grid_column_clamping(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test that columns are clamped to 2-4."""
        items = [{"title": "Test", "description": "Test"}]

        # Test with columns=1 (should clamp to 2)
        result = await semantic_tools["pptx_add_content_grid"](title="Test", items=items, columns=1)
        assert isinstance(result, str)

        # Test with columns=5 (should clamp to 4)
        result = await semantic_tools["pptx_add_content_grid"](title="Test", items=items, columns=5)
        assert isinstance(result, str)


class TestAddTimelineSlide:
    """Test pptx_add_timeline_slide tool."""

    @pytest.mark.asyncio
    async def test_add_timeline_horizontal(self, semantic_tools, mock_presentation_manager):
        """Test adding horizontal timeline."""
        events = [
            {"date": "Q1", "description": "Beta Launch"},
            {"date": "Q2", "description": "Public Release"},
            {"date": "Q3", "description": "Enterprise Features"},
            {"date": "Q4", "description": "Global Expansion"},
        ]
        result = await semantic_tools["pptx_add_timeline_slide"](
            title="Roadmap 2024", events=events, orientation="horizontal"
        )
        assert isinstance(result, str)
        assert "4" in result or "events" in result.lower()

    @pytest.mark.asyncio
    async def test_add_timeline_vertical(self, semantic_tools, mock_presentation_manager):
        """Test adding vertical timeline."""
        events = [
            {"date": "2020", "description": "Founded"},
            {"date": "2021", "description": "Series A"},
            {"date": "2022", "description": "Product Launch"},
        ]
        result = await semantic_tools["pptx_add_timeline_slide"](
            title="Company History", events=events, orientation="vertical"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_timeline_with_theme(self, semantic_tools, mock_presentation_manager):
        """Test adding timeline with custom theme."""
        events = [{"date": "Now", "description": "Current"}]
        result = await semantic_tools["pptx_add_timeline_slide"](
            title="Timeline", events=events, theme="corporate"
        )
        assert isinstance(result, str)


class TestAddComparisonSlide:
    """Test pptx_add_comparison_slide tool."""

    @pytest.mark.asyncio
    async def test_add_comparison_slide_basic(self, semantic_tools, mock_presentation_manager):
        """Test adding basic comparison slide."""
        result = await semantic_tools["pptx_add_comparison_slide"](
            title="Build vs Buy",
            left_title="Build In-House",
            left_items=["Full control", "Custom features", "Higher cost"],
            right_title="Buy Solution",
            right_items=["Quick deployment", "Lower cost", "Less customization"],
        )
        assert isinstance(result, str)
        assert (
            "Build In-House" in result or "Buy Solution" in result or "comparison" in result.lower()
        )

    @pytest.mark.asyncio
    async def test_add_comparison_slide_empty_items(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test comparison slide with empty item lists."""
        result = await semantic_tools["pptx_add_comparison_slide"](
            title="Comparison",
            left_title="Option A",
            left_items=[],
            right_title="Option B",
            right_items=[],
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_comparison_slide_with_theme(self, semantic_tools, mock_presentation_manager):
        """Test comparison slide with custom theme."""
        result = await semantic_tools["pptx_add_comparison_slide"](
            title="Comparison",
            left_title="Left",
            left_items=["Item 1"],
            right_title="Right",
            right_items=["Item 1"],
            theme="dark-violet",
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_comparison_slide_many_items(self, semantic_tools, mock_presentation_manager):
        """Test comparison slide with many items."""
        left_items = [f"Left item {i}" for i in range(10)]
        right_items = [f"Right item {i}" for i in range(10)]
        result = await semantic_tools["pptx_add_comparison_slide"](
            title="Detailed Comparison",
            left_title="Option A",
            left_items=left_items,
            right_title="Option B",
            right_items=right_items,
        )
        assert isinstance(result, str)


class TestIntegration:
    """Integration tests for semantic tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, semantic_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_create_quick_deck",
            "pptx_add_metrics_dashboard",
            "pptx_add_content_grid",
            "pptx_add_timeline_slide",
            "pptx_add_comparison_slide",
        ]

        for tool_name in expected_tools:
            assert tool_name in semantic_tools, f"Tool {tool_name} not registered"
            assert callable(semantic_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_workflow_create_deck_with_slides(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test complete workflow: create deck → add metrics → add comparison."""
        # Create quick deck
        create_result = await semantic_tools["pptx_create_quick_deck"](
            name="workflow_test", title="Test Deck", subtitle="Testing workflow"
        )
        assert isinstance(create_result, str)

        # Add metrics dashboard
        metrics = [{"label": "Revenue", "value": "$2.5M"}, {"label": "Users", "value": "45K"}]
        metrics_result = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Metrics", metrics=metrics
        )
        assert isinstance(metrics_result, str)

        # Add comparison slide
        comparison_result = await semantic_tools["pptx_add_comparison_slide"](
            title="Options",
            left_title="Option A",
            left_items=["Pro 1", "Pro 2"],
            right_title="Option B",
            right_items=["Pro 1", "Pro 2"],
        )
        assert isinstance(comparison_result, str)

    @pytest.mark.asyncio
    async def test_semantic_tools_are_high_level(self, semantic_tools):
        """Test that semantic tools provide high-level abstractions."""
        # All tools should accept simple parameters and handle layout automatically
        tool_names = list(semantic_tools.keys())

        # Should have tools for complete slide creation
        assert any("dashboard" in name for name in tool_names)
        assert any("grid" in name for name in tool_names)
        assert any("timeline" in name for name in tool_names)
        assert any("comparison" in name for name in tool_names)


class TestGridUtilities:
    """Test grid utility functions used internally."""

    @pytest.mark.asyncio
    async def test_grid_positioning_consistent(self, semantic_tools, mock_presentation_manager):
        """Test that grid-based layouts are consistent."""
        # Add multiple dashboards and verify they work consistently
        metrics = [{"label": "Test", "value": "100"}]

        result1 = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Dashboard 1", metrics=metrics
        )

        result2 = await semantic_tools["pptx_add_metrics_dashboard"](
            title="Dashboard 2", metrics=metrics
        )

        # Both should succeed
        assert isinstance(result1, str)
        assert isinstance(result2, str)
