"""
Comprehensive tests for async_server.py

Tests for MCP server tools that handle presentations.
Coverage target: 90%+
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

if TYPE_CHECKING:
    pass


class TestModuleImports:
    """Tests for module-level imports and initialization."""

    def test_mcp_server_exists(self) -> None:
        """Test that MCP server instance exists."""
        from chuk_mcp_pptx.async_server import mcp

        assert mcp is not None

    def test_manager_exists(self) -> None:
        """Test that PresentationManager instance exists."""
        from chuk_mcp_pptx.async_server import manager
        from chuk_mcp_pptx.core.presentation_manager import PresentationManager

        assert isinstance(manager, PresentationManager)

    def test_theme_manager_exists(self) -> None:
        """Test that ThemeManager instance exists."""
        from chuk_mcp_pptx.async_server import theme_manager
        from chuk_mcp_pptx.themes.theme_manager import ThemeManager

        assert isinstance(theme_manager, ThemeManager)


class TestToolsRegistration:
    """Tests for tool registration."""

    def test_placeholder_tools_registered(self) -> None:
        """Test that placeholder tools are registered."""
        from chuk_mcp_pptx.async_server import placeholder_tools

        assert placeholder_tools is not None

    def test_inspection_tools_registered(self) -> None:
        """Test that inspection tools are registered."""
        from chuk_mcp_pptx.async_server import inspection_tools

        assert inspection_tools is not None

    def test_layout_tools_registered(self) -> None:
        """Test that layout tools are registered."""
        from chuk_mcp_pptx.async_server import layout_tools

        assert layout_tools is not None

    def test_universal_component_api_registered(self) -> None:
        """Test that universal component API is registered."""
        from chuk_mcp_pptx.async_server import universal_component_api

        assert universal_component_api is not None

    def test_registry_tools_registered(self) -> None:
        """Test that registry tools are registered."""
        from chuk_mcp_pptx.async_server import registry_tools

        assert registry_tools is not None

    def test_theme_tools_registered(self) -> None:
        """Test that theme tools are registered."""
        from chuk_mcp_pptx.async_server import theme_tools

        assert theme_tools is not None

    def test_semantic_tools_registered(self) -> None:
        """Test that semantic tools are registered."""
        from chuk_mcp_pptx.async_server import semantic_tools

        assert semantic_tools is not None


class TestPptxCreate:
    """Tests for pptx_create tool."""

    @pytest.mark.asyncio
    async def test_create_basic(self) -> None:
        """Test creating a basic presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, manager

        # Clean up any existing presentations
        manager.clear_all()

        result = await pptx_create(name="test_create")
        data = json.loads(result)

        assert "error" not in data
        assert data["name"] == "test_create"
        assert data["slide_count"] == 0
        assert data["is_current"] is True

        # Clean up
        manager.clear_all()

    @pytest.mark.asyncio
    async def test_create_with_theme(self) -> None:
        """Test creating a presentation with a theme."""
        from chuk_mcp_pptx.async_server import pptx_create, manager

        manager.clear_all()

        result = await pptx_create(name="themed_pres", theme="dark-violet")
        data = json.loads(result)

        assert "error" not in data
        assert data["name"] == "themed_pres"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_create_exception_handling(self) -> None:
        """Test error handling when create fails."""
        from chuk_mcp_pptx.async_server import pptx_create, manager

        # Mock manager.create to raise an exception
        original_create = manager.create

        async def mock_create(*args, **kwargs):
            raise Exception("Test error")

        manager.create = mock_create

        try:
            result = await pptx_create(name="error_test")
            data = json.loads(result)

            assert "error" in data
            assert "Test error" in data["error"]
        finally:
            manager.create = original_create


