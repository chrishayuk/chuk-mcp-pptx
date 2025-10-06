"""
Tests for Card components.
"""

import pytest
from unittest.mock import MagicMock

from chuk_mcp_pptx.components.card import Card, MetricCard


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
        light_card = Card(variant="default", theme=light_theme
        )
        
        # Themes should be different
        assert dark_card.tokens != light_card.tokens


class TestMetricCard:
    """Test MetricCard component."""
    
    def test_init(self, dark_theme):
        """Test initialization."""
        card = MetricCard(
            label="Revenue",
            value="$12.5M",
            change="+15%",
            trend="up",
            theme=dark_theme
        )
        
        assert card.label == "Revenue"
        assert card.value == "$12.5M"
        assert card.change == "+15%"
        assert card.trend == "up"
    
    def test_trend_indicators(self, dark_theme):
        """Test different trend indicators."""
        trends = ["up", "down", "neutral"]
        
        for trend in trends:
            card = MetricCard(
                label="Test",
                value="100",
                change="5%",
                trend=trend,
                theme=dark_theme
            )
            assert card.trend == trend
    
    def test_render(self, mock_slide, dark_theme):
        """Test rendering metric card."""
        card = MetricCard(
            label="Sales",
            value="1,234",
            change="+8.5%",
            trend="up",
            theme=dark_theme
        )
        
        card.render(mock_slide, left=1, top=1, width=2.5, height=1.5)
        
        # Should add shapes for metric card
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called
    
    def test_no_change(self, dark_theme):
        """Test metric card without change value."""
        card = MetricCard(
            label="Total Users",
            value="10,000",
            change=None,
            trend=None,
            theme=dark_theme
        )
        
        assert card.change is None
        assert card.trend is None
    
    def test_format_options(self, dark_theme):
        """Test formatting options."""
        card = MetricCard(
            label="Percentage",
            value="85.5%",
            change="+2.3pp",
            trend="up",
            theme=dark_theme
        )
        
        assert card.value == "85.5%"
        assert card.change == "+2.3pp"
