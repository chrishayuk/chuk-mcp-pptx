"""
Template listing tools.

Provides tools to list and discover available presentation templates.
All responses use Pydantic models for type safety.
"""

import logging
from .models import (
    PresentationTemplateListResponse,
    BuiltinTemplateInfo,
    CustomTemplateInfo,
)

logger = logging.getLogger(__name__)


def register_list_tools(mcp, manager, template_manager):
    """Register template listing tools."""

    @mcp.tool
    async def pptx_list_templates() -> str:
        """
        List all available presentation templates (.pptx template files).

        **TEMPLATES** are complete .pptx files like "brand_proposal" that contain layouts,
        themes, and example slides. Use this when the user mentions "template", "brand template",
        "brand proposal template", etc.

        **NOT** for semantic slide types - use pptx_list_slide_types for that.

        Returns Pydantic-validated response with builtin and custom templates separated.

        Returns:
            JSON string with PresentationTemplateListResponse model

        Example:
            # User says: "use brand proposal template"
            result = await pptx_list_templates()
            # Returns: {
            #   "builtin_templates": [
            #     {"name": "brand_proposal", "display_name": "Brand Proposal", "layout_count": 55, ...}
            #   ],
            #   "custom_templates": [...],
            #   "total": 6
            # }

            # Then create:
            await pptx_create(name="my_deck", template_name="brand_proposal")
        """
        try:
            builtin_templates = []
            custom_templates = []

            # Get built-in templates from template manager
            if template_manager:
                builtin_list = template_manager.list_templates()
                for tmpl in builtin_list:
                    builtin_templates.append(
                        BuiltinTemplateInfo(
                            name=tmpl.name,
                            display_name=tmpl.display_name,
                            description=tmpl.description,
                            category=tmpl.category,
                            layout_count=tmpl.layout_count,
                            tags=tmpl.tags,
                            is_builtin=True,
                        )
                    )

            # Get custom templates from artifact store
            presentations_response = await manager.list_presentations()
            for pres_info in presentations_response.presentations:
                metadata = manager._metadata.get(pres_info.name)
                if metadata and metadata.namespace_id:
                    # Check if this is a template (stored in templates/ path)
                    if "/templates/" in (metadata.vfs_path or ""):
                        custom_templates.append(
                            CustomTemplateInfo(
                                name=pres_info.name,
                                slide_count=pres_info.slide_count,
                                namespace_id=pres_info.namespace_id,
                                is_builtin=False,
                                category="custom",
                            )
                        )

            # Build response
            response = PresentationTemplateListResponse(
                builtin_templates=builtin_templates,
                custom_templates=custom_templates,
                total=len(builtin_templates) + len(custom_templates),
            )

            return response.model_dump_json()

        except Exception as e:
            logger.error(f"Failed to list templates: {e}", exc_info=True)
            from ...models import ErrorResponse

            return ErrorResponse(error=str(e)).model_dump_json()

    return {
        "pptx_list_templates": pptx_list_templates,
    }
