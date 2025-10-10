"""
Shared fixtures for tools tests.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, Mock
from pptx import Presentation
from pptx.slide import Slide


@pytest.fixture
def mock_mcp_server():
    """Create a mock MCP server."""
    mcp = MagicMock()
    mcp.tool = lambda func: func  # Pass-through decorator
    return mcp


@pytest.fixture
def mock_presentation_manager():
    """Create a mock presentation manager."""
    manager = MagicMock()

    # Mock get method to return a presentation
    prs = MagicMock(spec=Presentation)

    # Create mock slides collection with add_slide method
    slides_list = []

    def mock_add_slide(layout):
        """Mock add_slide method."""
        slide = MagicMock(spec=Slide)
        slide.shapes = MagicMock()
        slide.shapes.title = MagicMock()
        slide.shapes.title.text = ""
        slide.shapes.add_shape = MagicMock(return_value=MagicMock())
        slide.shapes.add_textbox = MagicMock(return_value=MagicMock())
        slide.shapes.add_chart = MagicMock()
        slide.shapes.add_picture = MagicMock()
        slide.shapes.add_connector = MagicMock()
        slide.shapes._spTree = MagicMock()
        slide.slide_layout = layout
        slide.placeholders = [MagicMock() for _ in range(3)]
        slide.background = MagicMock()
        slide.background.fill = MagicMock()
        slide.background.fill.solid = MagicMock()
        slide.background.fill.fore_color = MagicMock()
        slide.background.fill.fore_color.rgb = None
        slides_list.append(slide)
        return slide

    prs.slides = MagicMock()
    prs.slides.__len__ = lambda self: len(slides_list)
    prs.slides.__getitem__ = lambda self, idx: slides_list[idx]
    prs.slides.__iter__ = lambda self: iter(slides_list)
    prs.slides.add_slide = mock_add_slide

    prs.slide_layouts = [MagicMock() for _ in range(11)]
    prs.slide_master = MagicMock()
    prs.slide_master.slide_layouts = prs.slide_layouts
    prs.slide_width = 9144000
    prs.slide_height = 5143500

    # Create initial mock slides
    for i in range(3):
        mock_add_slide(prs.slide_layouts[1])

    manager.get = MagicMock(return_value=prs)
    manager.get_current = MagicMock(return_value=prs)
    manager.get_current_name = MagicMock(return_value="test_presentation")
    manager.create = MagicMock(return_value="Created presentation")
    manager.update = MagicMock()
    manager._presentations = {"test_presentation": prs}

    return manager


@pytest.fixture
def registered_tools(mock_mcp_server, mock_presentation_manager):
    """Fixture to register tools and return them for testing."""
    tools = {}
    return tools


@pytest.fixture
async def async_run():
    """Helper to run async functions in tests."""
    import asyncio

    async def runner(coro):
        return await coro

    return runner
