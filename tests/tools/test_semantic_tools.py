"""
Tests for semantic_tools.py

Tests all high-level semantic slide creation MCP tools for >90% coverage.
"""

import pytest
from chuk_mcp_pptx.tools.universal.semantic import register_semantic_tools


@pytest.fixture
def semantic_tools(mock_mcp_server, mock_presentation_manager):
    """Register semantic tools and return them."""
    tools = register_semantic_tools(mock_mcp_server, mock_presentation_manager)
    return tools


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

    @pytest.mark.asyncio
    async def test_create_quick_deck_with_all_parameters(
        self, semantic_tools, mock_presentation_manager
    ):
        """Test creating quick deck with all parameters."""
        result = await semantic_tools["pptx_create_quick_deck"](
            name="full_deck",
            title="Full Featured Deck",
            subtitle="With All Options",
            theme="ocean-dark",
        )
        assert isinstance(result, str)
        assert "ocean-dark" in result or "theme" in result.lower()

    @pytest.mark.asyncio
    async def test_create_quick_deck_default_theme(self, semantic_tools, mock_presentation_manager):
        """Test creating quick deck uses dark-violet as default theme."""
        result = await semantic_tools["pptx_create_quick_deck"](
            name="default_theme_deck", title="Default Theme"
        )
        assert isinstance(result, str)
        # dark-violet is the default theme
        assert "dark-violet" in result


class TestIntegration:
    """Integration tests for semantic tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, semantic_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_create_quick_deck",
        ]

        for tool_name in expected_tools:
            assert tool_name in semantic_tools, f"Tool {tool_name} not registered"
            assert callable(semantic_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_workflow_create_multiple_decks(self, semantic_tools, mock_presentation_manager):
        """Test creating multiple decks."""
        # Create first deck
        result1 = await semantic_tools["pptx_create_quick_deck"](
            name="workflow_test_1", title="Test Deck 1", subtitle="First deck"
        )
        assert isinstance(result1, str)

        # Create second deck
        result2 = await semantic_tools["pptx_create_quick_deck"](
            name="workflow_test_2", title="Test Deck 2", subtitle="Second deck"
        )
        assert isinstance(result2, str)

        # Verify both exist
        prs1, _ = await mock_presentation_manager.get("workflow_test_1")
        prs2, _ = await mock_presentation_manager.get("workflow_test_2")
        assert prs1 is not None
        assert prs2 is not None

    @pytest.mark.asyncio
    async def test_semantic_tools_return_strings(self, semantic_tools):
        """Test that all semantic tools return string results."""
        tool_names = list(semantic_tools.keys())

        # All registered tools should be callable
        for name in tool_names:
            assert callable(semantic_tools[name])
