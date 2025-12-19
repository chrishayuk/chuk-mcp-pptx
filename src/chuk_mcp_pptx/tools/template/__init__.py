"""
Template tools package.

Consolidated template functionality:
- list.py: List and discover templates
- analyze.py: Analyze template structure and layouts
- import_tools.py: Import templates from files or builtins
- workflow.py: Working with template-based presentations
- extraction.py: Extract design system from templates
"""

from .list import register_list_tools
from .analyze import register_analyze_tools
from .import_tools import register_import_tools
from .workflow import register_workflow_tools
from .extraction import register_extraction_tools


def register_template_tools(mcp, manager, template_manager=None):
    """
    Register all template tools.

    This is the consolidated registration function that replaces the old
    template_tools.py module.

    Args:
        mcp: The MCP server instance
        manager: PresentationManager instance
        template_manager: Optional TemplateManager instance for built-in templates
    """
    from ...templates import TemplateManager

    if template_manager is None:
        template_manager = TemplateManager()

    # Register all tool groups
    list_tools = register_list_tools(mcp, manager, template_manager)
    analyze_tools = register_analyze_tools(mcp, manager, template_manager)
    import_tools = register_import_tools(mcp, manager, template_manager)
    workflow_tools = register_workflow_tools(mcp, manager, template_manager)

    # Merge all tools into single dictionary
    all_tools = {
        **list_tools,
        **analyze_tools,
        **import_tools,
        **workflow_tools,
    }

    return all_tools


__all__ = [
    "register_template_tools",
    "register_extraction_tools",
    "register_list_tools",
    "register_analyze_tools",
    "register_import_tools",
    "register_workflow_tools",
]