class TestPptxAddTitleSlide:
    """Tests for pptx_add_title_slide tool."""

    @pytest.mark.asyncio
    async def test_add_title_slide_basic(self) -> None:
        """Test adding a basic title slide."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test_title")

        result = await pptx_add_title_slide(title="Test Title", subtitle="Test Subtitle")
        data = json.loads(result)

        assert "error" not in data
        assert data["slide_index"] == 0
        assert data["slide_count"] == 1

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_title_slide_no_subtitle(self) -> None:
        """Test adding a title slide without subtitle."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="test_no_sub")

        result = await pptx_add_title_slide(title="Only Title")
        data = json.loads(result)

        assert "error" not in data
        assert data["slide_index"] == 0

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_title_slide_no_presentation(self) -> None:
        """Test adding title slide when no presentation exists."""
        from chuk_mcp_pptx.async_server import pptx_add_title_slide, manager

        manager.clear_all()

        result = await pptx_add_title_slide(title="Test")
        data = json.loads(result)

        assert "error" in data

    @pytest.mark.asyncio
    async def test_add_title_slide_with_presentation_name(self) -> None:
        """Test adding title slide to specific presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="pres1")
        await pptx_create(name="pres2")

        # Add to specific presentation (not current)
        result = await pptx_add_title_slide(title="Test", subtitle="Sub", presentation="pres1")
        data = json.loads(result)

        assert "error" not in data
        assert data["presentation"] == "pres1"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_title_slide_with_theme(self) -> None:
        """Test adding title slide applies theme."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_title_slide, manager

        manager.clear_all()
        await pptx_create(name="themed", theme="dark-violet")

        result = await pptx_add_title_slide(title="Themed Title")
        data = json.loads(result)

        assert "error" not in data

        manager.clear_all()


