"""
Tests for layout helper functions.
Tests validate_position, calculate_grid_layout, get_logo_position, get_safe_content_area.
"""

import pytest
from chuk_mcp_pptx.layout.helpers import (
    validate_position,
    calculate_grid_layout,
    get_logo_position,
    get_safe_content_area,
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    SLIDE_HEIGHT_4_3,
)


class TestValidatePosition:
    """Test validate_position function."""

    def test_validate_position_valid(self):
        """Test validation with valid position."""
        left, top, width, height = validate_position(1.0, 2.0, 3.0, 2.0)

        # Should return same values if valid
        assert left == 1.0
        assert top == 2.0
        assert width == 3.0
        assert height == 2.0

    def test_validate_position_auto_adjust_right_edge(self):
        """Test auto-adjustment when element extends past right edge."""
        # Element that would extend past right edge
        left, top, width, height = validate_position(8.0, 2.0, 5.0, 2.0, auto_adjust=True)

        # Should adjust to fit within slide
        assert left + width <= SLIDE_WIDTH
        assert width > 0

    def test_validate_position_auto_adjust_bottom_edge(self):
        """Test auto-adjustment when element extends past bottom edge."""
        # Element that would extend past bottom edge
        left, top, width, height = validate_position(1.0, 6.0, 3.0, 5.0, auto_adjust=True)

        # Should adjust to fit within slide
        assert top + height <= SLIDE_HEIGHT
        assert height > 0

    def test_validate_position_no_auto_adjust_raises_error(self):
        """Test that validation without auto_adjust raises error for invalid position."""
        # Element that extends past right edge
        with pytest.raises(ValueError, match="Element doesn't fit"):
            validate_position(8.0, 2.0, 5.0, 2.0, auto_adjust=False)

    def test_validate_position_minimum_size(self):
        """Test that minimum size is enforced."""
        # Very small dimensions
        left, top, width, height = validate_position(1.0, 2.0, 0.1, 0.1, auto_adjust=True)

        # Should enforce minimum size
        assert width >= 0.5
        assert height >= 0.5

    def test_validate_position_4_3_aspect_ratio(self):
        """Test validation with 4:3 aspect ratio."""
        left, top, width, height = validate_position(1.0, 2.0, 3.0, 2.0, aspect_ratio="4:3")

        # Should work with 4:3 slide dimensions
        assert left + width <= SLIDE_WIDTH
        assert top + height <= SLIDE_HEIGHT_4_3

    def test_validate_position_negative_coordinates(self):
        """Test validation adjusts negative coordinates."""
        left, top, width, height = validate_position(-1.0, -0.5, 3.0, 2.0, auto_adjust=True)

        # Should adjust to be within slide
        assert left >= 0
        assert top >= 0

    def test_validate_position_width_exceeds_slide(self):
        """Test when width exceeds slide width."""
        # Width larger than slide, should be adjusted
        left, top, width, height = validate_position(1.0, 2.0, 15.0, 2.0, auto_adjust=True)

        # Width should be reduced to fit from left position
        assert left + width <= SLIDE_WIDTH
        assert width < 15.0


