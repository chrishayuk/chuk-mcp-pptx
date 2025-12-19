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

        ⚠️ REQUIRED FIRST STEP - Before calling this tool:
        You MUST call pptx_analyze_template() first to see ALL available layouts.
        Templates often have 20-50+ different layouts (Title, Content, Comparison, etc.)
        and you should use a variety of them to create engaging presentations.

        Common layout types to look for:
        - Title slides (for section headers)
        - Content with Picture (text + image)
        - Two Content (side-by-side content)
        - Comparison (compare two things)
        - Quote/Testimonial (for quotes)
        - Section Header (chapter dividers)
        - Blank/Empty (for custom layouts)
        - Charts/Data layouts
        - Agenda layouts
        - Conclusion layouts

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

        CRITICAL NEXT STEPS after calling this tool:
            1. Review the layout_info.placeholders in the response
            2. Call pptx_populate_placeholder(slide_index=X, placeholder_idx=Y, content="...")
               for EACH placeholder you want to populate
            3. For PICTURE placeholders, use pptx_add_component with target_placeholder

        DO NOT:
        - Use the same layout repeatedly - templates have variety for a reason!
        - Use pptx_add_text_box or free-form positioning - it bypasses template design
        - Skip analyzing the template first - you'll miss better layout options

        Example Workflow:
            # Step 1: ALWAYS analyze template FIRST to see ALL layouts
            layouts = await pptx_analyze_template("brand_proposal")
            # Returns layouts like: "Title with Picture", "Content with Picture",
            # "Two Content", "Comparison", "Quote", "Data Chart", etc.
            # Note the index for each layout you want to use

            # Step 2: Choose appropriate layout for your content
            # Find "Content with Picture" in the layouts list (say it's at index 20)
            result = await pptx_add_slide_from_template(layout_index=20)

            # Step 3: Populate ALL placeholders
            await pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="Our Product")
            await pptx_populate_placeholder(slide_index=0, placeholder_idx=1, content="Features...")

            # For comparison slide -> find "Comparison" layout in the list
            result2 = await pptx_add_slide_from_template(layout_index=<index_from_analysis>)
            # Then populate left/right content placeholders

            # For data/charts -> find chart-friendly layout in the list
            result3 = await pptx_add_slide_from_template(layout_index=<index_from_analysis>)
            # Then add table/chart to the chart placeholder
        """
        try:
            from ...models.responses import SlideResponse, LayoutInfo, PlaceholderInfo

            # Get current presentation
            result = await manager.get(presentation)
            if not result:
                from ...models import ErrorResponse
            return ErrorResponse(error="Presentation not found").model_dump_json()

            prs, metadata = result

            # When created from template, presentation already has all layouts
            # No need to load template separately - just use the presentation's layouts
            if layout_index < 0 or layout_index >= len(prs.slide_layouts):
                from ...models import ErrorResponse
            return ErrorResponse(
                error=f"Invalid layout index: {layout_index} (presentation has {len(prs.slide_layouts)} layouts)"
            ).model_dump_json()

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
                            type=shape.placeholder_format.type.name
                            if hasattr(shape.placeholder_format.type, "name")
                            else str(shape.placeholder_format.type),
                            name=shape.name,
                        )
                    )
                except Exception as e:
                    logger.warning(f"Could not analyze placeholder: {e}")

            # Create guidance message with explicit placeholder requirements
            if placeholders:
                placeholder_list = ", ".join(
                    [f"idx={p.idx} {p.name} (type: {p.type})" for p in placeholders]
                )

                # Count placeholder types
                text_placeholders = [
                    p for p in placeholders if p.type in ("TITLE", "SUBTITLE", "BODY")
                ]
                picture_placeholders = [p for p in placeholders if p.type == "PICTURE"]
                chart_placeholders = [p for p in placeholders if p.type == "CHART"]
                table_placeholders = [p for p in placeholders if p.type == "TABLE"]
                object_placeholders = [
                    p for p in placeholders if p.type == "OBJECT"
                ]  # Generic content placeholder

                guidance_parts = [
                    f"✅ Slide {slide_index} added with layout '{layout.name}'.",
                    f"📋 Found {len(placeholders)} placeholders: {placeholder_list}",
                ]

                if text_placeholders:
                    text_ids = ", ".join([str(p.idx) for p in text_placeholders])
                    guidance_parts.append("⚠️ REQUIRED NEXT STEPS:")
                    guidance_parts.append(
                        f"   1. Call pptx_populate_placeholder() for EACH text placeholder: {text_ids}"
                    )
                    guidance_parts.append(
                        f"      Example: await pptx_populate_placeholder(slide_index={slide_index}, placeholder_idx={text_placeholders[0].idx}, content='Your text here')"
                    )

                if chart_placeholders:
                    chart_ids = ", ".join([str(p.idx) for p in chart_placeholders])
                    guidance_parts.append(
                        f"   🚨 CRITICAL: This layout has CHART placeholder(s) at indices {chart_ids}"
                    )
                    guidance_parts.append(
                        f"      ✅ RECOMMENDED (Simple): await pptx_populate_placeholder(slide_index={slide_index}, placeholder_idx={chart_placeholders[0].idx}, content={{'type': 'ColumnChart', 'series': {{...}}, 'categories': [...]}})"
                    )
                    guidance_parts.append(
                        f"      OR: await pptx_add_component(slide_index={slide_index}, component='ColumnChart', target_placeholder={chart_placeholders[0].idx}, params={{...}})"
                    )
                    guidance_parts.append(
                        "      ❌ DO NOT use left/top/width/height (creates overlays!)"
                    )

                if table_placeholders:
                    table_ids = ", ".join([str(p.idx) for p in table_placeholders])
                    guidance_parts.append(
                        f"   📊 CRITICAL: This layout has TABLE placeholder(s) at indices {table_ids}"
                    )
                    guidance_parts.append(
                        f"      ✅ RECOMMENDED (Simple): await pptx_populate_placeholder(slide_index={slide_index}, placeholder_idx={table_placeholders[0].idx}, content={{'type': 'Table', 'headers': [...], 'data': [[...]]}})"
                    )
                    guidance_parts.append(
                        f"      OR: await pptx_add_component(slide_index={slide_index}, component='Table', target_placeholder={table_placeholders[0].idx}, params={{...}})"
                    )
                    guidance_parts.append(
                        "      ❌ DO NOT use left/top/width/height (creates overlays!)"
                    )

                if object_placeholders:
                    obj_ids = ", ".join([str(p.idx) for p in object_placeholders])
                    guidance_parts.append(
                        f"   📦 OBJECT placeholder(s) at indices {obj_ids} - flexible content areas"
                    )
                    guidance_parts.append(
                        f"      ⚠️ ANALYZE THE LAYOUT FIRST: Look at the layout name '{layout.name}' to understand what content makes sense"
                    )
                    guidance_parts.append(
                        "      • Agenda/List layouts → Use text bullets, NOT tables"
                    )
                    guidance_parts.append(
                        "      • Data/Chart layouts → Use charts or tables with actual data"
                    )
                    guidance_parts.append(
                        "      • Content layouts → Use text, bullets, or simple visuals"
                    )
                    guidance_parts.append(
                        "      ✅ Populate with: pptx_populate_placeholder(placeholder_idx=X, content='text' OR {'type': 'Table/Chart', ...})"
                    )

                if picture_placeholders:
                    pic_ids = ", ".join([str(p.idx) for p in picture_placeholders])
                    guidance_parts.append(
                        f"   📷 For image placeholder(s) {pic_ids}: await pptx_populate_placeholder(placeholder_idx=X, content={{'type': 'Image', 'image_source': '...'}})"
                    )

                guidance_parts.append(
                    f"   🔍 CRITICAL - VERIFY AFTER POPULATING: Call pptx_list_slide_components(slide_index={slide_index})"
                )
                guidance_parts.append(
                    "      This command shows which placeholders are still empty and need content"
                )
                guidance_parts.append(
                    "      ⚠️ EVERY placeholder MUST be filled - empty placeholders show 'Click to add' text in the final presentation"
                )
                guidance_parts.append(
                    "🚫 DO NOT use pptx_add_text_box or free-form positioning - it will overlay the placeholders and break the template design!"
                )

                # Add verification reminder at the end
                guidance_parts.append("\n⚠️ MANDATORY VERIFICATION STEP:")
                guidance_parts.append(
                    "   After populating ALL placeholders on this slide, you MUST call:"
                )
                guidance_parts.append(f"   pptx_list_slide_components(slide_index={slide_index})")
                guidance_parts.append("   Check the response to ensure:")
                guidance_parts.append("   • No empty placeholders remain")
                guidance_parts.append("   • All images loaded successfully")
                guidance_parts.append(
                    f"   • Content is appropriate for the layout ('{layout.name}')"
                )

                guidance = " ".join(guidance_parts)
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
            from ...models import ErrorResponse

            return ErrorResponse(error=str(e)).model_dump_json()

    return {
        "pptx_add_slide_from_template": pptx_add_slide_from_template,
    }