class TestPptxAddSlide:
    """Tests for pptx_add_slide tool."""

    @pytest.mark.asyncio
    async def test_add_slide_basic(self) -> None:
        """Test adding a basic content slide."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_slide, manager

        manager.clear_all()
        await pptx_create(name="test_content")

        result = await pptx_add_slide(
            title="Content Slide", content=["Point 1", "Point 2", "Point 3"]
        )
        data = json.loads(result)

        assert "error" not in data
        assert data["slide_index"] == 0
        assert data["slide_count"] == 1

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_slide_empty_content(self) -> None:
        """Test adding a slide with empty content."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_slide, manager

        manager.clear_all()
        await pptx_create(name="test_empty")

        result = await pptx_add_slide(title="Empty Slide", content=[])
        data = json.loads(result)

        assert "error" not in data

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_add_slide_no_presentation(self) -> None:
        """Test adding slide when no presentation exists."""
        from chuk_mcp_pptx.async_server import pptx_add_slide, manager

        manager.clear_all()

        result = await pptx_add_slide(title="Test", content=["Item"])
        data = json.loads(result)

        assert "error" in data

    @pytest.mark.asyncio
    async def test_add_slide_with_theme(self) -> None:
        """Test adding content slide applies theme."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_add_slide, manager

        manager.clear_all()
        await pptx_create(name="themed_content", theme="tech-blue")

        result = await pptx_add_slide(title="Themed Content", content=["Bullet 1", "Bullet 2"])
        data = json.loads(result)

        assert "error" not in data

        manager.clear_all()


class TestPptxSave:
    """Tests for pptx_save tool."""

    @pytest.mark.asyncio
    async def test_save_basic(self) -> None:
        """Test saving a presentation to file."""
        import tempfile
        import os
        from chuk_mcp_pptx.async_server import pptx_create, pptx_save, manager

        manager.clear_all()
        await pptx_create(name="save_test")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.pptx")
            result = await pptx_save(path=path)
            data = json.loads(result)

            assert "error" not in data
            assert data["format"] == "file"
            assert data["path"] == path
            assert os.path.exists(path)

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_save_no_presentation(self) -> None:
        """Test saving when no presentation exists."""
        from chuk_mcp_pptx.async_server import pptx_save, manager

        manager.clear_all()

        result = await pptx_save(path="/tmp/nonexistent.pptx")
        data = json.loads(result)

        assert "error" in data

    @pytest.mark.asyncio
    async def test_save_specific_presentation(self) -> None:
        """Test saving a specific presentation by name."""
        import tempfile
        import os
        from chuk_mcp_pptx.async_server import pptx_create, pptx_save, manager

        manager.clear_all()
        await pptx_create(name="pres_a")
        await pptx_create(name="pres_b")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "pres_a.pptx")
            result = await pptx_save(path=path, presentation="pres_a")
            data = json.loads(result)

            assert "error" not in data
            assert data["name"] == "pres_a"

        manager.clear_all()


class TestPptxExportBase64:
    """Tests for pptx_export_base64 tool."""

    @pytest.mark.asyncio
    async def test_export_basic(self) -> None:
        """Test basic base64 export."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_export_base64, manager

        manager.clear_all()
        await pptx_create(name="export_test")

        result = await pptx_export_base64()
        data = json.loads(result)

        assert "error" not in data
        assert data["format"] == "base64"
        assert data["name"] == "export_test"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_export_no_presentation(self) -> None:
        """Test export when no presentation exists."""
        from chuk_mcp_pptx.async_server import pptx_export_base64, manager

        manager.clear_all()

        result = await pptx_export_base64()
        data = json.loads(result)

        assert "error" in data

    @pytest.mark.asyncio
    async def test_export_specific_presentation(self) -> None:
        """Test exporting a specific presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_export_base64, manager

        manager.clear_all()
        await pptx_create(name="exp_a")
        await pptx_create(name="exp_b")

        result = await pptx_export_base64(presentation="exp_a")
        data = json.loads(result)

        assert "error" not in data
        assert data["name"] == "exp_a"

        manager.clear_all()


class TestPptxImportBase64:
    """Tests for pptx_import_base64 tool."""

    @pytest.mark.asyncio
    async def test_import_basic(self) -> None:
        """Test basic base64 import."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_export_base64,
            pptx_import_base64,
            manager,
        )

        manager.clear_all()

        # Create and export a presentation
        await pptx_create(name="original")
        export_result = await pptx_export_base64()
        json.loads(export_result)

        # Get the actual base64 data from manager
        base64_data = await manager.export_base64("original")

        # Import with new name
        result = await pptx_import_base64(data=base64_data, name="imported")
        data = json.loads(result)

        assert "error" not in data
        assert data["name"] == "imported"
        assert data["source"] == "base64"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_import_invalid_data(self) -> None:
        """Test import with invalid base64 data."""
        from chuk_mcp_pptx.async_server import pptx_import_base64, manager

        manager.clear_all()

        result = await pptx_import_base64(data="invalid-data!", name="bad_import")
        data = json.loads(result)

        assert "error" in data


class TestPptxList:
    """Tests for pptx_list tool."""

    @pytest.mark.asyncio
    async def test_list_empty(self) -> None:
        """Test listing when no presentations exist."""
        from chuk_mcp_pptx.async_server import pptx_list, manager

        manager.clear_all()

        result = await pptx_list()
        data = json.loads(result)

        assert data["total"] == 0
        assert len(data["presentations"]) == 0

    @pytest.mark.asyncio
    async def test_list_single(self) -> None:
        """Test listing with one presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_list, manager

        manager.clear_all()
        await pptx_create(name="single")

        result = await pptx_list()
        data = json.loads(result)

        assert data["total"] == 1
        assert len(data["presentations"]) == 1
        assert data["presentations"][0]["name"] == "single"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_list_multiple(self) -> None:
        """Test listing with multiple presentations."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_list, manager

        manager.clear_all()
        await pptx_create(name="first")
        await pptx_create(name="second")
        await pptx_create(name="third")

        result = await pptx_list()
        data = json.loads(result)

        assert data["total"] == 3
        assert len(data["presentations"]) == 3

        names = {p["name"] for p in data["presentations"]}
        assert names == {"first", "second", "third"}

        manager.clear_all()