class TestCalculateGridLayout:
    """Test calculate_grid_layout function."""

    def test_calculate_grid_layout_basic(self):
        """Test creating basic grid layout."""
        positions = calculate_grid_layout(
            num_items=6,
            columns=3,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        assert len(positions) == 6

        # Should have 2 rows
        tops = [p["top"] for p in positions]
        assert len(set(tops)) == 2

    def test_calculate_grid_layout_auto_columns(self):
        """Test grid with automatic column calculation."""
        # 2 items should get 2 columns
        positions = calculate_grid_layout(
            num_items=2,
            columns=None,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        assert len(positions) == 2

    def test_calculate_grid_layout_auto_columns_3_items(self):
        """Test auto columns with 3 items."""
        positions = calculate_grid_layout(
            num_items=3,
            columns=None,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        # 3 items should get 2 columns
        assert len(positions) == 3

    def test_calculate_grid_layout_auto_columns_4_items(self):
        """Test auto columns with 4 items."""
        positions = calculate_grid_layout(
            num_items=4,
            columns=None,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        # 4 items should get 2 columns
        assert len(positions) == 4

    def test_calculate_grid_layout_auto_columns_9_items(self):
        """Test auto columns with 9 items."""
        positions = calculate_grid_layout(
            num_items=9,
            columns=None,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        # 9 items should get 3 columns
        assert len(positions) == 9

    def test_calculate_grid_layout_auto_columns_many_items(self):
        """Test auto columns with many items."""
        positions = calculate_grid_layout(
            num_items=16,
            columns=None,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        # More than 9 items should get 4 columns
        assert len(positions) == 16

    def test_calculate_grid_layout_empty(self):
        """Test grid with no items."""
        positions = calculate_grid_layout(
            num_items=0,
            columns=3,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        assert len(positions) == 0

    def test_calculate_grid_layout_spacing(self):
        """Test grid with custom spacing."""
        positions = calculate_grid_layout(
            num_items=4,
            columns=2,
            spacing=0.5,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        # Verify spacing between items
        assert positions[0]["left"] + positions[0]["width"] + 0.5 <= positions[1]["left"] + 0.1

    def test_calculate_grid_layout_all_have_required_fields(self):
        """Test that all positions have required fields."""
        positions = calculate_grid_layout(
            num_items=6,
            columns=3,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=4.0,
        )

        for pos in positions:
            assert "left" in pos
            assert "top" in pos
            assert "width" in pos
            assert "height" in pos

    def test_calculate_grid_layout_minimum_item_size(self):
        """Test that items have minimum size."""
        positions = calculate_grid_layout(
            num_items=12,
            columns=6,
            container_left=0.5,
            container_top=2.0,
            container_width=9.0,
            container_height=2.0,
        )

        # Items should have minimum dimensions
        for pos in positions:
            assert pos["width"] >= 1.0
            assert pos["height"] >= 0.75


class TestGetLogoPosition:
    """Test get_logo_position function."""

    def test_get_logo_position_top_left(self):
        """Test logo position at top-left."""
        pos = get_logo_position("top-left", size=1.0, margin=0.5)

        assert pos["left"] == 0.5
        assert pos["top"] == 0.5
        assert pos["width"] == 1.0
        assert pos["height"] == 1.0

    def test_get_logo_position_top_center(self):
        """Test logo position at top-center."""
        pos = get_logo_position("top-center", size=1.0, margin=0.5)

        # Should be centered horizontally
        assert pos["left"] == (SLIDE_WIDTH - 1.0) / 2
        assert pos["top"] == 0.5

    def test_get_logo_position_top_right(self):
        """Test logo position at top-right."""
        pos = get_logo_position("top-right", size=1.0, margin=0.5)

        # Should be at right edge with margin
        assert pos["left"] == SLIDE_WIDTH - 1.0 - 0.5
        assert pos["top"] == 0.5

    def test_get_logo_position_center_left(self):
        """Test logo position at center-left."""
        pos = get_logo_position("center-left", size=1.0, margin=0.5)

        assert pos["left"] == 0.5
        # Should be centered vertically
        assert pos["top"] == (SLIDE_HEIGHT - 1.0) / 2

    def test_get_logo_position_center(self):
        """Test logo position at center."""
        pos = get_logo_position("center", size=1.0)

        # Should be centered both horizontally and vertically
        assert pos["left"] == (SLIDE_WIDTH - 1.0) / 2
        assert pos["top"] == (SLIDE_HEIGHT - 1.0) / 2

    def test_get_logo_position_center_right(self):
        """Test logo position at center-right."""
        pos = get_logo_position("center-right", size=1.0, margin=0.5)

        assert pos["left"] == SLIDE_WIDTH - 1.0 - 0.5
        assert pos["top"] == (SLIDE_HEIGHT - 1.0) / 2

    def test_get_logo_position_bottom_left(self):
        """Test logo position at bottom-left."""
        pos = get_logo_position("bottom-left", size=1.0, margin=0.5)

        assert pos["left"] == 0.5
        assert pos["top"] == SLIDE_HEIGHT - 1.0 - 0.5

    def test_get_logo_position_bottom_center(self):
        """Test logo position at bottom-center."""
        pos = get_logo_position("bottom-center", size=1.0, margin=0.5)

        assert pos["left"] == (SLIDE_WIDTH - 1.0) / 2
        assert pos["top"] == SLIDE_HEIGHT - 1.0 - 0.5

    def test_get_logo_position_bottom_right(self):
        """Test logo position at bottom-right."""
        pos = get_logo_position("bottom-right", size=1.0, margin=0.5)

        assert pos["left"] == SLIDE_WIDTH - 1.0 - 0.5
        assert pos["top"] == SLIDE_HEIGHT - 1.0 - 0.5

    def test_get_logo_position_invalid_defaults_to_top_right(self):
        """Test that invalid position defaults to top-right."""
        pos = get_logo_position("invalid-position", size=1.0, margin=0.5)

        # Should default to top-right
        assert pos["left"] == SLIDE_WIDTH - 1.0 - 0.5
        assert pos["top"] == 0.5

    def test_get_logo_position_custom_size(self):
        """Test logo with custom size."""
        pos = get_logo_position("top-left", size=2.0, margin=0.5)

        assert pos["width"] == 2.0
        assert pos["height"] == 2.0

    def test_get_logo_position_custom_margin(self):
        """Test logo with custom margin."""
        pos = get_logo_position("top-left", size=1.0, margin=1.0)

        assert pos["left"] == 1.0
        assert pos["top"] == 1.0

    def test_get_logo_position_4_3_aspect_ratio(self):
        """Test logo positioning with 4:3 aspect ratio."""
        pos = get_logo_position("center", size=1.0, aspect_ratio="4:3")

        # Should work with 4:3 dimensions
        assert pos["left"] == (SLIDE_WIDTH - 1.0) / 2
        assert pos["top"] <= SLIDE_HEIGHT_4_3


class TestGetSafeContentArea:
    """Test get_safe_content_area function."""

    def test_get_safe_content_area_with_title(self):
        """Test safe area with title."""
        area = get_safe_content_area(has_title=True)

        assert "left" in area
        assert "top" in area
        assert "width" in area
        assert "height" in area

        # With title, top margin should be larger
        assert area["top"] > 0.5

    def test_get_safe_content_area_without_title(self):
        """Test safe area without title."""
        area = get_safe_content_area(has_title=False)

        # Without title, top margin should be smaller
        assert area["top"] == 0.5

    def test_get_safe_content_area_16_9_aspect_ratio(self):
        """Test safe area with 16:9 aspect ratio."""
        area = get_safe_content_area(has_title=True, aspect_ratio="16:9")

        # Should use 16:9 slide height
        assert area["top"] + area["height"] <= SLIDE_HEIGHT

    def test_get_safe_content_area_4_3_aspect_ratio(self):
        """Test safe area with 4:3 aspect ratio."""
        area = get_safe_content_area(has_title=True, aspect_ratio="4:3")

        # Should use 4:3 slide height
        assert area["top"] + area["height"] <= SLIDE_HEIGHT_4_3

    def test_get_safe_content_area_dimensions_positive(self):
        """Test that safe area has positive dimensions."""
        area = get_safe_content_area(has_title=True)

        assert area["width"] > 0
        assert area["height"] > 0

    def test_get_safe_content_area_within_slide_bounds(self):
        """Test that safe area is within slide bounds."""
        area = get_safe_content_area(has_title=True)

        assert area["left"] >= 0
        assert area["top"] >= 0
        assert area["left"] + area["width"] <= SLIDE_WIDTH
        assert area["top"] + area["height"] <= SLIDE_HEIGHT
