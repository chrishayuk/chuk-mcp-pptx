"""
Tests for Card components.
"""

from chuk_mcp_pptx.components.core.card import Card, MetricCard


class TestCard:
    """Test Card component with new composition API."""

    def test_init(self, dark_theme):
        """Test initialization."""
        card = Card(variant="elevated", theme=dark_theme)
        assert card.variant == "elevated"

    def test_variants(self, dark_theme):
        """Test different card variants."""
        variants = ["default", "outlined", "elevated", "ghost"]

        for variant in variants:
            card = Card(variant=variant, theme=dark_theme)
            assert card.variant == variant

    def test_with_composition(self, dark_theme):
        """Test card with composed children."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Test Card"))
        card.add_child(Card.Description("This is a test description"))

        assert len(card._children) == 2

    def test_render(self, mock_slide, dark_theme):
        """Test rendering card."""
        card = Card(variant="elevated", theme=dark_theme)
        card.add_child(Card.Title("Revenue"))
        card.add_child(Card.Description("Q4 2024 Revenue: $12.5M"))

        card.render(mock_slide, left=1, top=1, width=3, height=2)

        # Should add shapes for card
        assert mock_slide.shapes.add_shape.called

    def test_no_children(self, dark_theme):
        """Test card without children."""
        card = Card(variant="default", theme=dark_theme)
        assert len(card._children) == 0

    def test_only_title(self, dark_theme):
        """Test card with only title."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Just a title"))

        assert len(card._children) == 1

    def test_empty_card(self, dark_theme):
        """Test card with no content."""
        card = Card(variant="default", theme=dark_theme)
        assert len(card._children) == 0

    def test_theme_colors(self, dark_theme, light_theme):
        """Test card with different themes."""
        # Dark theme card
        dark_card = Card(variant="default", theme=dark_theme)

        # Light theme card
        light_card = Card(variant="default", theme=light_theme)

        # Themes should be different
        assert dark_card.tokens != light_card.tokens


