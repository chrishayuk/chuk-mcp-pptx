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
from .core.presentation_manager import PresentationManager
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

# Import organized tool modules
from .tools.core import register_placeholder_tools
from .tools.universal import (
    register_universal_component_api,
    register_registry_tools,
    register_semantic_tools,
)

# Legacy content tools removed - use universal component API instead
from .tools.theme import register_theme_tools
from .tools.template import register_template_tools, register_extraction_tools
from .tools.layout import register_layout_tools
from .tools.inspection import register_inspection_tools
from .themes.theme_manager import ThemeManager
from .templates import TemplateManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
mcp = ChukMCPServer("chuk-mcp-pptx-async")

# Create presentation manager instance
# Uses chuk-mcp-server's built-in artifact store context for persistence
manager = PresentationManager(base_path="presentations")

# Create theme manager instance
theme_manager = ThemeManager()

# Create template manager instance (for builtin templates)
template_manager = TemplateManager()

# Register all modular tools
# Legacy chart/image/table tools removed - use universal component API instead
theme_tools = register_theme_tools(mcp, manager)

# Register consolidated template tools
template_tools = register_template_tools(mcp, manager, template_manager)

# Register template extraction tools
extraction_tools = register_extraction_tools(mcp, manager, theme_manager)

# Register organized tool modules
placeholder_tools = register_placeholder_tools(mcp, manager)
universal_component_api = register_universal_component_api(mcp, manager)
registry_tools = register_registry_tools(mcp, manager)
semantic_tools = register_semantic_tools(mcp, manager)
layout_tools = register_layout_tools(mcp, manager)
inspection_tools = register_inspection_tools(mcp, manager)

# Make tools available at module level for easier imports
# Legacy chart/image/table tool exports removed - use universal component API

if inspection_tools:
    pptx_inspect_slide = inspection_tools["pptx_inspect_slide"]
    pptx_fix_slide_layout = inspection_tools["pptx_fix_slide_layout"]
    pptx_analyze_presentation_layout = inspection_tools["pptx_analyze_presentation_layout"]

