"""Tests for base chart component functionality."""
import pytest
from unittest.mock import MagicMock, patch
from pptx.util import Inches
from chuk_mcp_pptx.components.charts.base import ChartComponent
from chuk_mcp_pptx.layout.boundaries import validate_boundaries, adjust_to_boundaries


class TestChartComponent:
    """Test the ChartComponent base class."""
    
    @pytest.fixture
    def chart_component(self):
        """Create a basic chart component instance."""
        return ChartComponent(
            title="Test Chart",
            data={"values": [1, 2, 3]},
            theme={"colors": {"primary": "#FF0000"}},
            options={"show_legend": True}
        )
    
    def test_initialization(self, chart_component):
        """Test chart component initialization."""
        assert chart_component.title == "Test Chart"
        assert chart_component.data == {"values": [1, 2, 3]}
        assert chart_component._theme == {"colors": {"primary": "#FF0000"}}
        assert chart_component._options == {"show_legend": True}
    
    def test_validate_data_base(self, chart_component):
        """Test base validation returns expected values."""
        result = chart_component.validate_data()
        # Base implementation returns (True, None)
        assert result == (True, None)
    
    def test_validate_boundaries(self, chart_component):
        """Test boundary validation using layout.boundaries module."""
        # Test valid boundaries
        result = validate_boundaries(2.0, 2.0, 5.0, 3.0)
        assert result == (True, None)

        # Test exceeding width
        result = validate_boundaries(1.0, 1.0, 15.0, 3.0)
        is_valid, error = result
        assert is_valid is False
        assert "exceeds" in error.lower()

    def test_adjust_to_boundaries(self, chart_component):
        """Test boundary adjustment using layout.boundaries module."""
        # Test normal case - no adjustment needed
        adjusted = adjust_to_boundaries(2.0, 2.0, 5.0, 3.0)
        assert adjusted == (2.0, 2.0, 5.0, 3.0)

        # Test adjustment needed
        adjusted = adjust_to_boundaries(8.0, 2.0, 5.0, 3.0)
        left, top, width, height = adjusted
        assert left < 8.0  # Should be adjusted
    
    def test_initialization_defaults(self):
        """Test chart component with defaults."""
        chart = ChartComponent()
        assert chart.title is None
        assert chart.data is None
        assert chart._theme is None
        assert chart._options is None
    
    async def test_render_not_implemented(self, chart_component):
        """Test render method exists."""
        mock_slide = MagicMock()
        # Mock slide.shapes.title to return None (no title)
        mock_slide.shapes.title = None
        
        # ChartComponent._render_sync expects _prepare_chart_data to be implemented
        # Since this is the base class, it should raise NotImplementedError
        with pytest.raises(NotImplementedError, match="_prepare_chart_data"):
            await chart_component.render(mock_slide)
    
    def test_theme_property(self, chart_component):
        """Test theme property."""
        # Test getter
        assert chart_component.theme == {"colors": {"primary": "#FF0000"}}
        
        # Test setter
        new_theme = {"colors": {"secondary": "#00FF00"}}
        chart_component.theme = new_theme
        assert chart_component.theme == new_theme
    
    def test_options_property(self, chart_component):
        """Test options property."""
        # Test getter
        assert chart_component.options == {"show_legend": True}
        
        # Test setter
        new_options = {"show_grid": False}
        chart_component.options = new_options
        assert chart_component.options == new_options