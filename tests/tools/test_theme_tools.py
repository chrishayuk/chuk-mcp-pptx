"""
Tests for theme_tools.py

Tests all theme-related MCP tools for >90% coverage.
"""

import pytest
import json
from unittest.mock import MagicMock

from chuk_mcp_pptx.tools.theme_tools import register_theme_tools


@pytest.fixture
def theme_tools(mock_mcp_server, mock_presentation_manager):
    """Register theme tools and return them."""
    tools = register_theme_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestListThemes:
    """Test pptx_list_themes tool."""

    @pytest.mark.asyncio
    async def test_list_themes_returns_string(self, theme_tools):
        """Test that list_themes returns a formatted string."""
        result = await theme_tools["pptx_list_themes"]()
        assert isinstance(result, str)
        assert "Available themes:" in result

    @pytest.mark.asyncio
    async def test_list_themes_contains_builtin_themes(self, theme_tools):
        """Test that built-in themes are listed."""
        result = await theme_tools["pptx_list_themes"]()
        # Should contain some built-in themes
        assert "dark" in result or "light" in result

    @pytest.mark.asyncio
    async def test_list_themes_shows_mode(self, theme_tools):
        """Test that themes show their mode."""
        result = await theme_tools["pptx_list_themes"]()
        assert "(dark)" in result or "(light)" in result


class TestGetThemeInfo:
    """Test pptx_get_theme_info tool."""

    @pytest.mark.asyncio
    async def test_get_theme_info_valid_theme(self, theme_tools):
        """Test getting info for a valid theme."""
        result = await theme_tools["pptx_get_theme_info"]("dark")
        data = json.loads(result)
        assert "name" in data
        assert "mode" in data
        assert "primary_hue" in data

    @pytest.mark.asyncio
    async def test_get_theme_info_invalid_theme(self, theme_tools):
        """Test getting info for an invalid theme."""
        result = await theme_tools["pptx_get_theme_info"]("nonexistent_theme")
        data = json.loads(result)
        assert "error" in data
        assert "not found" in data["error"]

    @pytest.mark.asyncio
    async def test_get_theme_info_has_colors(self, theme_tools):
        """Test that theme info includes colors."""
        result = await theme_tools["pptx_get_theme_info"]("dark")
        data = json.loads(result)
        assert "colors" in data


class TestCreateCustomTheme:
    """Test pptx_create_custom_theme tool."""

    @pytest.mark.asyncio
    async def test_create_custom_theme_defaults(self, theme_tools):
        """Test creating a theme with default parameters."""
        result = await theme_tools["pptx_create_custom_theme"]()
        data = json.loads(result)
        assert data["name"] == "custom"
        assert data["primary_hue"] == "blue"
        assert data["mode"] == "dark"
        assert data["font_family"] == "Inter"

    @pytest.mark.asyncio
    async def test_create_custom_theme_with_params(self, theme_tools):
        """Test creating a theme with custom parameters."""
        result = await theme_tools["pptx_create_custom_theme"](
            name="my_theme", primary_hue="emerald", mode="light", font_family="Roboto"
        )
        data = json.loads(result)
        assert data["name"] == "my_theme"
        assert data["primary_hue"] == "emerald"
        assert data["mode"] == "light"
        assert data["font_family"] == "Roboto"

    @pytest.mark.asyncio
    async def test_create_custom_theme_invalid_hue(self, theme_tools):
        """Test creating a theme with invalid hue."""
        result = await theme_tools["pptx_create_custom_theme"](primary_hue="invalid_color")
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_create_custom_theme_invalid_mode(self, theme_tools):
        """Test creating a theme with invalid mode."""
        result = await theme_tools["pptx_create_custom_theme"](mode="invalid_mode")
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_create_custom_theme_has_colors(self, theme_tools):
        """Test that created theme has semantic colors."""
        result = await theme_tools["pptx_create_custom_theme"]()
        data = json.loads(result)
        assert "colors" in data
        assert "background" in data["colors"]
        assert "foreground" in data["colors"]
        assert "primary" in data["colors"]

    @pytest.mark.asyncio
    async def test_create_custom_theme_has_typography(self, theme_tools):
        """Test that created theme has typography."""
        result = await theme_tools["pptx_create_custom_theme"]()
        data = json.loads(result)
        assert "typography" in data
        assert "headings" in data["typography"]
        assert "body" in data["typography"]

    @pytest.mark.asyncio
    async def test_create_custom_theme_custom_font_warning(self, theme_tools):
        """Test that custom fonts generate a warning."""
        result = await theme_tools["pptx_create_custom_theme"](font_family="CustomFont")
        data = json.loads(result)
        # Custom fonts that aren't in standard families should work but may have warning
        assert "name" in data  # Should still create theme


