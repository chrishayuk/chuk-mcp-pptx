"""
Tests for layout pattern functions.

Tests for dashboard, comparison, hero, and gallery layout patterns.
"""


class TestCalculateCellPosition:
    """Tests for the _calculate_cell_position helper function."""

    def test_basic_calculation(self) -> None:
        """Test basic cell position calculation."""
        from chuk_mcp_pptx.layout.patterns import _calculate_cell_position

        pos = _calculate_cell_position(
            col_span=1,
            col_start=0,
            row_start=0,
            col_width=1.0,
            row_height=1.0,
            gap_value=0.1,
            left=0.5,
            top=1.0,
        )

        assert "left" in pos
        assert "top" in pos
        assert "width" in pos
        assert pos["left"] == 0.5
        assert pos["top"] == 1.0
        assert pos["width"] == 1.0

    def test_with_col_offset(self) -> None:
        """Test cell position with column offset."""
        from chuk_mcp_pptx.layout.patterns import _calculate_cell_position

        pos = _calculate_cell_position(
            col_span=1,
            col_start=2,
            row_start=0,
            col_width=1.0,
            row_height=1.0,
            gap_value=0.1,
            left=0.5,
            top=1.0,
        )

        # Expected left = 0.5 + (2 * (1.0 + 0.1)) = 0.5 + 2.2 = 2.7
        assert pos["left"] == 2.7

    def test_with_row_offset(self) -> None:
        """Test cell position with row offset."""
        from chuk_mcp_pptx.layout.patterns import _calculate_cell_position

        pos = _calculate_cell_position(
            col_span=1,
            col_start=0,
            row_start=2,
            col_width=1.0,
            row_height=1.0,
            gap_value=0.1,
            left=0.5,
            top=1.0,
        )

        # Expected top = 1.0 + (2 * (1.0 + 0.1)) = 1.0 + 2.2 = 3.2
        assert pos["top"] == 3.2

    def test_with_col_span(self) -> None:
        """Test cell position with column span."""
        from chuk_mcp_pptx.layout.patterns import _calculate_cell_position

        pos = _calculate_cell_position(
            col_span=3,
            col_start=0,
            row_start=0,
            col_width=1.0,
            row_height=1.0,
            gap_value=0.1,
            left=0.5,
            top=1.0,
        )

        # Expected width = (3 * 1.0) + ((3 - 1) * 0.1) = 3.0 + 0.2 = 3.2
        assert pos["width"] == 3.2

    def test_auto_height_true(self) -> None:
        """Test that height is not included when auto_height is True."""
        from chuk_mcp_pptx.layout.patterns import _calculate_cell_position

        pos = _calculate_cell_position(
            col_span=1,
            col_start=0,
            row_start=0,
            col_width=1.0,
            row_height=2.0,
            gap_value=0.1,
            left=0.5,
            top=1.0,
            auto_height=True,
        )

        assert "height" not in pos

    def test_auto_height_false(self) -> None:
        """Test that height is included when auto_height is False."""
        from chuk_mcp_pptx.layout.patterns import _calculate_cell_position

        pos = _calculate_cell_position(
            col_span=1,
            col_start=0,
            row_start=0,
            col_width=1.0,
            row_height=2.0,
            gap_value=0.1,
            left=0.5,
            top=1.0,
            auto_height=False,
        )

        assert "height" in pos
        assert pos["height"] == 2.0