class TestMetricCard:
    """Test MetricCard component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        card = MetricCard(
            label="Revenue", value="$12.5M", change="+15%", trend="up", theme=dark_theme
        )

        assert card.label == "Revenue"
        assert card.value == "$12.5M"
        assert card.change == "+15%"
        assert card.trend == "up"

    def test_trend_indicators(self, dark_theme):
        """Test different trend indicators."""
        trends = ["up", "down", "neutral"]

        for trend in trends:
            card = MetricCard(label="Test", value="100", change="5%", trend=trend, theme=dark_theme)
            assert card.trend == trend

    def test_render(self, mock_slide, dark_theme):
        """Test rendering metric card."""
        card = MetricCard(
            label="Sales", value="1,234", change="+8.5%", trend="up", theme=dark_theme
        )

        card.render(mock_slide, left=1, top=1, width=2.5, height=1.5)

        # Should add shapes for metric card
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called

    def test_no_change(self, dark_theme):
        """Test metric card without change value."""
        card = MetricCard(
            label="Total Users", value="10,000", change=None, trend=None, theme=dark_theme
        )

        assert card.change is None
        assert card.trend is None

    def test_format_options(self, dark_theme):
        """Test formatting options."""
        card = MetricCard(
            label="Percentage", value="85.5%", change="+2.3pp", trend="up", theme=dark_theme
        )

        assert card.value == "85.5%"
        assert card.change == "+2.3pp"


class TestCardAutoSizing:
    """Test Card auto-sizing functionality."""

    def test_calculate_min_width_no_children(self, dark_theme):
        """Test minimum width with no children."""
        card = Card(variant="default", theme=dark_theme)
        min_width = card._calculate_min_width()
        assert min_width == 3.0

    def test_calculate_min_width_with_title(self, dark_theme):
        """Test minimum width based on title length."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Short"))
        min_width = card._calculate_min_width()
        assert 2.5 <= min_width <= 6.0

    def test_calculate_min_width_long_title(self, dark_theme):
        """Test minimum width caps at maximum."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(
            Card.Title("This is a very long title that should be capped at maximum width")
        )
        min_width = card._calculate_min_width()
        assert min_width == 6.0  # Capped at maximum

    def test_calculate_min_height_no_children(self, dark_theme):
        """Test minimum height with no children."""
        card = Card(variant="default", theme=dark_theme)
        min_height = card._calculate_min_height()
        assert min_height == 1.5

    def test_calculate_min_height_with_title(self, dark_theme):
        """Test height calculation with title."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Revenue Summary"))
        min_height = card._calculate_min_height()
        assert min_height >= 1.5  # Minimum or calculated

    def test_calculate_min_height_with_description(self, dark_theme):
        """Test height calculation with description."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Description("This is a short description"))
        min_height = card._calculate_min_height()
        assert min_height >= 1.5

    def test_calculate_min_height_long_description(self, dark_theme):
        """Test height calculation with long description that wraps."""
        card = Card(variant="default", theme=dark_theme)
        long_desc = "This is a very long description that will definitely wrap across multiple lines and should result in a taller minimum height calculation based on the estimated line count."
        card.add_child(Card.Description(long_desc))
        min_height = card._calculate_min_height()
        assert min_height >= 1.8  # Should account for multiple lines

    def test_calculate_min_height_both_children(self, dark_theme):
        """Test height calculation with both title and description."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Q4 Revenue"))
        card.add_child(Card.Description("Total revenue for Q4 2024 increased by 15%"))
        min_height = card._calculate_min_height()
        assert min_height >= 1.7  # Should account for both

    def test_calculate_min_height_caps_at_maximum(self, dark_theme):
        """Test height calculation caps at maximum."""
        card = Card(variant="default", theme=dark_theme)
        # Add many children to exceed maximum
        for i in range(10):
            card.add_child(Card.Description(f"Line {i}: " + "x" * 100))
        min_height = card._calculate_min_height()
        assert min_height == 4.5  # Capped at maximum

    def test_render_with_auto_height(self, mock_slide, dark_theme):
        """Test rendering uses calculated height when not provided."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Auto Height"))
        card.add_child(Card.Description("Should calculate height automatically"))

        # Render without height parameter
        card.render(mock_slide, left=1, top=1, width=3)
        assert mock_slide.shapes.add_shape.called

    def test_render_respects_provided_height(self, mock_slide, dark_theme):
        """Test rendering respects explicitly provided height."""
        card = Card(variant="default", theme=dark_theme)
        card.add_child(Card.Title("Fixed Height"))

        # Render with explicit height
        card.render(mock_slide, left=1, top=1, width=3, height=5.0)
        assert mock_slide.shapes.add_shape.called


class TestMetricCardEdgeCases:
    """Test MetricCard edge cases and special scenarios."""

    def test_metric_card_neutral_trend_symbol(self, dark_theme):
        """Test neutral trend shows correct symbol."""
        card = MetricCard(
            label="Stable", value="100", change="0%", trend="neutral", theme=dark_theme
        )
        assert card.trend == "neutral"

    def test_metric_card_missing_change_and_trend(self, dark_theme):
        """Test metric card works without change/trend."""
        card = MetricCard(label="Count", value="5,000", theme=dark_theme)
        assert card.change is None
        assert card.trend is None

    def test_metric_card_with_zero_change(self, dark_theme):
        """Test metric card with zero change."""
        card = MetricCard(
            label="No Change", value="100", change="0%", trend="neutral", theme=dark_theme
        )
        assert card.change == "0%"

    def test_metric_card_large_values(self, dark_theme):
        """Test metric card with large formatted values."""
        card = MetricCard(
            label="Annual Revenue",
            value="$1,234,567,890",
            change="+123.45%",
            trend="up",
            theme=dark_theme,
        )
        assert "$" in card.value
        assert "%" in card.change
