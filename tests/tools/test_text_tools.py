"""
Tests for text_tools.py

Tests all text-related MCP tools for >90% coverage.
"""

import pytest
from chuk_mcp_pptx.tools.text_tools import register_text_tools


@pytest.fixture
def text_tools(mock_mcp_server, mock_presentation_manager):
    """Register text tools and return them."""
    tools = register_text_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestAddTextSlide:
    """Test pptx_add_text_slide tool."""

    @pytest.mark.asyncio
    async def test_add_text_slide_basic(self, text_tools, mock_presentation_manager):
        """Test adding text slide with basic parameters."""
        result = await text_tools["pptx_add_text_slide"](
            title="Test Title", text="Test paragraph text"
        )
        assert isinstance(result, str)
        assert "Test Title" in result or "Added text slide" in result

    @pytest.mark.asyncio
    async def test_add_text_slide_with_presentation(self, text_tools, mock_presentation_manager):
        """Test adding text slide with specific presentation."""
        result = await text_tools["pptx_add_text_slide"](
            title="Slide Title", text="Slide content", presentation="test_presentation"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_slide_long_text(self, text_tools, mock_presentation_manager):
        """Test adding text slide with long text content."""
        long_text = "This is a very long paragraph. " * 20
        result = await text_tools["pptx_add_text_slide"](title="Long Content", text=long_text)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_slide_no_presentation(self, text_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await text_tools["pptx_add_text_slide"](
            title="Title", text="Text", presentation="nonexistent"
        )
        assert "No presentation found" in result


class TestExtractAllText:
    """Test pptx_extract_all_text tool."""

    @pytest.mark.asyncio
    async def test_extract_text_basic(self, text_tools, mock_presentation_manager):
        """Test extracting text from presentation."""
        result = await text_tools["pptx_extract_all_text"]()
        assert isinstance(result, (str, dict))

    @pytest.mark.asyncio
    async def test_extract_text_with_presentation(self, text_tools, mock_presentation_manager):
        """Test extracting text from specific presentation."""
        result = await text_tools["pptx_extract_all_text"](presentation="test_presentation")
        assert isinstance(result, (str, dict))

    @pytest.mark.asyncio
    async def test_extract_text_no_presentation(self, text_tools, mock_presentation_manager):
        """Test error when extracting from non-existent presentation."""
        # Use a non-existent presentation name instead of mocking
        result = await text_tools["pptx_extract_all_text"](presentation="nonexistent")
        # Should return string with JSON error
        assert isinstance(result, str)
        assert '"error":' in result


class TestAddTextBox:
    """Test pptx_add_text_box tool."""

    @pytest.mark.asyncio
    async def test_add_text_box_basic(self, text_tools, mock_presentation_manager):
        """Test adding text box with basic parameters."""
        result = await text_tools["pptx_add_text_box"](slide_index=0, text="Test text box")
        assert isinstance(result, str)
        assert "text box" in result.lower() or "slide 0" in result

    @pytest.mark.asyncio
    async def test_add_text_box_with_position(self, text_tools, mock_presentation_manager):
        """Test text box with custom position."""
        result = await text_tools["pptx_add_text_box"](
            slide_index=0, text="Positioned text", left=2.0, top=3.0, width=5.0, height=2.0
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_with_formatting(self, text_tools, mock_presentation_manager):
        """Test text box with formatting options."""
        result = await text_tools["pptx_add_text_box"](
            slide_index=0, text="Formatted text", font_size=24, bold=True, alignment="center"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_with_color(self, text_tools, mock_presentation_manager):
        """Test text box with color."""
        result = await text_tools["pptx_add_text_box"](
            slide_index=0, text="Colored text", color="#FF0000"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_with_semantic_color(self, text_tools, mock_presentation_manager):
        """Test text box with semantic color."""
        result = await text_tools["pptx_add_text_box"](
            slide_index=0, text="Semantic colored text", color="primary.DEFAULT"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_all_alignments(self, text_tools, mock_presentation_manager):
        """Test text box with all alignment options."""
        alignments = ["left", "center", "right", "justify"]
        for alignment in alignments:
            result = await text_tools["pptx_add_text_box"](
                slide_index=0, text="Aligned text", alignment=alignment
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_various_font_sizes(self, text_tools, mock_presentation_manager):
        """Test text box with various font sizes."""
        font_sizes = [10, 14, 18, 24, 32, 48]
        for size in font_sizes:
            result = await text_tools["pptx_add_text_box"](
                slide_index=0, text="Text", font_size=size
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_bold_variations(self, text_tools, mock_presentation_manager):
        """Test text box with bold on and off."""
        for bold in [True, False]:
            result = await text_tools["pptx_add_text_box"](slide_index=0, text="Text", bold=bold)
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_text_box_invalid_slide(self, text_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await text_tools["pptx_add_text_box"](slide_index=999, text="Text")
        # Error is returned as JSON
        assert '{"error":' in result
        assert "not found" in result

    @pytest.mark.asyncio
    async def test_add_text_box_no_presentation(self, text_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await text_tools["pptx_add_text_box"](
            slide_index=0, text="Text", presentation="nonexistent"
        )
        assert "No presentation found" in result

    @pytest.mark.asyncio
    async def test_add_text_box_with_presentation_name(self, text_tools, mock_presentation_manager):
        """Test text box with specific presentation name."""
        result = await text_tools["pptx_add_text_box"](
            slide_index=0, text="Text", presentation="test_presentation"
        )
        assert isinstance(result, str)


class TestIntegration:
    """Integration tests for text tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, text_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_add_text_slide",
            "pptx_extract_all_text",
            "pptx_add_text_box",
        ]

        for tool_name in expected_tools:
            assert tool_name in text_tools, f"Tool {tool_name} not registered"
            assert callable(text_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_workflow_add_slide_then_text_box(self, text_tools, mock_presentation_manager):
        """Test workflow: add text slide then add text box."""
        # Add text slide
        result1 = await text_tools["pptx_add_text_slide"](
            title="Test Slide", text="Initial content"
        )
        assert isinstance(result1, str)

        # Add text box to slide 0
        result2 = await text_tools["pptx_add_text_box"](slide_index=0, text="Additional text box")
        assert isinstance(result2, str)

    @pytest.mark.asyncio
    async def test_multiple_text_boxes_same_slide(self, text_tools, mock_presentation_manager):
        """Test adding multiple text boxes to same slide."""
        positions = [(1.0, 1.0), (4.0, 1.0), (1.0, 4.0), (4.0, 4.0)]

        for i, (left, top) in enumerate(positions):
            result = await text_tools["pptx_add_text_box"](
                slide_index=0, text=f"Text box {i + 1}", left=left, top=top
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_text_tools_with_extract(self, text_tools, mock_presentation_manager):
        """Test adding text and then extracting it."""
        # Add text slide
        await text_tools["pptx_add_text_slide"](title="Extract Test", text="Content to extract")

        # Extract text
        result = await text_tools["pptx_extract_all_text"]()
        assert isinstance(result, (str, dict))