class TestGetDashboardPositions:
    """Tests for the get_dashboard_positions function."""

    def test_default_parameters(self) -> None:
        """Test dashboard positions with default parameters."""
        from chuk_mcp_pptx.layout.patterns import get_dashboard_positions

        positions = get_dashboard_positions()

        assert "metrics" in positions
        assert "main" in positions
        assert "sidebar" in positions
        assert "description" in positions
        assert len(positions["metrics"]) == 3

    def test_metrics_have_height(self) -> None:
        """Test that metric positions include height."""
        from chuk_mcp_pptx.layout.patterns import get_dashboard_positions

        positions = get_dashboard_positions()

        for metric in positions["metrics"]:
            assert "left" in metric
            assert "top" in metric
            assert "width" in metric
            assert "height" in metric

    def test_main_has_height(self) -> None:
        """Test that main position includes height."""
        from chuk_mcp_pptx.layout.patterns import get_dashboard_positions

        positions = get_dashboard_positions()

        assert "height" in positions["main"]

    def test_sidebar_has_height(self) -> None:
        """Test that sidebar position includes height."""
        from chuk_mcp_pptx.layout.patterns import get_dashboard_positions

        positions = get_dashboard_positions()

        assert "height" in positions["sidebar"]

    def test_custom_gap(self) -> None:
        """Test dashboard positions with custom gap."""
        from chuk_mcp_pptx.layout.patterns import get_dashboard_positions

        positions_sm = get_dashboard_positions(gap="sm")
        positions_lg = get_dashboard_positions(gap="lg")

        # With larger gap, positions should be different
        assert (
            positions_sm["metrics"][0]["left"] != positions_lg["metrics"][0]["left"]
            or positions_sm["metrics"][0]["width"] != positions_lg["metrics"][0]["width"]
        )

    def test_custom_dimensions(self) -> None:
        """Test dashboard positions with custom dimensions."""
        from chuk_mcp_pptx.layout.patterns import get_dashboard_positions

        positions = get_dashboard_positions(left=1.0, top=2.0, width=8.0, height=5.0)

        assert positions["metrics"][0]["left"] >= 1.0
        assert positions["metrics"][0]["top"] >= 2.0


class TestGetComparisonPositions:
    """Tests for the get_comparison_positions function."""

    def test_default_parameters(self) -> None:
        """Test comparison positions with default parameters."""
        from chuk_mcp_pptx.layout.patterns import get_comparison_positions

        positions = get_comparison_positions()

        assert "left" in positions
        assert "right" in positions
        assert "description" in positions
        assert "header" not in positions  # No header by default

    def test_without_header(self) -> None:
        """Test comparison layout without header."""
        from chuk_mcp_pptx.layout.patterns import get_comparison_positions

        positions = get_comparison_positions(include_header=False)

        assert "header" not in positions
        assert "left" in positions
        assert "right" in positions

    def test_with_header(self) -> None:
        """Test comparison layout with header."""
        from chuk_mcp_pptx.layout.patterns import get_comparison_positions

        positions = get_comparison_positions(include_header=True)

        assert "header" in positions
        assert "left" in positions
        assert "right" in positions
        assert "height" in positions["header"]
        assert "height" in positions["left"]
        assert "height" in positions["right"]

    def test_left_right_same_width(self) -> None:
        """Test that left and right columns have same width."""
        from chuk_mcp_pptx.layout.patterns import get_comparison_positions

        positions = get_comparison_positions()

        assert positions["left"]["width"] == positions["right"]["width"]

    def test_custom_gap(self) -> None:
        """Test comparison positions with custom gap."""
        from chuk_mcp_pptx.layout.patterns import get_comparison_positions

        positions_sm = get_comparison_positions(gap="sm")
        positions_lg = get_comparison_positions(gap="lg")

        # Widths should be different with different gaps
        assert positions_sm["left"]["width"] != positions_lg["left"]["width"]

    def test_custom_dimensions(self) -> None:
        """Test comparison positions with custom dimensions."""
        from chuk_mcp_pptx.layout.patterns import get_comparison_positions

        positions = get_comparison_positions(left=1.0, top=2.0, width=8.0, height=5.0)

        assert positions["left"]["left"] >= 1.0
        assert positions["left"]["top"] >= 2.0


