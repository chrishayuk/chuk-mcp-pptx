"""
Tests for Card components.
"""

import pytest
from unittest.mock import MagicMock

from chuk_mcp_pptx.components.card import Card, MetricCard, FeatureCard


class TestCard:
    """Test Card component."""
    
    def test_init(self, dark_theme):
        """Test initialization."""
        card = Card(
            title="Test Card",
            description="This is a test description",
            variant="elevated",
            theme=dark_theme
        )
        
        assert card.title == "Test Card"
        assert card.description == "This is a test description"
        assert card.variant == "elevated"
    
    def test_variants(self, dark_theme):
        """Test different card variants."""
        variants = ["default", "bordered", "elevated"]
        
        for variant in variants:
            card = Card(
                title="Test",
                description="Description",
                variant=variant,
                theme=dark_theme
            )
            assert card.variant == variant
    
    def test_render(self, mock_slide, dark_theme):
        """Test rendering card."""
        card = Card(
            title="Revenue",
            description="Q4 2024 Revenue: $12.5M",
            variant="elevated",
            theme=dark_theme
        )
        
        card.render(mock_slide, left=1, top=1, width=3, height=2)
        
        # Should add shapes for card
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called
    
    def test_no_title(self, dark_theme):
        """Test card without title."""
        card = Card(
            title=None,
            description="Just a description",
            theme=dark_theme
        )
        
        assert card.title is None
        assert card.description == "Just a description"
    
    def test_no_description(self, dark_theme):
        """Test card without description."""
        card = Card(
            title="Just a title",
            description=None,
            theme=dark_theme
        )
        
        assert card.title == "Just a title"
        assert card.description is None
    
    def test_empty_card(self, dark_theme):
        """Test card with no content."""
        card = Card(
            title=None,
            description=None,
            theme=dark_theme
        )
        
        assert card.title is None
        assert card.description is None
    
    def test_theme_colors(self, dark_theme, light_theme):
        """Test card with different themes."""
        # Dark theme card
        dark_card = Card(
            title="Dark Card",
            description="Dark theme",
            theme=dark_theme
        )
        
        # Light theme card
        light_card = Card(
            title="Light Card",
            description="Light theme",
            theme=light_theme
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


class TestFeatureCard:
    """Test FeatureCard component."""
    
    def test_init(self, dark_theme):
        """Test initialization."""
        card = FeatureCard(
            title="New Feature",
            description="Amazing new functionality",
            icon="🚀",
            features=["Fast", "Reliable", "Secure"],
            theme=dark_theme
        )
        
        assert card.title == "New Feature"
        assert card.description == "Amazing new functionality"
        assert card.icon == "🚀"
        assert card.features == ["Fast", "Reliable", "Secure"]
    
    def test_no_icon(self, dark_theme):
        """Test feature card without icon."""
        card = FeatureCard(
            title="Feature",
            description="Description",
            icon=None,
            features=["Feature 1", "Feature 2"],
            theme=dark_theme
        )
        
        assert card.icon is None
    
    def test_empty_features(self, dark_theme):
        """Test feature card with empty features list."""
        card = FeatureCard(
            title="Feature",
            description="Description",
            features=[],
            theme=dark_theme
        )
        
        assert card.features == []
    
    def test_render(self, mock_slide, dark_theme):
        """Test rendering feature card."""
        card = FeatureCard(
            title="Premium Plan",
            description="Everything you need",
            icon="⭐",
            features=[
                "Unlimited users",
                "Advanced analytics",
                "24/7 support",
                "Custom integrations"
            ],
            theme=dark_theme
        )
        
        card.render(mock_slide, left=1, top=1, width=3, height=3)
        
        # Should add shapes for feature card
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called
    
    def test_max_features(self, dark_theme):
        """Test feature card with many features."""
        features = [f"Feature {i}" for i in range(20)]
        
        card = FeatureCard(
            title="Many Features",
            description="Lots of capabilities",
            features=features,
            theme=dark_theme
        )
        
        assert len(card.features) == 20
        # Max features would be handled by the render method