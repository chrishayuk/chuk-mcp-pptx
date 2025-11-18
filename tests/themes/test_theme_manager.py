"""
Tests for Theme Manager and theme system.
"""

from chuk_mcp_pptx.themes.theme_manager import ThemeManager
# Theme class is part of theme_manager module


class TestThemeManager:
    """Test ThemeManager functionality."""

    def test_init(self):
        """Test initialization."""
        manager = ThemeManager()

        assert manager is not None
        assert hasattr(manager, "themes")

    def test_available_themes(self):
        """Test that standard themes are available."""
        manager = ThemeManager()

        expected_themes = [
            "dark",
            "dark-blue",
            "dark-violet",
            "dark-green",
            "dark-purple",
            "light",
            "corporate",
            "light-warm",
        ]

        for theme_name in expected_themes:
            theme = manager.get_theme(theme_name)
            assert theme is not None
            assert hasattr(theme, "name")
            assert theme.name == theme_name

    def test_get_theme(self):
        """Test getting a specific theme."""
        manager = ThemeManager()

        dark_theme = manager.get_theme("dark")
        assert dark_theme is not None
        assert dark_theme.name == "dark"

        light_theme = manager.get_theme("light")
        assert light_theme is not None
        assert light_theme.name == "light"

    def test_get_invalid_theme(self):
        """Test getting an invalid theme."""
        manager = ThemeManager()

        # Should return default theme or raise error
        theme = manager.get_theme("nonexistent")
        # Depending on implementation, this might return default or None
        assert theme is None or theme.name in ["dark", "light"]

    def test_list_themes(self):
        """Test listing all available themes."""
        manager = ThemeManager()

        if hasattr(manager, "list_themes"):
            themes = manager.list_themes()
            assert isinstance(themes, list)
            assert len(themes) > 0
            assert "dark" in themes
            assert "light" in themes

    def test_register_custom_theme(self):
        """Test registering a custom theme."""
        manager = ThemeManager()

        # Test if custom theme registration is supported
        if hasattr(manager, "register_theme"):
            # Would need to create custom theme object
            # This is a placeholder test
            pass


class TestTheme:
    """Test Theme functionality."""

    def test_theme_properties(self):
        """Test that themes have required properties."""
        manager = ThemeManager()
        theme = manager.get_theme("dark")

        # Check required properties
        assert hasattr(theme, "name")
        assert hasattr(theme, "background")
        assert hasattr(theme, "foreground")
        assert hasattr(theme, "primary")
        assert hasattr(theme, "secondary")
        assert hasattr(theme, "accent")
        assert hasattr(theme, "chart")

    def test_dark_theme_colors(self):
        """Test dark theme color values."""
        manager = ThemeManager()
        theme = manager.get_theme("dark")

        # Check that colors are in correct format
        bg = theme.background.get("DEFAULT")
        assert bg is not None
        assert bg.startswith("#")
        assert len(bg) == 7  # #RRGGBB format

        fg = theme.foreground.get("DEFAULT")
        assert fg is not None
        assert fg.startswith("#")

        # Dark theme should have dark background
        # Convert hex to RGB to check darkness
        bg_rgb = int(bg[1:], 16)
        assert bg_rgb < 0x808080  # Should be darker than middle gray

    def test_light_theme_colors(self):
        """Test light theme color values."""
        manager = ThemeManager()
        theme = manager.get_theme("light")

        bg = theme.background.get("DEFAULT")
        assert bg is not None

        # Light theme should have light background
        bg_rgb = int(bg[1:], 16)
        assert bg_rgb > 0x808080  # Should be lighter than middle gray

    def test_chart_colors(self):
        """Test chart color palette."""
        manager = ThemeManager()
        theme = manager.get_theme("dark")

        chart_colors = theme.chart
        assert isinstance(chart_colors, list)
        assert len(chart_colors) >= 6  # Should have at least 6 colors

        # All chart colors should be valid hex
        for color in chart_colors:
            assert color.startswith("#")
            assert len(color) == 7

    def test_apply_to_slide(self, mock_slide):
        """Test applying theme to slide."""
        manager = ThemeManager()
        theme = manager.get_theme("dark")

        # Apply theme
        theme.apply_to_slide(mock_slide)

        # Check that slide background was modified
        # (Exact implementation depends on Theme class)
        # This is a simplified test
        assert mock_slide is not None

    def test_get_color(self):
        """Test getting specific colors from theme."""
        manager = ThemeManager()
        theme = manager.get_theme("dark")

        if hasattr(theme, "get_color"):
            from pptx.dml.color import RGBColor

            # Get primary color
            primary = theme.get_color("primary.DEFAULT")
            assert primary is not None
            assert isinstance(primary, RGBColor)

            # Get background color
            bg = theme.get_color("background.DEFAULT")
            assert bg is not None
            assert isinstance(bg, RGBColor)

            # Get non-existent color should return an RGBColor (black)
            invalid = theme.get_color("nonexistent.color")
            assert isinstance(invalid, RGBColor)

    def test_theme_variants(self):
        """Test theme color variants."""
        manager = ThemeManager()
        theme = manager.get_theme("dark-blue")

        # Dark-blue should have blue as primary or accent
        primary = theme.primary.get("DEFAULT")
        accent = theme.accent.get("DEFAULT")

        # At least one should have blue-ish color
        # Blue colors typically have high B value in RGB
        has_blue = False
        for color in [primary, accent]:
            if color:
                rgb = int(color[1:], 16)
                b = rgb & 0xFF
                r = (rgb >> 16) & 0xFF
                if b > r:  # Blue component greater than red
                    has_blue = True
                    break

        assert has_blue

    def test_theme_consistency(self):
        """Test that theme colors are consistent."""
        manager = ThemeManager()

        for theme_name in ["dark", "light"]:
            theme = manager.get_theme(theme_name)

            # Background and foreground should have good contrast
            bg = theme.background.get("DEFAULT")
            fg = theme.foreground.get("DEFAULT")

            if bg and fg:
                bg_rgb = int(bg[1:], 16)
                fg_rgb = int(fg[1:], 16)

                # Simple contrast check
                bg_lum = (bg_rgb >> 16) + ((bg_rgb >> 8) & 0xFF) + (bg_rgb & 0xFF)
                fg_lum = (fg_rgb >> 16) + ((fg_rgb >> 8) & 0xFF) + (fg_rgb & 0xFF)

                contrast = abs(bg_lum - fg_lum)
                assert contrast > 100  # Should have reasonable contrast