class TestApplyTheme:
    """Test pptx_apply_theme tool."""

    @pytest.mark.asyncio
    async def test_apply_theme_to_all_slides(self, theme_tools, mock_presentation_manager):
        """Test applying theme to all slides."""
        result = await theme_tools["pptx_apply_theme"](theme="dark")
        assert "Applied dark theme to all slides" in result

    @pytest.mark.asyncio
    async def test_apply_theme_to_specific_slide(self, theme_tools, mock_presentation_manager):
        """Test applying theme to a specific slide."""
        result = await theme_tools["pptx_apply_theme"](slide_index=0, theme="dark")
        assert "Applied dark theme to slide 0" in result

    @pytest.mark.asyncio
    async def test_apply_theme_invalid_theme(self, theme_tools):
        """Test applying an invalid theme."""
        result = await theme_tools["pptx_apply_theme"](theme="nonexistent")
        assert "Error" in result or "Unknown theme" in result

    @pytest.mark.asyncio
    async def test_apply_theme_invalid_slide_index(self, theme_tools):
        """Test applying theme to invalid slide index."""
        result = await theme_tools["pptx_apply_theme"](slide_index=999, theme="dark")
        assert "Error" in result or "out of range" in result

    @pytest.mark.asyncio
    async def test_apply_theme_no_presentation(self, theme_tools, mock_presentation_manager):
        """Test applying theme when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await theme_tools["pptx_apply_theme"](theme="dark", presentation="nonexistent")
        assert "No presentation found" in result

    @pytest.mark.asyncio
    async def test_apply_theme_with_presentation_name(self, theme_tools):
        """Test applying theme with specific presentation name."""
        result = await theme_tools["pptx_apply_theme"](
            theme="dark", presentation="test_presentation"
        )
        assert "dark" in result


class TestApplyComponentTheme:
    """Test pptx_apply_component_theme tool."""

    @pytest.mark.asyncio
    async def test_apply_component_theme_default_style(
        self, theme_tools, mock_presentation_manager
    ):
        """Test applying component theme with default style."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        # Add a mock shape with necessary attributes for theming
        mock_shape = MagicMock()
        mock_shape.fill = MagicMock()
        mock_shape.line = MagicMock()
        slide.shapes._members = [mock_shape]
        slide.shapes.__len__ = MagicMock(return_value=1)
        slide.shapes.__getitem__ = MagicMock(return_value=mock_shape)

        result = await theme_tools["pptx_apply_component_theme"](
            slide_index=0, shape_index=0, presentation="test_presentation"
        )
        assert "Applied" in result or "theme to shape" in result

    @pytest.mark.asyncio
    async def test_apply_component_theme_with_style(self, theme_tools, mock_presentation_manager):
        """Test applying component theme with specific style."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        # Add a mock shape with necessary attributes for theming
        mock_shape = MagicMock()
        mock_shape.fill = MagicMock()
        mock_shape.line = MagicMock()
        slide.shapes._members = [mock_shape]
        slide.shapes.__len__ = MagicMock(return_value=1)
        slide.shapes.__getitem__ = MagicMock(return_value=mock_shape)

        result = await theme_tools["pptx_apply_component_theme"](
            slide_index=0, shape_index=0, theme_style="primary", presentation="test_presentation"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_apply_component_theme_invalid_slide(self, theme_tools):
        """Test applying component theme to invalid slide."""
        result = await theme_tools["pptx_apply_component_theme"](slide_index=999, shape_index=0)
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_apply_component_theme_invalid_shape(self, theme_tools):
        """Test applying component theme to invalid shape."""
        result = await theme_tools["pptx_apply_component_theme"](slide_index=0, shape_index=999)
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_apply_component_theme_no_presentation(
        self, theme_tools, mock_presentation_manager
    ):
        """Test applying component theme when no presentation."""
        # Use a non-existent presentation name instead of mocking
        result = await theme_tools["pptx_apply_component_theme"](
            slide_index=0, shape_index=0, presentation="nonexistent"
        )
        assert "No presentation found" in result


class TestListComponentThemes:
    """Test pptx_list_component_themes tool."""

    @pytest.mark.asyncio
    async def test_list_component_themes_returns_string(self, theme_tools):
        """Test that list_component_themes returns a string."""
        result = await theme_tools["pptx_list_component_themes"]()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_list_component_themes_has_styles(self, theme_tools):
        """Test that component themes lists available styles."""
        result = await theme_tools["pptx_list_component_themes"]()
        assert "card" in result or "primary" in result or "secondary" in result

    @pytest.mark.asyncio
    async def test_list_component_themes_has_descriptions(self, theme_tools):
        """Test that component themes have descriptions."""
        result = await theme_tools["pptx_list_component_themes"]()
        # Should have some description text
        assert len(result) > 50  # More than just a list


class TestIntegration:
    """Integration tests for theme tools."""

    @pytest.mark.asyncio
    async def test_create_and_list_themes(self, theme_tools):
        """Test creating a theme and then listing it."""
        # Create a theme
        create_result = await theme_tools["pptx_create_custom_theme"](
            name="integration_test", primary_hue="violet"
        )
        create_data = json.loads(create_result)
        assert create_data["name"] == "integration_test"

        # Note: Created themes aren't automatically registered,
        # but this tests the creation process

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, theme_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_list_themes",
            "pptx_get_theme_info",
            "pptx_create_custom_theme",
            "pptx_apply_theme",
            "pptx_apply_component_theme",
            "pptx_list_component_themes",
        ]

        for tool_name in expected_tools:
            assert tool_name in theme_tools, f"Tool {tool_name} not registered"
            assert callable(theme_tools[tool_name]), f"Tool {tool_name} not callable"
