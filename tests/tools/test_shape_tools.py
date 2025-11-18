"""
Tests for shape_tools.py

Tests all shape and SmartArt-related MCP tools for >90% coverage.
"""

import pytest
from chuk_mcp_pptx.tools.shape_tools import register_shape_tools


@pytest.fixture
def shape_tools(mock_mcp_server, mock_presentation_manager):
    """Register shape tools and return them."""
    tools = register_shape_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestAddArrow:
    """Test pptx_add_arrow tool."""

    @pytest.mark.asyncio
    async def test_add_arrow_basic(self, shape_tools, mock_presentation_manager):
        """Test adding arrow with basic parameters."""
        result = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=2.0, start_y=2.0, end_x=5.0, end_y=3.0
        )
        assert isinstance(result, str)
        assert "arrow" in result.lower()

    @pytest.mark.asyncio
    async def test_add_arrow_connector_types(self, shape_tools, mock_presentation_manager):
        """Test all connector types."""
        connector_types = ["straight", "elbow", "curved"]
        for connector_type in connector_types:
            result = await shape_tools["pptx_add_arrow"](
                slide_index=0,
                start_x=1.0,
                start_y=1.0,
                end_x=4.0,
                end_y=2.0,
                connector_type=connector_type,
            )
            assert connector_type in result.lower()

    @pytest.mark.asyncio
    async def test_add_arrow_with_color(self, shape_tools, mock_presentation_manager):
        """Test arrow with custom color."""
        result = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=1.0, start_y=1.0, end_x=3.0, end_y=2.0, line_color="#FF0000"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_arrow_with_line_width(self, shape_tools, mock_presentation_manager):
        """Test arrow with custom line width."""
        result = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=1.0, start_y=1.0, end_x=3.0, end_y=2.0, line_width=3.0
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_arrow_with_arrowheads(self, shape_tools, mock_presentation_manager):
        """Test arrow with different arrowhead configurations."""
        # Test arrow at end only
        result1 = await shape_tools["pptx_add_arrow"](
            slide_index=0,
            start_x=1.0,
            start_y=1.0,
            end_x=3.0,
            end_y=2.0,
            arrow_start=False,
            arrow_end=True,
        )
        assert isinstance(result1, str)

        # Test arrow at both ends
        result2 = await shape_tools["pptx_add_arrow"](
            slide_index=0,
            start_x=1.0,
            start_y=2.0,
            end_x=3.0,
            end_y=3.0,
            arrow_start=True,
            arrow_end=True,
        )
        assert isinstance(result2, str)

        # Test arrow at start only
        result3 = await shape_tools["pptx_add_arrow"](
            slide_index=0,
            start_x=1.0,
            start_y=3.0,
            end_x=3.0,
            end_y=4.0,
            arrow_start=True,
            arrow_end=False,
        )
        assert isinstance(result3, str)

    @pytest.mark.asyncio
    async def test_add_arrow_with_presentation(self, shape_tools, mock_presentation_manager):
        """Test arrow with specific presentation."""
        result = await shape_tools["pptx_add_arrow"](
            slide_index=0,
            start_x=1.0,
            start_y=1.0,
            end_x=3.0,
            end_y=2.0,
            presentation="test_presentation",
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_arrow_invalid_slide(self, shape_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await shape_tools["pptx_add_arrow"](
            slide_index=999, start_x=1.0, start_y=1.0, end_x=3.0, end_y=2.0
        )
        assert "Error" in result or "out of range" in result

    @pytest.mark.asyncio
    async def test_add_arrow_no_presentation(self, shape_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await shape_tools["pptx_add_arrow"](
            slide_index=0,
            start_x=1.0,
            start_y=1.0,
            end_x=3.0,
            end_y=2.0,
            presentation="nonexistent",
        )
        assert "No presentation found" in result or "Error" in result


class TestAddSmartArt:
    """Test pptx_add_smart_art tool."""

    @pytest.mark.asyncio
    async def test_add_smart_art_process(self, shape_tools, mock_presentation_manager):
        """Test adding process SmartArt."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="process", items=["Step 1", "Step 2", "Step 3"]
        )
        assert isinstance(result, str)
        assert "process" in result.lower() or "3" in result

    @pytest.mark.asyncio
    async def test_add_smart_art_cycle(self, shape_tools, mock_presentation_manager):
        """Test adding cycle SmartArt."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="cycle", items=["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        )
        assert isinstance(result, str)
        assert "cycle" in result.lower() or "4" in result

    @pytest.mark.asyncio
    async def test_add_smart_art_hierarchy(self, shape_tools, mock_presentation_manager):
        """Test adding hierarchy SmartArt."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="hierarchy", items=["CEO", "VP Sales", "VP Eng", "VP Ops"]
        )
        assert isinstance(result, str)
        assert "hierarchy" in result.lower() or "4" in result

    @pytest.mark.asyncio
    async def test_add_smart_art_with_title(self, shape_tools, mock_presentation_manager):
        """Test SmartArt with title."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="process", items=["A", "B", "C"], title="Process Title"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_smart_art_custom_position(self, shape_tools, mock_presentation_manager):
        """Test SmartArt with custom position and size."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0,
            art_type="process",
            items=["X", "Y", "Z"],
            left=2.0,
            top=2.5,
            width=6.0,
            height=4.0,
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_smart_art_color_schemes(self, shape_tools, mock_presentation_manager):
        """Test SmartArt with different color schemes."""
        color_schemes = ["modern_blue", "corporate_gray", "warm_orange"]
        for color_scheme in color_schemes:
            result = await shape_tools["pptx_add_smart_art"](
                slide_index=0, art_type="process", items=["A", "B"], color_scheme=color_scheme
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_smart_art_unsupported_type(self, shape_tools, mock_presentation_manager):
        """Test error with unsupported art type."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="unsupported_type", items=["A", "B"]
        )
        assert "Error" in result or "Unsupported" in result

    @pytest.mark.asyncio
    async def test_add_smart_art_many_items(self, shape_tools, mock_presentation_manager):
        """Test SmartArt with many items."""
        items = [f"Item {i}" for i in range(10)]
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="process", items=items
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_smart_art_invalid_slide(self, shape_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=999, art_type="process", items=["A", "B"]
        )
        assert "Error" in result or "out of range" in result

    @pytest.mark.asyncio
    async def test_add_smart_art_no_presentation(self, shape_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await shape_tools["pptx_add_smart_art"](
            slide_index=0, art_type="process", items=["A", "B"], presentation="nonexistent"
        )
        assert "No presentation found" in result or "Error" in result


class TestAddCodeBlock:
    """Test pptx_add_code_block tool."""

    @pytest.mark.asyncio
    async def test_add_code_block_basic(self, shape_tools, mock_presentation_manager):
        """Test adding code block with basic parameters."""
        result = await shape_tools["pptx_add_code_block"](
            slide_index=0, code="print('Hello, World!')"
        )
        assert isinstance(result, str)
        assert "code" in result.lower()

    @pytest.mark.asyncio
    async def test_add_code_block_languages(self, shape_tools, mock_presentation_manager):
        """Test code block with different languages."""
        languages = ["python", "javascript", "java", "go", "rust"]
        for language in languages:
            result = await shape_tools["pptx_add_code_block"](
                slide_index=0, code=f"// {language} code", language=language
            )
            assert language in result.lower()

    @pytest.mark.asyncio
    async def test_add_code_block_multiline(self, shape_tools, mock_presentation_manager):
        """Test code block with multiline code."""
        code = """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))"""
        result = await shape_tools["pptx_add_code_block"](
            slide_index=0, code=code, language="python"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_code_block_custom_position(self, shape_tools, mock_presentation_manager):
        """Test code block with custom position and size."""
        result = await shape_tools["pptx_add_code_block"](
            slide_index=0,
            code="const x = 42;",
            language="javascript",
            left=1.5,
            top=2.0,
            width=7.0,
            height=4.0,
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_code_block_themes(self, shape_tools, mock_presentation_manager):
        """Test code block with different themes."""
        themes = ["dark_modern", "dark_purple", "light"]
        for theme in themes:
            result = await shape_tools["pptx_add_code_block"](
                slide_index=0, code="x = 1", theme=theme
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_code_block_with_presentation(self, shape_tools, mock_presentation_manager):
        """Test code block with specific presentation."""
        result = await shape_tools["pptx_add_code_block"](
            slide_index=0, code="console.log('test');", presentation="test_presentation"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_code_block_invalid_slide(self, shape_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await shape_tools["pptx_add_code_block"](slide_index=999, code="code")
        assert "Error" in result or "out of range" in result

    @pytest.mark.asyncio
    async def test_add_code_block_no_presentation(self, shape_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await shape_tools["pptx_add_code_block"](
            slide_index=0, code="code", presentation="nonexistent"
        )
        assert "No presentation found" in result or "Error" in result


class TestIntegration:
    """Integration tests for shape tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, shape_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_add_arrow",
            "pptx_add_smart_art",
            "pptx_add_code_block",
        ]

        for tool_name in expected_tools:
            assert tool_name in shape_tools, f"Tool {tool_name} not registered"
            assert callable(shape_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_multiple_arrows_same_slide(self, shape_tools, mock_presentation_manager):
        """Test adding multiple arrows to same slide."""
        # Horizontal arrow
        result1 = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=1.0, start_y=2.0, end_x=4.0, end_y=2.0
        )
        assert isinstance(result1, str)

        # Vertical arrow
        result2 = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=5.0, start_y=1.0, end_x=5.0, end_y=4.0
        )
        assert isinstance(result2, str)

        # Diagonal arrow
        result3 = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=6.0, start_y=1.0, end_x=8.0, end_y=3.0
        )
        assert isinstance(result3, str)

    @pytest.mark.asyncio
    async def test_smartart_with_arrows(self, shape_tools, mock_presentation_manager):
        """Test combining SmartArt with arrows."""
        # Add SmartArt
        result1 = await shape_tools["pptx_add_smart_art"](
            slide_index=0,
            art_type="process",
            items=["Start", "Process", "End"],
            top=1.0,
            height=2.0,
        )
        assert isinstance(result1, str)

        # Add connecting arrow
        result2 = await shape_tools["pptx_add_arrow"](
            slide_index=0, start_x=1.0, start_y=4.0, end_x=5.0, end_y=4.0
        )
        assert isinstance(result2, str)

    @pytest.mark.asyncio
    async def test_code_block_with_diagram(self, shape_tools, mock_presentation_manager):
        """Test code block with SmartArt diagram."""
        # Add code block
        result1 = await shape_tools["pptx_add_code_block"](
            slide_index=0, code="def process():\n    pass", language="python", top=1.0, height=2.0
        )
        assert isinstance(result1, str)

        # Add diagram below
        result2 = await shape_tools["pptx_add_smart_art"](
            slide_index=0,
            art_type="process",
            items=["Input", "Process", "Output"],
            top=4.0,
            height=2.0,
        )
        assert isinstance(result2, str)