class TestPptxSwitch:
    """Tests for pptx_switch tool."""

    @pytest.mark.asyncio
    async def test_switch_basic(self) -> None:
        """Test basic presentation switching."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_switch, manager

        manager.clear_all()
        await pptx_create(name="pres1")
        await pptx_create(name="pres2")

        # Current is pres2
        assert manager.get_current_name() == "pres2"

        # Switch to pres1
        result = await pptx_switch(name="pres1")
        data = json.loads(result)

        assert "error" not in data
        assert manager.get_current_name() == "pres1"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_switch_nonexistent(self) -> None:
        """Test switching to nonexistent presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_switch, manager

        manager.clear_all()
        await pptx_create(name="exists")

        result = await pptx_switch(name="does_not_exist")
        data = json.loads(result)

        assert "error" in data

        manager.clear_all()


class TestPptxDelete:
    """Tests for pptx_delete tool."""

    @pytest.mark.asyncio
    async def test_delete_basic(self) -> None:
        """Test basic presentation deletion."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_delete, pptx_list, manager

        manager.clear_all()
        await pptx_create(name="to_delete")

        result = await pptx_delete(name="to_delete")
        data = json.loads(result)

        assert "error" not in data

        # Verify deletion
        list_result = await pptx_list()
        list_data = json.loads(list_result)
        assert list_data["total"] == 0

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self) -> None:
        """Test deleting nonexistent presentation."""
        from chuk_mcp_pptx.async_server import pptx_delete, manager

        manager.clear_all()

        result = await pptx_delete(name="nonexistent")
        data = json.loads(result)

        assert "error" in data


class TestPptxGetInfo:
    """Tests for pptx_get_info tool."""

    @pytest.mark.asyncio
    async def test_get_info_basic(self) -> None:
        """Test getting presentation info."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_info, manager

        manager.clear_all()
        await pptx_create(name="info_test")

        result = await pptx_get_info()
        data = json.loads(result)

        assert "error" not in data
        assert data["name"] == "info_test"
        assert "slide_count" in data

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_info_specific(self) -> None:
        """Test getting specific presentation info."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_info, manager

        manager.clear_all()
        await pptx_create(name="info_a")
        await pptx_create(name="info_b")

        result = await pptx_get_info(presentation="info_a")
        data = json.loads(result)

        assert "error" not in data
        assert data["name"] == "info_a"

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_info_no_presentation(self) -> None:
        """Test getting info when no presentation exists."""
        from chuk_mcp_pptx.async_server import pptx_get_info, manager

        manager.clear_all()

        result = await pptx_get_info()
        data = json.loads(result)

        assert "error" in data


class TestToolExportsConditional:
    """Tests for conditional tool exports based on registration success."""

    def test_inspection_tools_exports(self) -> None:
        """Test inspection tool functions are exported."""
        from chuk_mcp_pptx import async_server

        if async_server.inspection_tools:
            assert hasattr(async_server, "pptx_inspect_slide")
            assert hasattr(async_server, "pptx_fix_slide_layout")
            assert hasattr(async_server, "pptx_analyze_presentation_layout")

    def test_layout_tools_exports(self) -> None:
        """Test layout tool functions are exported."""
        from chuk_mcp_pptx import async_server

        if async_server.layout_tools:
            assert hasattr(async_server, "pptx_list_layouts")
            assert hasattr(async_server, "pptx_add_slide_with_layout")
            assert hasattr(async_server, "pptx_customize_layout")
            assert hasattr(async_server, "pptx_apply_master_layout")
            assert hasattr(async_server, "pptx_duplicate_slide")
            assert hasattr(async_server, "pptx_reorder_slides")

    def test_theme_tools_exports(self) -> None:
        """Test theme tool functions are exported."""
        from chuk_mcp_pptx import async_server

        if async_server.theme_tools:
            assert hasattr(async_server, "pptx_list_themes")
            assert hasattr(async_server, "pptx_get_theme_info")
            assert hasattr(async_server, "pptx_create_custom_theme")
            assert hasattr(async_server, "pptx_apply_theme")
            assert hasattr(async_server, "pptx_apply_component_theme")
            assert hasattr(async_server, "pptx_list_component_themes")


class TestExceptionHandling:
    """Tests for exception handling in tools."""

    @pytest.mark.asyncio
    async def test_add_title_slide_exception(self) -> None:
        """Test exception handling in add_title_slide."""
        from chuk_mcp_pptx.async_server import pptx_add_title_slide, manager

        manager.clear_all()

        # Create mock presentation that raises on slide addition
        mock_prs = MagicMock()
        mock_prs.slide_layouts = MagicMock()
        mock_prs.slide_layouts.__getitem__ = MagicMock(side_effect=Exception("Layout error"))

        original_get = manager.get_presentation
        manager.get_presentation = MagicMock(return_value=mock_prs)

        try:
            result = await pptx_add_title_slide(title="Test")
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.get_presentation = original_get

    @pytest.mark.asyncio
    async def test_add_slide_exception(self) -> None:
        """Test exception handling in add_slide."""
        from chuk_mcp_pptx.async_server import pptx_add_slide, manager

        manager.clear_all()

        mock_prs = MagicMock()
        mock_prs.slide_layouts = MagicMock()
        mock_prs.slide_layouts.__getitem__ = MagicMock(side_effect=Exception("Layout error"))

        original_get = manager.get_presentation
        manager.get_presentation = MagicMock(return_value=mock_prs)

        try:
            result = await pptx_add_slide(title="Test", content=["Item"])
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.get_presentation = original_get

    @pytest.mark.asyncio
    async def test_save_exception(self) -> None:
        """Test exception handling in save."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_save, manager

        manager.clear_all()
        await pptx_create(name="save_error")

        # Try to save to invalid path
        result = await pptx_save(path="/nonexistent/directory/file.pptx")
        data = json.loads(result)

        assert "error" in data

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_export_exception(self) -> None:
        """Test exception handling in export."""
        from chuk_mcp_pptx.async_server import pptx_export_base64, manager

        manager.clear_all()

        # Mock export to raise an exception
        original_export = manager.export_base64

        async def mock_export(*args, **kwargs):
            raise Exception("Export failed")

        manager.export_base64 = mock_export

        try:
            # First create a presentation so there's something to export
            from chuk_mcp_pptx.async_server import pptx_create

            await pptx_create(name="export_err")

            result = await pptx_export_base64()
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.export_base64 = original_export
            manager.clear_all()

    @pytest.mark.asyncio
    async def test_import_exception(self) -> None:
        """Test exception handling in import."""
        from chuk_mcp_pptx.async_server import pptx_import_base64, manager

        manager.clear_all()

        original_import = manager.import_base64

        async def mock_import(*args, **kwargs):
            raise Exception("Import failed")

        manager.import_base64 = mock_import

        try:
            result = await pptx_import_base64(data="test", name="import_err")
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.import_base64 = original_import

    @pytest.mark.asyncio
    async def test_list_exception(self) -> None:
        """Test exception handling in list."""
        from chuk_mcp_pptx.async_server import pptx_list, manager

        original_list = manager.list_presentations

        async def mock_list(*args, **kwargs):
            raise Exception("List failed")

        manager.list_presentations = mock_list

        try:
            result = await pptx_list()
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.list_presentations = original_list

    @pytest.mark.asyncio
    async def test_switch_exception(self) -> None:
        """Test exception handling in switch."""
        from chuk_mcp_pptx.async_server import pptx_switch, manager

        original_set_current = manager.set_current

        async def mock_set_current(*args, **kwargs):
            raise Exception("Switch failed")

        manager.set_current = mock_set_current

        try:
            result = await pptx_switch(name="test")
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.set_current = original_set_current

    @pytest.mark.asyncio
    async def test_delete_exception(self) -> None:
        """Test exception handling in delete."""
        from chuk_mcp_pptx.async_server import pptx_delete, manager

        original_delete = manager.delete

        async def mock_delete(*args, **kwargs):
            raise Exception("Delete failed")

        manager.delete = mock_delete

        try:
            result = await pptx_delete(name="test")
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.delete = original_delete

    @pytest.mark.asyncio
    async def test_get_info_exception(self) -> None:
        """Test exception handling in get_info."""
        from chuk_mcp_pptx.async_server import pptx_get_info, manager

        original_get = manager.get

        async def mock_get(*args, **kwargs):
            raise Exception("Get failed")

        manager.get = mock_get

        try:
            result = await pptx_get_info()
            data = json.loads(result)
            assert "error" in data
        finally:
            manager.get = original_get


