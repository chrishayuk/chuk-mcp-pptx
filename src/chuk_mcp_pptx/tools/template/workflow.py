"""
Template workflow tools.

Provides tools for working with template-based presentations.
All responses use Pydantic models for type safety.
"""

import logging

logger = logging.getLogger(__name__)


def register_workflow_tools(mcp, manager, template_manager):
    """Register template workflow tools."""

    @mcp.tool
    async def pptx_add_slide_from_template(
        layout_index: int,
        template_name: str | None = None,
        presentation: str | None = None,
    ) -> str:
        """
        Add a slide using a specific layout from the template.

        When a presentation is created from a template, this tool adds a new slide
        using one of the template's layouts. Use pptx_analyze_template to see
        available layout indices and their names.

        Args:
            layout_index: Index of the layout to use (from pptx_analyze_template)
            template_name: Optional template name (if different from presentation's template)
            presentation: Optional presentation name (uses current if not specified)

        Returns:
            JSON string with SlideResponse including:
            - slide_index: The index of the newly added slide
            - layout_info: Object containing:
                - layout_name: Name of the layout used
                - placeholders: List of available placeholders with idx, type, and name
                - message: Guidance on how to populate the placeholders

        CRITICAL NEXT STEPS:
            After calling this tool, you MUST:
            1. Review the layout_info.placeholders in the response
            2. Call pptx_populate_placeholder(slide_index=X, placeholder_idx=Y, content="...")
               for EACH placeholder you want to populate
            3. Optionally call pptx_list_slide_components(slide_index=X) to see any
               pre-existing components from the layout (shapes, images, etc.)

        DO NOT use pptx_add_text_box or other overlay tools - they bypass the template
        design. Always use pptx_populate_placeholder to respect the template's styling.

        Example Workflow:
            # Step 1: Analyze template to find layout indices
            layouts = await pptx_analyze_template("brand_proposal")
            # You see: layout 1 = "Content with Picture"

            # Step 2: Add slide with that layout
            result = await pptx_add_slide_from_template(layout_index=1)
            # Response: slide_index=5, placeholders=[
            #   {idx=0, type=TITLE, name="Title 1"},
            #   {idx=1, type=OBJECT, name="Content Placeholder 2"},
            #   {idx=2, type=PICTURE, name="Picture Placeholder 3"}
            # ]

            # Step 3: Populate text placeholders
            await pptx_populate_placeholder(slide_index=5, placeholder_idx=0, content="Our Product")
            await pptx_populate_placeholder(slide_index=5, placeholder_idx=1, content="Key features...")

            # Step 4: Check what other components exist
            components = await pptx_list_slide_components(slide_index=5)
            # Shows any decorative shapes or elements from the layout

            # Step 5: Add image to picture placeholder if needed
            # Use pptx_add_component for images into PICTURE placeholders
        """
        try:
            from ...models.responses import SlideResponse, LayoutInfo, PlaceholderInfo

            # Get current presentation
            result = await manager.get(presentation)
            if not result:
                from ...models import ErrorResponse; return ErrorResponse(error="Presentation not found").model_dump_json()

            prs, metadata = result

            # When created from template, presentation already has all layouts
            # No need to load template separately - just use the presentation's layouts
            if layout_index < 0 or layout_index >= len(prs.slide_layouts):
                from ...models import ErrorResponse; return ErrorResponse(error=f"Invalid layout index: {layout_index} (presentation has {len(prs.slide_layouts)} layouts)").model_dump_json()

            layout = prs.slide_layouts[layout_index]

            # Add slide with layout
            slide = prs.slides.add_slide(layout)
            slide_index = len(prs.slides) - 1

            # Analyze layout placeholders
            placeholders = []
            for shape in slide.placeholders:
                try:
                    placeholders.append(
                        PlaceholderInfo(
                            idx=shape.placeholder_format.idx,
                            type=shape.placeholder_format.type.name if hasattr(shape.placeholder_format.type, 'name') else str(shape.placeholder_format.type),
                            name=shape.name,
                        )
                    )
                except Exception as e:
                    logger.warning(f"Could not analyze placeholder: {e}")

            # Create guidance message
            if placeholders:
                placeholder_list = ", ".join([f"idx={p.idx} {p.name} (type: {p.type})" for p in placeholders])
                guidance = (
                    f"Slide added with layout '{layout.name}'. Available placeholders: {placeholder_list}. "
                    f"IMPORTANT: Use pptx_populate_placeholder(slide_index={slide_index}, placeholder_idx=X, content='...') "
                    f"to populate each placeholder and respect the template's design system. "
                    f"Do NOT use pptx_add_text_box as it overlays content and bypasses the template design."
                )
            else:
                guidance = f"Slide added with layout '{layout.name}'. No placeholders detected - this may be a blank layout."

            # Create layout info
            layout_info = LayoutInfo(
                layout_index=layout_index,
                layout_name=layout.name,
                placeholders=placeholders,
                message=guidance,
            )

            # Update metadata
            await manager.update_slide_metadata(slide_index)
            metadata.update_modified()

            # Save to artifact store
            await manager._save_to_store(metadata.name, prs)

            # Return Pydantic response
            response = SlideResponse(
                presentation=metadata.name,
                slide_index=slide_index,
                message=f"Added slide with layout '{layout.name}'",
                slide_count=len(prs.slides),
                layout_info=layout_info,
            )

            return response.model_dump_json()

        except Exception as e:
            logger.error(f"Failed to add slide from template: {e}")
            from ...models import ErrorResponse; return ErrorResponse(error=str(e)).model_dump_json()

    return {
        "pptx_add_slide_from_template": pptx_add_slide_from_template,
    }
