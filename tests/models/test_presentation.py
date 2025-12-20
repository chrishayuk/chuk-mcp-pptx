# tests/models/test_presentation.py
"""
Tests for presentation metadata models.

Tests the Pydantic models:
- SlideMetadata
- PresentationMetadata
"""

import pytest
from datetime import datetime
from pydantic import ValidationError


# ============================================================================
# Test SlideMetadata
# ============================================================================


class TestSlideMetadata:
    """Tests for SlideMetadata model."""

    def test_slide_metadata_required_fields(self):
        """Test that index is required."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        slide = SlideMetadata(index=0)
        assert slide.index == 0

    def test_slide_metadata_defaults(self):
        """Test default values."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        slide = SlideMetadata(index=0)
        assert slide.layout == "Blank"
        assert slide.has_title is False
        assert slide.title_text is None
        assert slide.shape_count == 0
        assert slide.has_chart is False
        assert slide.has_table is False
        assert slide.has_images is False
        assert slide.component_types == []

    def test_slide_metadata_all_fields(self):
        """Test with all fields specified."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        slide = SlideMetadata(
            index=1,
            layout="Title Slide",
            has_title=True,
            title_text="My Title",
            shape_count=5,
            has_chart=True,
            has_table=True,
            has_images=True,
            component_types=["text", "chart", "image"],
        )
        assert slide.index == 1
        assert slide.layout == "Title Slide"
        assert slide.has_title is True
        assert slide.title_text == "My Title"
        assert slide.shape_count == 5
        assert slide.has_chart is True
        assert slide.has_table is True
        assert slide.has_images is True
        assert "chart" in slide.component_types

    def test_slide_metadata_index_validation(self):
        """Test that index must be >= 0."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        with pytest.raises(ValidationError):
            SlideMetadata(index=-1)

    def test_slide_metadata_shape_count_validation(self):
        """Test that shape_count must be >= 0."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        with pytest.raises(ValidationError):
            SlideMetadata(index=0, shape_count=-1)

    def test_slide_metadata_extra_fields_forbidden(self):
        """Test that extra fields are not allowed."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        with pytest.raises(ValidationError):
            SlideMetadata(index=0, extra_field="not allowed")


# ============================================================================
# Test PresentationMetadata
# ============================================================================


class TestPresentationMetadata:
    """Tests for PresentationMetadata model."""

    def test_presentation_metadata_required_fields(self):
        """Test that name is required."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        pres = PresentationMetadata(name="test")
        assert pres.name == "test"

    def test_presentation_metadata_defaults(self):
        """Test default values."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        pres = PresentationMetadata(name="test")
        assert pres.slide_count == 0
        assert pres.theme is None
        assert pres.vfs_path is None
        assert pres.namespace_id is None
        assert pres.is_saved is False
        assert pres.template_path is None
        assert pres.slides == []
        assert isinstance(pres.created_at, datetime)
        assert isinstance(pres.modified_at, datetime)

    def test_presentation_metadata_all_fields(self):
        """Test with all fields specified."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        now = datetime.now()
        slide = SlideMetadata(index=0)

        pres = PresentationMetadata(
            name="My Presentation",
            slide_count=1,
            created_at=now,
            modified_at=now,
            theme="corporate",
            vfs_path="artifacts://ns-123/presentation.pptx",
            namespace_id="ns-123",
            is_saved=True,
            template_path="/templates/corporate.pptx",
            slides=[slide],
        )
        assert pres.name == "My Presentation"
        assert pres.slide_count == 1
        assert pres.theme == "corporate"
        assert pres.vfs_path == "artifacts://ns-123/presentation.pptx"
        assert pres.namespace_id == "ns-123"
        assert pres.is_saved is True
        assert pres.template_path == "/templates/corporate.pptx"
        assert len(pres.slides) == 1

    def test_presentation_metadata_name_validation(self):
        """Test that name must have minimum length."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        with pytest.raises(ValidationError):
            PresentationMetadata(name="")

    def test_presentation_metadata_slide_count_validation(self):
        """Test that slide_count must be >= 0."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        with pytest.raises(ValidationError):
            PresentationMetadata(name="test", slide_count=-1)

    def test_presentation_metadata_extra_fields_forbidden(self):
        """Test that extra fields are not allowed."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        with pytest.raises(ValidationError):
            PresentationMetadata(name="test", extra_field="not allowed")


# ============================================================================
# Test PresentationMetadata Methods
# ============================================================================


