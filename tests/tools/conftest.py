"""
Shared fixtures for tools tests.

Updated for Pydantic-native architecture with VFS integration.
"""

import pytest
import sys
import os
from unittest.mock import MagicMock, AsyncMock, Mock
from pptx import Presentation
from pptx.slide import Slide
from chuk_virtual_fs import AsyncVirtualFileSystem

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from chuk_mcp_pptx.presentation_manager import PresentationManager


@pytest.fixture
def mock_mcp_server():
    """Create a mock MCP server."""
    mcp = MagicMock()
    mcp.tool = lambda func: func  # Pass-through decorator
    return mcp


@pytest.fixture
async def vfs_for_tools():
    """Create an async virtual filesystem with memory provider for tool testing."""
    async with AsyncVirtualFileSystem(provider="memory") as fs:
        yield fs


@pytest.fixture
async def presentation_manager_for_tools(vfs_for_tools):
    """Create a PresentationManager with VFS for tool testing.

    Pre-creates a test presentation with 3 slides.
    """
    manager = PresentationManager(vfs=vfs_for_tools, base_path="test_presentations")

    # Create a test presentation with 3 slides
    metadata = await manager.create(name="test_presentation", theme=None)

    # Add 3 slides to the presentation
    result = await manager.get(name="test_presentation")
    if result:
        prs, _ = result
        # Add slides using the presentation object directly
        for i in range(3):
            prs.slides.add_slide(prs.slide_layouts[1])  # TITLE_AND_CONTENT layout

    return manager


# Keep old name for backward compatibility
@pytest.fixture
async def mock_presentation_manager(presentation_manager_for_tools):
    """Alias for backward compatibility with existing tests."""
    return presentation_manager_for_tools


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
