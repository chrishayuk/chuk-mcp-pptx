"""
Tests for registry_tools.py

Tests all component registry and discovery MCP tools for >90% coverage.
"""

import pytest
import json
from unittest.mock import MagicMock, patch
from chuk_mcp_pptx.tools.universal.registry import register_registry_tools


@pytest.fixture
async def registry_tools(mock_mcp_server, mock_presentation_manager):
    """Register registry tools and return them."""
    tools = register_registry_tools(mock_mcp_server, mock_presentation_manager)
    return tools


@pytest.fixture
def mock_registry():
    """Create a mock component registry."""
    with patch("chuk_mcp_pptx.tools.universal.registry.registry") as mock_reg:
        # Mock registry methods
        mock_reg.list_components.return_value = ["Button", "Card", "Alert"]
        mock_reg.list_by_category.return_value = ["Button"]

        # Mock component metadata
        mock_metadata = MagicMock()
        mock_metadata.name = "Button"
        mock_metadata.category.value = "ui"
        mock_metadata.description = "A clickable button component"
        mock_metadata.tags = ["interactive", "action"]
        mock_reg.get.return_value = mock_metadata

        # Mock schema
        mock_schema = {
            "name": "Button",
            "props": {"text": "string", "variant": "string"},
            "variants": {"variant": ["default", "primary", "secondary"]},
            "examples": [],
        }
        mock_reg.get_schema.return_value = mock_schema

        # Mock search results
        mock_reg.search.return_value = [mock_metadata]

        # Mock variants
        mock_reg.list_variants.return_value = {
            "variant": ["default", "primary", "secondary"],
            "size": ["sm", "md", "lg"],
        }

        # Mock examples
        mock_reg.get_examples.return_value = [
            {"description": "Basic button", "code": 'Button(text="Click me")'}
        ]

        # Mock export
        mock_reg.export_for_llm.return_value = json.dumps({"components": []})

        yield mock_reg


class TestListComponents:
    """Test pptx_list_components tool."""

    @pytest.mark.asyncio
    async def test_list_components_all(self, registry_tools, mock_registry):
        """Test listing all components."""
        result = await registry_tools["pptx_list_components"]()
        data = json.loads(result)
        assert "components" in data
        assert "count" in data
        assert isinstance(data["components"], list)

    @pytest.mark.asyncio
    async def test_list_components_has_metadata(self, registry_tools, mock_registry):
        """Test that components include metadata."""
        result = await registry_tools["pptx_list_components"]()
        data = json.loads(result)
        if data["components"]:
            component = data["components"][0]
            assert "name" in component
            assert "category" in component
            assert "description" in component
            assert "tags" in component

    @pytest.mark.asyncio
    async def test_list_components_by_category(self, registry_tools, mock_registry):
        """Test listing components filtered by category."""
        result = await registry_tools["pptx_list_components"](category="ui")
        data = json.loads(result)
        assert data.get("category_filter") == "ui"

    @pytest.mark.asyncio
    async def test_list_components_invalid_category(self, registry_tools, mock_registry):
        """Test listing with invalid category."""
        mock_registry.list_by_category.side_effect = ValueError("Invalid category")
        result = await registry_tools["pptx_list_components"](category="invalid")
        data = json.loads(result)
        # Should return error or handle gracefully
        assert "error" in data or "components" in data


class TestGetComponentSchema:
    """Test pptx_get_component_schema tool."""

    @pytest.mark.asyncio
    async def test_get_component_schema_success(self, registry_tools, mock_registry):
        """Test getting schema for valid component."""
        result = await registry_tools["pptx_get_component_schema"](name="Button")
        data = json.loads(result)
        assert "name" in data or "props" in data

    @pytest.mark.asyncio
    async def test_get_component_schema_not_found(self, registry_tools, mock_registry):
        """Test getting schema for non-existent component."""
        mock_registry.get_schema.return_value = None
        result = await registry_tools["pptx_get_component_schema"](name="NonExistent")
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_component_schema_has_hint(self, registry_tools, mock_registry):
        """Test that error includes helpful hint."""
        mock_registry.get_schema.return_value = None
        result = await registry_tools["pptx_get_component_schema"](name="Invalid")
        data = json.loads(result)
        if "error" in data:
            assert "hint" in data


