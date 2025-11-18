"""
Comprehensive tests for the token system.
"""

import pytest
from chuk_mcp_pptx.tokens import (
    PALETTE,
    get_semantic_tokens,
    GRADIENTS,
    FONT_FAMILIES,
    FONT_SIZES,
    FONT_WEIGHTS,
    LINE_HEIGHTS,
    LETTER_SPACING,
    get_text_style,
    TYPOGRAPHY_SCALE,
    SPACING,
    MARGINS,
    PADDING,
    GAPS,
    RADIUS,
    BORDER_WIDTH,
    SHADOWS,
    GRID,
    CONTAINERS,
    ASPECT_RATIOS,
    get_layout_spacing,
    get_all_tokens,
    export_tokens_json,
)


class TestColorTokens:
    """Test color token system."""

    def test_palette_has_all_colors(self):
        """Test that palette includes all expected color families."""
        expected_colors = [
            "slate",
            "zinc",
            "red",
            "orange",
            "amber",
            "yellow",
            "lime",
            "green",
            "emerald",
            "teal",
            "cyan",
            "sky",
            "blue",
            "indigo",
            "violet",
            "purple",
            "fuchsia",
            "pink",
            "rose",
        ]

        for color in expected_colors:
            assert color in PALETTE, f"Missing color: {color}"

    def test_palette_color_scales(self):
        """Test that each color has proper scale values."""
        expected_shades = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

        for color_name, color_scale in PALETTE.items():
            for shade in expected_shades:
                assert shade in color_scale, f"{color_name} missing shade {shade}"
                assert isinstance(color_scale[shade], str)
                assert color_scale[shade].startswith("#")

    def test_semantic_tokens_dark_mode(self):
        """Test semantic token generation for dark mode."""
        tokens = get_semantic_tokens("blue", "dark")

        # Check required keys
        assert "background" in tokens
        assert "foreground" in tokens
        assert "primary" in tokens
        assert "secondary" in tokens
        assert "accent" in tokens
        assert "chart" in tokens

        # Check nested structure
        assert "DEFAULT" in tokens["background"]
        assert "DEFAULT" in tokens["primary"]
        assert "foreground" in tokens["primary"]

    def test_semantic_tokens_light_mode(self):
        """Test semantic token generation for light mode."""
        tokens = get_semantic_tokens("violet", "light")

        # Should have same structure as dark mode
        assert "background" in tokens
        assert "foreground" in tokens

        # Light mode should have lighter background
        bg = tokens["background"]["DEFAULT"]
        assert bg == "#ffffff"

    def test_semantic_tokens_different_hues(self):
        """Test that different hues produce different primary colors."""
        blue_tokens = get_semantic_tokens("blue", "dark")
        green_tokens = get_semantic_tokens("emerald", "dark")

        assert blue_tokens["primary"]["DEFAULT"] != green_tokens["primary"]["DEFAULT"]

    def test_gradients_exist(self):
        """Test that gradient definitions exist."""
        expected_gradients = [
            "sunset",
            "ocean",
            "forest",
            "flame",
            "aurora",
            "cosmic",
            "mint",
            "lavender",
        ]

        for grad in expected_gradients:
            assert grad in GRADIENTS
            assert isinstance(GRADIENTS[grad], list)
            assert len(GRADIENTS[grad]) >= 3


