"""
Template import tools.

Provides tools to import templates from files or builtin sources.
All responses use Pydantic models for type safety.
"""

import io
import logging
from pptx import Presentation

logger = logging.getLogger(__name__)


def register_import_tools(mcp, manager, template_manager):
    """Register template import tools."""

    @mcp.tool
    async def pptx_import_template(file_path: str, template_name: str) -> str:
        """
        Import a PowerPoint file as a template into the artifact store.

        This allows you to load an existing PowerPoint file as a template that can
        be used to create new presentations with the same layouts, styles, and themes.

        Args:
            file_path: Path to the PowerPoint file to import as template
            template_name: Name to save the template as (used in pptx_create)

        Returns:
            JSON string with success/error message and template info

        Example:
            await pptx_import_template(
                file_path="/path/to/corporate_template.pptx",
                template_name="corporate"
            )
        """
        try:
            from ...models import ErrorResponse

            success = await manager.import_template(file_path, template_name)
            if success:
                # Get template info by loading the analyze module
                from .analyze import register_analyze_tools

                analyze_tools = register_analyze_tools(mcp, manager, template_manager)
                template_info = await analyze_tools["pptx_analyze_template"](template_name)
                return template_info
            else:
                return ErrorResponse(
                    error=f"Failed to import template from {file_path}"
                ).model_dump_json()
        except Exception as e:
            logger.error(f"Failed to import template: {e}")
            from ...models import ErrorResponse

            return ErrorResponse(error=str(e)).model_dump_json()

    @mcp.tool
    async def pptx_get_builtin_template(template_name: str, save_as: str) -> str:
        """
        Load a built-in template and save it to the artifact store.

        This imports a built-in template (like "corporate", "modern", "tech") into
        your artifact store so it can be used with pptx_create.

        Args:
            template_name: Name of the built-in template (use pptx_list_templates to see options)
            save_as: Name to save the template as in artifact store

        Returns:
            JSON string with success message and template info

        Example:
            await pptx_get_builtin_template(
                template_name="corporate",
                save_as="my_corporate_template"
            )
        """
        try:
            from ...models import ErrorResponse, SuccessResponse

            # Get template data from template manager
            template_data = await template_manager.get_template_data(template_name)
            if not template_data:
                return ErrorResponse(
                    error=f"Built-in template not found: {template_name}"
                ).model_dump_json()

            # Import into artifact store
            from chuk_mcp_server import NamespaceType, StorageScope

            store = manager._get_store()
            if not store:
                return ErrorResponse(error="No artifact store available").model_dump_json()

            # Verify it's a valid presentation
            buffer = io.BytesIO(template_data)
            prs = Presentation(buffer)

            # Create namespace for template
            safe_name = manager._sanitize_name(save_as)
            namespace_info = await store.create_namespace(
                type=NamespaceType.BLOB,
                scope=StorageScope.SESSION,
                name=f"{manager.base_path}/templates/{safe_name}",
                metadata={
                    "mime_type": manager.PPTX_MIME_TYPE,
                    "template_name": save_as,
                    "file_extension": ".pptx",
                    "is_template": True,
                    "source": f"builtin:{template_name}",
                },
            )
            manager._namespace_ids[save_as] = namespace_info.namespace_id

            # Write template data
            await store.write_namespace(namespace_info.namespace_id, data=template_data)

            # Get layout count from loaded presentation
            layout_count = len(prs.slide_layouts) if prs.slide_layouts else 0

            return SuccessResponse(
                message=f"Built-in template '{template_name}' imported successfully as '{save_as}' with {layout_count} layouts"
            ).model_dump_json()
        except Exception as e:
            logger.error(f"Failed to get builtin template: {e}")
            from ...models import ErrorResponse

            return ErrorResponse(error=str(e)).model_dump_json()

    return {
        "pptx_import_template": pptx_import_template,
        "pptx_get_builtin_template": pptx_get_builtin_template,
    }
