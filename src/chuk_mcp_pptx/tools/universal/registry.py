"""
MCP tools for component registry discovery and schema access.
Enables LLMs to discover and understand available components.
"""

import json

from ...components.registry import registry


def register_registry_tools(mcp, manager):
    """
    Register component registry tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        manager: PresentationManager instance (not used but kept for consistency)

    Returns:
        Dictionary of registered tools
    """
    tools = {}

    @mcp.tool
    async def pptx_list_components(category: str | None = None) -> str:
        """
        List all available PowerPoint components.

        Returns all components in the design system registry, optionally
        filtered by category. This is the starting point for discovering
        what components are available for building presentations.

        Args:
            category: Optional category filter (layout, ui, chart, data, text, media, container)

        Returns:
            JSON list of available components with brief descriptions

        Example:
            # List all components
            components = await pptx_list_components()

            # List only UI components
            ui_components = await pptx_list_components(category="ui")
        """

        from ...components.registry import ComponentCategory

        if category:
            try:
                cat = ComponentCategory(category.lower())
                component_names = registry.list_by_category(cat)
            except ValueError:
                return json.dumps(
                    {
                        "error": f"Invalid category '{category}'",
                        "valid_categories": [c.value for c in ComponentCategory],
                    }
                )
        else:
            component_names = registry.list_components()

        components = []
        for name in component_names:
            metadata = registry.get(name)
            if metadata:
                components.append(
                    {
                        "name": name,
                        "category": metadata.category.value,
                        "description": metadata.description,
                        "tags": metadata.tags,
                    }
                )

        return json.dumps(
            {"components": components, "count": len(components), "category_filter": category},
            indent=2,
        )

    @mcp.tool
    async def pptx_get_component_schema(name: str) -> str:
        """
        Get detailed schema for a specific component.

        Returns the complete schema definition including props, variants,
        composition support, and usage examples for a component.

        Args:
            name: Component name (e.g., "Button", "Card", "Alert")

        Returns:
            JSON schema with component details

        Example:
            schema = await pptx_get_component_schema(name="Button")
            # Returns complete schema with props, variants, examples
        """

        schema = registry.get_schema(name)
        if not schema:
            return json.dumps(
                {
                    "error": f"Component '{name}' not found",
                    "hint": "Use pptx_list_components() to see available components",
                }
            )

        return json.dumps(schema, indent=2)

    @mcp.tool
    async def pptx_search_components(query: str) -> str:
        """
        Search for components by keyword.

        Searches component names, descriptions, and tags to find
        relevant components for your use case.

        Args:
            query: Search query (e.g., "button", "chart", "metric")

        Returns:
            JSON list of matching components

        Example:
            results = await pptx_search_components(query="metric")
            # Finds MetricCard, ValueTile, etc.
        """

        results = registry.search(query)

        components = []
        for metadata in results:
            components.append(
                {
                    "name": metadata.name,
                    "category": metadata.category.value,
                    "description": metadata.description,
                    "tags": metadata.tags,
                }
            )

        return json.dumps(
            {"query": query, "results": components, "count": len(components)}, indent=2
        )

    @mcp.tool
    async def pptx_get_component_variants(name: str) -> str:
        """
        Get available variants for a component.

        Returns all variant options for a component (e.g., button variants:
        default, secondary, outline, ghost, destructive).

        Args:
            name: Component name

        Returns:
            JSON with variant options

        Example:
            variants = await pptx_get_component_variants(name="Button")
            # Returns: {"variant": ["default", "secondary", ...], "size": ["sm", "md", "lg"]}
        """

        variants = registry.list_variants(name)
        if variants is None:
            return json.dumps({"error": f"Component '{name}' not found"})

        return json.dumps({"component": name, "variants": variants}, indent=2)

    @mcp.tool
    async def pptx_get_component_examples(name: str) -> str:
        """
        Get usage examples for a component.

        Returns code examples showing how to use the component
        in different scenarios.

        Args:
            name: Component name

        Returns:
            JSON with usage examples

        Example:
            examples = await pptx_get_component_examples(name="Card")
            # Returns code examples and descriptions
        """

        examples = registry.get_examples(name)
        if not examples:
            metadata = registry.get(name)
            if not metadata:
                return json.dumps({"error": f"Component '{name}' not found"})
            return json.dumps({"component": name, "examples": []})

        return json.dumps({"component": name, "examples": examples}, indent=2)

    @mcp.tool
    async def pptx_export_registry_docs() -> str:
        """
        Export complete component registry documentation.

        Returns the full registry as LLM-friendly JSON documentation.
        Useful for understanding the entire component system at once.

        Returns:
            Complete registry documentation in JSON format

        Example:
            docs = await pptx_export_registry_docs()
            # Returns complete documentation for all components
        """

        return registry.export_for_llm()

    # Store tools for return
    tools["pptx_list_components"] = pptx_list_components
    tools["pptx_get_component_schema"] = pptx_get_component_schema
    tools["pptx_search_components"] = pptx_search_components
    tools["pptx_get_component_variants"] = pptx_get_component_variants
    tools["pptx_get_component_examples"] = pptx_get_component_examples
    tools["pptx_export_registry_docs"] = pptx_export_registry_docs

    return tools