class TestTypographyTokens:
    """Test typography token system."""

    def test_font_families(self):
        """Test font family definitions."""
        assert "sans" in FONT_FAMILIES
        assert "serif" in FONT_FAMILIES
        assert "mono" in FONT_FAMILIES
        assert "display" in FONT_FAMILIES

        # Each should be a list
        for family_list in FONT_FAMILIES.values():
            assert isinstance(family_list, list)
            assert len(family_list) > 0

    def test_font_sizes(self):
        """Test font size scale."""
        expected_sizes = [
            "xs",
            "sm",
            "base",
            "lg",
            "xl",
            "2xl",
            "3xl",
            "4xl",
            "5xl",
            "6xl",
            "7xl",
            "8xl",
            "9xl",
        ]

        for size in expected_sizes:
            assert size in FONT_SIZES
            assert isinstance(FONT_SIZES[size], (int, float))
            assert FONT_SIZES[size] > 0

        # Sizes should increase
        assert FONT_SIZES["xs"] < FONT_SIZES["sm"] < FONT_SIZES["base"] < FONT_SIZES["xl"]

    def test_font_weights(self):
        """Test font weight definitions."""
        expected_weights = [
            "thin",
            "extralight",
            "light",
            "normal",
            "medium",
            "semibold",
            "bold",
            "extrabold",
            "black",
        ]

        for weight in expected_weights:
            assert weight in FONT_WEIGHTS
            assert 100 <= FONT_WEIGHTS[weight] <= 900

        # Weights should increase
        assert FONT_WEIGHTS["thin"] < FONT_WEIGHTS["normal"] < FONT_WEIGHTS["bold"]

    def test_line_heights(self):
        """Test line height definitions."""
        assert "none" in LINE_HEIGHTS
        assert "tight" in LINE_HEIGHTS
        assert "normal" in LINE_HEIGHTS
        assert "relaxed" in LINE_HEIGHTS

        # All should be positive multipliers
        for lh in LINE_HEIGHTS.values():
            assert lh > 0

    def test_letter_spacing(self):
        """Test letter spacing definitions."""
        assert "normal" in LETTER_SPACING
        assert "tight" in LETTER_SPACING
        assert "wide" in LETTER_SPACING

        assert LETTER_SPACING["normal"] == 0

    def test_get_text_style(self):
        """Test text style getter."""
        # Test heading styles
        h1 = get_text_style("h1")
        assert "font_family" in h1
        assert "font_size" in h1
        assert "font_weight" in h1
        assert "line_height" in h1

        # Test body style
        body = get_text_style("body")
        assert body["font_size"] < h1["font_size"]

        # Test code style
        code = get_text_style("code")
        assert code["font_family"] == FONT_FAMILIES["mono"][0]

    def test_typography_scale(self):
        """Test typography scale definitions."""
        assert "display" in TYPOGRAPHY_SCALE
        assert "heading" in TYPOGRAPHY_SCALE

        for scale_type in TYPOGRAPHY_SCALE.values():
            assert "2xl" in scale_type
            assert "xl" in scale_type
            assert "lg" in scale_type


