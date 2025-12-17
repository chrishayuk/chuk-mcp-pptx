"""
Core Placeholder Tools

Essential tool for populating template placeholders, respecting the template's design system.
"""

import logging

logger = logging.getLogger(__name__)


def register_placeholder_tools(mcp, manager):
    """Register placeholder population tool."""

    @mcp.tool
    async def pptx_populate_placeholder(
        slide_index: int,
        placeholder_idx: int,
        content: str,
        presentation: str | None = None,
    ) -> str:
        """
        Populate a specific placeholder in a slide with content.

        This tool respects the template's design system by filling placeholders
        rather than overlaying arbitrary text boxes. Use this after adding a slide
        from a template to populate its placeholders.

        IMPORTANT: After calling pptx_add_slide_from_template, use the placeholder
        information from layout_info to populate each placeholder with this tool.

        Args:
            slide_index: Index of the slide (0-based)
            placeholder_idx: Index of the placeholder to populate (from layout_info)
            content: Text content to insert into the placeholder
            presentation: Name of presentation (uses current if not specified)

        Returns:
            JSON string with success/error message

        Placeholder Types:
            - TITLE (type 1): Main title placeholder
            - BODY (type 2): Content area (can be text or bullets)
            - SUBTITLE (type 3): Subtitle text
            - OBJECT (type 7): Multi-purpose content area (text, bullets, charts, tables)
            - PICTURE (type 18): Image placeholder (use pptx_add_component for images)

        BEST PRACTICE - Verify After Populating:
            After populating placeholders on a slide, call pptx_list_slide_components
            to verify the slide layout and ensure all components are positioned correctly.
            This helps catch any issues early before moving to the next slide.

        Example workflow:
            # 1. Add slide with template layout
            result = await pptx_add_slide_from_template(layout_index=1)
            # Response shows: placeholder 0 (TITLE), placeholder 1 (OBJECT)

            # 2. Populate the title placeholder
            await pptx_populate_placeholder(
                slide_index=16,
                placeholder_idx=0,
                content="Our Story"
            )

            # 3. Populate the content placeholder
            await pptx_populate_placeholder(
                slide_index=16,
                placeholder_idx=1,
                content="Cheesums started as a small artisan cooperative..."
            )

            # 4. VERIFY the slide layout (RECOMMENDED)
            components = await pptx_list_slide_components(slide_index=16)
            # Review that text is populated correctly and layout looks good

        Example with bullets:
            # For body placeholders, use newlines for bullet points
            await pptx_populate_placeholder(
                slide_index=17,
                placeholder_idx=1,
                content="First bullet point\\nSecond bullet point\\nThird bullet point"
            )

            # VERIFY the bullets rendered correctly
            components = await pptx_list_slide_components(slide_index=17)
        """
        try:
            from ...models import ErrorResponse
            from ...constants import ErrorMessages

            # Get presentation
            prs = manager.get_presentation(presentation)
            if not prs:
                return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

            # Validate slide index
            if slide_index < 0 or slide_index >= len(prs.slides):
                return ErrorResponse(
                    error=f"Slide index {slide_index} not found. Presentation has {len(prs.slides)} slides."
                ).model_dump_json()

            slide = prs.slides[slide_index]

            # Find the placeholder by idx
            placeholder = None
            for shape in slide.placeholders:
                if shape.placeholder_format.idx == placeholder_idx:
                    placeholder = shape
                    break

            if not placeholder:
                # List available placeholders to help debugging
                available = [
                    f"idx={ph.placeholder_format.idx} ({ph.placeholder_format.type})"
                    for ph in slide.placeholders
                ]
                return ErrorResponse(
                    error=f"Placeholder {placeholder_idx} not found on slide {slide_index}. "
                    f"Available placeholders: {', '.join(available) if available else 'none'}"
                ).model_dump_json()

            # Populate based on placeholder type
            placeholder_type = placeholder.placeholder_format.type

            # For TITLE (1), SUBTITLE (3), or simple text placeholders
            if placeholder_type in (1, 3):  # TITLE or SUBTITLE
                if hasattr(placeholder, 'text_frame'):
                    placeholder.text_frame.text = content
                elif hasattr(placeholder, 'text'):
                    placeholder.text = content
                else:
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} (type {placeholder_type}) "
                        f"does not support text content"
                    ).model_dump_json()

            # For BODY (2) or OBJECT (7) - content placeholders that can have bullets
            elif placeholder_type in (2, 7):  # BODY or OBJECT
                if not hasattr(placeholder, 'text_frame'):
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} does not have a text frame"
                    ).model_dump_json()

                text_frame = placeholder.text_frame
                text_frame.clear()  # Clear existing content

                # Split content by newlines to create bullet points
                lines = content.split('\\n')
                for idx, line in enumerate(lines):
                    if idx == 0:
                        # Use existing first paragraph
                        p = text_frame.paragraphs[0]
                    else:
                        # Add new paragraphs for additional bullets
                        p = text_frame.add_paragraph()
                    p.text = line
                    p.level = 0  # Top-level bullet

            # For PICTURE placeholders
            elif placeholder_type == 18:  # PICTURE
                return ErrorResponse(
                    error=f"Placeholder {placeholder_idx} is a PICTURE placeholder. "
                    f"Use pptx_add_component(component_type='Image', ...) to populate image placeholders."
                ).model_dump_json()

            # Other placeholder types
            else:
                # Try to populate as text
                if hasattr(placeholder, 'text_frame'):
                    placeholder.text_frame.text = content
                elif hasattr(placeholder, 'text'):
                    placeholder.text = content
                else:
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} (type {placeholder_type}) "
                        f"does not support text content"
                    ).model_dump_json()

            # Update in VFS
            await manager.update(presentation)

            pres_name = presentation or manager.get_current_name() or "presentation"

            from ...models import SuccessResponse
            return SuccessResponse(
                message=f"Populated placeholder {placeholder_idx} on slide {slide_index} in {pres_name}"
            ).model_dump_json()

        except Exception as e:
            logger.error(f"Failed to populate placeholder: {e}", exc_info=True)
            from ...models import ErrorResponse
            return ErrorResponse(error=str(e)).model_dump_json()

    return {
        "pptx_populate_placeholder": pptx_populate_placeholder,
    }
