#!/usr/bin/env python3
"""
Async PowerPoint MCP Server using chuk-mcp-server

This server provides async MCP tools for creating and managing PowerPoint presentations
using the python-pptx library. It supports multiple presentations with chuk-artifacts
integration for flexible storage (memory, filesystem, sqlite, s3).

Storage is managed through chuk-mcp-server's built-in artifact store context.
"""

import asyncio
import logging

from chuk_mcp_server import ChukMCPServer
from .presentation_manager import PresentationManager
from .models import (
    ErrorResponse,
    SuccessResponse,
    PresentationResponse,
    SlideResponse,
)
from .constants import (
    SlideLayoutIndex,
    ErrorMessages,
    SuccessMessages,
)

# Text utilities now handled by tools/text.py via register_text_tools()
# Shape utilities now available as components in components.core

# Import modular tools modules
from .chart_tools import register_chart_tools
from .tools.image_tools import register_image_tools
from .tools.text_tools import register_text_tools
from .inspection_tools import register_inspection_tools
from .tools.table_tools import register_table_tools
from .tools.slide_layout_tools import register_layout_tools
from .tools.component_tools import register_component_tools
from .tools.registry_tools import register_registry_tools
from .tools.token_tools import register_token_tools
from .tools.semantic_tools import register_semantic_tools
from .tools.theme_tools import register_theme_tools
from .tools.shape_tools import register_shape_tools
from .themes.theme_manager import ThemeManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
mcp = ChukMCPServer("chuk-mcp-pptx-async")

# Create presentation manager instance
# Uses chuk-mcp-server's built-in artifact store context for persistence
manager = PresentationManager(base_path="presentations")

# Create theme manager instance
theme_manager = ThemeManager()

# Register all modular tools
chart_tools = register_chart_tools(mcp, manager)
image_tools = register_image_tools(mcp, manager)
text_tools = register_text_tools(mcp, manager)
inspection_tools = register_inspection_tools(mcp, manager)
table_tools = register_table_tools(mcp, manager)
layout_tools = register_layout_tools(mcp, manager)
shape_tools = register_shape_tools(mcp, manager)

# Register design system tools (NEW)
component_tools = register_component_tools(mcp, manager)
registry_tools = register_registry_tools(mcp, manager)
token_tools = register_token_tools(mcp, manager)
theme_tools = register_theme_tools(mcp, manager)

# Register LLM-friendly semantic tools (NEW)
semantic_tools = register_semantic_tools(mcp, manager)

# Make tools available at module level for easier imports
if chart_tools:
    pptx_add_chart = chart_tools["pptx_add_chart"]

if image_tools:
    pptx_add_image_slide = image_tools["pptx_add_image_slide"]
    pptx_add_image = image_tools["pptx_add_image"]
    pptx_add_background_image = image_tools["pptx_add_background_image"]
    pptx_add_image_gallery = image_tools["pptx_add_image_gallery"]
    pptx_add_image_with_caption = image_tools["pptx_add_image_with_caption"]
    pptx_add_logo = image_tools["pptx_add_logo"]
    pptx_replace_image = image_tools["pptx_replace_image"]

if inspection_tools:
    pptx_inspect_slide = inspection_tools["pptx_inspect_slide"]
    pptx_fix_slide_layout = inspection_tools["pptx_fix_slide_layout"]
    pptx_analyze_presentation_layout = inspection_tools["pptx_analyze_presentation_layout"]

if table_tools:
    pptx_add_data_table = table_tools["pptx_add_data_table"]
    pptx_add_comparison_table = table_tools["pptx_add_comparison_table"]
    pptx_update_table_cell = table_tools["pptx_update_table_cell"]
    pptx_format_table = table_tools["pptx_format_table"]

if layout_tools:
    pptx_list_layouts = layout_tools["pptx_list_layouts"]
    pptx_add_slide_with_layout = layout_tools["pptx_add_slide_with_layout"]
    pptx_customize_layout = layout_tools["pptx_customize_layout"]
    pptx_apply_master_layout = layout_tools["pptx_apply_master_layout"]
    pptx_duplicate_slide = layout_tools["pptx_duplicate_slide"]
    pptx_reorder_slides = layout_tools["pptx_reorder_slides"]

