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

from ..themes.theme_manager import ThemeManager

from ..constants import (
    SlideLayoutIndex,
)


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
        name: str, title: str, subtitle: str | None = None, theme: str = "dark-violet"
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
        # Create presentation with theme in metadata
        metadata = await manager.create(name, theme=theme)
        result = await manager.get(name)
        if not result:
            raise ValueError(f"Failed to get presentation '{name}'")
        prs, metadata = result

        # Add title slide
        slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE]
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle

        # Apply theme to title slide
        theme_obj = theme_manager.get_theme(theme)
        if theme_obj:
            theme_obj.apply_to_slide(slide)

        await manager.update(name)
        return f"Created '{name}' with title slide (theme: {theme})"

    @mcp.tool
    async def pptx_add_metrics_dashboard(
        title: str, metrics: list[dict[str, str]], theme: str | None = None, layout: str = "grid"
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
        from ..slide_templates import MetricsDashboard

        result = await manager.get()
        if not result:
            raise ValueError("No active presentation")
        prs, metadata = result

        # Get theme
        theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
        theme_dict = theme_obj.__dict__ if hasattr(theme_obj, "__dict__") else theme_obj

        # Use template to create slide
        template = MetricsDashboard(title=title, metrics=metrics, layout=layout, theme=theme_dict)
        slide_idx = template.render(prs)

        # Apply theme background only (components already have themed colors)
        if theme_obj:
            slide = prs.slides[slide_idx]
            theme_obj.apply_to_slide(slide, override_text_colors=False)

        await manager.update()
        return f"Added metrics dashboard with {len(metrics)} metrics at slide {slide_idx}"

    @mcp.tool
    async def pptx_add_content_grid(
        title: str,
        items: list[dict[str, str]],
        item_type: str = "card",
        columns: int = 2,
        theme: str | None = None,
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
        from ..slide_templates import ContentGridSlide

        result = await manager.get()
        if not result:
            raise ValueError("No active presentation")
        prs, metadata = result

        # Get theme
        theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
        theme_dict = theme_obj.__dict__ if hasattr(theme_obj, "__dict__") else theme_obj

        # Use template to create slide
        template = ContentGridSlide(
            title=title, items=items, item_type=item_type, columns=columns, theme=theme_dict
        )
        slide_idx = template.render(prs)

        # Apply theme background only (components already have themed colors)
        if theme_obj:
            slide = prs.slides[slide_idx]
            theme_obj.apply_to_slide(slide, override_text_colors=False)

        await manager.update()
        return f"Added content grid with {len(items)} {item_type}s in {columns} columns at slide {slide_idx}"

    @mcp.tool
    async def pptx_add_timeline_slide(
        title: str,
        events: list[dict[str, str]],
        orientation: str = "horizontal",
        theme: str | None = None,
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
        from ..slide_templates import TimelineSlide

        result = await manager.get()
        if not result:
            raise ValueError("No active presentation")
        prs, metadata = result

        # Get theme
        theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
        theme_dict = theme_obj.__dict__ if hasattr(theme_obj, "__dict__") else theme_obj

        # Use template to create slide
        template = TimelineSlide(
            title=title, events=events, orientation=orientation, theme=theme_dict
        )
        slide_idx = template.render(prs)

        # Apply theme background only (components already have themed colors)
        if theme_obj:
            slide = prs.slides[slide_idx]
            theme_obj.apply_to_slide(slide, override_text_colors=False)

        await manager.update()
        return f"Added timeline slide with {len(events)} events at slide {slide_idx}"

    @mcp.tool
    async def pptx_add_comparison_slide(
        title: str,
        left_title: str,
        left_items: list[str],
        right_title: str,
        right_items: list[str],
        theme: str | None = None,
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
        from ..slide_templates import ComparisonSlide

        result = await manager.get()
        if not result:
            raise ValueError("No active presentation")
        prs, metadata = result

        # Get theme
        theme_obj = theme_manager.get_theme(theme) if theme else theme_manager.get_theme("dark")
        theme_dict = theme_obj.__dict__ if hasattr(theme_obj, "__dict__") else theme_obj

        # Use template to create slide
        template = ComparisonSlide(
            title=title,
            left_title=left_title,
            left_items=left_items,
            right_title=right_title,
            right_items=right_items,
            theme=theme_dict,
        )
        slide_idx = template.render(prs)

        # Apply theme background only (components already have themed colors)
        if theme_obj:
            slide = prs.slides[slide_idx]
            theme_obj.apply_to_slide(slide, override_text_colors=False)

        await manager.update()
        return f"Added comparison slide: {left_title} vs {right_title} at slide {slide_idx}"

    @mcp.tool
    async def pptx_list_slide_templates(category: str | None = None) -> str:
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
        from ..slide_templates.registry import list_templates
        import json

        templates = list_templates(category)
        return json.dumps(templates, indent=2)

    @mcp.tool
    async def pptx_get_template_info(template_name: str) -> str:
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
        from ..slide_templates.registry import get_template_info
        import json

        info = get_template_info(template_name)
        if info is None:
            return json.dumps({"error": f"Template '{template_name}' not found"})
        return json.dumps(info, indent=2)

    # Store tools for return
    tools.update(
        {
            "pptx_create_quick_deck": pptx_create_quick_deck,
            "pptx_add_metrics_dashboard": pptx_add_metrics_dashboard,
            "pptx_add_content_grid": pptx_add_content_grid,
            "pptx_add_timeline_slide": pptx_add_timeline_slide,
            "pptx_add_comparison_slide": pptx_add_comparison_slide,
            "pptx_list_slide_templates": pptx_list_slide_templates,
            "pptx_get_template_info": pptx_get_template_info,
        }
    )

    return tools
