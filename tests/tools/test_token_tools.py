"""
Tests for token_tools.py

Tests all design token MCP tools for >90% coverage.
"""

import pytest
import json
from chuk_mcp_pptx.tools.token_tools import register_token_tools


@pytest.fixture
def token_tools(mock_mcp_server, mock_presentation_manager):
    """Register token tools and return them."""
    tools = register_token_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestGetColorPalette:
    """Test pptx_get_color_palette tool."""

    @pytest.mark.asyncio
    async def test_get_color_palette_returns_json(self, token_tools):
        """Test that get_color_palette returns JSON."""
        result = await token_tools["pptx_get_color_palette"]()
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_color_palette_has_palette(self, token_tools):
        """Test that palette is included."""
        result = await token_tools["pptx_get_color_palette"]()
        data = json.loads(result)
        assert "palette" in data
        assert isinstance(data["palette"], dict)

    @pytest.mark.asyncio
    async def test_get_color_palette_has_hues(self, token_tools):
        """Test that hues list is included."""
        result = await token_tools["pptx_get_color_palette"]()
        data = json.loads(result)
        assert "hues" in data
        assert isinstance(data["hues"], list)
        assert len(data["hues"]) > 0

    @pytest.mark.asyncio
    async def test_get_color_palette_has_common_colors(self, token_tools):
        """Test that common colors are in palette."""
        result = await token_tools["pptx_get_color_palette"]()
        data = json.loads(result)
        hues = data["hues"]
        # Check for common colors
        common_colors = ["blue", "red", "green"]
        for color in common_colors:
            assert color in hues

    @pytest.mark.asyncio
    async def test_get_color_palette_has_shades(self, token_tools):
        """Test that shades are listed."""
        result = await token_tools["pptx_get_color_palette"]()
        data = json.loads(result)
        assert "shades" in data
        assert isinstance(data["shades"], list)


class TestGetSemanticColors:
    """Test pptx_get_semantic_colors tool."""

    @pytest.mark.asyncio
    async def test_get_semantic_colors_default(self, token_tools):
        """Test getting semantic colors with defaults."""
        result = await token_tools["pptx_get_semantic_colors"]()
        data = json.loads(result)
        assert "primary_hue" in data
        assert "mode" in data
        assert "tokens" in data

    @pytest.mark.asyncio
    async def test_get_semantic_colors_custom_hue(self, token_tools):
        """Test getting semantic colors with custom hue."""
        result = await token_tools["pptx_get_semantic_colors"](primary_hue="violet")
        data = json.loads(result)
        assert data["primary_hue"] == "violet"

    @pytest.mark.asyncio
    async def test_get_semantic_colors_light_mode(self, token_tools):
        """Test getting semantic colors in light mode."""
        result = await token_tools["pptx_get_semantic_colors"](mode="light")
        data = json.loads(result)
        assert data["mode"] == "light"

    @pytest.mark.asyncio
    async def test_get_semantic_colors_dark_mode(self, token_tools):
        """Test getting semantic colors in dark mode."""
        result = await token_tools["pptx_get_semantic_colors"](mode="dark")
        data = json.loads(result)
        assert data["mode"] == "dark"

    @pytest.mark.asyncio
    async def test_get_semantic_colors_has_background(self, token_tools):
        """Test that semantic colors include background."""
        result = await token_tools["pptx_get_semantic_colors"]()
        data = json.loads(result)
        assert "background" in data["tokens"]

    @pytest.mark.asyncio
    async def test_get_semantic_colors_has_primary(self, token_tools):
        """Test that semantic colors include primary."""
        result = await token_tools["pptx_get_semantic_colors"]()
        data = json.loads(result)
        assert "primary" in data["tokens"]

    @pytest.mark.asyncio
    async def test_get_semantic_colors_has_chart_colors(self, token_tools):
        """Test that semantic colors include chart colors."""
        result = await token_tools["pptx_get_semantic_colors"]()
        data = json.loads(result)
        assert "chart" in data["tokens"]
        assert isinstance(data["tokens"]["chart"], list)

    @pytest.mark.asyncio
    async def test_get_semantic_colors_invalid_inputs(self, token_tools):
        """Test getting semantic colors with potentially invalid inputs."""
        # Should still work or return helpful error
        result = await token_tools["pptx_get_semantic_colors"](
            primary_hue="invalid_color", mode="invalid_mode"
        )
        data = json.loads(result)
        # Should have error or tokens
        assert "error" in data or "tokens" in data


class TestGetTypographyTokens:
    """Test pptx_get_typography_tokens tool."""

    @pytest.mark.asyncio
    async def test_get_typography_tokens_returns_json(self, token_tools):
        """Test that get_typography_tokens returns JSON."""
        result = await token_tools["pptx_get_typography_tokens"]()
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_typography_tokens_has_font_families(self, token_tools):
        """Test that typography tokens include font families."""
        result = await token_tools["pptx_get_typography_tokens"]()
        data = json.loads(result)
        assert "font_families" in data
        assert isinstance(data["font_families"], dict)

    @pytest.mark.asyncio
    async def test_get_typography_tokens_has_font_sizes(self, token_tools):
        """Test that typography tokens include font sizes."""
        result = await token_tools["pptx_get_typography_tokens"]()
        data = json.loads(result)
        assert "font_sizes" in data
        assert isinstance(data["font_sizes"], dict)

    @pytest.mark.asyncio
    async def test_get_typography_tokens_has_font_weights(self, token_tools):
        """Test that typography tokens include font weights."""
        result = await token_tools["pptx_get_typography_tokens"]()
        data = json.loads(result)
        assert "font_weights" in data

    @pytest.mark.asyncio
    async def test_get_typography_tokens_has_line_heights(self, token_tools):
        """Test that typography tokens include line heights."""
        result = await token_tools["pptx_get_typography_tokens"]()
        data = json.loads(result)
        assert "line_heights" in data


