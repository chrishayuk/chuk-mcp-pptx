"""
High-level semantic tools for LLM-friendly slide creation.

Provides quick-start convenience wrappers for common presentation patterns.
Most functionality should use the universal component API directly.
"""

from ...themes.theme_manager import ThemeManager

from ...constants import (
    SlideLayoutIndex,
)


def register_semantic_tools(mcp, manager):
    """
    Register high-level semantic tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        manager: PresentationManager instance

    Returns:
        Dictionary of registered tools
    """
    tools = {}
    theme_manager = ThemeManager()

    @mcp.tool
    async def pptx_create_quick_deck(
        name: str, title: str, subtitle: str | None = None, theme: str = "dark-violet"
    ) -> str:
        """
        Create a complete presentation with title slide in one call.

        This is the fastest way to start a presentation. Creates the presentation,
        adds a styled title slide, and sets the theme.

        Args:
            name: Presentation name
            title: Main title
            subtitle: Optional subtitle
            theme: Theme name (default: dark-violet)

        Returns:
            Success message with presentation info

        Example:
            await pptx_create_quick_deck(
                name="my_pitch",
                title="Product Launch 2024",
                subtitle="Revolutionary Innovation",
                theme="dark-violet"
            )
        """
        # Create presentation with theme in metadata
        metadata = await manager.create(name, theme=theme)
        result = await manager.get(name)
        if not result:
            raise ValueError(f"Failed to get presentation '{name}'")
        prs, metadata = result

        # Add title slide
        slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE]
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle

        # Apply theme to title slide
        theme_obj = theme_manager.get_theme(theme)
        if theme_obj:
            theme_obj.apply_to_slide(slide)

        await manager.update(name)
        return f"Created '{name}' with title slide (theme: {theme})"

    # Store tools for return
    tools.update(
        {
            "pptx_create_quick_deck": pptx_create_quick_deck,
        }
    )

    return tools