class TestSpacingTokens:
    """Test spacing token system."""

    def test_spacing_scale(self):
        """Test spacing scale values."""
        assert "0" in SPACING
        assert "4" in SPACING
        assert "8" in SPACING
        assert "16" in SPACING

        # All values should be non-negative
        for value in SPACING.values():
            assert value >= 0

        # Values should generally increase
        assert SPACING["0"] < SPACING["4"] < SPACING["8"]

    def test_margins(self):
        """Test margin presets."""
        expected_margins = ["none", "xs", "sm", "md", "lg", "xl", "2xl", "3xl"]

        for margin in expected_margins:
            assert margin in MARGINS
            assert MARGINS[margin] >= 0

        # Should increase in size
        assert MARGINS["xs"] < MARGINS["md"] < MARGINS["xl"]

    def test_padding(self):
        """Test padding presets."""
        expected_padding = ["none", "xs", "sm", "md", "lg", "xl", "2xl", "3xl"]

        for pad in expected_padding:
            assert pad in PADDING
            assert PADDING[pad] >= 0

    def test_gaps(self):
        """Test gap presets."""
        assert "none" in GAPS
        assert "md" in GAPS
        assert GAPS["none"] == 0

    def test_radius(self):
        """Test border radius values."""
        assert "none" in RADIUS
        assert "sm" in RADIUS
        assert "md" in RADIUS
        assert "lg" in RADIUS
        assert "full" in RADIUS

        assert RADIUS["none"] == 0
        assert RADIUS["full"] > RADIUS["lg"]

    def test_border_width(self):
        """Test border width values."""
        assert "0" in BORDER_WIDTH
        assert "1" in BORDER_WIDTH
        assert "2" in BORDER_WIDTH

        assert BORDER_WIDTH["0"] == 0

    def test_shadows(self):
        """Test shadow definitions."""
        assert "none" in SHADOWS
        assert "sm" in SHADOWS
        assert "md" in SHADOWS
        assert "lg" in SHADOWS

        # None should be None
        assert SHADOWS["none"] is None

        # Others should have required properties
        for key, shadow in SHADOWS.items():
            if shadow is not None:
                assert "offset_x" in shadow or key == "none"
                assert "blur" in shadow or key == "none"

    def test_grid_system(self):
        """Test grid system configuration."""
        assert "cols" in GRID
        assert "gutter" in GRID
        assert "margin" in GRID

        assert GRID["cols"] == 12

    def test_containers(self):
        """Test container width definitions."""
        assert "sm" in CONTAINERS
        assert "md" in CONTAINERS
        assert "lg" in CONTAINERS
        assert "full" in CONTAINERS

        # Should increase in size
        assert CONTAINERS["sm"] < CONTAINERS["md"] < CONTAINERS["lg"]

    def test_aspect_ratios(self):
        """Test aspect ratio definitions."""
        assert "square" in ASPECT_RATIOS
        assert "video" in ASPECT_RATIOS
        assert "photo" in ASPECT_RATIOS

        assert ASPECT_RATIOS["square"] == "1:1"
        assert ASPECT_RATIOS["video"] == "16:9"

    def test_get_layout_spacing(self):
        """Test layout spacing getter."""
        compact = get_layout_spacing("compact")
        assert "margin" in compact
        assert "padding" in compact
        assert "gap" in compact

        get_layout_spacing("default")
        comfortable = get_layout_spacing("comfortable")

        # Comfortable should have larger values than compact
        assert comfortable["padding"] > compact["padding"]


class TestTokenUtilities:
    """Test token utility functions."""

    def test_get_all_tokens(self):
        """Test getting all tokens at once."""
        tokens = get_all_tokens("blue", "dark")

        assert "colors" in tokens
        assert "typography" in tokens
        assert "spacing" in tokens
        assert "borders" in tokens
        assert "shadows" in tokens
        assert "layout" in tokens

        # Check nested structure
        assert "palette" in tokens["colors"]
        assert "semantic" in tokens["colors"]
        assert "families" in tokens["typography"]
        assert "scale" in tokens["spacing"]

    def test_export_tokens_json(self):
        """Test JSON export."""
        json_str = export_tokens_json("violet", "light")

        assert isinstance(json_str, str)
        assert len(json_str) > 0

        # Should be valid JSON
        import json

        data = json.loads(json_str)
        assert "colors" in data
        assert "typography" in data

    def test_token_consistency(self):
        """Test that tokens are internally consistent."""
        # Padding values should come from spacing scale
        for pad_value in PADDING.values():
            assert pad_value in SPACING.values() or pad_value == 0

        # Margins should come from spacing scale
        for margin_value in MARGINS.values():
            assert margin_value in SPACING.values() or margin_value == 0


class TestTokenIntegration:
    """Test token integration and real-world usage."""

    def test_theme_compatible_tokens(self):
        """Test that tokens work with theme system."""
        tokens = get_semantic_tokens("emerald", "dark")

        # Should be able to get color paths
        assert tokens["background"]["DEFAULT"]
        assert tokens["primary"]["DEFAULT"]
        assert tokens["primary"]["foreground"]

    def test_component_compatible_tokens(self):
        """Test that tokens work for component props."""
        # A component should be able to use these values
        text_style = get_text_style("h1")
        assert text_style["font_size"] in FONT_SIZES.values()

        spacing = get_layout_spacing("default")
        assert spacing["padding"] in PADDING.values()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