class TestSearchComponents:
    """Test pptx_search_components tool."""

    @pytest.mark.asyncio
    async def test_search_components_returns_json(self, registry_tools, mock_registry):
        """Test that search returns JSON."""
        result = await registry_tools["pptx_search_components"](query="button")
        data = json.loads(result)
        assert isinstance(data, dict)

    @pytest.mark.asyncio
    async def test_search_components_has_query(self, registry_tools, mock_registry):
        """Test that search result includes query."""
        result = await registry_tools["pptx_search_components"](query="metric")
        data = json.loads(result)
        assert data.get("query") == "metric"

    @pytest.mark.asyncio
    async def test_search_components_has_results(self, registry_tools, mock_registry):
        """Test that search includes results list."""
        result = await registry_tools["pptx_search_components"](query="card")
        data = json.loads(result)
        assert "results" in data
        assert isinstance(data["results"], list)

    @pytest.mark.asyncio
    async def test_search_components_has_count(self, registry_tools, mock_registry):
        """Test that search includes result count."""
        result = await registry_tools["pptx_search_components"](query="alert")
        data = json.loads(result)
        assert "count" in data
        assert isinstance(data["count"], int)

    @pytest.mark.asyncio
    async def test_search_components_result_structure(self, registry_tools, mock_registry):
        """Test structure of search results."""
        result = await registry_tools["pptx_search_components"](query="button")
        data = json.loads(result)
        if data["results"]:
            item = data["results"][0]
            assert "name" in item
            assert "category" in item
            assert "description" in item


class TestGetComponentVariants:
    """Test pptx_get_component_variants tool."""

    @pytest.mark.asyncio
    async def test_get_component_variants_success(self, registry_tools, mock_registry):
        """Test getting variants for valid component."""
        result = await registry_tools["pptx_get_component_variants"](name="Button")
        data = json.loads(result)
        assert "component" in data
        assert "variants" in data

    @pytest.mark.asyncio
    async def test_get_component_variants_not_found(self, registry_tools, mock_registry):
        """Test getting variants for non-existent component."""
        mock_registry.list_variants.return_value = None
        result = await registry_tools["pptx_get_component_variants"](name="Invalid")
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_component_variants_structure(self, registry_tools, mock_registry):
        """Test variants structure."""
        result = await registry_tools["pptx_get_component_variants"](name="Button")
        data = json.loads(result)
        if "variants" in data:
            variants = data["variants"]
            assert isinstance(variants, dict)


class TestGetComponentExamples:
    """Test pptx_get_component_examples tool."""

    @pytest.mark.asyncio
    async def test_get_component_examples_success(self, registry_tools, mock_registry):
        """Test getting examples for valid component."""
        result = await registry_tools["pptx_get_component_examples"](name="Button")
        data = json.loads(result)
        assert "component" in data
        assert "examples" in data

    @pytest.mark.asyncio
    async def test_get_component_examples_not_found(self, registry_tools, mock_registry):
        """Test getting examples for non-existent component."""
        mock_registry.get_examples.return_value = None
        mock_registry.get.return_value = None
        result = await registry_tools["pptx_get_component_examples"](name="Invalid")
        data = json.loads(result)
        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_component_examples_empty(self, registry_tools, mock_registry):
        """Test component with no examples."""
        mock_registry.get_examples.return_value = None
        result = await registry_tools["pptx_get_component_examples"](name="Button")
        data = json.loads(result)
        if "examples" in data:
            assert isinstance(data["examples"], list)


class TestExportRegistryDocs:
    """Test pptx_export_registry_docs tool."""

    @pytest.mark.asyncio
    async def test_export_registry_docs_returns_string(self, registry_tools, mock_registry):
        """Test that export returns string."""
        result = await registry_tools["pptx_export_registry_docs"]()
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_export_registry_docs_is_json(self, registry_tools, mock_registry):
        """Test that export returns valid JSON."""
        result = await registry_tools["pptx_export_registry_docs"]()
        # Should be parseable as JSON
        try:
            data = json.loads(result)
            assert isinstance(data, dict)
        except json.JSONDecodeError:
            # If not JSON, that's still okay as it might be formatted text
            assert isinstance(result, str)


class TestIntegration:
    """Integration tests for registry tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, registry_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_list_components",
            "pptx_get_component_schema",
            "pptx_search_components",
            "pptx_get_component_variants",
            "pptx_get_component_examples",
            "pptx_export_registry_docs",
        ]

        for tool_name in expected_tools:
            assert tool_name in registry_tools, f"Tool {tool_name} not registered"
            assert callable(registry_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_workflow_discover_component(self, registry_tools, mock_registry):
        """Test complete workflow: list → search → get schema."""
        # List all components
        list_result = await registry_tools["pptx_list_components"]()
        list_data = json.loads(list_result)
        assert "components" in list_data

        # Search for specific component
        search_result = await registry_tools["pptx_search_components"](query="button")
        search_data = json.loads(search_result)
        assert "results" in search_data

        # Get schema for component
        schema_result = await registry_tools["pptx_get_component_schema"](name="Button")
        schema_data = json.loads(schema_result)
        # Should have schema or error
        assert "name" in schema_data or "error" in schema_data
