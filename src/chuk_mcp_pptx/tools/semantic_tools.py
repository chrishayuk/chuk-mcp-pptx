# src/chuk_mcp_pptx/tools/semantic_tools.py
"""
High-level semantic tools for LLM-friendly slide creation.

These tools provide:
- Automatic layout and positioning
- Smart defaults
- Semantic/intent-based API
- Complete slide creation in one call
- Grid-based positioning instead of inches

Philosophy: LLMs should describe WHAT they want, not HOW to position it.
"""

import asyncio
from typing import Dict, Any, Optional, List

from ..themes.theme_manager import ThemeManager


def register_semantic_tools(mcp, manager):
    """
    Register high-level semantic tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        manager: PresentationManager instance

    Returns:
        Dictionary of registered tools
    """
    tools = {}
    theme_manager = ThemeManager()

    # Layout grid: 10x10 grid on a standard slide
    SLIDE_WIDTH = 10.0  # inches
    SLIDE_HEIGHT = 7.5  # inches
    GRID_COLS = 10
    GRID_ROWS = 10

    def grid_to_position(col: int, row: int):
        """Convert grid position to inches."""
        left = (col / GRID_COLS) * SLIDE_WIDTH
        top = (row / GRID_ROWS) * SLIDE_HEIGHT
        return left, top

    def grid_size(cols: int, rows: int):
        """Convert grid size to inches."""
        width = (cols / GRID_COLS) * SLIDE_WIDTH
        height = (rows / GRID_ROWS) * SLIDE_HEIGHT
        return width, height

    @mcp.tool
    async def pptx_create_quick_deck(
        name: str,
        title: str,
        subtitle: Optional[str] = None,
        theme: str = "dark-violet"
    ) -> str:
        """
        Create a complete presentation with title slide in one call.

        This is the fastest way to start a presentation. Creates the presentation,
        adds a styled title slide, and sets the theme.

        Args:
            name: Presentation name
            title: Main title
            subtitle: Optional subtitle
            theme: Theme name (default: dark-violet)

        Returns:
            Success message with presentation info

        Example:
            await pptx_create_quick_deck(
                name="my_pitch",
                title="Product Launch 2024",
                subtitle="Revolutionary Innovation",
                theme="dark-violet"
            )
        """
        def _create():
            # Create presentation
            manager.create(name)
            prs = manager.get(name)

            # Add title slide
            slide_layout = prs.slide_layouts[0]
            slide = prs.slides.add_slide(slide_layout)
            slide.shapes.title.text = title
            if subtitle and len(slide.placeholders) > 1:
                slide.placeholders[1].text = subtitle

            # Apply theme
            theme_obj = theme_manager.get_theme(theme)
            if theme_obj:
                theme_obj.apply_to_slide(slide)

            manager.update(name)
            return f"Created '{name}' with title slide (theme: {theme})"

        return await asyncio.get_event_loop().run_in_executor(None, _create)

    @mcp.tool
    async def pptx_add_metrics_dashboard(
        title: str,
        metrics: List[Dict[str, str]],
        theme: Optional[str] = None,
        layout: str = "grid"
    ) -> str:
        """
        Add a complete metrics dashboard slide with automatic layout.

        Creates a slide with title and metric cards automatically positioned
        in a grid or row layout. Perfect for KPI dashboards.

        Uses the MetricsDashboard template with Grid-based positioning.

        Args:
            title: Slide title
            metrics: List of dicts with 'label', 'value', optional 'change' and 'trend'
            theme: Optional theme name
            layout: Layout style ('grid' for 2x2 grid, 'row' for horizontal row)

        Returns:
            Success message

        Example:
            await pptx_add_metrics_dashboard(
                title="Q4 Performance",
                metrics=[
                    {"label": "Revenue", "value": "$2.5M", "change": "+12%", "trend": "up"},
                    {"label": "Users", "value": "45K", "change": "+8%", "trend": "up"},
                    {"label": "NPS", "value": "72", "change": "+5pts", "trend": "up"},
                    {"label": "MRR", "value": "$180K", "change": "+15%", "trend": "up"}
                ],
                layout="grid"
            )
        """
        def _add_dashboard():
            from ..slide_templates import MetricsDashboard

            prs = manager.get_current()
            if not prs:
                raise ValueError("No active presentation")

            # Get theme
            theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
            theme_dict = theme_obj.__dict__ if hasattr(theme_obj, '__dict__') else theme_obj

            # Use template to create slide
            template = MetricsDashboard(
                title=title,
                metrics=metrics,
                layout=layout,
                theme=theme_dict
            )
            slide_idx = template.render(prs)

            # Apply theme to slide
            if theme_obj:
                slide = prs.slides[slide_idx]
                theme_obj.apply_to_slide(slide)

            manager.update()
            return f"Added metrics dashboard with {len(metrics)} metrics at slide {slide_idx}"

        return await asyncio.get_event_loop().run_in_executor(None, _add_dashboard)

    @mcp.tool
    async def pptx_add_content_grid(
        title: str,
        items: List[Dict[str, str]],
        item_type: str = "card",
        columns: int = 2,
        theme: Optional[str] = None
    ) -> str:
        """
        Add a grid of content items with automatic layout.

        Creates a slide with items arranged in a responsive grid. Items can be
        cards, tiles, or buttons. Layout is automatic based on number of items.

        Uses the ContentGrid template with Grid-based positioning.

        Args:
            title: Slide title
            items: List of dicts with content (structure depends on item_type)
            item_type: Type of items ('card', 'tile', 'button')
            columns: Number of columns in grid (2-4)
            theme: Optional theme name

        Returns:
            Success message

        Example:
            await pptx_add_content_grid(
                title="Key Features",
                items=[
                    {"title": "Fast", "description": "Lightning quick performance"},
                    {"title": "Secure", "description": "Enterprise-grade security"},
                    {"title": "Scalable", "description": "Grows with your needs"},
                    {"title": "Reliable", "description": "99.9% uptime guarantee"}
                ],
                item_type="card",
                columns=2
            )
        """
        def _add_grid():
            from ..slide_templates import ContentGridSlide

            prs = manager.get_current()
            if not prs:
                raise ValueError("No active presentation")

            # Get theme
            theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
            theme_dict = theme_obj.__dict__ if hasattr(theme_obj, '__dict__') else theme_obj

            # Use template to create slide
            template = ContentGridSlide(
                title=title,
                items=items,
                item_type=item_type,
                columns=columns,
                theme=theme_dict
            )
            slide_idx = template.render(prs)

            # Apply theme
            if theme_obj:
                slide = prs.slides[slide_idx]
                theme_obj.apply_to_slide(slide)

            manager.update()
            return f"Added content grid with {len(items)} {item_type}s in {columns} columns at slide {slide_idx}"

        return await asyncio.get_event_loop().run_in_executor(None, _add_grid)

    @mcp.tool
    async def pptx_add_timeline_slide(
        title: str,
        events: List[Dict[str, str]],
        orientation: str = "horizontal",
        theme: Optional[str] = None
    ) -> str:
        """
        Add a timeline slide with automatic layout.

        Creates a complete timeline slide with title and events.
        Events are automatically spaced and styled.

        Uses the TimelineSlide template with Grid-based positioning.

        Args:
            title: Slide title
            events: List of dicts with 'date' and 'description'
            orientation: Timeline direction ('horizontal' or 'vertical')
            theme: Optional theme name

        Returns:
            Success message

        Example:
            await pptx_add_timeline_slide(
                title="Product Roadmap 2024",
                events=[
                    {"date": "Q1", "description": "Beta Launch"},
                    {"date": "Q2", "description": "Public Release"},
                    {"date": "Q3", "description": "Enterprise Features"},
                    {"date": "Q4", "description": "Global Expansion"}
                ]
            )
        """
        def _add_timeline():
            from ..slide_templates import TimelineSlide

            prs = manager.get_current()
            if not prs:
                raise ValueError("No active presentation")

            # Get theme
            theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
            theme_dict = theme_obj.__dict__ if hasattr(theme_obj, '__dict__') else theme_obj

            # Use template to create slide
            template = TimelineSlide(
                title=title,
                events=events,
                orientation=orientation,
                theme=theme_dict
            )
            slide_idx = template.render(prs)

            # Apply theme
            if theme_obj:
                slide = prs.slides[slide_idx]
                theme_obj.apply_to_slide(slide)

            manager.update()
            return f"Added timeline slide with {len(events)} events at slide {slide_idx}"

        return await asyncio.get_event_loop().run_in_executor(None, _add_timeline)

    @mcp.tool
    async def pptx_add_comparison_slide(
        title: str,
        left_title: str,
        left_items: List[str],
        right_title: str,
        right_items: List[str],
        theme: Optional[str] = None
    ) -> str:
        """
        Add a two-column comparison slide.

        Creates a slide comparing two options, features, or approaches
        side-by-side with automatic layout.

        Uses the ComparisonSlide template with Grid-based positioning.

        Args:
            title: Slide title
            left_title: Title for left column
            left_items: Items for left column
            right_title: Title for right column
            right_items: Items for right column
            theme: Optional theme name

        Returns:
            Success message

        Example:
            await pptx_add_comparison_slide(
                title="Build vs Buy",
                left_title="Build In-House",
                left_items=["Full control", "Custom features", "Higher cost", "Longer timeline"],
                right_title="Buy Solution",
                right_items=["Quick deployment", "Proven reliability", "Lower initial cost", "Less customization"]
            )
        """
        def _add_comparison():
            from ..slide_templates import ComparisonSlide

            prs = manager.get_current()
            if not prs:
                raise ValueError("No active presentation")

            # Get theme
            theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
            theme_dict = theme_obj.__dict__ if hasattr(theme_obj, '__dict__') else theme_obj

            # Use template to create slide
            template = ComparisonSlide(
                title=title,
                left_title=left_title,
                left_items=left_items,
                right_title=right_title,
                right_items=right_items,
                theme=theme_dict
            )
            slide_idx = template.render(prs)

            # Apply theme
            if theme_obj:
                slide = prs.slides[slide_idx]
                theme_obj.apply_to_slide(slide)

            manager.update()
            return f"Added comparison slide: {left_title} vs {right_title} at slide {slide_idx}"

        return await asyncio.get_event_loop().run_in_executor(None, _add_comparison)

    @mcp.tool
    async def pptx_list_slide_templates(
        category: Optional[str] = None
    ) -> str:
        """
        List all available slide templates.

        Returns metadata about all registered slide templates including
        their properties, examples, and usage information. LLMs can use
        this to discover what slide types are available.

        Args:
            category: Optional category filter (opening, content, dashboard, comparison, timeline, closing, layout)

        Returns:
            JSON array of template metadata

        Example:
            # List all templates
            templates = await pptx_list_slide_templates()

            # List only dashboard templates
            dashboards = await pptx_list_slide_templates(category="dashboard")
        """
        def _list_templates():
            from ..slide_templates.registry import list_templates
            import json
            templates = list_templates(category)
            return json.dumps(templates, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _list_templates)

    @mcp.tool
    async def pptx_get_template_info(
        template_name: str
    ) -> str:
        """
        Get detailed information about a specific slide template.

        Returns complete metadata including all properties, their types,
        required/optional status, examples, and usage patterns.

        Args:
            template_name: Name of the template (e.g., "MetricsDashboard", "ComparisonSlide")

        Returns:
            JSON object with template details

        Example:
            info = await pptx_get_template_info(template_name="MetricsDashboard")
            # Returns full metadata about the MetricsDashboard template
        """
        def _get_info():
            from ..slide_templates.registry import get_template_info
            import json
            info = get_template_info(template_name)
            if info is None:
                return json.dumps({"error": f"Template '{template_name}' not found"})
            return json.dumps(info, indent=2)

        return await asyncio.get_event_loop().run_in_executor(None, _get_info)

    # Store tools for return
    tools.update({
        'pptx_create_quick_deck': pptx_create_quick_deck,
        'pptx_add_metrics_dashboard': pptx_add_metrics_dashboard,
        'pptx_add_content_grid': pptx_add_content_grid,
        'pptx_add_timeline_slide': pptx_add_timeline_slide,
        'pptx_add_comparison_slide': pptx_add_comparison_slide,
        'pptx_list_slide_templates': pptx_list_slide_templates,
        'pptx_get_template_info': pptx_get_template_info,
    })

    return tools
