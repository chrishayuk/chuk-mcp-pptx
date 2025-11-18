"""
Tests for component_tools.py

Tests all component-based MCP tools for >90% coverage.
"""

import pytest
from chuk_mcp_pptx.tools.component_tools import register_component_tools


@pytest.fixture
def component_tools(mock_mcp_server, mock_presentation_manager):
    """Register component tools and return them."""
    tools = register_component_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestAlertComponent:
    """Test pptx_add_alert tool."""

    @pytest.mark.asyncio
    async def test_add_alert_minimal(self, component_tools, mock_presentation_manager):
        """Test adding alert with minimal parameters."""
        result = await component_tools["pptx_add_alert"](
            slide_index=0, message="Test alert message", left=2.0, top=2.0
        )
        assert isinstance(result, str)
        assert "alert" in result.lower()

    @pytest.mark.asyncio
    async def test_add_alert_all_variants(self, component_tools, mock_presentation_manager):
        """Test all alert variants."""
        variants = ["info", "warning", "error", "success"]
        for variant in variants:
            result = await component_tools["pptx_add_alert"](
                slide_index=0, message=f"{variant} message", left=1.0, top=1.0, variant=variant
            )
            assert variant in result.lower()

    @pytest.mark.asyncio
    async def test_add_alert_with_title(self, component_tools, mock_presentation_manager):
        """Test alert with title."""
        result = await component_tools["pptx_add_alert"](
            slide_index=0, message="Message", left=1.0, top=1.0, title="Alert Title"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_alert_custom_size(self, component_tools, mock_presentation_manager):
        """Test alert with custom width and height."""
        result = await component_tools["pptx_add_alert"](
            slide_index=0, message="Message", left=1.0, top=1.0, width=5.0, height=1.5
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_alert_with_theme(self, component_tools, mock_presentation_manager):
        """Test alert with theme."""
        result = await component_tools["pptx_add_alert"](
            slide_index=0, message="Message", left=1.0, top=1.0, theme="dark"
        )
        assert isinstance(result, str)


class TestAvatarComponent:
    """Test avatar-related tools."""

    @pytest.mark.asyncio
    async def test_add_avatar(self, component_tools, mock_presentation_manager):
        """Test adding single avatar."""
        result = await component_tools["pptx_add_avatar"](
            slide_index=0, initials="JD", left=1.0, top=1.0
        )
        assert "avatar" in result.lower()

    @pytest.mark.asyncio
    async def test_add_avatar_variants(self, component_tools, mock_presentation_manager):
        """Test avatar shape variants."""
        variants = ["circle", "square", "rounded"]
        for variant in variants:
            result = await component_tools["pptx_add_avatar"](
                slide_index=0, initials="AB", left=1.0, top=1.0, variant=variant
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_avatar_custom_size(self, component_tools, mock_presentation_manager):
        """Test avatar with custom size."""
        result = await component_tools["pptx_add_avatar"](
            slide_index=0, initials="XY", left=1.0, top=1.0, size=1.0
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_avatar_group(self, component_tools, mock_presentation_manager):
        """Test adding avatar group."""
        result = await component_tools["pptx_add_avatar_group"](
            slide_index=0, initials_list=["JD", "SM", "RJ"], left=2.0, top=1.0
        )
        assert "3" in result or "avatar" in result.lower()

    @pytest.mark.asyncio
    async def test_add_avatar_group_max_visible(self, component_tools, mock_presentation_manager):
        """Test avatar group with max_visible."""
        result = await component_tools["pptx_add_avatar_group"](
            slide_index=0, initials_list=["A", "B", "C", "D", "E"], left=2.0, top=1.0, max_visible=3
        )
        assert isinstance(result, str)


class TestBadgeComponent:
    """Test pptx_add_badge tool."""

    @pytest.mark.asyncio
    async def test_add_badge(self, component_tools, mock_presentation_manager):
        """Test adding badge."""
        result = await component_tools["pptx_add_badge"](
            slide_index=0, text="New", left=1.0, top=1.0
        )
        assert "badge" in result.lower()

    @pytest.mark.asyncio
    async def test_add_badge_variants(self, component_tools, mock_presentation_manager):
        """Test all badge variants."""
        variants = ["default", "primary", "secondary", "success", "warning", "error"]
        for variant in variants:
            result = await component_tools["pptx_add_badge"](
                slide_index=0, text="Badge", left=1.0, top=1.0, variant=variant
            )
            assert variant in result.lower()


class TestButtonComponent:
    """Test pptx_add_button tool."""

    @pytest.mark.asyncio
    async def test_add_button(self, component_tools, mock_presentation_manager):
        """Test adding button."""
        result = await component_tools["pptx_add_button"](
            slide_index=0, text="Click Me", left=2.0, top=2.0
        )
        assert "button" in result.lower()

    @pytest.mark.asyncio
    async def test_add_button_variants(self, component_tools, mock_presentation_manager):
        """Test button variants."""
        variants = ["default", "secondary", "outline", "ghost", "destructive"]
        for variant in variants:
            result = await component_tools["pptx_add_button"](
                slide_index=0, text="Button", left=1.0, top=1.0, variant=variant
            )
            assert variant in result.lower()

    @pytest.mark.asyncio
    async def test_add_button_sizes(self, component_tools, mock_presentation_manager):
        """Test button sizes."""
        sizes = ["sm", "md", "lg"]
        for size in sizes:
            result = await component_tools["pptx_add_button"](
                slide_index=0, text="Button", left=1.0, top=1.0, size=size
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_button_custom_dimensions(self, component_tools, mock_presentation_manager):
        """Test button with custom width and height."""
        result = await component_tools["pptx_add_button"](
            slide_index=0, text="Custom Button", left=1.0, top=1.0, width=3.0, height=0.8
        )
        assert isinstance(result, str)


class TestCardComponent:
    """Test card-related tools."""

    @pytest.mark.asyncio
    async def test_add_card(self, component_tools, mock_presentation_manager):
        """Test adding card."""
        result = await component_tools["pptx_add_card"](slide_index=0, left=2.0, top=2.0)
        assert "card" in result.lower()

    @pytest.mark.asyncio
    async def test_add_card_with_content(self, component_tools, mock_presentation_manager):
        """Test card with title and description."""
        result = await component_tools["pptx_add_card"](
            slide_index=0, left=1.0, top=1.0, title="Card Title", description="Card description"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_card_variants(self, component_tools, mock_presentation_manager):
        """Test card variants."""
        variants = ["default", "bordered", "elevated"]
        for variant in variants:
            result = await component_tools["pptx_add_card"](
                slide_index=0, left=1.0, top=1.0, variant=variant
            )
            assert variant in result.lower()

    @pytest.mark.asyncio
    async def test_add_metric_card(self, component_tools, mock_presentation_manager):
        """Test adding metric card."""
        result = await component_tools["pptx_add_metric_card"](
            slide_index=0, label="Revenue", value="$100K", left=2.0, top=2.0
        )
        assert "Revenue" in result or "metric" in result.lower()

    @pytest.mark.asyncio
    async def test_add_metric_card_with_trend(self, component_tools, mock_presentation_manager):
        """Test metric card with change and trend."""
        result = await component_tools["pptx_add_metric_card"](
            slide_index=0, label="Sales", value="$50K", left=1.0, top=1.0, change="+12%", trend="up"
        )
        assert isinstance(result, str)


class TestIconComponent:
    """Test pptx_add_icon tool."""

    @pytest.mark.asyncio
    async def test_add_icon(self, component_tools, mock_presentation_manager):
        """Test adding icon."""
        result = await component_tools["pptx_add_icon"](
            slide_index=0, icon_type="check", left=1.0, top=1.0
        )
        assert "icon" in result.lower()

    @pytest.mark.asyncio
    async def test_add_icon_types(self, component_tools, mock_presentation_manager):
        """Test different icon types."""
        icon_types = ["check", "cross", "arrow", "info", "warning"]
        for icon_type in icon_types:
            result = await component_tools["pptx_add_icon"](
                slide_index=0, icon_type=icon_type, left=1.0, top=1.0
            )
            assert icon_type in result.lower()

    @pytest.mark.asyncio
    async def test_add_icon_variants(self, component_tools, mock_presentation_manager):
        """Test icon variants."""
        variants = ["default", "filled", "outlined"]
        for variant in variants:
            result = await component_tools["pptx_add_icon"](
                slide_index=0, icon_type="check", left=1.0, top=1.0, variant=variant
            )
            assert isinstance(result, str)


class TestProgressComponent:
    """Test pptx_add_progress_bar tool."""

    @pytest.mark.asyncio
    async def test_add_progress_bar(self, component_tools, mock_presentation_manager):
        """Test adding progress bar."""
        result = await component_tools["pptx_add_progress_bar"](
            slide_index=0, value=75.0, left=2.0, top=3.0
        )
        assert "75" in result or "progress" in result.lower()

    @pytest.mark.asyncio
    async def test_add_progress_bar_variants(self, component_tools, mock_presentation_manager):
        """Test progress bar variants."""
        variants = ["default", "success", "warning", "error"]
        for variant in variants:
            result = await component_tools["pptx_add_progress_bar"](
                slide_index=0, value=50.0, left=1.0, top=1.0, variant=variant
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_progress_bar_with_label(self, component_tools, mock_presentation_manager):
        """Test progress bar with label."""
        result = await component_tools["pptx_add_progress_bar"](
            slide_index=0, value=60.0, left=1.0, top=1.0, show_label=True
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_progress_bar_without_label(self, component_tools, mock_presentation_manager):
        """Test progress bar without label."""
        result = await component_tools["pptx_add_progress_bar"](
            slide_index=0, value=80.0, left=1.0, top=1.0, show_label=False
        )
        assert isinstance(result, str)


class TestTileComponent:
    """Test pptx_add_tile tool."""

    @pytest.mark.asyncio
    async def test_add_tile(self, component_tools, mock_presentation_manager):
        """Test adding tile."""
        result = await component_tools["pptx_add_tile"](
            slide_index=0, label="Users", value="1,234", left=1.0, top=2.0
        )
        assert "Users" in result or "tile" in result.lower()

    @pytest.mark.asyncio
    async def test_add_tile_variants(self, component_tools, mock_presentation_manager):
        """Test tile variants."""
        variants = ["default", "primary", "secondary", "accent"]
        for variant in variants:
            result = await component_tools["pptx_add_tile"](
                slide_index=0, label="Metric", value="100", left=1.0, top=1.0, variant=variant
            )
            assert isinstance(result, str)


class TestShapeComponent:
    """Test pptx_add_shape tool."""

    @pytest.mark.asyncio
    async def test_add_shape(self, component_tools, mock_presentation_manager):
        """Test adding shape."""
        result = await component_tools["pptx_add_shape"](
            slide_index=0, shape_type="rectangle", left=2.0, top=2.0
        )
        assert "rectangle" in result.lower()

    @pytest.mark.asyncio
    async def test_add_shape_types(self, component_tools, mock_presentation_manager):
        """Test different shape types."""
        shape_types = ["rectangle", "circle", "triangle", "arrow"]
        for shape_type in shape_types:
            result = await component_tools["pptx_add_shape"](
                slide_index=0, shape_type=shape_type, left=1.0, top=1.0
            )
            assert shape_type in result.lower()

    @pytest.mark.asyncio
    async def test_add_shape_with_text(self, component_tools, mock_presentation_manager):
        """Test shape with text."""
        result = await component_tools["pptx_add_shape"](
            slide_index=0, shape_type="rectangle", left=1.0, top=1.0, text="Shape Text"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_shape_with_color(self, component_tools, mock_presentation_manager):
        """Test shape with fill color."""
        result = await component_tools["pptx_add_shape"](
            slide_index=0, shape_type="circle", left=1.0, top=1.0, fill_color="#FF0000"
        )
        assert isinstance(result, str)


class TestConnectorComponent:
    """Test pptx_add_connector tool."""

    @pytest.mark.asyncio
    async def test_add_connector(self, component_tools, mock_presentation_manager):
        """Test adding connector."""
        result = await component_tools["pptx_add_connector"](
            slide_index=0, start_x=2.0, start_y=2.0, end_x=5.0, end_y=3.0
        )
        assert "connector" in result.lower()

    @pytest.mark.asyncio
    async def test_add_connector_types(self, component_tools, mock_presentation_manager):
        """Test different connector types."""
        connector_types = ["straight", "elbow", "curved"]
        for connector_type in connector_types:
            result = await component_tools["pptx_add_connector"](
                slide_index=0,
                start_x=1.0,
                start_y=1.0,
                end_x=4.0,
                end_y=2.0,
                connector_type=connector_type,
            )
            assert connector_type in result.lower()


class TestProcessFlowComponent:
    """Test pptx_add_process_flow tool."""

    @pytest.mark.asyncio
    async def test_add_process_flow(self, component_tools, mock_presentation_manager):
        """Test adding process flow."""
        result = await component_tools["pptx_add_process_flow"](
            slide_index=0, steps=["Step 1", "Step 2", "Step 3"], left=1.0, top=2.0
        )
        assert "3" in result or "process" in result.lower()

    @pytest.mark.asyncio
    async def test_add_process_flow_orientations(self, component_tools, mock_presentation_manager):
        """Test process flow orientations."""
        orientations = ["horizontal", "vertical"]
        for orientation in orientations:
            result = await component_tools["pptx_add_process_flow"](
                slide_index=0, steps=["A", "B", "C"], left=1.0, top=1.0, orientation=orientation
            )
            assert isinstance(result, str)


class TestTimelineComponent:
    """Test pptx_add_timeline tool."""

    @pytest.mark.asyncio
    async def test_add_timeline(self, component_tools, mock_presentation_manager):
        """Test adding timeline."""
        events = [
            {"date": "Q1", "description": "Event 1"},
            {"date": "Q2", "description": "Event 2"},
        ]
        result = await component_tools["pptx_add_timeline"](
            slide_index=0, events=events, left=1.0, top=2.0
        )
        assert "2" in result or "timeline" in result.lower()

    @pytest.mark.asyncio
    async def test_add_timeline_orientations(self, component_tools, mock_presentation_manager):
        """Test timeline orientations."""
        events = [{"date": "2020", "description": "Event"}]
        orientations = ["horizontal", "vertical"]
        for orientation in orientations:
            result = await component_tools["pptx_add_timeline"](
                slide_index=0, events=events, left=1.0, top=1.0, orientation=orientation
            )
            assert isinstance(result, str)


class TestTextComponent:
    """Test text-related tools."""

    @pytest.mark.asyncio
    async def test_add_textbox(self, component_tools, mock_presentation_manager):
        """Test adding textbox."""
        result = await component_tools["pptx_add_textbox"](
            slide_index=0, text="Test text", left=2.0, top=3.0
        )
        assert "text" in result.lower()

    @pytest.mark.asyncio
    async def test_add_textbox_with_formatting(self, component_tools, mock_presentation_manager):
        """Test textbox with formatting."""
        result = await component_tools["pptx_add_textbox"](
            slide_index=0,
            text="Formatted text",
            left=1.0,
            top=1.0,
            font_size=24,
            alignment="center",
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_textbox_alignments(self, component_tools, mock_presentation_manager):
        """Test different text alignments."""
        alignments = ["left", "center", "right"]
        for alignment in alignments:
            result = await component_tools["pptx_add_textbox"](
                slide_index=0, text="Text", left=1.0, top=1.0, alignment=alignment
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_bullet_list(self, component_tools, mock_presentation_manager):
        """Test adding bullet list."""
        result = await component_tools["pptx_add_bullet_list"](
            slide_index=0, items=["Item 1", "Item 2", "Item 3"], left=2.0, top=2.0
        )
        assert "3" in result or "bullet" in result.lower()


class TestTableComponent:
    """Test pptx_add_table_component tool."""

    @pytest.mark.asyncio
    async def test_add_table(self, component_tools, mock_presentation_manager):
        """Test adding table."""
        result = await component_tools["pptx_add_table_component"](
            slide_index=0,
            headers=["Col1", "Col2"],
            rows=[["A", "B"], ["C", "D"]],
            left=1.0,
            top=2.0,
        )
        assert "2" in result or "table" in result.lower()

    @pytest.mark.asyncio
    async def test_add_table_variants(self, component_tools, mock_presentation_manager):
        """Test table variants."""
        variants = ["default", "striped", "bordered"]
        for variant in variants:
            result = await component_tools["pptx_add_table_component"](
                slide_index=0, headers=["A"], rows=[["1"]], left=1.0, top=1.0, variant=variant
            )
            assert isinstance(result, str)


class TestImageComponent:
    """Test pptx_add_image_component tool."""

    @pytest.mark.asyncio
    async def test_add_image(self, component_tools, mock_presentation_manager):
        """Test adding image - should handle error gracefully."""
        result = await component_tools["pptx_add_image_component"](
            slide_index=0, image_path="nonexistent.png", left=2.0, top=2.0
        )
        # Should return some result even if image doesn't exist
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_with_dimensions(self, component_tools, mock_presentation_manager):
        """Test image with custom dimensions."""
        result = await component_tools["pptx_add_image_component"](
            slide_index=0, image_path="test.png", left=1.0, top=1.0, width=4.0, height=3.0
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_maintain_aspect(self, component_tools, mock_presentation_manager):
        """Test image with maintain aspect ratio."""
        result = await component_tools["pptx_add_image_component"](
            slide_index=0, image_path="test.png", left=1.0, top=1.0, maintain_aspect=True
        )
        assert isinstance(result, str)


class TestIntegration:
    """Integration tests for component tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, component_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_add_alert",
            "pptx_add_avatar",
            "pptx_add_avatar_group",
            "pptx_add_badge",
            "pptx_add_button",
            "pptx_add_card",
            "pptx_add_metric_card",
            "pptx_add_icon",
            "pptx_add_progress_bar",
            "pptx_add_tile",
            "pptx_add_shape",
            "pptx_add_connector",
            "pptx_add_process_flow",
            "pptx_add_timeline",
            "pptx_add_textbox",
            "pptx_add_bullet_list",
            "pptx_add_table_component",
            "pptx_add_image_component",
        ]

        for tool_name in expected_tools:
            assert tool_name in component_tools, f"Tool {tool_name} not registered"
            assert callable(component_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_multiple_components_same_slide(self, component_tools, mock_presentation_manager):
        """Test adding multiple components to the same slide."""
        # Add alert
        result1 = await component_tools["pptx_add_alert"](
            slide_index=0, message="Alert", left=1.0, top=1.0
        )
        assert isinstance(result1, str)

        # Add button
        result2 = await component_tools["pptx_add_button"](
            slide_index=0, text="Button", left=3.0, top=1.0
        )
        assert isinstance(result2, str)

        # Add badge
        result3 = await component_tools["pptx_add_badge"](
            slide_index=0, text="New", left=5.0, top=1.0
        )
        assert isinstance(result3, str)
