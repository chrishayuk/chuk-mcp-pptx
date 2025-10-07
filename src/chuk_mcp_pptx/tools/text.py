"""
Text Tools for PowerPoint MCP Server

Provides async MCP tools for handling text in presentations.
Supports text extraction, formatting, and component-based text creation.
"""
import asyncio
from typing import Optional

from ..utilities.text_utils import extract_presentation_text


def register_text_tools(mcp, manager):
    """Register all text tools with the MCP server."""

    from ..components.core import TextBox, BulletList

    @mcp.tool
    async def pptx_add_text_slide(
        title: str,
        text: str,
        presentation: Optional[str] = None
    ) -> str:
        """
        Add a slide with title and text content.

        Creates a slide with a title and paragraph text. Suitable for
        descriptions, summaries, or any narrative content.

        Args:
            title: Title text for the slide
            text: Paragraph text content for the slide body
            presentation: Name of presentation to add slide to (uses current if not specified)

        Returns:
            Success message confirming slide addition

        Example:
            await pptx_add_text_slide(
                title="Executive Summary",
                text="This quarter demonstrated exceptional growth across all business units. "
                     "Revenue increased by 25% year-over-year, driven primarily by our cloud "
                     "services division."
            )
        """
        def _add_text_slide():
            prs = manager.get(presentation)
            if not prs:
                return "Error: No presentation found. Create one first with pptx_create()"

            slide_layout = prs.slide_layouts[1]  # Title and content layout
            slide = prs.slides.add_slide(slide_layout)

            slide.shapes.title.text = title

            if len(slide.placeholders) > 1:
                slide.placeholders[1].text_frame.text = text

            # Update in VFS if enabled
            manager.update(presentation)

            return f"Added text slide '{title}' to '{presentation or manager.get_current_name()}'"

        return await asyncio.get_event_loop().run_in_executor(None, _add_text_slide)

    @mcp.tool
    async def pptx_extract_all_text(presentation: Optional[str] = None) -> str:
        """
        Extract all text content from a presentation.

        Extracts text from all slides including titles, body text, placeholders,
        text boxes, and tables. Useful for content analysis, search, or migration.

        Args:
            presentation: Name of presentation to extract from (uses current if not specified)

        Returns:
            JSON object with extracted text organized by slide

        Example:
            text = await pptx_extract_all_text()
            # Returns JSON with all text content from the presentation
        """
        def _extract():
            prs = manager.get(presentation)
            if not prs:
                return {"error": "No presentation found"}

            return extract_presentation_text(prs)

        return await asyncio.get_event_loop().run_in_executor(None, _extract)

    @mcp.tool
    async def pptx_add_text_box(
        slide_index: int,
        text: str,
        left: float = 1.0,
        top: float = 2.0,
        width: float = 8.0,
        height: float = 1.0,
        font_size: int = 18,
        bold: bool = False,
        color: Optional[str] = None,
        alignment: str = "left",
        presentation: Optional[str] = None
    ) -> str:
        """
        Add a formatted text box to a slide.

        Adds a text box with custom positioning, sizing, and formatting.
        Supports semantic colors from the theme or hex colors.

        Args:
            slide_index: Index of the slide to add text to (0-based)
            text: Text content
            left: Left position in inches
            top: Top position in inches
            width: Width in inches
            height: Height in inches
            font_size: Font size in points
            bold: Whether text should be bold
            color: Text color (semantic like "primary.DEFAULT" or hex like "#FF0000")
            alignment: Text alignment (left, center, right, justify)
            presentation: Name of presentation (uses current if not specified)

        Returns:
            Success message confirming text box addition

        Example:
            await pptx_add_text_box(
                slide_index=0,
                text="Important Notice",
                font_size=24,
                bold=True,
                color="primary.DEFAULT",
                alignment="center"
            )
        """
        def _add_text_box():
            prs = manager.get(presentation)
            if not prs:
                return "Error: No presentation found"

            if slide_index >= len(prs.slides):
                return f"Error: Slide index {slide_index} out of range"

            slide = prs.slides[slide_index]

            # Get theme if using semantic colors
            theme_obj = None
            if color and '.' in color:
                from ...themes.theme_manager import ThemeManager
                theme_manager = ThemeManager()
                theme_obj = theme_manager.get_theme()  # Get current theme

            # Create text box component
            text_comp = TextBox(
                text=text,
                font_size=font_size,
                bold=bold,
                color=color,
                alignment=alignment,
                theme=theme_obj.__dict__ if theme_obj else None
            )

            # Render to slide
            text_comp.render(slide, left=left, top=top, width=width, height=height)

            # Update in VFS if enabled
            manager.update(presentation)

            return f"Added text box to slide {slide_index}"

        return await asyncio.get_event_loop().run_in_executor(None, _add_text_box)

    @mcp.tool
    async def pptx_add_bullet_list(
        slide_index: int,
        items: list,
        left: float = 1.0,
        top: float = 2.0,
        width: float = 8.0,
        height: float = 4.0,
        font_size: int = 16,
        color: Optional[str] = None,
        bullet_char: str = "•",
        presentation: Optional[str] = None
    ) -> str:
        """
        Add a bullet list to a slide.

        Creates a formatted bullet list with custom bullet characters and styling.

        Args:
            slide_index: Index of the slide to add list to (0-based)
            items: List of items to display
            left: Left position in inches
            top: Top position in inches
            width: Width in inches
            height: Height in inches
            font_size: Font size in points
            color: Text color (semantic like "foreground.DEFAULT" or hex like "#000000")
            bullet_char: Character to use for bullets (e.g., "•", "→", "✓")
            presentation: Name of presentation (uses current if not specified)

        Returns:
            Success message confirming bullet list addition

        Example:
            await pptx_add_bullet_list(
                slide_index=1,
                items=["Increase revenue", "Reduce costs", "Improve quality"],
                font_size=18,
                color="primary.DEFAULT",
                bullet_char="→"
            )
        """
        def _add_bullet_list():
            prs = manager.get(presentation)
            if not prs:
                return "Error: No presentation found"

            if slide_index >= len(prs.slides):
                return f"Error: Slide index {slide_index} out of range"

            slide = prs.slides[slide_index]

            # Get theme if using semantic colors
            theme_obj = None
            if color and '.' in color:
                from ...themes.theme_manager import ThemeManager
                theme_manager = ThemeManager()
                theme_obj = theme_manager.get_theme()  # Get current theme

            # Create bullet list component
            bullets = BulletList(
                items=items,
                font_size=font_size,
                color=color,
                bullet_char=bullet_char,
                theme=theme_obj.__dict__ if theme_obj else None
            )

            # Render to slide
            bullets.render(slide, left=left, top=top, width=width, height=height)

            # Update in VFS if enabled
            manager.update(presentation)

            return f"Added bullet list with {len(items)} items to slide {slide_index}"

        return await asyncio.get_event_loop().run_in_executor(None, _add_bullet_list)

    # Return the tools for external access
    return {
        'pptx_add_text_slide': pptx_add_text_slide,
        'pptx_extract_all_text': pptx_extract_all_text,
        'pptx_add_text_box': pptx_add_text_box,
        'pptx_add_bullet_list': pptx_add_bullet_list,
    }
