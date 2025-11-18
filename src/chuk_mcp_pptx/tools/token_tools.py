# src/chuk_mcp_pptx/tools/token_tools.py
"""
MCP tools for design token management.
Provides access to colors, typography, spacing, and other design tokens.
"""

import asyncio
import json
from ..tokens.colors import PALETTE, get_semantic_tokens
from ..tokens.typography import (
    FONT_FAMILIES,
    FONT_SIZES,
    FONT_WEIGHTS,
    LINE_HEIGHTS,
    get_text_style,
)
from ..tokens.spacing import SPACING, PADDING, MARGINS, RADIUS


def register_token_tools(mcp, manager):
    """
    Register design token tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        manager: PresentationManager instance (not used but kept for consistency)

    Returns:
        Dictionary of registered tools
    """
    tools = {}

    @mcp.tool
    async def pptx_get_color_palette() -> str:
        """
        Get the complete color palette with all available colors.

        Returns all color hues and shades available in the design system.
        Useful for understanding what colors are available for theming.

        Returns:
            JSON with complete color palette

        Example:
            palette = await pptx_get_color_palette()
            # Returns all colors organized by hue and shade
        """

        def _get_palette():
            return json.dumps(
                {
                    "palette": PALETTE,
                    "hues": list(PALETTE.keys()),
                    "shades": [
                        "50",
                        "100",
                        "200",
                        "300",
                        "400",
                        "500",
                        "600",
                        "700",
                        "800",
                        "900",
                        "950",
                    ],
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get_palette)

    @mcp.tool
    async def pptx_get_semantic_colors(primary_hue: str = "blue", mode: str = "dark") -> str:
        """
        Get semantic color tokens for a specific theme configuration.

        Returns semantic colors (background, foreground, primary, secondary, etc.)
        for a given primary hue and mode (dark/light).

        Args:
            primary_hue: Primary color hue (blue, violet, green, orange, purple, etc.)
            mode: Color mode (dark or light)

        Returns:
            JSON with semantic color tokens

        Example:
            colors = await pptx_get_semantic_colors(primary_hue="violet", mode="dark")
            # Returns semantic tokens like background, foreground, primary, etc.
        """

        def _get_semantic():
            try:
                tokens = get_semantic_tokens(primary_hue, mode)
                return json.dumps(
                    {"primary_hue": primary_hue, "mode": mode, "tokens": tokens}, indent=2
                )
            except Exception as e:
                return json.dumps(
                    {
                        "error": str(e),
                        "hint": "Use valid primary_hue (blue, violet, green, etc.) and mode (dark, light)",
                    }
                )

        return await asyncio.get_event_loop().run_in_executor(None, _get_semantic)

    @mcp.tool
    async def pptx_get_typography_tokens() -> str:
        """
        Get typography design tokens.

        Returns font families, sizes, weights, and line heights available
        in the design system.

        Returns:
            JSON with typography tokens

        Example:
            typography = await pptx_get_typography_tokens()
            # Returns font families, sizes, weights, and line heights
        """

        def _get_typography():
            return json.dumps(
                {
                    "font_families": FONT_FAMILIES,
                    "font_sizes": FONT_SIZES,
                    "font_weights": FONT_WEIGHTS,
                    "line_heights": LINE_HEIGHTS,
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get_typography)

    @mcp.tool
    async def pptx_get_text_style(variant: str = "body") -> str:
        """
        Get a specific text style configuration.

        Returns the complete style configuration for a text variant
        including font family, size, weight, and line height.

        Args:
            variant: Text style variant (h1, h2, h3, h4, body, small, caption, etc.)

        Returns:
            JSON with text style configuration

        Example:
            style = await pptx_get_text_style(variant="h1")
            # Returns font configuration for h1 headings
        """

        def _get_style():
            try:
                style = get_text_style(variant)
                return json.dumps({"variant": variant, "style": style}, indent=2)
            except Exception as e:
                return json.dumps(
                    {
                        "error": str(e),
                        "hint": "Use valid variant (h1, h2, h3, h4, body, small, caption)",
                    }
                )

        return await asyncio.get_event_loop().run_in_executor(None, _get_style)

    @mcp.tool
    async def pptx_get_spacing_tokens() -> str:
        """
        Get spacing design tokens.

        Returns spacing scale, padding presets, margins, and border radius
        values available in the design system.

        Returns:
            JSON with spacing tokens

        Example:
            spacing = await pptx_get_spacing_tokens()
            # Returns spacing scale, padding, margins, and radius values
        """

        def _get_spacing():
            return json.dumps(
                {"spacing": SPACING, "padding": PADDING, "margins": MARGINS, "radius": RADIUS},
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get_spacing)

    @mcp.tool
    async def pptx_get_all_tokens() -> str:
        """
        Get all design tokens in one call.

        Returns the complete set of design tokens including colors,
        typography, and spacing.

        Returns:
            JSON with all design tokens

        Example:
            tokens = await pptx_get_all_tokens()
            # Returns complete token system
        """

        def _get_all():
            return json.dumps(
                {
                    "colors": {"palette": PALETTE, "hues": list(PALETTE.keys())},
                    "typography": {
                        "font_families": FONT_FAMILIES,
                        "font_sizes": FONT_SIZES,
                        "font_weights": FONT_WEIGHTS,
                        "line_heights": LINE_HEIGHTS,
                    },
                    "spacing": {
                        "spacing": SPACING,
                        "padding": PADDING,
                        "margins": MARGINS,
                        "radius": RADIUS,
                    },
                },
                indent=2,
            )

        return await asyncio.get_event_loop().run_in_executor(None, _get_all)

    # pptx_create_custom_theme has been moved to tools/theme_tools.py for better organization
    # Use: pptx_create_custom_theme (from theme_tools)

    # Store tools for return
    tools["pptx_get_color_palette"] = pptx_get_color_palette
    tools["pptx_get_semantic_colors"] = pptx_get_semantic_colors
    tools["pptx_get_typography_tokens"] = pptx_get_typography_tokens
    tools["pptx_get_text_style"] = pptx_get_text_style
    tools["pptx_get_spacing_tokens"] = pptx_get_spacing_tokens
    tools["pptx_get_all_tokens"] = pptx_get_all_tokens

    return tools
