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
        content: str | dict,
        presentation: str | None = None,
    ) -> str:
        """
        Populate a specific placeholder in a slide with content.

        This is a SMART TOOL that automatically handles ALL content types:
        - Text strings → Populates text/title/body placeholders
        - Structured dicts → Renders tables/charts/images directly into placeholders

        This is the PREFERRED way to populate placeholders as it:
        1. Respects the template's design system
        2. Automatically sizes content to fit the placeholder
        3. Validates content before rendering
        4. Tracks components properly

        IMPORTANT: After calling pptx_add_slide_from_template, use the placeholder
        information from layout_info to populate each placeholder with this tool.

        Args:
            slide_index: Index of the slide (0-based)
            placeholder_idx: Index of the placeholder to populate (from layout_info)
            content: Content to insert - can be:
                - String: Text content for text/title/body placeholders
                - Dict: Structured content for tables/charts/images (rendered directly)
                - JSON string: Will be parsed and handled as dict
            presentation: Name of presentation (uses current if not specified)

        Returns:
            JSON string with success/error message

        Content Types (String):
            Simple text for TITLE, SUBTITLE, BODY placeholders

        Content Types (Dict - Rendered directly into placeholder):
            Tables:
                {'type': 'Table', 'headers': [...], 'data': [[...]], 'variant': 'striped'}
            Charts:
                {'type': 'ColumnChart', 'series': {...}, 'categories': [...], 'title': '...'}
            Images:
                {'type': 'Image', 'image_source': 'url', 'alt': '...'}
            Videos:
                {'type': 'Video', 'video_source': 'url', 'poster_image': '...', 'autoplay': false}

        Placeholder Types:
            - TITLE (type 1): Main title placeholder → use string content
            - BODY (type 2): Content area (can be text or bullets) → use string content
            - SUBTITLE (type 3): Subtitle text → use string content
            - OBJECT (type 7): Multi-purpose content area → use string OR dict (tables/charts)
            - CHART (type 12): Chart placeholder → use dict with chart data
            - TABLE (type 14): Table placeholder → use dict with table data
            - PICTURE (type 18): Image placeholder → use dict with image data

        BEST PRACTICE - Verify After Populating:
            After populating placeholders on a slide, call pptx_list_slide_components
            to verify the slide layout and ensure all components are positioned correctly.
            This helps catch any issues early before moving to the next slide.

        Example 1 - Text placeholders:
            # 1. Add slide with template layout
            result = await pptx_add_slide_from_template(layout_index=1)
            # Response shows: placeholder 0 (TITLE), placeholder 1 (BODY)

            # 2. Populate the title placeholder (STRING)
            await pptx_populate_placeholder(
                slide_index=0,
                placeholder_idx=0,
                content="Our Story"
            )

            # 3. Populate the body placeholder with bullets (STRING)
            await pptx_populate_placeholder(
                slide_index=0,
                placeholder_idx=1,
                content="Started in 2020\\nFamily-owned\\nArtisan quality"
            )

        Example 2 - Table in placeholder (DICT - rendered directly):
            # Add slide with table placeholder
            result = await pptx_add_slide_from_template(layout_index=50)
            # Response shows: placeholder 14 (OBJECT)

            # Populate with table data (DICT - rendered directly into placeholder)
            await pptx_populate_placeholder(
                slide_index=3,
                placeholder_idx=14,
                content={
                    'type': 'Table',
                    'headers': ['Product', 'Description', 'Price'],
                    'data': [
                        ['Cheesums Classic', 'Aged cow\\'s milk', '$9.99'],
                        ['Truffle Bliss', 'Black truffle', '$19.99']
                    ],
                    'variant': 'striped'
                }
            )

        Example 3 - Chart in placeholder (DICT - rendered directly):
            # Add slide with chart placeholder
            result = await pptx_add_slide_from_template(layout_index=40)
            # Response shows: placeholder 2 (CHART)

            # Populate with chart data (DICT - rendered directly into placeholder)
            await pptx_populate_placeholder(
                slide_index=5,
                placeholder_idx=2,
                content={
                    'type': 'ColumnChart',
                    'title': 'Revenue Forecast',
                    'categories': ['2025', '2026', '2027'],
                    'series': {
                        'Retail': [120, 180, 260],
                        'Wholesale': [80, 120, 170]
                    }
                }
            )

        Example 4 - Image in placeholder (DICT - rendered directly):
            # Add slide with picture placeholder
            result = await pptx_add_slide_from_template(layout_index=51)
            # Response shows: placeholder 15 (PICTURE)

            # Populate with image (DICT - rendered directly into placeholder)
            await pptx_populate_placeholder(
                slide_index=6,
                placeholder_idx=15,
                content={
                    'type': 'Image',
                    'image_source': 'https://example.com/cheese.jpg',
                    'alt': 'Cheese platter'
                }
            )

        Example 5 - JSON string content (automatically parsed):
            # MCP may pass content as JSON string - will be parsed automatically
            await pptx_populate_placeholder(
                slide_index=6,
                placeholder_idx=15,
                content='{"type":"Image","image_source":"https://example.com/photo.jpg"}'
            )
            # This is automatically parsed and handled as a dict
        """
        try:
            from ...models import ErrorResponse
            from ...constants import ErrorMessages
            import json

            # Parse content if it's a JSON string
            parsed_content = content
            if isinstance(content, str):
                # Try to parse as JSON - if it looks like a dict/object
                content_stripped = content.strip()
                if content_stripped.startswith("{") and content_stripped.endswith("}"):
                    try:
                        parsed_content = json.loads(content)
                        logger.info(f"Parsed JSON string content into dict: {parsed_content}")
                    except json.JSONDecodeError:
                        # Not valid JSON, treat as plain text
                        parsed_content = content
                else:
                    # Plain text string
                    parsed_content = content

            # SMART ROUTING: If content is a dict, handle structured content (tables, charts, images)
            if isinstance(parsed_content, dict):
                # Extract component type and params
                component_type = parsed_content.get("type")
                if not component_type:
                    return ErrorResponse(
                        error="Dict content must include 'type' field (e.g., 'Table', 'ColumnChart', 'Image')"
                    ).model_dump_json()

                # Build params dict (everything except 'type')
                params = {k: v for k, v in parsed_content.items() if k != "type"}

                logger.info(
                    f"Smart routing: Detected structured content for {component_type}, rendering to placeholder {placeholder_idx}"
                )

                # Get presentation
                result = await manager.get(presentation)
                if not result:
                    return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

                prs, metadata = result

                # Validate slide index
                if slide_index < 0 or slide_index >= len(prs.slides):
                    return ErrorResponse(
                        error=f"Slide index {slide_index} not found. Presentation has {len(prs.slides)} slides."
                    ).model_dump_json()

                slide = prs.slides[slide_index]

                # Find the placeholder
                placeholder = None
                for shape in slide.placeholders:
                    if shape.placeholder_format.idx == placeholder_idx:
                        placeholder = shape
                        break

                if not placeholder:
                    available = [
                        f"idx={ph.placeholder_format.idx} ({ph.placeholder_format.type})"
                        for ph in slide.placeholders
                    ]
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} not found on slide {slide_index}. "
                        f"Available placeholders: {', '.join(available) if available else 'none'}"
                    ).model_dump_json()

                # Import component registry and get component class
                from ...components.registry import get_component_class
                from ...components.tracking import component_tracker

                try:
                    component_class = get_component_class(component_type)
                    if not component_class:
                        return ErrorResponse(
                            error=f"Unknown component type: {component_type}"
                        ).model_dump_json()

                    # Filter params to only include valid parameters for this component
                    import inspect

                    sig = inspect.signature(component_class.__init__)
                    valid_params = set(sig.parameters.keys()) - {"self"}

                    # Filter out invalid params and warn about them
                    filtered_params = {}
                    invalid_params = []
                    for key, value in params.items():
                        if key in valid_params:
                            filtered_params[key] = value
                        else:
                            invalid_params.append(key)

                    if invalid_params:
                        logger.warning(
                            f"Ignoring invalid parameters for {component_type}: {invalid_params}"
                        )

                    # Instantiate component with filtered params (validation happens in __init__)
                    component_instance = component_class(**filtered_params)

                    # Extract placeholder bounds for sizing
                    left = placeholder.left.inches
                    top = placeholder.top.inches
                    width = placeholder.width.inches
                    height = placeholder.height.inches

                    # Render component to placeholder
                    shape = await component_instance.render(
                        slide=slide,
                        left=left,
                        top=top,
                        width=width,
                        height=height,
                        placeholder=placeholder,
                    )

                    # Track component
                    component_tracker.register(
                        presentation=metadata.name,
                        slide_index=slide_index,
                        component_id=f"{component_type.lower()}_{placeholder_idx}",
                        component_type=component_type,
                        left=left,
                        top=top,
                        width=width,
                        height=height,
                        target_type="placeholder",
                        target_id=placeholder_idx,
                        params=filtered_params,
                    )

                    # Update presentation
                    await manager.update(presentation)

                    from ...models import SuccessResponse

                    return SuccessResponse(
                        message=f"Populated placeholder {placeholder_idx} with {component_type} on slide {slide_index}"
                    ).model_dump_json()

                except Exception as e:
                    logger.error(
                        f"Failed to render {component_type} to placeholder: {e}", exc_info=True
                    )
                    return ErrorResponse(
                        error=f"Failed to render {component_type}: {str(e)}"
                    ).model_dump_json()

            # STRING CONTENT: Handle as text placeholder population
            if not isinstance(content, str):
                return ErrorResponse(
                    error=f"Content must be a string or dict, got {type(content).__name__}"
                ).model_dump_json()

            # Get presentation
            prs = await manager.get_presentation(presentation)
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
                if hasattr(placeholder, "text_frame"):
                    placeholder.text_frame.text = content
                elif hasattr(placeholder, "text"):
                    placeholder.text = content
                else:
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} (type {placeholder_type}) "
                        f"does not support text content"
                    ).model_dump_json()

            # For BODY (2) or OBJECT (7) - content placeholders that can have bullets
            elif placeholder_type in (2, 7):  # BODY or OBJECT
                if not hasattr(placeholder, "text_frame"):
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} does not have a text frame"
                    ).model_dump_json()

                text_frame = placeholder.text_frame
                text_frame.clear()  # Clear existing content

                # Split content by newlines to create bullet points
                lines = content.split("\\n")
                for idx, line in enumerate(lines):
                    if idx == 0:
                        # Use existing first paragraph
                        p = text_frame.paragraphs[0]
                    else:
                        # Add new paragraphs for additional bullets
                        p = text_frame.add_paragraph()
                    p.text = line
                    p.level = 0  # Top-level bullet

            # For PICTURE, CHART, TABLE placeholders when given string content
            # Handle intelligently - treat as text content for these placeholders
            elif placeholder_type in (12, 14, 18):  # CHART, TABLE, PICTURE
                # These placeholders can have text content too (caption, title, etc.)
                # Try to populate as text if they have a text_frame
                if hasattr(placeholder, "text_frame"):
                    text_frame = placeholder.text_frame
                    text_frame.text = content
                elif hasattr(placeholder, "text"):
                    placeholder.text = content
                else:
                    # Only error if we truly can't add text
                    type_names = {12: "CHART", 14: "TABLE", 18: "PICTURE"}
                    type_name = type_names.get(placeholder_type, "content")
                    return ErrorResponse(
                        error=f"Placeholder {placeholder_idx} is a {type_name} placeholder without text capability. "
                        f"Use dict content: pptx_populate_placeholder(placeholder_idx={placeholder_idx}, "
                        f"content={{'type': 'Image/Table/ColumnChart', ...}})"
                    ).model_dump_json()

            # Other placeholder types
            else:
                # Try to populate as text
                if hasattr(placeholder, "text_frame"):
                    placeholder.text_frame.text = content
                elif hasattr(placeholder, "text"):
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