class TestPresentationMetadataMethods:
    """Tests for PresentationMetadata methods."""

    def test_update_modified(self):
        """Test update_modified method."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata
        import time

        pres = PresentationMetadata(name="test")
        original_modified = pres.modified_at

        # Wait a tiny bit to ensure time difference
        time.sleep(0.01)

        pres.update_modified()
        assert pres.modified_at > original_modified

    def test_add_slide_metadata(self):
        """Test add_slide_metadata method."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        assert pres.slide_count == 0
        assert len(pres.slides) == 0

        slide = SlideMetadata(index=0, layout="Title Slide", has_title=True)
        pres.add_slide_metadata(slide)

        assert pres.slide_count == 1
        assert len(pres.slides) == 1
        assert pres.slides[0].layout == "Title Slide"

    def test_add_multiple_slides(self):
        """Test adding multiple slides."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")

        for i in range(5):
            slide = SlideMetadata(index=i, layout=f"Layout {i}")
            pres.add_slide_metadata(slide)

        assert pres.slide_count == 5
        assert len(pres.slides) == 5
        assert pres.slides[2].layout == "Layout 2"

    def test_add_slide_metadata_updates_modified(self):
        """Test that add_slide_metadata updates modified timestamp."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata
        import time

        pres = PresentationMetadata(name="test")
        original_modified = pres.modified_at

        time.sleep(0.01)

        slide = SlideMetadata(index=0)
        pres.add_slide_metadata(slide)

        assert pres.modified_at > original_modified

    def test_get_slide_metadata_valid_index(self):
        """Test get_slide_metadata with valid index."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        slide = SlideMetadata(index=0, layout="Content", has_title=True, title_text="Test")
        pres.add_slide_metadata(slide)

        result = pres.get_slide_metadata(0)
        assert result is not None
        assert result.layout == "Content"
        assert result.title_text == "Test"

    def test_get_slide_metadata_invalid_index_negative(self):
        """Test get_slide_metadata with negative index."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        slide = SlideMetadata(index=0)
        pres.add_slide_metadata(slide)

        result = pres.get_slide_metadata(-1)
        assert result is None

    def test_get_slide_metadata_invalid_index_too_large(self):
        """Test get_slide_metadata with index beyond slides list."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        slide = SlideMetadata(index=0)
        pres.add_slide_metadata(slide)

        result = pres.get_slide_metadata(5)
        assert result is None

    def test_get_slide_metadata_empty_slides(self):
        """Test get_slide_metadata with no slides."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        pres = PresentationMetadata(name="test")

        result = pres.get_slide_metadata(0)
        assert result is None

    def test_get_slide_metadata_boundary_valid(self):
        """Test get_slide_metadata at boundary (last valid index)."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        for i in range(3):
            pres.add_slide_metadata(SlideMetadata(index=i))

        # Index 2 is the last valid index
        result = pres.get_slide_metadata(2)
        assert result is not None
        assert result.index == 2

    def test_get_slide_metadata_boundary_invalid(self):
        """Test get_slide_metadata just past boundary."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        for i in range(3):
            pres.add_slide_metadata(SlideMetadata(index=i))

        # Index 3 is out of bounds (only 0, 1, 2 exist)
        result = pres.get_slide_metadata(3)
        assert result is None


# ============================================================================
# Test Edge Cases
# ============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_slide_metadata_with_none_title(self):
        """Test slide with no title text."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        slide = SlideMetadata(index=0, has_title=True, title_text=None)
        assert slide.has_title is True
        assert slide.title_text is None

    def test_presentation_metadata_datetime_types(self):
        """Test that datetime fields are proper datetime objects."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata

        pres = PresentationMetadata(name="test")
        assert isinstance(pres.created_at, datetime)
        assert isinstance(pres.modified_at, datetime)

    def test_slide_metadata_empty_component_types(self):
        """Test slide with empty component types list."""
        from chuk_mcp_pptx.models.presentation import SlideMetadata

        slide = SlideMetadata(index=0, component_types=[])
        assert slide.component_types == []

    def test_presentation_metadata_model_dump(self):
        """Test that model can be serialized."""
        from chuk_mcp_pptx.models.presentation import PresentationMetadata, SlideMetadata

        pres = PresentationMetadata(name="test")
        pres.add_slide_metadata(SlideMetadata(index=0))

        data = pres.model_dump()
        assert "name" in data
        assert "slides" in data
        assert len(data["slides"]) == 1