class TestIntegration:
    """Integration tests for complete workflows."""

    @pytest.mark.asyncio
    async def test_full_workflow(self) -> None:
        """Test a complete presentation workflow."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_add_title_slide,
            pptx_add_slide,
            pptx_list,
            pptx_get_info,
            pptx_export_base64,
            pptx_delete,
            manager,
        )

        manager.clear_all()

        # Create presentation
        create_result = await pptx_create(name="workflow_test")
        assert "error" not in json.loads(create_result)

        # Add title slide
        title_result = await pptx_add_title_slide(
            title="Workflow Test", subtitle="Integration Testing"
        )
        assert "error" not in json.loads(title_result)

        # Add content slide
        content_result = await pptx_add_slide(
            title="Key Points", content=["Point 1", "Point 2", "Point 3"]
        )
        assert "error" not in json.loads(content_result)

        # List presentations
        list_result = await pptx_list()
        list_data = json.loads(list_result)
        assert list_data["total"] == 1

        # Get info
        info_result = await pptx_get_info()
        info_data = json.loads(info_result)
        assert info_data["slide_count"] == 2

        # Export
        export_result = await pptx_export_base64()
        assert "error" not in json.loads(export_result)

        # Delete
        delete_result = await pptx_delete(name="workflow_test")
        assert "error" not in json.loads(delete_result)

        # Verify deleted
        list_result2 = await pptx_list()
        assert json.loads(list_result2)["total"] == 0

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_multiple_presentations_workflow(self) -> None:
        """Test working with multiple presentations."""
        from chuk_mcp_pptx.async_server import (
            pptx_create,
            pptx_add_title_slide,
            pptx_switch,
            pptx_list,
            manager,
        )

        manager.clear_all()

        # Create first presentation
        await pptx_create(name="pres_1")
        await pptx_add_title_slide(title="Presentation 1")

        # Create second presentation
        await pptx_create(name="pres_2")
        await pptx_add_title_slide(title="Presentation 2")

        # Verify both exist
        list_result = await pptx_list()
        list_data = json.loads(list_result)
        assert list_data["total"] == 2

        # Switch and verify current
        await pptx_switch(name="pres_1")
        assert manager.get_current_name() == "pres_1"

        manager.clear_all()


class TestPptxGetDownloadUrl:
    """Tests for pptx_get_download_url tool."""

    @pytest.mark.asyncio
    async def test_get_download_url_no_presentation(self) -> None:
        """Test getting download URL when no presentation exists."""
        from chuk_mcp_pptx.async_server import pptx_get_download_url, manager

        manager.clear_all()

        result = await pptx_get_download_url()
        data = json.loads(result)

        assert "error" in data

    @pytest.mark.asyncio
    async def test_get_download_url_works_without_namespace_id(self) -> None:
        """Test getting download URL works even without prior namespace ID."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="no_namespace")

        # Clear namespace IDs - the new implementation doesn't require it
        manager._namespace_ids.clear()

        # Mock artifact store
        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-123")
        mock_store.presign = AsyncMock(return_value="https://example.com/url")

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url()
                data = json.loads(result)

                # Should succeed because the new implementation stores as artifact directly
                assert data.get("presentation") == "no_namespace"
                assert "url" in data

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_specific_presentation(self) -> None:
        """Test getting download URL for specific presentation."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="specific")

        # Mock artifact store
        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-123")
        mock_store.presign = AsyncMock(return_value="https://example.com/url")

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url(presentation="specific")
                data = json.loads(result)

                # Should succeed with mocked artifact store
                assert data.get("presentation") == "specific"
                assert "url" in data

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_nonexistent_presentation(self) -> None:
        """Test getting download URL for nonexistent presentation."""
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="exists")

        result = await pptx_get_download_url(presentation="does_not_exist")
        data = json.loads(result)

        assert "error" in data

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_with_custom_expires_in(self) -> None:
        """Test getting download URL with custom expiration."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="custom_expires")

        # Mock artifact store
        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-123")
        mock_store.presign = AsyncMock(return_value="https://example.com/url")

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url(expires_in=7200)
                data = json.loads(result)

                # Should succeed with mocked artifact store
                assert data.get("expires_in") == 7200

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_no_artifact_store(self) -> None:
        """Test getting download URL when no artifact store is configured."""
        from unittest.mock import patch
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="no_store")

        # Mock has_artifact_store to return False
        with patch("chuk_mcp_server.has_artifact_store", return_value=False):
            result = await pptx_get_download_url()
            data = json.loads(result)

            # Should fail because no artifact store configured
            assert "error" in data
            assert "artifact store" in data["error"].lower()

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_with_mocked_store(self) -> None:
        """Test getting download URL with a mocked artifact store."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="mocked_store")

        # Create mock store with both store() and presign() methods
        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-123")
        mock_store.presign = AsyncMock(return_value="https://example.com/presigned-url")

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url()
                data = json.loads(result)

                assert data["url"] == "https://example.com/presigned-url"
                assert data["presentation"] == "mocked_store"
                assert data["artifact_id"] == "artifact-123"
                assert data["expires_in"] == 86400  # Default is 24 hours

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_with_custom_expires_mocked(self) -> None:
        """Test getting download URL with custom expiration using mocked store."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="custom_exp")

        # Create mock store
        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-456")
        mock_store.presign = AsyncMock(return_value="https://example.com/custom-url")

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url(expires_in=7200)
                data = json.loads(result)

                assert data["expires_in"] == 7200

                # Verify presign was called with correct expires
                mock_store.presign.assert_called_once_with("artifact-456", expires=7200)

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_presign_exception(self) -> None:
        """Test handling of presign exception."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="presign_error")

        # Create mock store that raises exception on presign
        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-789")
        mock_store.presign = AsyncMock(side_effect=Exception("Presign failed"))

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url()
                data = json.loads(result)

                assert "error" in data
                assert "Presign failed" in data["error"]

        manager.clear_all()

    @pytest.mark.asyncio
    async def test_get_download_url_uses_current_presentation(self) -> None:
        """Test that download URL uses current presentation when not specified."""
        from unittest.mock import patch, AsyncMock, MagicMock
        from chuk_mcp_pptx.async_server import pptx_create, pptx_get_download_url, manager

        manager.clear_all()
        await pptx_create(name="first")
        await pptx_create(name="second")  # This becomes current

        mock_store = MagicMock()
        mock_store.store = AsyncMock(return_value="artifact-second")
        mock_store.presign = AsyncMock(return_value="https://example.com/url")

        with patch("chuk_mcp_server.has_artifact_store", return_value=True):
            with patch("chuk_mcp_server.get_artifact_store", return_value=mock_store):
                result = await pptx_get_download_url()
                data = json.loads(result)

                # Should use "second" (current presentation)
                assert data["presentation"] == "second"
                mock_store.presign.assert_called_once_with("artifact-second", expires=86400)

        manager.clear_all()
