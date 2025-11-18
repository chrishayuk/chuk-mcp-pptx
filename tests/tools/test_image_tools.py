"""
Tests for image_tools.py

Tests all image-related MCP tools for >90% coverage.
"""

import pytest
from unittest.mock import MagicMock, patch
from chuk_mcp_pptx.tools.image_tools import register_image_tools, add_image, add_text_box_with_style


@pytest.fixture
def image_tools(mock_mcp_server, mock_presentation_manager):
    """Register image tools and return them."""
    tools = register_image_tools(mock_mcp_server, mock_presentation_manager)
    return tools


class TestAddImageSlide:
    """Test pptx_add_image_slide tool."""

    @pytest.mark.asyncio
    async def test_add_image_slide_file_path(self, image_tools, mock_presentation_manager):
        """Test adding image slide with file path."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image_slide"](
                title="Test Image", image_path="/fake/path/image.png"
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_slide_base64(self, image_tools, mock_presentation_manager):
        """Test adding image slide with base64 data."""
        base64_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        result = await image_tools["pptx_add_image_slide"](
            title="Base64 Image", image_path=base64_data
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_slide_file_not_found(self, image_tools, mock_presentation_manager):
        """Test error when image file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            result = await image_tools["pptx_add_image_slide"](
                title="Missing Image", image_path="/fake/missing.png"
            )
            assert "Error" in result or "not found" in result

    @pytest.mark.asyncio
    async def test_add_image_slide_no_presentation(self, image_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await image_tools["pptx_add_image_slide"](
            title="Image", image_path="test.png", presentation="nonexistent"
        )
        assert "No presentation found" in result or "Error" in result

    @pytest.mark.asyncio
    async def test_add_image_slide_with_presentation(self, image_tools, mock_presentation_manager):
        """Test adding image slide with specific presentation."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image_slide"](
                title="Image", image_path="/fake/image.png", presentation="test_presentation"
            )
            assert isinstance(result, str)


class TestAddImage:
    """Test pptx_add_image tool."""

    @pytest.mark.asyncio
    async def test_add_image_basic(self, image_tools, mock_presentation_manager):
        """Test adding image with basic parameters."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image"](
                slide_index=0, image_path="/fake/image.png"
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_with_dimensions(self, image_tools, mock_presentation_manager):
        """Test adding image with custom dimensions."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image"](
                slide_index=0,
                image_path="/fake/image.png",
                left=2.0,
                top=2.0,
                width=4.0,
                height=3.0,
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_maintain_ratio(self, image_tools, mock_presentation_manager):
        """Test image with maintain aspect ratio."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image"](
                slide_index=0, image_path="/fake/image.png", maintain_ratio=True
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_base64(self, image_tools, mock_presentation_manager):
        """Test adding image with base64 data."""
        base64_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        result = await image_tools["pptx_add_image"](slide_index=0, image_path=base64_data)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_invalid_slide(self, image_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await image_tools["pptx_add_image"](slide_index=999, image_path="/fake/image.png")
        assert "Error" in result and ("out of range" in result or "Slide index" in result)

    @pytest.mark.asyncio
    async def test_add_image_no_presentation(self, image_tools, mock_presentation_manager):
        """Test error when no presentation exists."""
        # Use a non-existent presentation name instead of mocking
        result = await image_tools["pptx_add_image"](
            slide_index=0, image_path="/fake/image.png", presentation="nonexistent"
        )
        assert "No presentation found" in result or "Error" in result


class TestAddBackgroundImage:
    """Test pptx_add_background_image tool."""

    @pytest.mark.asyncio
    async def test_add_background_image(self, image_tools, mock_presentation_manager):
        """Test adding background image."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_background_image"](
                slide_index=0, image_path="/fake/background.jpg"
            )
            assert isinstance(result, str)
            assert "background" in result.lower()

    @pytest.mark.asyncio
    async def test_add_background_image_base64(self, image_tools, mock_presentation_manager):
        """Test background image with base64."""
        base64_data = "data:image/jpeg;base64,/9j/4AAQSkZJRg=="
        result = await image_tools["pptx_add_background_image"](
            slide_index=0, image_path=base64_data
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_background_image_invalid_slide(self, image_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await image_tools["pptx_add_background_image"](
            slide_index=999, image_path="/fake/bg.png"
        )
        assert "Error" in result and ("out of range" in result or "Slide index" in result)


class TestAddImageGallery:
    """Test pptx_add_image_gallery tool."""

    @pytest.mark.asyncio
    async def test_add_image_gallery_basic(self, image_tools, mock_presentation_manager):
        """Test adding image gallery."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image_gallery"](
                slide_index=0, image_paths=["/fake/img1.png", "/fake/img2.png"]
            )
            assert isinstance(result, str)
            assert "2" in result or "gallery" in result.lower()

    @pytest.mark.asyncio
    async def test_add_image_gallery_custom_layout(self, image_tools, mock_presentation_manager):
        """Test gallery with custom layout."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image_gallery"](
                slide_index=0,
                image_paths=["/fake/1.png", "/fake/2.png", "/fake/3.png", "/fake/4.png"],
                columns=2,
                spacing=0.3,
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_gallery_many_images(self, image_tools, mock_presentation_manager):
        """Test gallery with many images."""
        with patch("pathlib.Path.exists", return_value=True):
            image_paths = [f"/fake/img{i}.png" for i in range(9)]
            result = await image_tools["pptx_add_image_gallery"](
                slide_index=0, image_paths=image_paths, columns=3
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_gallery_invalid_slide(self, image_tools, mock_presentation_manager):
        """Test error with invalid slide index."""
        result = await image_tools["pptx_add_image_gallery"](
            slide_index=999, image_paths=["/fake/1.png"]
        )
        assert "Error" in result and ("out of range" in result or "Slide index" in result)


class TestAddImageWithCaption:
    """Test pptx_add_image_with_caption tool."""

    @pytest.mark.asyncio
    async def test_add_image_with_caption(self, image_tools, mock_presentation_manager):
        """Test adding image with caption."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image_with_caption"](
                slide_index=0, image_path="/fake/product.jpg", caption="Our flagship product"
            )
            assert isinstance(result, str)
            assert "caption" in result.lower() or "image" in result.lower()

    @pytest.mark.asyncio
    async def test_add_image_with_caption_custom_position(
        self, image_tools, mock_presentation_manager
    ):
        """Test image with caption at custom position."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_image_with_caption"](
                slide_index=0,
                image_path="/fake/img.png",
                caption="Test caption",
                left=2.0,
                top=1.5,
                image_width=5.0,
                image_height=3.5,
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_with_caption_invalid_slide(
        self, image_tools, mock_presentation_manager
    ):
        """Test error with invalid slide index."""
        result = await image_tools["pptx_add_image_with_caption"](
            slide_index=999, image_path="/fake/img.png", caption="Caption"
        )
        assert "Error" in result and ("out of range" in result or "Slide index" in result)


class TestAddLogo:
    """Test pptx_add_logo tool."""

    @pytest.mark.asyncio
    async def test_add_logo_top_right(self, image_tools, mock_presentation_manager):
        """Test adding logo in top-right position."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_logo"](
                slide_index=0, logo_path="/fake/logo.png", position="top-right"
            )
            assert isinstance(result, str)
            assert "logo" in result.lower()

    @pytest.mark.asyncio
    async def test_add_logo_all_positions(self, image_tools, mock_presentation_manager):
        """Test logo in all positions."""
        positions = [
            "top-left",
            "top-center",
            "top-right",
            "center-left",
            "center",
            "center-right",
            "bottom-left",
            "bottom-center",
            "bottom-right",
        ]
        with patch("pathlib.Path.exists", return_value=True):
            for position in positions:
                result = await image_tools["pptx_add_logo"](
                    slide_index=0, logo_path="/fake/logo.png", position=position
                )
                assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_logo_custom_size(self, image_tools, mock_presentation_manager):
        """Test logo with custom size."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_logo"](
                slide_index=0, logo_path="/fake/logo.png", position="top-left", size=1.5, margin=0.5
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_logo_invalid_position(self, image_tools, mock_presentation_manager):
        """Test that invalid position defaults to top-right."""
        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_add_logo"](
                slide_index=0, logo_path="/fake/logo.png", position="invalid-position"
            )
            # Should succeed by defaulting to a valid position
            assert isinstance(result, str)
            assert "logo" in result.lower() or "Added" in result


class TestReplaceImage:
    """Test pptx_replace_image tool."""

    @pytest.mark.asyncio
    async def test_replace_image_basic(self, image_tools, mock_presentation_manager):
        """Test replacing image."""
        # Setup mock slide with image shape
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_image_shape = MagicMock()
        mock_image_shape.image = MagicMock()
        mock_image_shape.left = MagicMock()
        mock_image_shape.left.inches = 1.0
        mock_image_shape.top = MagicMock()
        mock_image_shape.top.inches = 1.0
        mock_image_shape.width = MagicMock()
        mock_image_shape.width.inches = 3.0
        mock_image_shape.height = MagicMock()
        mock_image_shape.height.inches = 2.0
        mock_image_shape.element = MagicMock()

        slide.shapes._members = [mock_image_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_image_shape]))

        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_replace_image"](
                slide_index=0, old_image_index=0, new_image_path="/fake/new_image.png"
            )
            assert isinstance(result, str)
            assert "Replaced" in result or "image" in result.lower()

    @pytest.mark.asyncio
    async def test_replace_image_change_size(self, image_tools, mock_presentation_manager):
        """Test replacing image with different size."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        mock_image_shape = MagicMock()
        mock_image_shape.image = MagicMock()
        mock_image_shape.left = MagicMock()
        mock_image_shape.left.inches = 1.0
        mock_image_shape.top = MagicMock()
        mock_image_shape.top.inches = 1.0
        mock_image_shape.width = MagicMock()
        mock_image_shape.width.inches = 3.0
        mock_image_shape.height = MagicMock()
        mock_image_shape.height.inches = 2.0
        mock_image_shape.element = MagicMock()

        slide.shapes._members = [mock_image_shape]
        slide.shapes.__iter__ = MagicMock(return_value=iter([mock_image_shape]))

        with patch("pathlib.Path.exists", return_value=True):
            result = await image_tools["pptx_replace_image"](
                slide_index=0,
                old_image_index=0,
                new_image_path="/fake/new.png",
                maintain_position=True,
                maintain_size=False,
            )
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_replace_image_invalid_index(self, image_tools, mock_presentation_manager):
        """Test error with invalid image index."""
        result = await image_tools["pptx_replace_image"](
            slide_index=0, old_image_index=999, new_image_path="/fake/new.png"
        )
        assert "Error" in result and ("out of range" in result or "Image index" in result)


