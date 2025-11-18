# src/chuk_mcp_pptx/tools/text_tools.py
"""
Text Tools for PowerPoint MCP Server

Provides async MCP tools for handling text in presentations.
Supports text extraction, formatting, and component-based text creation.
"""

from ..utilities.text_utils import extract_presentation_text
from ..models import ErrorResponse, SlideResponse
from ..constants import SlideLayoutIndex, ErrorMessages, SuccessMessages


def register_text_tools(mcp, manager):
    """Register all text tools with the MCP server.

    Note: pptx_add_bullet_list is provided by component_tools.py as part of the
    comprehensive design system. This module provides text utilities and slides.
    """

    from ..components.core import TextBox
    from ..themes.theme_manager import ThemeManager

    theme_manager = ThemeManager()

    @mcp.tool
    async def pptx_add_text_slide(title: str, text: str, presentation: str | None = None) -> str:
        """
        Add a slide with title and text content.

        Creates a slide with a title and paragraph text. Suitable for
        descriptions, summaries, or any narrative content.

        Args:
            title: Title text for the slide
            text: Paragraph text content for the slide body
            presentation: Name of presentation to add slide to (uses current if not specified)

        Returns:
            JSON string with SlideResponse model

        Example:
            await pptx_add_text_slide(
                title="Executive Summary",
                text="This quarter demonstrated exceptional growth across all business units. "
                     "Revenue increased by 25% year-over-year, driven primarily by our cloud "
                     "services division."
            )
        """
        try:
            prs = manager.get_presentation(presentation)
            if not prs:
                return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

            slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE_AND_CONTENT]
            slide = prs.slides.add_slide(slide_layout)

            slide.shapes.title.text = title

            if len(slide.placeholders) > 1:
                slide.placeholders[1].text_frame.text = text

            # Apply presentation theme to the slide
            metadata = manager.get_metadata(presentation)
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            slide_index = len(prs.slides) - 1

            # Update metadata
            manager.update_slide_metadata(slide_index)

            # Update in VFS
            await manager.update(presentation)

            pres_name = presentation or manager.get_current_name() or "presentation"

            return SlideResponse(
                presentation=pres_name,
                slide_index=slide_index,
                message=SuccessMessages.SLIDE_ADDED.format(
                    slide_type="text", presentation=pres_name
                ),
                slide_count=len(prs.slides),
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

    @mcp.tool
    async def pptx_extract_all_text(presentation: str | None = None) -> str:
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
        try:
            prs = manager.get_presentation(presentation)
            if not prs:
                return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

            text_data = extract_presentation_text(prs)
            # Return as JSON string
            import json

            return json.dumps(text_data)
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

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
        color: str | None = None,
        alignment: str = "left",
        presentation: str | None = None,
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
        try:
            prs = manager.get_presentation(presentation)
            if not prs:
                return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

            if slide_index >= len(prs.slides):
                return ErrorResponse(
                    error=ErrorMessages.SLIDE_NOT_FOUND.format(index=slide_index)
                ).model_dump_json()

            slide = prs.slides[slide_index]

            # Get theme if using semantic colors
            theme_obj = None
            if color and "." in color:
                theme_manager = ThemeManager()
                theme_obj = theme_manager.get_default_theme()

            # Create text box component
            text_comp = TextBox(
                text=text,
                font_size=font_size,
                bold=bold,
                color=color,
                alignment=alignment,
                theme=theme_obj.__dict__ if theme_obj else None,
            )

            # Render to slide
            text_comp.render(slide, left=left, top=top, width=width, height=height)

            # Update metadata
            manager.update_slide_metadata(slide_index)

            # Update in VFS
            await manager.update(presentation)

            pres_name = presentation or manager.get_current_name() or "presentation"

            from ..models import ComponentResponse

            return ComponentResponse(
                presentation=pres_name,
                slide_index=slide_index,
                component="text_box",
                message=SuccessMessages.COMPONENT_ADDED.format(
                    component="text box", index=slide_index
                ),
                variant=None,
            ).model_dump_json()
        except Exception as e:
            return ErrorResponse(error=str(e)).model_dump_json()

    # pptx_add_bullet_list removed - now in component_tools.py as part of design system

    # Return the tools for external access
    # Note: pptx_add_bullet_list is provided by component_tools.py
    return {
        "pptx_add_text_slide": pptx_add_text_slide,
        "pptx_extract_all_text": pptx_extract_all_text,
        "pptx_add_text_box": pptx_add_text_box,
    }