class TestGetTextStyle:
    """Test pptx_get_text_style tool."""

    @pytest.mark.asyncio
    async def test_get_text_style_body(self, token_tools):
        """Test getting body text style."""
        result = await token_tools["pptx_get_text_style"](variant="body")
        data = json.loads(result)
        assert data["variant"] == "body"
        assert "style" in data

    @pytest.mark.asyncio
    async def test_get_text_style_h1(self, token_tools):
        """Test getting h1 text style."""
        result = await token_tools["pptx_get_text_style"](variant="h1")
        data = json.loads(result)
        assert data["variant"] == "h1"

    @pytest.mark.asyncio
    async def test_get_text_style_h2(self, token_tools):
        """Test getting h2 text style."""
        result = await token_tools["pptx_get_text_style"](variant="h2")
        data = json.loads(result)
        assert data["variant"] == "h2"

    @pytest.mark.asyncio
    async def test_get_text_style_small(self, token_tools):
        """Test getting small text style."""
        result = await token_tools["pptx_get_text_style"](variant="small")
        data = json.loads(result)
        assert data["variant"] == "small"

    @pytest.mark.asyncio
    async def test_get_text_style_caption(self, token_tools):
        """Test getting caption text style."""
        result = await token_tools["pptx_get_text_style"](variant="caption")
        data = json.loads(result)
        # Should return data or error
        assert "variant" in data or "error" in data

    @pytest.mark.asyncio
    async def test_get_text_style_invalid_variant(self, token_tools):
        """Test getting invalid text style variant."""
        result = await token_tools["pptx_get_text_style"](variant="invalid")
        data = json.loads(result)
        # Should return error or fallback to default style
        assert "error" in data or "style" in data


class TestGetSpacingTokens:
    """Test pptx_get_spacing_tokens tool."""

    @pytest.mark.asyncio
    async def test_get_spacing_tokens_returns_json(self, token_tools):
        """Test that get_spacing_tokens returns JSON."""
        result = await token_tools["pptx_get_spacing_tokens"]()
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_spacing_tokens_has_spacing(self, token_tools):
        """Test that spacing tokens include spacing scale."""
        result = await token_tools["pptx_get_spacing_tokens"]()
        data = json.loads(result)
        assert "spacing" in data

    @pytest.mark.asyncio
    async def test_get_spacing_tokens_has_padding(self, token_tools):
        """Test that spacing tokens include padding."""
        result = await token_tools["pptx_get_spacing_tokens"]()
        data = json.loads(result)
        assert "padding" in data

    @pytest.mark.asyncio
    async def test_get_spacing_tokens_has_margins(self, token_tools):
        """Test that spacing tokens include margins."""
        result = await token_tools["pptx_get_spacing_tokens"]()
        data = json.loads(result)
        assert "margins" in data

    @pytest.mark.asyncio
    async def test_get_spacing_tokens_has_radius(self, token_tools):
        """Test that spacing tokens include border radius."""
        result = await token_tools["pptx_get_spacing_tokens"]()
        data = json.loads(result)
        assert "radius" in data


class TestGetAllTokens:
    """Test pptx_get_all_tokens tool."""

    @pytest.mark.asyncio
    async def test_get_all_tokens_returns_json(self, token_tools):
        """Test that get_all_tokens returns JSON."""
        result = await token_tools["pptx_get_all_tokens"]()
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_get_all_tokens_has_colors(self, token_tools):
        """Test that all tokens include colors."""
        result = await token_tools["pptx_get_all_tokens"]()
        data = json.loads(result)
        assert "colors" in data

    @pytest.mark.asyncio
    async def test_get_all_tokens_has_typography(self, token_tools):
        """Test that all tokens include typography."""
        result = await token_tools["pptx_get_all_tokens"]()
        data = json.loads(result)
        assert "typography" in data

    @pytest.mark.asyncio
    async def test_get_all_tokens_has_spacing(self, token_tools):
        """Test that all tokens include spacing."""
        result = await token_tools["pptx_get_all_tokens"]()
        data = json.loads(result)
        assert "spacing" in data

    @pytest.mark.asyncio
    async def test_get_all_tokens_comprehensive(self, token_tools):
        """Test that all tokens is comprehensive."""
        result = await token_tools["pptx_get_all_tokens"]()
        data = json.loads(result)

        # Should have nested structures
        assert "palette" in data["colors"]
        assert "font_families" in data["typography"]
        assert "spacing" in data["spacing"]


class TestIntegration:
    """Integration tests for token tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, token_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_get_color_palette",
            "pptx_get_semantic_colors",
            "pptx_get_typography_tokens",
            "pptx_get_text_style",
            "pptx_get_spacing_tokens",
            "pptx_get_all_tokens",
        ]

        for tool_name in expected_tools:
            assert tool_name in token_tools, f"Tool {tool_name} not registered"
            assert callable(token_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_color_palette_and_semantic_colors_consistent(self, token_tools):
        """Test that palette hues work with semantic colors."""
        # Get palette
        palette_result = await token_tools["pptx_get_color_palette"]()
        palette_data = json.loads(palette_result)

        # Try first hue with semantic colors
        if palette_data["hues"]:
            first_hue = palette_data["hues"][0]
            semantic_result = await token_tools["pptx_get_semantic_colors"](primary_hue=first_hue)
            semantic_data = json.loads(semantic_result)

            # Should work without error
            assert "tokens" in semantic_data or "error" not in semantic_data