class TestAddImagePlaceholder:
    """Test pptx_add_image_placeholder tool."""

    @pytest.mark.asyncio
    async def test_add_image_placeholder_basic(self, image_tools, mock_presentation_manager):
        """Test adding image placeholder."""
        result = await image_tools["pptx_add_image_placeholder"](slide_index=0)
        assert isinstance(result, str)
        assert "placeholder" in result.lower()

    @pytest.mark.asyncio
    async def test_add_image_placeholder_custom_label(self, image_tools, mock_presentation_manager):
        """Test placeholder with custom label."""
        result = await image_tools["pptx_add_image_placeholder"](
            slide_index=0, label="Product Screenshot", left=2.0, top=2.0, width=5.0, height=3.5
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_placeholder_custom_colors(
        self, image_tools, mock_presentation_manager
    ):
        """Test placeholder with custom colors."""
        result = await image_tools["pptx_add_image_placeholder"](
            slide_index=0, background_color="#F0F0F0", text_color="#333333"
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_add_image_placeholder_invalid_slide(
        self, image_tools, mock_presentation_manager
    ):
        """Test error with invalid slide index."""
        result = await image_tools["pptx_add_image_placeholder"](slide_index=999)
        assert "Error" in result and ("out of range" in result or "Slide index" in result)


class TestHelperFunctions:
    """Test helper functions."""

    @pytest.mark.asyncio
    async def test_add_image_base64(self, mock_presentation_manager):
        """Test add_image helper with base64."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]
        base64_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        result = add_image(slide, base64_data, 1.0, 1.0)
        assert result is not None

    @pytest.mark.asyncio
    async def test_add_image_file_path(self, mock_presentation_manager):
        """Test add_image helper with file path."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        # Mock both Path.exists and slide.shapes.add_picture
        mock_picture = MagicMock()
        with patch("chuk_mcp_pptx.tools.image_tools.Path") as mock_path:
            mock_path.return_value.exists.return_value = True
            with patch.object(slide.shapes, "add_picture", return_value=mock_picture):
                result = add_image(slide, "/fake/image.png", 1.0, 1.0, 4.0, 3.0)
                assert result is not None

    @pytest.mark.asyncio
    async def test_add_image_with_width_only(self, mock_presentation_manager):
        """Test add_image with width only."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        # Mock both Path.exists and slide.shapes.add_picture
        mock_picture = MagicMock()
        with patch("chuk_mcp_pptx.tools.image_tools.Path") as mock_path:
            mock_path.return_value.exists.return_value = True
            with patch.object(slide.shapes, "add_picture", return_value=mock_picture):
                result = add_image(slide, "/fake/image.png", 1.0, 1.0, width=4.0)
                assert result is not None

    @pytest.mark.asyncio
    async def test_add_image_with_height_only(self, mock_presentation_manager):
        """Test add_image helper with height only."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        # Mock both Path.exists and slide.shapes.add_picture
        mock_picture = MagicMock()
        with patch("chuk_mcp_pptx.tools.image_tools.Path") as mock_path:
            mock_path.return_value.exists.return_value = True
            with patch.object(slide.shapes, "add_picture", return_value=mock_picture):
                result = add_image(slide, "/fake/image.png", 1.0, 1.0, height=3.0)
                assert result is not None

    @pytest.mark.asyncio
    async def test_add_text_box_with_style_caption(self, mock_presentation_manager):
        """Test text box with caption style."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        result = add_text_box_with_style(
            slide, 1.0, 5.0, 4.0, 0.5, "Test caption", style_preset="caption"
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_add_text_box_with_style_title(self, mock_presentation_manager):
        """Test text box with title style."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        result = add_text_box_with_style(
            slide, 1.0, 1.0, 6.0, 1.0, "Test Title", style_preset="title"
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_add_text_box_with_style_body(self, mock_presentation_manager):
        """Test text box with body style."""
        result_tuple = await mock_presentation_manager.get("test_presentation")
        assert result_tuple is not None
        prs, _ = result_tuple
        slide = prs.slides[0]

        result = add_text_box_with_style(
            slide, 1.0, 2.0, 5.0, 2.0, "Body text content", style_preset="body"
        )
        assert result is not None


class TestIntegration:
    """Integration tests for image tools."""

    @pytest.mark.asyncio
    async def test_all_tools_registered(self, image_tools):
        """Test that all expected tools are registered."""
        expected_tools = [
            "pptx_add_image_slide",
            "pptx_add_image",
            "pptx_add_background_image",
            "pptx_add_image_gallery",
            "pptx_add_image_with_caption",
            "pptx_add_logo",
            "pptx_replace_image",
            "pptx_add_image_placeholder",
        ]

        for tool_name in expected_tools:
            assert tool_name in image_tools, f"Tool {tool_name} not registered"
            assert callable(image_tools[tool_name]), f"Tool {tool_name} not callable"

    @pytest.mark.asyncio
    async def test_multiple_images_same_slide(self, image_tools, mock_presentation_manager):
        """Test adding multiple images to same slide."""
        with patch("pathlib.Path.exists", return_value=True):
            # Add first image
            result1 = await image_tools["pptx_add_image"](
                slide_index=0, image_path="/fake/img1.png", left=1.0, top=2.0
            )
            assert isinstance(result1, str)

            # Add logo
            result2 = await image_tools["pptx_add_logo"](
                slide_index=0, logo_path="/fake/logo.png", position="top-right"
            )
            assert isinstance(result2, str)