class TestGetHeroPositions:
    """Tests for the get_hero_positions function."""

    def test_default_parameters(self) -> None:
        """Test hero positions with default parameters."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions = get_hero_positions()

        assert "hero_image" in positions
        assert "title" in positions
        assert "subtitle" in positions
        assert "body" in positions
        assert "description" in positions

    def test_image_left(self) -> None:
        """Test hero layout with image on left."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions = get_hero_positions(image_side="left")

        # Image should be on the left (smaller left value)
        assert positions["hero_image"]["left"] < positions["title"]["left"]
        assert "left" in positions["description"]

    def test_image_right(self) -> None:
        """Test hero layout with image on right."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions = get_hero_positions(image_side="right")

        # Image should be on the right (larger left value)
        assert positions["hero_image"]["left"] > positions["title"]["left"]
        assert "right" in positions["description"]

    def test_hero_image_has_height(self) -> None:
        """Test that hero image includes height."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions = get_hero_positions()

        assert "height" in positions["hero_image"]

    def test_text_areas_no_height(self) -> None:
        """Test that text areas don't include height (auto-height)."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions = get_hero_positions()

        # Text areas use auto-height by default
        assert "height" not in positions["title"]
        assert "height" not in positions["subtitle"]
        assert "height" not in positions["body"]

    def test_custom_gap(self) -> None:
        """Test hero positions with custom gap."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions_sm = get_hero_positions(gap="sm")
        positions_lg = get_hero_positions(gap="lg")

        # Widths should be different with different gaps
        assert positions_sm["hero_image"]["width"] != positions_lg["hero_image"]["width"]

    def test_custom_dimensions(self) -> None:
        """Test hero positions with custom dimensions."""
        from chuk_mcp_pptx.layout.patterns import get_hero_positions

        positions = get_hero_positions(left=1.0, top=2.0, width=8.0, height=5.0)

        assert positions["hero_image"]["left"] >= 1.0
        assert positions["hero_image"]["top"] >= 2.0


class TestGetGalleryPositions:
    """Tests for the get_gallery_positions function."""

    def test_default_parameters(self) -> None:
        """Test gallery positions with default parameters (2x2)."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions()

        assert "items" in positions
        assert "pattern" in positions
        assert "count" in positions
        assert "description" in positions
        assert positions["pattern"] == "2x2"
        assert positions["count"] == 4
        assert len(positions["items"]) == 4

    def test_2x2_layout(self) -> None:
        """Test 2x2 gallery layout."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(layout_style="2x2")

        assert positions["count"] == 4
        assert len(positions["items"]) == 4

    def test_3x2_layout(self) -> None:
        """Test 3x2 gallery layout."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(layout_style="3x2")

        assert positions["count"] == 6
        assert len(positions["items"]) == 6

    def test_3x3_layout(self) -> None:
        """Test 3x3 gallery layout."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(layout_style="3x3")

        assert positions["count"] == 9
        assert len(positions["items"]) == 9

    def test_4x2_layout(self) -> None:
        """Test 4x2 gallery layout."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(layout_style="4x2")

        assert positions["count"] == 8
        assert len(positions["items"]) == 8

    def test_invalid_layout_style(self) -> None:
        """Test gallery with invalid layout style."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(layout_style="invalid")

        assert "error" in positions

    def test_items_have_all_dimensions(self) -> None:
        """Test that gallery items include all dimensions."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions()

        for item in positions["items"]:
            assert "left" in item
            assert "top" in item
            assert "width" in item
            assert "height" in item

    def test_items_equal_size(self) -> None:
        """Test that all gallery items have equal size."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(layout_style="2x2")

        widths = [item["width"] for item in positions["items"]]
        heights = [item["height"] for item in positions["items"]]

        # All items should have same width and height
        assert len(set(widths)) == 1
        assert len(set(heights)) == 1

    def test_custom_gap(self) -> None:
        """Test gallery positions with custom gap."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions_sm = get_gallery_positions(gap="sm")
        positions_lg = get_gallery_positions(gap="lg")

        # Widths should be different with different gaps
        assert positions_sm["items"][0]["width"] != positions_lg["items"][0]["width"]

    def test_custom_dimensions(self) -> None:
        """Test gallery positions with custom dimensions."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        positions = get_gallery_positions(left=1.0, top=2.0, width=8.0, height=5.0)

        assert positions["items"][0]["left"] >= 1.0
        assert positions["items"][0]["top"] >= 2.0

    def test_description_includes_pattern(self) -> None:
        """Test that description includes the pattern."""
        from chuk_mcp_pptx.layout.patterns import get_gallery_positions

        for pattern in ["2x2", "3x2", "3x3", "4x2"]:
            positions = get_gallery_positions(layout_style=pattern)
            assert pattern in positions["description"]
