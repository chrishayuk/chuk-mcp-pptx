# src/chuk_mcp_pptx/tools/theme/management.py
"""
Theme Management Tools for PowerPoint MCP Server

Provides async MCP tools for managing and applying themes to presentations.
Consolidates all theme-related functionality including design tokens.
"""

import json
from ...tokens.colors import PALETTE, get_semantic_tokens
from ...tokens.typography import (
    FONT_FAMILIES,
    FONT_SIZES,
    FONT_WEIGHTS,
    LINE_HEIGHTS,
    get_text_style,
)
from ...tokens.spacing import SPACING, PADDING, MARGINS, RADIUS

from ...constants import (
    ErrorMessages,
)


def register_theme_tools(mcp, manager):
    """Register all theme-related tools with the MCP server."""

    from ...themes.theme_manager import ThemeManager

    @mcp.tool
    async def pptx_list_themes() -> str:
        """
        List all available themes with descriptions.

        Returns a list of built-in themes and their characteristics including
        mode (dark/light), primary colors, and font families.

        Returns:
            List of available themes and their characteristics

        Example:
            themes = await pptx_list_themes()
            # Returns:
            # Available themes:
            # • dark (dark): Primary: #3b82f6
            # • dark-violet (dark): Primary: #8b5cf6
            # • light (light): Primary: #2563eb
            # ...
        """
        theme_manager = ThemeManager()
        themes = theme_manager.list_themes()

        theme_list = []
        for theme_name in themes:
            theme_obj = theme_manager.get_theme(theme_name)
            if theme_obj is None:
                continue
            mode = theme_obj.mode
            # Access primary color through property
            primary = (
                theme_obj.primary.get("DEFAULT", "N/A")
                if isinstance(theme_obj.primary, dict)
                else "N/A"
            )
            theme_list.append(f"• {theme_name} ({mode}): Primary: {primary}")

        return "Available themes:\n" + "\n".join(theme_list)

    @mcp.tool
    async def pptx_get_theme_info(theme_name: str) -> str:
        """
        Get detailed information about a specific theme.

        Returns complete theme configuration including colors, typography,
        and usage information.

        Args:
            theme_name: Name of the theme to get info for

        Returns:
            JSON with complete theme details

        Example:
            info = await pptx_get_theme_info("dark-violet")
            # Returns theme configuration with all colors and settings
        """

        theme_manager = ThemeManager()
        info = theme_manager.get_theme_info(theme_name)

        if not info:
            return json.dumps(
                {
                    "error": f"Theme '{theme_name}' not found",
                    "hint": "Use pptx_list_themes() to see available themes",
                },
                indent=2,
            )

        return json.dumps(info, indent=2)

    @mcp.tool
    async def pptx_create_custom_theme(
        name: str = "custom",
        primary_hue: str = "blue",
        mode: str = "dark",
        font_family: str = "Inter",
    ) -> str:
        """
        Create a custom theme with specified design parameters.

        Generates a complete theme configuration based on a primary color hue,
        mode (dark/light), and font family. The theme uses the design token
        system to generate semantic colors automatically.

        Args:
            name: Theme name (e.g., "my-brand", "custom-dark")
            primary_hue: Primary color hue from palette (see pptx_get_color_palette)
                Available hues: blue, violet, green, emerald, orange, red, pink,
                purple, amber, yellow, cyan, sky, indigo, teal, lime, rose, fuchsia
            mode: Color mode - "dark" or "light"
            font_family: Font family to use throughout the theme
                Available: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins,
                Source Sans Pro, Raleway, Merriweather, Georgia, etc.

        Returns:
            JSON with complete theme configuration including all semantic colors

        Example:
            theme = await pptx_create_custom_theme(
                name="brand-theme",
                primary_hue="emerald",
                mode="dark",
                font_family="Montserrat"
            )
            # Returns theme configuration with all colors, typography, etc.

            # Use the theme with pptx_apply_theme():
            # await pptx_apply_theme(slide_index=0, theme="brand-theme")
        """

        # Validate primary_hue
        valid_hues = list(PALETTE.keys())
        if primary_hue not in valid_hues:
            return json.dumps(
                {
                    "error": f"Invalid primary_hue '{primary_hue}'",
                    "hint": f"Choose from: {', '.join(valid_hues)}",
                },
                indent=2,
            )

        # Validate mode
        if mode not in ["dark", "light"]:
            return json.dumps(
                {"error": f"Invalid mode '{mode}'", "hint": "Choose 'dark' or 'light'"},
                indent=2,
            )

        # Validate font_family
        valid_fonts = list(FONT_FAMILIES.values())
        if font_family not in valid_fonts:
            # Allow custom fonts but warn
            font_warning = f"Font '{font_family}' not in standard families. Using anyway."
        else:
            font_warning = None

        # Generate semantic tokens
        try:
            semantic_colors = get_semantic_tokens(primary_hue, mode)
        except Exception as e:
            return json.dumps({"error": f"Failed to generate theme: {str(e)}"}, indent=2)

        # Build complete theme configuration
        theme_config = {
            "name": name,
            "primary_hue": primary_hue,
            "mode": mode,
            "font_family": font_family,
            "colors": semantic_colors,
            "typography": {
                "font_family": font_family,
                "headings": {
                    "h1": get_text_style("h1"),
                    "h2": get_text_style("h2"),
                    "h3": get_text_style("h3"),
                    "h4": get_text_style("h4"),
                },
                "body": get_text_style("body"),
                "small": get_text_style("small"),
            },
            "spacing": {"padding": PADDING, "radius": RADIUS},
            "usage": {
                "description": f"Custom {mode} theme with {primary_hue} as primary color",
                "apply": "Use pptx_apply_theme() to apply this theme to slides",
                "components": "Components will automatically use these colors when theme is active",
            },
        }

        if font_warning:
            theme_config["warning"] = font_warning

        return json.dumps(theme_config, indent=2)

    @mcp.tool
    async def pptx_apply_theme(
        slide_index: int | None = None, theme: str = "dark", presentation: str | None = None
    ) -> str:
        """
        Apply a theme to slides.

        Applies background colors and default text colors from the specified theme.
        Can apply to a single slide or all slides in the presentation.

        Args:
            slide_index: Index of slide to theme (None for all slides)
            theme: Name of theme to apply (e.g., "dark", "light-violet", "corporate")
            presentation: Name of presentation (uses current if not specified)

        Returns:
            Success message confirming theme application

        Example:
            # Apply to all slides
            await pptx_apply_theme(theme="dark-violet")

            # Apply to specific slide
            await pptx_apply_theme(slide_index=0, theme="corporate")
        """
        try:
            result = await manager.get(presentation)
            if not result:
                return ErrorMessages.NO_PRESENTATION

            prs, metadata = result

            theme_manager = ThemeManager()
            available_themes = theme_manager.list_themes()

            if theme not in available_themes:
                return (
                    f"Error: Unknown theme '{theme}'. Available: {', '.join(available_themes[:10])}"
                )

            theme_obj = theme_manager.get_theme(theme)

            if theme_obj is None:
                return f"Error: Could not load theme '{theme}'"

            if slide_index is not None:
                if slide_index >= len(prs.slides):
                    return f"Error: Slide index {slide_index} out of range"
                slides = [prs.slides[slide_index]]
            else:
                slides = prs.slides

            # Apply theme to slides using the theme's built-in method
            for slide in slides:
                theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update(presentation)

            slide_msg = f"slide {slide_index}" if slide_index is not None else "all slides"
            return f"Applied {theme} theme to {slide_msg}"

        except Exception as e:
            return f"Error applying theme: {str(e)}"

    @mcp.tool
    async def pptx_apply_component_theme(
        slide_index: int,
        shape_index: int,
        theme_style: str = "card",
        presentation: str | None = None,
    ) -> str:
        """
        Apply a theme style to a specific component/shape.

        Applies theme-based styling (colors, borders) to individual shapes
        on a slide. Useful for styling cards, containers, and other components.

        Args:
            slide_index: Index of the slide containing the shape
            shape_index: Index of the shape to style
            theme_style: Style variant to apply:
                - "card": Default card styling (neutral background)
                - "primary": Primary color styling
                - "secondary": Secondary color styling
                - "accent": Accent color styling
                - "muted": Muted/subtle styling
            presentation: Name of presentation (uses current if not specified)

        Returns:
            Success message confirming style application

        Example:
            await pptx_apply_component_theme(
                slide_index=0,
                shape_index=2,
                theme_style="primary"
            )
        """
        try:
            result = await manager.get(presentation)
            if not result:
                return ErrorMessages.NO_PRESENTATION

            prs, metadata = result

            if slide_index >= len(prs.slides):
                return f"Error: Slide index {slide_index} out of range"

            slide = prs.slides[slide_index]

            if shape_index >= len(slide.shapes):
                return f"Error: Shape index {shape_index} out of range"

            shape = slide.shapes[shape_index]

            theme_manager = ThemeManager()
            theme_obj = theme_manager.get_theme("dark")  # Get default theme

            if theme_obj:
                theme_obj.apply_to_shape(shape, style=theme_style)
                await manager.update(presentation)
                return f"Applied {theme_style} theme to shape {shape_index} on slide {slide_index}"
            else:
                return "Error: No default theme available"

        except Exception as e:
            return f"Error applying component theme: {str(e)}"

    @mcp.tool
    async def pptx_list_component_themes() -> str:
        """
        List available component theme styles.

        Returns the available style variants that can be used with
        pptx_apply_component_theme().

        Returns:
            List of available component theme styles

        Example:
            themes = await pptx_list_component_themes()
            # Returns available style variants
        """
        styles = {
            "card": "Default card styling with neutral background",
            "primary": "Primary color styling (brand color)",
            "secondary": "Secondary color styling (subtle)",
            "accent": "Accent color styling (highlight)",
            "muted": "Muted styling (low emphasis)",
        }

        style_list = [f"• {name}: {desc}" for name, desc in styles.items()]
        return "Available component theme styles:\n" + "\n".join(style_list)

    # Design Token Tools
    @mcp.tool
    async def pptx_get_color_palette() -> str:
        """
        Get the complete color palette with all hues and shades.

        Returns all available colors in the design token system, organized by hue
        (blue, violet, green, etc.) with their shade variations (50-900).

        Returns:
            JSON object with complete color palette

        Example:
            palette = await pptx_get_color_palette()
            # Returns all color hues with their shade variations
            # Use these colors in components or custom themes
        """

        return json.dumps(PALETTE, indent=2)

    @mcp.tool
    async def pptx_get_semantic_colors(primary_hue: str = "blue", mode: str = "dark") -> str:
        """
        Get semantic color tokens for a specific primary hue and mode.

        Generates the complete set of semantic tokens (primary, secondary, accent,
        background, etc.) based on a primary color hue and mode (dark/light).

        Args:
            primary_hue: Primary color hue from palette (blue, violet, green, etc.)
            mode: Color mode - "dark" or "light"

        Returns:
            JSON object with all semantic color tokens

        Example:
            colors = await pptx_get_semantic_colors(primary_hue="emerald", mode="dark")
            # Returns primary, secondary, accent, background, text colors, etc.
        """

        try:
            tokens = get_semantic_tokens(primary_hue, mode)
            return json.dumps(tokens, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool
    async def pptx_get_typography_tokens() -> str:
        """
        Get all typography design tokens.

        Returns font families, sizes, weights, and line heights used throughout
        the design system.

        Returns:
            JSON object with typography tokens

        Example:
            typography = await pptx_get_typography_tokens()
            # Returns font families, sizes, weights, line heights
        """

        tokens = {
            "font_families": FONT_FAMILIES,
            "font_sizes": FONT_SIZES,
            "font_weights": FONT_WEIGHTS,
            "line_heights": LINE_HEIGHTS,
        }
        return json.dumps(tokens, indent=2)

    @mcp.tool
    async def pptx_get_text_style(variant: str = "body") -> str:
        """
        Get text style configuration for a specific variant.

        Returns complete text style config (font size, weight, line height)
        for a specific text variant.

        Args:
            variant: Text style variant - "h1", "h2", "h3", "h4", "h5", "h6",
                    "body", "small", "tiny"

        Returns:
            JSON object with text style configuration

        Example:
            style = await pptx_get_text_style(variant="h1")
            # Returns: {"size": 36, "weight": 700, "line_height": 1.2}
        """

        try:
            style = get_text_style(variant)
            return json.dumps(style, indent=2)
        except ValueError as e:
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.tool
    async def pptx_get_spacing_tokens() -> str:
        """
        Get all spacing design tokens.

        Returns spacing scale, padding values, margin values, and border radius
        values used throughout the design system.

        Returns:
            JSON object with spacing tokens

        Example:
            spacing = await pptx_get_spacing_tokens()
            # Returns spacing scale, padding, margins, radius values
        """

        tokens = {
            "spacing": SPACING,
            "padding": PADDING,
            "margins": MARGINS,
            "radius": RADIUS,
        }
        return json.dumps(tokens, indent=2)

    @mcp.tool
    async def pptx_get_all_tokens() -> str:
        """
        Get all design tokens in a single call.

        Returns the complete design token system including colors, typography,
        spacing, padding, margins, and radius values.

        Returns:
            JSON object with all design tokens

        Example:
            tokens = await pptx_get_all_tokens()
            # Returns comprehensive object with all design tokens
        """

        tokens = {
            "colors": PALETTE,
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
        }
        return json.dumps(tokens, indent=2)

    # Return all tools
    return {
        "pptx_list_themes": pptx_list_themes,
        "pptx_get_theme_info": pptx_get_theme_info,
        "pptx_create_custom_theme": pptx_create_custom_theme,
        "pptx_apply_theme": pptx_apply_theme,
        "pptx_apply_component_theme": pptx_apply_component_theme,
        "pptx_list_component_themes": pptx_list_component_themes,
        "pptx_get_color_palette": pptx_get_color_palette,
        "pptx_get_semantic_colors": pptx_get_semantic_colors,
        "pptx_get_typography_tokens": pptx_get_typography_tokens,
        "pptx_get_text_style": pptx_get_text_style,
        "pptx_get_spacing_tokens": pptx_get_spacing_tokens,
        "pptx_get_all_tokens": pptx_get_all_tokens,
    }
