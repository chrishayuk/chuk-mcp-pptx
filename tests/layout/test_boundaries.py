"""
Tests for boundary validation and adjustment utilities.
"""

from chuk_mcp_pptx.layout import (
    validate_boundaries,
    adjust_to_boundaries,
    validate_position,
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
)


class TestValidateBoundaries:
    """Test boundary validation for elements."""

    def test_valid_boundaries(self):
        """Test valid element within slide boundaries."""
        is_valid, error = validate_boundaries(1.0, 1.0, 5.0, 3.0)
        assert is_valid is True
        assert error is None

    def test_exceeds_width(self):
        """Test element exceeding slide width."""
        is_valid, error = validate_boundaries(8.0, 1.0, 5.0, 3.0)
        assert is_valid is False
        assert "width" in error.lower()

    def test_exceeds_height(self):
        """Test element exceeding slide height."""
        is_valid, error = validate_boundaries(1.0, 5.0, 3.0, 3.0)
        assert is_valid is False
        assert "height" in error.lower()

    def test_negative_position(self):
        """Test negative position."""
        is_valid, error = validate_boundaries(-1.0, 1.0, 3.0, 2.0)
        assert is_valid is False
        assert "negative" in error.lower()

    def test_zero_dimensions(self):
        """Test zero or negative dimensions."""
        is_valid, error = validate_boundaries(1.0, 1.0, 0, 2.0)
        assert is_valid is False
        assert "positive" in error.lower()

    def test_exactly_at_boundary(self):
        """Test element exactly at slide boundary (should be valid)."""
        is_valid, error = validate_boundaries(0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
        assert is_valid is True
        assert error is None


class TestAdjustToBoundaries:
    """Test automatic boundary adjustment."""

    def test_no_adjustment_needed(self):
        """Test element that doesn't need adjustment."""
        left, top, width, height = adjust_to_boundaries(1.0, 1.0, 5.0, 3.0)
        assert left == 1.0
        assert top == 1.0
        assert width == 5.0
        assert height == 3.0

    def test_adjust_left_position(self):
        """Test adjusting left position when exceeding width."""
        left, top, width, height = adjust_to_boundaries(8.0, 1.0, 5.0, 3.0)
        # Should adjust left to fit
        assert left + width <= SLIDE_WIDTH
        assert width == 5.0  # Width preserved if possible

    def test_adjust_top_position(self):
        """Test adjusting top position when exceeding height."""
        left, top, width, height = adjust_to_boundaries(1.0, 5.0, 3.0, 3.0)
        # Should adjust top to fit
        assert top + height <= SLIDE_HEIGHT
        assert height == 3.0  # Height preserved if possible

    def test_shrink_oversized_width(self):
        """Test shrinking element that's too wide."""
        left, top, width, height = adjust_to_boundaries(1.0, 1.0, 15.0, 3.0)
        # Should shrink width to fit
        assert left + width <= SLIDE_WIDTH
        assert width < 15.0

    def test_shrink_oversized_height(self):
        """Test shrinking element that's too tall."""
        left, top, width, height = adjust_to_boundaries(1.0, 1.0, 5.0, 10.0)
        # Should shrink height to fit
        assert top + height <= SLIDE_HEIGHT
        assert height < 10.0

    def test_negative_position_adjusted(self):
        """Test negative positions are adjusted to margins."""
        left, top, width, height = adjust_to_boundaries(-1.0, -1.0, 3.0, 2.0)
        assert left >= 0
        assert top >= 0


class TestValidatePosition:
    """Test comprehensive position validation and adjustment."""

    def test_valid_position(self):
        """Test valid position within safe area."""
        left, top, width, height = validate_position(1.0, 2.0, 6.0, 3.0)
        # Should fit within slide
        assert left + width <= SLIDE_WIDTH
        assert top + height <= SLIDE_HEIGHT

    def test_preserve_dimensions_when_possible(self):
        """Test that dimensions are preserved when element fits."""
        original_width = 5.0
        original_height = 3.0
        left, top, width, height = validate_position(1.0, 1.5, original_width, original_height)

        assert width == original_width
        assert height == original_height

    def test_adjust_position_to_fit(self):
        """Test adjusting position when element goes off slide."""
        # Position that would go off right edge
        left, top, width, height = validate_position(8.0, 1.0, 4.0, 3.0)

        # Should adjust left position but keep width
        assert left + width <= SLIDE_WIDTH
        assert width == 4.0

    def test_both_position_and_size_adjustment(self):
        """Test case where both position and size need adjustment."""
        # Oversized element at bad position
        left, top, width, height = validate_position(8.0, 5.0, 8.0, 6.0)

        # Should fit within slide
        assert left + width <= SLIDE_WIDTH
        assert top + height <= SLIDE_HEIGHT
        assert left >= 0
        assert top >= 0


class TestIntegrationWithCharts:
    """Test boundary utilities in chart context."""

    def test_default_chart_dimensions(self):
        """Test that default chart dimensions are valid."""
        # Default chart size from ChartComponent (adjusted for actual slide height)
        is_valid, error = validate_boundaries(1.0, 1.0, 8.0, 4.0)
        assert is_valid is True

    def test_full_width_chart(self):
        """Test full-width chart with margins."""
        # Full width chart respecting margins
        left, top, width, height = validate_position(0.5, 1.5, 9.0, 4.0)

        assert left + width <= SLIDE_WIDTH
        assert top + height <= SLIDE_HEIGHT

    def test_chart_grid_layout(self):
        """Test multiple charts in grid layout."""
        # Simulate 2x2 grid of small charts (adjusted for actual slide height)
        chart_width = 4.0
        chart_height = 2.0  # Reduced to fit in 5.625" height
        spacing = 0.3

        positions = [
            (0.5, 1.0),  # Top left
            (0.5 + chart_width + spacing, 1.0),  # Top right
            (0.5, 1.0 + chart_height + spacing),  # Bottom left
            (0.5 + chart_width + spacing, 1.0 + chart_height + spacing),  # Bottom right
        ]

        for left, top in positions:
            is_valid, error = validate_boundaries(left, top, chart_width, chart_height)
            # All should fit
            assert is_valid is True, f"Chart at ({left}, {top}) doesn't fit: {error}"


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_minimum_dimensions(self):
        """Test very small but valid dimensions."""
        is_valid, error = validate_boundaries(1.0, 1.0, 0.1, 0.1)
        assert is_valid is True

    def test_floating_point_precision(self):
        """Test floating point edge cases."""
        # Exactly at boundary with floating point
        is_valid, error = validate_boundaries(
            0.0, 0.0, SLIDE_WIDTH - 0.0000001, SLIDE_HEIGHT - 0.0000001
        )
        assert is_valid is True

    def test_aspect_ratio_4_3(self):
        """Test with 4:3 aspect ratio."""
        is_valid, error = validate_boundaries(1.0, 1.0, 5.0, 4.0, aspect_ratio="4:3")
        assert is_valid is True

    def test_centered_element(self):
        """Test centering an element."""
        width = 4.0
        height = 3.0
        left = (SLIDE_WIDTH - width) / 2
        top = (SLIDE_HEIGHT - height) / 2

        is_valid, error = validate_boundaries(left, top, width, height)
        assert is_valid is True


class TestOverlapDetection:
    """Test check_overlap function."""

    def test_elements_do_not_overlap(self):
        """Test elements that don't overlap."""
        from chuk_mcp_pptx.layout.boundaries import check_overlap

        # Elements side by side
        overlap = check_overlap(
            left1=1.0,
            top1=2.0,
            width1=2.0,
            height1=1.0,
            left2=3.5,
            top2=2.0,
            width2=2.0,
            height2=1.0,
        )
        assert overlap is False

    def test_elements_overlap(self):
        """Test elements that do overlap."""
        from chuk_mcp_pptx.layout.boundaries import check_overlap

        # Elements overlap
        overlap = check_overlap(
            left1=1.0,
            top1=2.0,
            width1=3.0,
            height1=2.0,
            left2=2.0,
            top2=2.5,
            width2=2.0,
            height2=1.5,
        )
        assert overlap is True

    def test_elements_touching_edge_to_edge(self):
        """Test elements that are exactly touching edge to edge."""
        from chuk_mcp_pptx.layout.boundaries import check_overlap

        # Elements exactly touching (edge to edge)
        overlap = check_overlap(
            left1=1.0,
            top1=2.0,
            width1=2.0,
            height1=1.0,
            left2=3.0,
            top2=2.0,
            width2=2.0,
            height2=1.0,
        )
        # Note: Edge-to-edge touching is considered overlap (>=, not >)
        assert overlap is True

    def test_one_element_inside_another(self):
        """Test when one element is completely inside another."""
        from chuk_mcp_pptx.layout.boundaries import check_overlap

        # Small element inside larger one
        overlap = check_overlap(
            left1=1.0,
            top1=1.0,
            width1=5.0,
            height1=4.0,  # Large
            left2=2.0,
            top2=2.0,
            width2=1.0,
            height2=1.0,  # Small inside
        )
        assert overlap is True


class TestAvailableSpace:
    """Test get_available_space function."""

    def test_available_space_from_origin(self):
        """Test available space from top-left (accounts for margins)."""
        from chuk_mcp_pptx.layout.boundaries import (
            get_available_space,
            SLIDE_WIDTH,
            SLIDE_HEIGHT,
            MARGIN_RIGHT,
            MARGIN_BOTTOM,
        )

        width_avail, height_avail = get_available_space(left=0, top=0)

        # Function subtracts right and bottom margins
        assert width_avail == SLIDE_WIDTH - MARGIN_RIGHT
        assert height_avail == SLIDE_HEIGHT - MARGIN_BOTTOM

    def test_available_space_from_position(self):
        """Test available space from a specific position."""
        from chuk_mcp_pptx.layout.boundaries import (
            get_available_space,
            SLIDE_WIDTH,
            SLIDE_HEIGHT,
            MARGIN_RIGHT,
            MARGIN_BOTTOM,
        )

        left = 2.0
        top = 1.5

        width_avail, height_avail = get_available_space(left=left, top=top)

        # Available = slide_dimension - position - margin
        assert abs(width_avail - (SLIDE_WIDTH - left - MARGIN_RIGHT)) < 0.01
        assert abs(height_avail - (SLIDE_HEIGHT - top - MARGIN_BOTTOM)) < 0.01

    def test_available_space_near_edge(self):
        """Test available space when close to edge."""
        from chuk_mcp_pptx.layout.boundaries import get_available_space

        # Very close to right/bottom edges
        width_avail, height_avail = get_available_space(left=9.0, top=5.0)

        # Should be small but positive
        assert width_avail >= 0
        assert height_avail >= 0

    def test_available_space_4_3_aspect_ratio(self):
        """Test available space with 4:3 aspect ratio."""
        from chuk_mcp_pptx.layout.boundaries import (
            get_available_space,
            SLIDE_WIDTH_4_3,
            SLIDE_HEIGHT_4_3,
            MARGIN_RIGHT,
            MARGIN_BOTTOM,
        )

        width_avail, height_avail = get_available_space(left=0, top=0, aspect_ratio="4:3")

        assert width_avail == SLIDE_WIDTH_4_3 - MARGIN_RIGHT
        assert height_avail == SLIDE_HEIGHT_4_3 - MARGIN_BOTTOM