if layout_tools:
    pptx_list_layouts = layout_tools["pptx_list_layouts"]
    pptx_add_slide_with_layout = layout_tools["pptx_add_slide_with_layout"]
    pptx_customize_layout = layout_tools["pptx_customize_layout"]
    pptx_apply_master_layout = layout_tools["pptx_apply_master_layout"]
    pptx_duplicate_slide = layout_tools["pptx_duplicate_slide"]
    pptx_reorder_slides = layout_tools["pptx_reorder_slides"]


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
async def pptx_create(name: str, theme: str | None = None, template_name: str | None = None) -> str:
    """
    Create a new PowerPoint presentation, optionally from a template.

    Creates a new presentation and sets it as the current active presentation.
    Can create from scratch, apply a theme, or use a builtin or custom template.
    Automatically saves to the virtual filesystem for persistence.

    Args:
        name: Unique name for the presentation (used for reference in other commands)
        theme: Optional theme to apply (e.g., "dark-violet", "tech-blue")
        template_name: Optional built-in template name to use as base. IMPORTANT:
            - Use this to get professional layouts and designs
            - Built-in templates: "brand_proposal" (55 layouts), "corporate", "minimal"
            - Use pptx_list_templates() to see all available templates
            - DO NOT use pptx_get_builtin_template first - just pass the name directly
            - Example: pptx_create(name="my_deck", template_name="brand_proposal")

    Returns:
        JSON string with PresentationResponse model. When created from a template,
        the response includes template_info with:
        - layout_count: Number of layouts available
        - message: Guidance on how to use the layouts

    TEMPLATE WORKFLOW (CRITICAL - REQUIRED STEPS):
        When creating from a template, you MUST follow this exact workflow:

        1. Create presentation with template_name parameter
        2. ⚠️ IMMEDIATELY call pptx_analyze_template(template_name) to see ALL layouts
           - Templates have 20-50+ different layouts (not just 2-3!)
           - Examples: Title, Content, Two Content, Comparison, Quote, Charts, etc.
           - You MUST review ALL layouts before adding any slides
           - Using variety makes presentations more engaging and professional

        3. For EACH slide you want to add:
           a. Choose the BEST layout from the analyzed list (use variety!)
           b. Call pptx_add_slide_from_template(layout_index=X) with that layout
           c. Review the layout_info in the response to see available placeholders
           d. Call pptx_populate_placeholder() for EACH text placeholder
           e. For images/tables, use pptx_add_component with target_placeholder
           f. VERIFY with pptx_list_slide_components() to ensure all placeholders filled

        DO NOT:
        - Use the same layout repeatedly (templates have variety - use it!)
        - Skip analyzing layouts (you'll miss better options)
        - Use pptx_add_slide, pptx_add_title_slide, or pptx_add_text_box (bypasses template)
        - Add free-form content over placeholders (breaks template design)

        TIP: Use pptx_list_slide_components(slide_index=X) after adding a slide
        to see what decorative shapes/elements exist from the template layout.

    Examples:
        # Create blank presentation
        await pptx_create(name="quarterly_report", theme="tech-blue")

        # Create from built-in template - RECOMMENDED WORKFLOW
        # DO NOT call pptx_get_builtin_template first - just use template_name parameter
        result = await pptx_create(name="new_brand", template_name="brand_proposal")
        # This creates presentation with ALL layouts from the template

        # Step 1: Analyze template to see ALL available layouts
        layouts = await pptx_analyze_template("brand_proposal")
        # Shows: index 0 = "Title with Picture", index 1 = "Content", etc.
        # Note which layout indices match your content needs

        # Step 2: Add title slide (find title layout in analysis results)
        slide_result = await pptx_add_slide_from_template(layout_index=<title_layout_index>)
        # Response shows: placeholder 0 (TITLE), placeholder 1 (SUBTITLE), etc.

        # Step 3: Populate ALL placeholders on the title slide
        await pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="My Brand")
        await pptx_populate_placeholder(slide_index=0, placeholder_idx=1, content="Tagline")

        # Step 3b: VERIFY placeholders were populated correctly
        await pptx_list_slide_components(slide_index=0)
        # Should show no empty placeholders - all should have content

        # Step 4: Add content slide (find content layout in analysis)
        slide_result = await pptx_add_slide_from_template(layout_index=<content_layout_index>)
        # Response shows available placeholders for this layout

        # Step 5: Populate ALL content placeholders
        await pptx_populate_placeholder(slide_index=1, placeholder_idx=0, content="Section Title")
        await pptx_populate_placeholder(slide_index=1, placeholder_idx=1, content="Content here")

        # Step 6: VERIFY again - ensures no "Click to add text" remains
        await pptx_list_slide_components(slide_index=1)
        # All placeholders should be filled with your content
    """
    try:
        logger.info(
            f"🎯 pptx_create called: name={name!r}, theme={theme!r}, template={template_name!r}"
        )
        logger.info(
            f"   name type: {type(name)}, theme type: {type(theme)}, template type: {type(template_name)}"
        )

        # Create presentation (returns PresentationMetadata model)
        metadata = await manager.create(name=name, theme=theme, template_name=template_name)
        logger.info(f"✓ Presentation created successfully: {metadata.name}")

        message = f"Created presentation '{metadata.name}'"
        if template_name:
            message += f" from template '{template_name}'"
        if metadata.slide_count > 0:
            message += f" with {metadata.slide_count} slide(s)"

        # If template was used, add layout info to help AI understand what's available
        template_info = None
        if template_name:
            result = await manager.get(metadata.name)
            if result:
                from .models.responses import TemplateInfo

                prs, _ = result
                layout_count = len(prs.slide_layouts) if prs.slide_layouts else 0
                template_info = TemplateInfo(
                    template_name=template_name,
                    layout_count=layout_count,
                    message=f"Template loaded with {layout_count} layouts. Use pptx_add_slide_from_template(layout_index=X) to use specific layouts, or call pptx_analyze_template('{template_name}') to see all available layouts with their names and placeholders.",
                )

        # Return PresentationResponse as JSON
        return PresentationResponse(
            name=metadata.name,
            message=message,
            slide_count=metadata.slide_count,
            is_current=True,
            template_info=template_info,
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to create presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_add_title_slide(
    title: str, subtitle: str = "", presentation: str | None = None
) -> str:
    """
    ⚠️ DEPRECATED: Use pptx_add_slide_from_template() instead for template-based presentations.

    This tool bypasses template designs and should ONLY be used for blank presentations
    created without a template_name parameter.

    For template-based presentations:
    1. Call pptx_analyze_template() to see available layouts
    2. Find a title layout (e.g., "Title with Picture", "Title Slide")
    3. Call pptx_add_slide_from_template(layout_index=X)
    4. Populate placeholders with pptx_populate_placeholder()

    Args:
        title: Main title text for the slide
        subtitle: Optional subtitle text (appears below the title)
        presentation: Name of presentation to add slide to (uses current if not specified)

    Returns:
        JSON string with SlideResponse model or error if used with template

    Example (ONLY for blank presentations):
        await pptx_add_title_slide(
            title="Annual Report 2024",
            subtitle="Financial Results and Strategic Outlook"
        )
    """
    try:
        prs = await manager.get_presentation(presentation)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Check if presentation was created from a template
        metadata = await manager.get_metadata(presentation)
        if metadata and metadata.template_path:
            return ErrorResponse(
                error=f"This presentation was created from template '{metadata.template_path}'. "
                f"You must use pptx_add_slide_from_template(layout_index=X) to add slides with "
                f"specific template layouts. Call pptx_analyze_template('{metadata.template_path}') "
                f"to see all {len(prs.slide_layouts)} available layouts."
            ).model_dump_json()

        slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE]
        slide = prs.slides.add_slide(slide_layout)

        slide.shapes.title.text = title
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle

        # Apply presentation theme to the slide
        metadata = await manager.get_metadata(presentation)
        if metadata and metadata.theme:
            theme_obj = theme_manager.get_theme(metadata.theme)
            if theme_obj:
                theme_obj.apply_to_slide(slide)

        slide_index = len(prs.slides) - 1

        # Update metadata
        await manager.update_slide_metadata(slide_index)

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
    ⚠️ DEPRECATED: Use pptx_add_slide_from_template() instead for template-based presentations.

    This tool bypasses template designs and should ONLY be used for blank presentations
    created without a template_name parameter.

    For template-based presentations:
    1. Call pptx_analyze_template() to see available layouts
    2. Find a content layout (e.g., "Content", "Two Content", "Bullets")
    3. Call pptx_add_slide_from_template(layout_index=X)
    4. Populate title placeholder with pptx_populate_placeholder()
    5. Populate content placeholder(s) with pptx_populate_placeholder()

    Args:
        title: Title text for the slide
        content: List of strings, each becoming a bullet point
        presentation: Name of presentation to add slide to (uses current if not specified)

    Returns:
        JSON string with SlideResponse model or error if used with template

    Example (ONLY for blank presentations):
        await pptx_add_slide(
            title="Project Milestones",
            content=[
                "Phase 1: Research completed",
                "Phase 2: Development in progress"
            ]
        )
    """
    try:
        prs = await manager.get_presentation(presentation)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Check if presentation was created from a template
        metadata = await manager.get_metadata(presentation)
        if metadata and metadata.template_path:
            return ErrorResponse(
                error=f"This presentation was created from template '{metadata.template_path}'. "
                f"You must use pptx_add_slide_from_template(layout_index=X) to add slides with "
                f"specific template layouts. Call pptx_analyze_template('{metadata.template_path}') "
                f"to see all {len(prs.slide_layouts)} available layouts."
            ).model_dump_json()

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
        metadata = await manager.get_metadata(presentation)
        if metadata and metadata.theme:
            theme_obj = theme_manager.get_theme(metadata.theme)
            if theme_obj:
                theme_obj.apply_to_slide(slide)

        slide_index = len(prs.slides) - 1

        # Update metadata
        await manager.update_slide_metadata(slide_index)

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
    Save the presentation to a PowerPoint file and artifact store.

    Saves the current or specified presentation to a .pptx file on disk
    and to the artifact store (if configured). Returns the artifact URI
    for cloud deployments.

    Args:
        path: File path where to save the .pptx file
        presentation: Name of presentation to save (uses current if not specified)

    Returns:
        JSON string with ExportResponse model including artifact_uri

    Example:
        await pptx_save(path="reports/quarterly_report.pptx")
    """
    try:
        pres_name = presentation or manager.get_current_name()
        if not pres_name:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        prs = await manager.get_presentation(pres_name)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Save to local file
        await asyncio.to_thread(prs.save, path)

        # Also save to artifact store to get artifact URI
        await manager.save(pres_name)

        # Get file size
        from pathlib import Path

        size_bytes = Path(path).stat().st_size if Path(path).exists() else None

        # Get artifact URI and generate download URL if available
        artifact_uri = manager.get_artifact_uri(pres_name)
        namespace_id = manager.get_namespace_id(pres_name)
        download_url = None

        # Try to generate a presigned download URL by storing as artifact
        try:
            from chuk_mcp_server import get_artifact_store, has_artifact_store

            if has_artifact_store():
                store = get_artifact_store()
                logger.info("Storing presentation as artifact for presigned URL")

                # Read the saved file and store as artifact
                from pathlib import Path

                pptx_path = Path(path)
                if pptx_path.exists():
                    pptx_data = pptx_path.read_bytes()

                    # Store as artifact to get presigned URL
                    artifact_id = await store.store(
                        data=pptx_data,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        summary=f"{pres_name}.pptx",
                        meta={
                            "filename": f"{pres_name}.pptx",
                            "presentation_name": pres_name,
                            "expiration_days": 30,  # Hint for S3 lifecycle policy
                        },
                    )
                    logger.info(f"Stored as artifact: {artifact_id}")

                    # Generate presigned URL with 24-hour expiration
                    download_url = await store.presign(artifact_id, expires=86400)
                    logger.info(
                        f"Generated presigned URL (24h expiry): {download_url[:80] if download_url else 'None'}..."
                    )
            else:
                logger.warning("Artifact store not available for presigned URL generation")
        except Exception as e:
            logger.warning(f"Could not generate download URL: {e}", exc_info=True)

        from .models import ExportResponse

        return ExportResponse(
            name=pres_name,
            format="file",
            path=path,
            artifact_uri=artifact_uri,
            namespace_id=namespace_id,
            download_url=download_url,
            size_bytes=size_bytes,
            message=SuccessMessages.PRESENTATION_SAVED.format(path=path),
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to save presentation: {e}")
        return ErrorResponse(error=ErrorMessages.SAVE_FAILED.format(error=str(e))).model_dump_json()


@mcp.tool  # type: ignore[arg-type]
async def pptx_get_download_url(presentation: str | None = None, expires_in: int = 86400) -> str:
    """
    Get a presigned download URL for the presentation.

    Generates a temporary URL that can be used to download the presentation
    directly from cloud storage (S3/Tigris). The URL expires after the specified
    duration.

    Args:
        presentation: Name of presentation (uses current if not specified)
        expires_in: URL expiration time in seconds (default: 86400 = 24 hours)
            Common values:
            - 3600 = 1 hour
            - 86400 = 24 hours (default)
            - 604800 = 7 days
            - Maximum: 604800 (7 days) for most S3 providers

    Returns:
        JSON string with download URL or error

    Example:
        # Get URL with default 24-hour expiration
        result = await pptx_get_download_url()

        # Get URL with 7-day expiration
        result = await pptx_get_download_url(expires_in=604800)
    """
    try:
        import io

        from chuk_mcp_server import get_artifact_store, has_artifact_store

        pres_name = presentation or manager.get_current_name()
        if not pres_name:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Make sure presentation exists
        prs = await manager.get_presentation(pres_name)
        if not prs:
            return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

        # Get artifact store
        if not has_artifact_store():
            return ErrorResponse(
                error="No artifact store configured. Set up S3/Tigris storage."
            ).model_dump_json()

        store = get_artifact_store()

        # Export presentation to bytes
        buffer = io.BytesIO()
        await asyncio.to_thread(prs.save, buffer)
        buffer.seek(0)
        pptx_data = buffer.read()

        # Store as artifact to get presigned URL
        artifact_id = await store.store(
            data=pptx_data,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            summary=f"{pres_name}.pptx",
            meta={
                "filename": f"{pres_name}.pptx",
                "presentation_name": pres_name,
                "expiration_days": 30,  # Hint for S3 lifecycle policy
            },
        )
        logger.info(f"Stored presentation as artifact: {artifact_id}")

        # Generate presigned URL
        url = await store.presign(artifact_id, expires=expires_in)
        logger.info(f"Generated presigned URL for {pres_name}")

        from .models import DownloadUrlResponse

        return DownloadUrlResponse(
            url=url,
            presentation=pres_name,
            artifact_id=artifact_id,
            expires_in=expires_in,
            message=f"Generated download URL for {pres_name}, expires in {expires_in} seconds",
        ).model_dump_json()
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
            download_url=None,
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

        prs = await manager.get_presentation(name)
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


@mcp.tool  # type: ignore[arg-type]
async def pptx_status() -> str:
    """
    Get server status and configuration information.

    Returns information about the server, storage configuration,
    and loaded presentations. Useful for debugging and monitoring.

    Returns:
        JSON string with StatusResponse model

    Example:
        status = await pptx_status()
    """
    import os

    from chuk_mcp_server import has_artifact_store

    from .models import StatusResponse

    try:
        provider = os.environ.get("CHUK_ARTIFACTS_PROVIDER", "memory")
        storage_path = manager.base_path

        return StatusResponse(
            server="chuk-mcp-pptx",
            version="0.2.1",
            storage_provider=provider,
            storage_path=storage_path,
            presentations_loaded=len(manager._presentations),
            current_presentation=manager.get_current_name(),
            artifact_store_available=has_artifact_store(),
        ).model_dump_json()
    except Exception as e:
        logger.error(f"Failed to get server status: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()


# Run the server
if __name__ == "__main__":
    logger.info("Starting PowerPoint MCP Server...")
    logger.info(f"Base Path: {manager.base_path}")
    logger.info("Storage: Using chuk-mcp-server artifact store context")

    # Run in stdio mode when executed directly
    mcp.run(stdio=True)