if shape_tools:
    pptx_add_arrow = shape_tools["pptx_add_arrow"]
    pptx_add_smart_art = shape_tools["pptx_add_smart_art"]
    pptx_add_code_block = shape_tools["pptx_add_code_block"]

# Theme tools now in their own module
if theme_tools:
    pptx_list_themes = theme_tools["pptx_list_themes"]
    pptx_get_theme_info = theme_tools["pptx_get_theme_info"]
    pptx_create_custom_theme = theme_tools["pptx_create_custom_theme"]
    pptx_apply_theme = theme_tools["pptx_apply_theme"]
    pptx_apply_component_theme = theme_tools["pptx_apply_component_theme"]
    pptx_list_component_themes = theme_tools["pptx_list_component_themes"]

# Note: Function references are already created by the register_*_tools() calls above
# No need for backward compatibility layer as tools are registered directly with mcp


@mcp.tool  # type: ignore[arg-type]
async def pptx_create(name: str, theme: str | None = None) -> str:
    """
    Create a new PowerPoint presentation.

    Creates a new blank presentation and sets it as the current active presentation.
    Automatically saves to the virtual filesystem for persistence.

    Args:
        name: Unique name for the presentation (used for reference in other commands)
        theme: Optional theme to apply (e.g., "dark-violet", "tech-blue")

    Returns:
        JSON string with PresentationResponse model

    Example:
        await pptx_create(name="quarterly_report", theme="tech-blue")
    """
    try:
        logger.info(f"🎯 pptx_create called: name={name!r}, theme={theme!r}")
        logger.info(f"   name type: {type(name)}, theme type: {type(theme)}")

        # Create presentation (returns PresentationMetadata model)
        metadata = await manager.create(name=name, theme=theme)
        logger.info(f"✓ Presentation created successfully: {metadata.name}")

        # Return PresentationResponse as JSON
        return PresentationResponse(
            name=metadata.name,
            message=f"Created presentation '{metadata.name}'",
            slide_count=metadata.slide_count,
            is_current=True,
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to create presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_add_title_slide(
    title: str, subtitle: str = "", presentation: str | None = None
) -> str:
    """
    Add a title slide to the current presentation.

    Creates a standard title slide with a main title and optional subtitle.
    This is typically used as the first slide in a presentation.

    Args:
        title: Main title text for the slide
        subtitle: Optional subtitle text (appears below the title)
        presentation: Name of presentation to add slide to (uses current if not specified)

    Returns:
        JSON string with SlideResponse model

    Example:
        await pptx_add_title_slide(
            title="Annual Report 2024",
            subtitle="Financial Results and Strategic Outlook"
        )
    """
    try:
        prs = manager.get_presentation(presentation)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE]
        slide = prs.slides.add_slide(slide_layout)

        slide.shapes.title.text = title
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle

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
            message=SuccessMessages.SLIDE_ADDED.format(slide_type="title", presentation=pres_name),
            slide_count=len(prs.slides),
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to add title slide: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_add_slide(title: str, content: list[str], presentation: str | None = None) -> str:
    """
    Add a text content slide with title and bullet points.

    Creates a slide with a title and bulleted text list.

    ⚠️  For CHARTS use pptx_add_chart instead - this only creates text bullets.

    Perfect for: agendas, key points, lists, text content.
    NOT for: charts, graphs, data visualizations (use pptx_add_chart).

    Args:
        title: Title text for the slide
        content: List of strings, each becoming a bullet point (TEXT only)
        presentation: Name of presentation to add slide to (uses current if not specified)

    Returns:
        JSON string with SlideResponse model

    Example:
        await pptx_add_slide(
            title="Project Milestones",
            content=[
                "Phase 1: Research completed",
                "Phase 2: Development in progress",
                "Phase 3: Testing scheduled for Q2"
            ]
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
            text_frame = slide.placeholders[1].text_frame
            for idx, bullet in enumerate(content):
                if idx == 0:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()
                p.text = bullet
                p.level = 0  # First level bullet

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
                slide_type="content", presentation=pres_name
            ),
            slide_count=len(prs.slides),
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to add slide: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


# Note: pptx_add_text_slide is now provided by text_tools.py
# The function is registered via register_text_tools()


@mcp.tool  # type: ignore[arg-type]
async def pptx_save(path: str, presentation: str | None = None) -> str:
    """
    Save the presentation to a PowerPoint file.

    Saves the current or specified presentation to a .pptx file on disk.

    Args:
        path: File path where to save the .pptx file
        presentation: Name of presentation to save (uses current if not specified)

    Returns:
        JSON string with ExportResponse model

    Example:
        await pptx_save(path="reports/quarterly_report.pptx")
    """
    try:
        prs = manager.get_presentation(presentation)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        await asyncio.to_thread(prs.save, path)

        # Get file size
        from pathlib import Path

        size_bytes = Path(path).stat().st_size if Path(path).exists() else None

        pres_name = presentation or manager.get_current_name() or "presentation"

        from .models import ExportResponse

        return ExportResponse(
            name=pres_name,
            format="file",
            path=path,
            artifact_uri=manager.get_artifact_uri(pres_name),
            namespace_id=manager.get_namespace_id(pres_name),
            size_bytes=size_bytes,
            message=SuccessMessages.PRESENTATION_SAVED.format(path=path),
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to save presentation: {e}")
        return ErrorResponse(error=ErrorMessages.SAVE_FAILED.format(error=str(e))).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_get_download_url(presentation: str | None = None, expires_in: int = 3600) -> str:
    """
    Get a presigned download URL for the presentation.

    Generates a temporary URL that can be used to download the presentation
    directly from cloud storage (S3/Tigris). The URL expires after the specified
    duration.

    Args:
        presentation: Name of presentation (uses current if not specified)
        expires_in: URL expiration time in seconds (default: 3600 = 1 hour)

    Returns:
        JSON string with download URL or error

    Example:
        result = await pptx_get_download_url()
        # Returns: {"url": "https://...", "expires_in": 3600}
    """
    try:
        from chuk_mcp_server import get_artifact_store, has_artifact_store

        pres_name = presentation or manager.get_current_name()
        if not pres_name:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Make sure presentation exists and is saved to store
        prs = manager.get_presentation(pres_name)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Get namespace ID
        namespace_id = manager.get_namespace_id(pres_name)
        if not namespace_id:
            # Try to save first
            saved = await manager.save(pres_name)
            if not saved:
                return ErrorResponse(
                    error="Presentation not saved to artifact store. Save it first."
                ).model_dump_json()
            namespace_id = manager.get_namespace_id(pres_name)

        if not namespace_id:
            return ErrorResponse(
                error="Could not get namespace ID for presentation."
            ).model_dump_json()

        # Get artifact store
        if not has_artifact_store():
            return ErrorResponse(
                error="No artifact store configured. Set up S3/Tigris storage."
            ).model_dump_json()

        store = get_artifact_store()

        # Generate presigned URL
        url = await store.presign(namespace_id, expires=expires_in)

        import json

        return json.dumps(
            {
                "success": True,
                "url": url,
                "presentation": pres_name,
                "namespace_id": namespace_id,
                "expires_in": expires_in,
                "filename": f"{pres_name}.pptx",
            }
        )
    except Exception as e:
        logger.error(f"Failed to generate download URL: {e}")
        return ErrorResponse(error=f"Failed to generate download URL: {str(e)}").model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_export_base64(presentation: str | None = None) -> str:
    """
    Export the presentation as a base64-encoded string.

    Exports the current or specified presentation as a base64 string that can be
    saved, transmitted, or imported later.

    Args:
        presentation: Name of presentation to export (uses current if not specified)

    Returns:
        JSON string with ExportResponse model including base64 data

    Example:
        result = await pptx_export_base64()
    """
    try:
        data = await manager.export_base64(presentation)
        if not data:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        pres_name = presentation or manager.get_current_name() or "presentation"

        from .models import ExportResponse

        return ExportResponse(
            name=pres_name,
            format="base64",
            path=None,
            artifact_uri=manager.get_artifact_uri(pres_name),
            namespace_id=manager.get_namespace_id(pres_name),
            size_bytes=len(data),
            message=f"Exported presentation '{pres_name}' as base64 ({len(data)} bytes)",
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to export presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_import_base64(data: str, name: str) -> str:
    """
    Import a presentation from a base64-encoded string.

    Imports a presentation from a base64 string and creates it with the given name.
    The imported presentation becomes the current active presentation.

    Args:
        data: Base64-encoded string of the .pptx file
        name: Name to give to the imported presentation

    Returns:
        JSON string with ImportResponse model

    Example:
        await pptx_import_base64(
            data="UEsDBBQABgAIAAAAIQA...",
            name="imported_presentation"
        )
    """
    try:
        success = await manager.import_base64(data, name)
        if not success:
            return ErrorResponse(error="Failed to import presentation").model_dump_json()

        prs = manager.get_presentation(name)
        slide_count = len(prs.slides) if prs else 0

        from .models import ImportResponse

        return ImportResponse(
            name=name,
            source="base64",
            slide_count=slide_count,
            artifact_uri=manager.get_artifact_uri(name),
            namespace_id=manager.get_namespace_id(name),
            message=f"Imported presentation '{name}' with {slide_count} slides",
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to import presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_list() -> str:
    """
    List all presentations currently in memory.

    Returns a JSON array of presentation names with metadata.

    Returns:
        JSON string with ListPresentationsResponse model

    Example:
        presentations = await pptx_list()
    """
    try:
        response = await manager.list_presentations()
        return response.model_dump_json()
    except Exception as e:
        logger.error(f"Failed to list presentations: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_switch(name: str) -> str:
    """
    Switch to a different presentation.

    Changes the current active presentation to the specified one.

    Args:
        name: Name of the presentation to switch to

    Returns:
        JSON string with SuccessResponse model

    Example:
        await pptx_switch(name="sales_pitch")
    """
    try:
        success = await manager.set_current(name)
        if not success:
            return ErrorResponse(
                error=ErrorMessages.PRESENTATION_NOT_FOUND.format(name=name)
            ).model_dump_json()

        return SuccessResponse(message=f"Switched to presentation '{name}'").model_dump_json()
    except Exception as e:
        logger.error(f"Failed to switch presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_delete(name: str) -> str:
    """
    Delete a presentation from memory and VFS.

    Removes the specified presentation from memory and VFS storage.

    Args:
        name: Name of the presentation to delete

    Returns:
        JSON string with SuccessResponse model

    Example:
        await pptx_delete(name="old_presentation")
    """
    try:
        success = await manager.delete(name)
        if not success:
            return ErrorResponse(
                error=ErrorMessages.PRESENTATION_NOT_FOUND.format(name=name)
            ).model_dump_json()

        return SuccessResponse(message=f"Deleted presentation '{name}'").model_dump_json()
    except Exception as e:
        logger.error(f"Failed to delete presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_get_info(presentation: str | None = None) -> str:
    """
    Get information about a presentation.

    Returns detailed metadata about the specified presentation including
    slide count, metadata, and storage status.

    Args:
        presentation: Name of presentation to get info for (uses current if not specified)

    Returns:
        JSON string with PresentationMetadata model

    Example:
        info = await pptx_get_info()
    """
    try:
        result = await manager.get(presentation)
        if not result:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        prs, metadata = result
        return metadata.model_dump_json()
    except Exception as e:
        logger.error(f"Failed to get presentation info: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


# Additional async tools for shapes, text extraction, etc.

# Note: pptx_extract_all_text is now provided by text_tools.py
# The function is registered via register_text_tools()

# Note: pptx_add_data_table is now provided by table_tools.py with layout validation
# The function is registered via register_table_tools()


# Run the server
if __name__ == "__main__":
    logger.info("Starting PowerPoint MCP Server...")
    logger.info(f"Base Path: {manager.base_path}")
    logger.info("Storage: Using chuk-mcp-server artifact store context")

    # Run in stdio mode when executed directly
    mcp.run(stdio=True)
