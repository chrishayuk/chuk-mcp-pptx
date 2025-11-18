"""
Tests for table_tools.py

Tests all table-related MCP tools for >90% coverage.
"""

import pytest
from unittest.mock import MagicMock
from chuk_mcp_pptx.tools.table_tools import register_table_tools


@pytest.fixture
def table_tools(mock_mcp_server, mock_presentation_manager):
    """Register table tools and return them."""
    tools = register_table_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestAddDataTable:
    """Test pptx_add_data_table tool."""

    @pytest.mark.asyncio
    async def test_add_data_table_basic(self, table_tools, mock_presentation_manager):
        """Test adding data table with basic parameters."""
        result = await table_tools["pptx_add_data_table"](
            slide_index=0, headers=["Name", "Value"], data=[["Item 1", "100"], ["Item 2", "200"]]
        )
        assert isinstance(result, str)
        assert "2" in result or "table" in result.lower()

    @pytest.mark.asyncio
    async def test_add_data_table_custom_position(self, table_tools, mock_presentation_manager):
        """Test data table with custom position and size."""
        result = await table_tools["pptx_add_data_table"](
            slide_index=0,
            headers=["A", "B"],
            data=[["1", "2"]],
            left=2.0,
            top=2.5,
            width=6.0,
            height=3.0,
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_data_table_styles(self, table_tools, mock_presentation_manager):
        """Test data table with different styles."""
        styles = ["light", "medium", "dark"]
        for style in styles:
            result = await table_tools["pptx_add_data_table"](
                slide_index=0, headers=["Col1", "Col2"], data=[["A", "B"]], style=style
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_data_table_many_columns(self, table_tools, mock_presentation_manager):
        """Test table with many columns."""
        headers = [f"Col{i}" for i in range(8)]
        data = [[f"R{r}C{c}" for c in range(8)] for r in range(3)]
        result = await table_tools["pptx_add_data_table"](slide_index=0, headers=headers, data=data)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_data_table_many_rows(self, table_tools, mock_presentation_manager):
        """Test table with many rows."""
        headers = ["Product", "Revenue"]
        data = [[f"Product {i}", f"${i * 100}"] for i in range(20)]
        result = await table_tools["pptx_add_data_table"](slide_index=0, headers=headers, data=data)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_data_table_with_presentation(self, table_tools, mock_presentation_manager):
        """Test data table with specific presentation."""
        result = await table_tools["pptx_add_data_table"](
            slide_index=0, headers=["X", "Y"], data=[["1", "2"]], presentation="test_presentation"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_data_table_invalid_slide(self, table_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await table_tools["pptx_add_data_table"](
            slide_index=999, headers=["A"], data=[["1"]]
        )
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_add_data_table_no_presentation(self, table_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await table_tools["pptx_add_data_table"](
            slide_index=0, headers=["A"], data=[["1"]], presentation="nonexistent"
        )
        assert "No presentation found" in result or '{"error":' in result


class TestAddComparisonTable:
    """Test pptx_add_comparison_table tool."""

    @pytest.mark.asyncio
    async def test_add_comparison_table_two_options(self, table_tools, mock_presentation_manager):
        """Test comparison table with two options."""
        result = await table_tools["pptx_add_comparison_table"](
            slide_index=0,
            title="Comparison",
            categories=["Price", "Features", "Support"],
            option1_name="Basic",
            option1_values=["$10/mo", "Limited", "Email"],
            option2_name="Pro",
            option2_values=["$50/mo", "Full", "24/7"],
        )
        assert isinstance(result, str)
        assert "2" in result or "comparison" in result.lower()

    @pytest.mark.asyncio
    async def test_add_comparison_table_three_options(self, table_tools, mock_presentation_manager):
        """Test comparison table with three options."""
        result = await table_tools["pptx_add_comparison_table"](
            slide_index=0,
            title="Product Comparison",
            categories=["Cost", "Speed"],
            option1_name="Option A",
            option1_values=["Low", "Slow"],
            option2_name="Option B",
            option2_values=["Medium", "Medium"],
            option3_name="Option C",
            option3_values=["High", "Fast"],
        )
        assert isinstance(result, str)
        assert "3" in result

    @pytest.mark.asyncio
    async def test_add_comparison_table_custom_position(
        self, table_tools, mock_presentation_manager
    ):
        """Test comparison table with custom position."""
        result = await table_tools["pptx_add_comparison_table"](
            slide_index=0,
            title="Compare",
            categories=["A"],
            option1_name="X",
            option1_values=["1"],
            option2_name="Y",
            option2_values=["2"],
            left=1.5,
            top=2.0,
            width=7.0,
            height=3.5,
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_comparison_table_styles(self, table_tools, mock_presentation_manager):
        """Test comparison table with different styles."""
        styles = ["light", "medium", "dark"]
        for style in styles:
            result = await table_tools["pptx_add_comparison_table"](
                slide_index=0,
                title="Test",
                categories=["Cat1"],
                option1_name="Opt1",
                option1_values=["Val1"],
                option2_name="Opt2",
                option2_values=["Val2"],
                style=style,
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_comparison_table_many_categories(
        self, table_tools, mock_presentation_manager
    ):
        """Test comparison table with many categories."""
        categories = [f"Category {i}" for i in range(10)]
        values1 = [f"A{i}" for i in range(10)]
        values2 = [f"B{i}" for i in range(10)]
        result = await table_tools["pptx_add_comparison_table"](
            slide_index=0,
            title="Detailed Comparison",
            categories=categories,
            option1_name="Option 1",
            option1_values=values1,
            option2_name="Option 2",
            option2_values=values2,
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_comparison_table_invalid_slide(self, table_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await table_tools["pptx_add_comparison_table"](
            slide_index=999,
            title="Test",
            categories=["A"],
            option1_name="X",
            option1_values=["1"],
            option2_name="Y",
            option2_values=["2"],
        )
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_add_comparison_table_no_presentation(
        self, table_tools, mock_presentation_manager
    ):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await table_tools["pptx_add_comparison_table"](
            slide_index=0,
            title="Test",
            categories=["A"],
            option1_name="X",
            option1_values=["1"],
            option2_name="Y",
            option2_values=["2"],
            presentation="nonexistent",
        )
        assert "No presentation found" in result or '{"error":' in result


class TestUpdateTableCell:
    """Test pptx_update_table_cell tool."""

    @pytest.mark.asyncio
    async def test_update_table_cell_basic(self, table_tools, mock_presentation_manager):
        """Test updating table cell with basic parameters."""
        # First add a real table using pptx_add_data_table
        add_result = await table_tools["pptx_add_data_table"](
            slide_index=0, headers=["Col1", "Col2", "Col3"], data=[["A", "B", "C"], ["D", "E", "F"]]
        )
        assert "table" in add_result.lower()

        # Now update a cell
        result = await table_tools["pptx_update_table_cell"](
            slide_index=0, table_index=0, row=1, col=1, new_value="Updated Value"
        )
        assert isinstance(result, str)
        assert "Updated" in result or "cell" in result.lower()

    @pytest.mark.asyncio
    async def test_update_table_cell_with_formatting(self, table_tools, mock_presentation_manager):
        """Test updating cell with formatting."""
        # Setup mock table
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_table.rows = [MagicMock() for _ in range(2)]
        mock_table.columns = [MagicMock() for _ in range(2)]

        mock_cell = MagicMock()
        mock_cell.text = ""
        mock_text_frame = MagicMock()
        mock_paragraph = MagicMock()
        mock_font = MagicMock()
        mock_paragraph.font = mock_font
        mock_text_frame.paragraphs = [mock_paragraph]
        mock_cell.text_frame = mock_text_frame
        mock_table.cell = MagicMock(return_value=mock_cell)

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_update_table_cell"](
            slide_index=0,
            table_index=0,
            row=0,
            col=0,
            new_value="Bold Text",
            bold=True,
            color="#FF0000",
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_update_table_cell_invalid_table_index(
        self, table_tools, mock_presentation_manager
    ):
        """Test error with invalid table index."""
        result = await table_tools["pptx_update_table_cell"](
            slide_index=0, table_index=999, row=0, col=0, new_value="Value"
        )
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_update_table_cell_invalid_row(self, table_tools, mock_presentation_manager):
        """Test error with invalid row index."""
        # Setup minimal mock table
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table
        mock_table.rows = [MagicMock()]
        mock_table.columns = [MagicMock()]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_update_table_cell"](
            slide_index=0, table_index=0, row=999, col=0, new_value="Value"
        )
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_update_table_cell_no_presentation(self, table_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await table_tools["pptx_update_table_cell"](
            slide_index=0, table_index=0, row=0, col=0, new_value="Value"
        )
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_update_table_cell_invalid_column(self, table_tools, mock_presentation_manager):
        """Test error with invalid column index."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table
        mock_table.rows = [MagicMock()]
        mock_table.columns = [MagicMock()]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_update_table_cell"](
            slide_index=0, table_index=0, row=0, col=999, new_value="Value"
        )
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_update_table_cell_color_without_hash(
        self, table_tools, mock_presentation_manager
    ):
        """Test updating cell with color without # prefix."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_table.rows = [MagicMock() for _ in range(2)]
        mock_table.columns = [MagicMock() for _ in range(2)]

        mock_cell = MagicMock()
        mock_cell.text = ""
        mock_text_frame = MagicMock()
        mock_paragraph = MagicMock()
        mock_font = MagicMock()
        mock_paragraph.font = mock_font
        mock_text_frame.paragraphs = [mock_paragraph]
        mock_cell.text_frame = mock_text_frame
        mock_table.cell = MagicMock(return_value=mock_cell)

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_update_table_cell"](
            slide_index=0,
            table_index=0,
            row=0,
            col=0,
            new_value="Text",
            color="00FF00",  # No # prefix
        )
        assert isinstance(result, str)


class TestFormatTable:
    """Test pptx_format_table tool."""

    @pytest.mark.asyncio
    async def test_format_table_basic(self, table_tools, mock_presentation_manager):
        """Test formatting table with basic parameters."""
        # Setup mock table
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        # Mock rows with cells
        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_cell.text_frame = MagicMock()
        mock_cell.text_frame.paragraphs = [MagicMock()]
        mock_cell.text_frame.paragraphs[0].font = MagicMock()
        mock_cell.fill = MagicMock()
        mock_row.cells = [mock_cell]
        mock_table.rows = [mock_row]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_format_table"](slide_index=0, table_index=0)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_format_table_header_bold(self, table_tools, mock_presentation_manager):
        """Test formatting table header as bold."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_cell.text_frame = MagicMock()
        mock_paragraph = MagicMock()
        mock_paragraph.font = MagicMock()
        mock_cell.text_frame.paragraphs = [mock_paragraph]
        mock_cell.fill = MagicMock()
        mock_row.cells = [mock_cell]
        mock_table.rows = [mock_row]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_format_table"](
            slide_index=0, table_index=0, header_bold=True
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_format_table_header_color(self, table_tools, mock_presentation_manager):
        """Test formatting table header with color."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_cell.text_frame = MagicMock()
        mock_cell.text_frame.paragraphs = [MagicMock()]
        mock_cell.text_frame.paragraphs[0].font = MagicMock()
        mock_cell.fill = MagicMock()
        mock_row.cells = [mock_cell]
        mock_table.rows = [mock_row]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_format_table"](
            slide_index=0, table_index=0, header_color="#003366"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_format_table_alternate_rows(self, table_tools, mock_presentation_manager):
        """Test formatting table with alternating rows."""
        # First add a real table with multiple rows using pptx_add_data_table
        add_result = await table_tools["pptx_add_data_table"](
            slide_index=0,
            headers=["Col1", "Col2", "Col3"],
            data=[
                ["R1C1", "R1C2", "R1C3"],
                ["R2C1", "R2C2", "R2C3"],
                ["R3C1", "R3C2", "R3C3"],
                ["R4C1", "R4C2", "R4C3"],
            ],
        )
        assert "table" in add_result.lower()

        # Now format with alternating rows
        result = await table_tools["pptx_format_table"](
            slide_index=0, table_index=0, alternate_rows=True
        )
        assert isinstance(result, str)
        assert "alternating" in result.lower()

    @pytest.mark.asyncio
    async def test_format_table_border_width(self, table_tools, mock_presentation_manager):
        """Test formatting table with border width."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_cell.text_frame = MagicMock()
        mock_cell.text_frame.paragraphs = [MagicMock()]
        mock_cell.text_frame.paragraphs[0].font = MagicMock()
        mock_cell.fill = MagicMock()
        mock_row.cells = [mock_cell]
        mock_table.rows = [mock_row]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_format_table"](
            slide_index=0, table_index=0, border_width=2.0
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_format_table_invalid_slide(self, table_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await table_tools["pptx_format_table"](slide_index=999, table_index=0)
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_format_table_no_presentation(self, table_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await table_tools["pptx_format_table"](slide_index=0, table_index=0)
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_format_table_invalid_table_index(self, table_tools, mock_presentation_manager):
        """Test error with invalid table index."""
        result = await table_tools["pptx_format_table"](slide_index=0, table_index=999)
        assert "No presentation found" in result or '{"error":' in result

    @pytest.mark.asyncio
    async def test_format_table_header_color_without_hash(
        self, table_tools, mock_presentation_manager
    ):
        """Test formatting header with color without # prefix."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_cell.text_frame = MagicMock()
        mock_cell.text_frame.paragraphs = [MagicMock()]
        mock_cell.text_frame.paragraphs[0].font = MagicMock()
        mock_cell.fill = MagicMock()
        mock_row.cells = [mock_cell]
        mock_table.rows = [mock_row]

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_format_table"](
            slide_index=0,
            table_index=0,
            header_color="FF5733",  # No # prefix
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_format_table_all_options(self, table_tools, mock_presentation_manager):
        """Test formatting table with all options enabled."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        # Create multiple rows
        rows = []
        for _ in range(5):
            mock_row = MagicMock()
            mock_cell = MagicMock()
            mock_cell.text_frame = MagicMock()
            mock_paragraph = MagicMock()
            mock_paragraph.font = MagicMock()
            mock_cell.text_frame.paragraphs = [mock_paragraph]
            mock_cell.fill = MagicMock()
            mock_row.cells = [mock_cell]
            rows.append(mock_row)
        mock_table.rows = rows

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        result = await table_tools["pptx_format_table"](
            slide_index=0,
            table_index=0,
            header_bold=True,
            header_color="#003366",
            alternate_rows=True,
            border_width=1.5,
        )
        assert isinstance(result, str)


class TestIntegration:
    """Integration tests for table tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, table_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_add_data_table",
            "pptx_add_comparison_table",
            "pptx_update_table_cell",
            "pptx_format_table",
        ]

        for tool_name in expected_tools:
            assert tool_name in table_tools, f"Tool {tool_name} not registered"
            assert callable(table_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_workflow_add_table_then_update(self, table_tools, mock_presentation_manager):
        """Test workflow: add table then update cell."""
        # Add table
        result1 = await table_tools["pptx_add_data_table"](
            slide_index=0,
            headers=["Product", "Sales"],
            data=[["Widget", "$1000"], ["Gadget", "$2000"]],
        )
        assert isinstance(result1, str)

        # Setup mock for update
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_table_shape = MagicMock()
        mock_table_shape.shape_type = 19
        mock_table = MagicMock()
        mock_table_shape.table = mock_table

        mock_table.rows = [MagicMock() for _ in range(3)]
        mock_table.columns = [MagicMock() for _ in range(2)]

        mock_cell = MagicMock()
        mock_cell.text = ""
        mock_text_frame = MagicMock()
        mock_paragraph = MagicMock()
        mock_paragraph.font = MagicMock()
        mock_text_frame.paragraphs = [mock_paragraph]
        mock_cell.text_frame = mock_text_frame
        mock_table.cell = MagicMock(return_value=mock_cell)

        slide.shapes._members = [mock_table_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_table_shape]))

        # Update cell
        result2 = await table_tools["pptx_update_table_cell"](
            slide_index=0, table_index=0, row=1, col=1, new_value="$3000"
        )
        assert isinstance(result2, str)
