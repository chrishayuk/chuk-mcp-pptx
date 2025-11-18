"""
MCP tools for component-based PowerPoint creation.
Provides async tools for ALL core components in the design system.

This module exposes the complete suite of shadcn-inspired components:
- UI Components: Alert, Avatar, Badge, Button, Card, Icon, Progress, Tile
- Layout Components: Shape, Connector, SmartArt, Timeline
- Content Components: Text, Table, Image
- Data Components: Charts (via separate chart_tools.py)
"""

# Import ALL core components
from ..components.core import (
    # UI Components
    Alert,
    Avatar,
    AvatarGroup,
    Badge,
    Button,
    Card,
    MetricCard,
    Icon,
    ProgressBar,
    Tile,
    Shape,
    Connector,
    ProcessFlow,
    Timeline,
    # Content Components
    TextBox,
    BulletList,
    Table,
    Image,
)

from ..themes.theme_manager import ThemeManager


def register_component_tools(mcp, manager):
    """
    Register ALL component-based tools with the MCP server.

    Args:
        mcp: ChukMCPServer instance
        manager: PresentationManager instance

    Returns:
        Dictionary of registered tools
    """
    tools = {}
    theme_manager = ThemeManager()

    def get_theme_dict(theme_name: str | None = None):
        """Helper to get theme dictionary."""
        theme_obj = theme_manager.get_theme(theme_name) if theme_name else None
        if not theme_obj:
            theme_obj = theme_manager.get_theme("dark")
        return theme_obj.__dict__ if hasattr(theme_obj, "__dict__") else theme_obj

    # ============================================================================
    # ALERT COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_alert(
        slide_index: int,
        message: str,
        left: float,
        top: float,
        variant: str = "info",
        title: str | None = None,
        width: float = 4.0,
        height: float = 1.0,
        theme: str | None = None,
    ) -> str:
        """
        Add an alert/notification component to a slide.

        Alerts display important messages with different severity levels.
        Perfect for warnings, errors, info messages, or success notifications.

        Args:
            slide_index: Index of the slide (0-based)
            message: Alert message text
            left: Left position in inches
            top: Top position in inches
            variant: Alert type (info, warning, error, success)
            title: Optional alert title
            width: Alert width in inches
            height: Alert height in inches
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_alert(
                slide_index=0,
                message="System maintenance scheduled for tonight",
                left=2.0,
                top=2.0,
                variant="warning",
                title="Maintenance Alert"
            )
        """

        async def _add_alert():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            alert = Alert(
                description=message, variant=variant, title=title, theme=get_theme_dict(theme)
            )
            alert.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {variant} alert to slide {slide_index}"

        return await _add_alert()

    # ============================================================================
    # AVATAR COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_avatar(
        slide_index: int,
        initials: str,
        left: float,
        top: float,
        size: float = 0.5,
        variant: str = "circle",
        theme: str | None = None,
    ) -> str:
        """
        Add an avatar component to a slide.

        Avatars display user identity with initials or icons.

        Args:
            slide_index: Index of the slide (0-based)
            initials: User initials (e.g., "JD" for John Doe)
            left: Left position in inches
            top: Top position in inches
            size: Avatar size in inches
            variant: Avatar shape (circle, square, rounded)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_avatar(
                slide_index=0,
                initials="JD",
                left=1.0,
                top=1.0,
                variant="circle"
            )
        """

        async def _add_avatar():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            avatar = Avatar(text=initials, size=size, variant=variant, theme=get_theme_dict(theme))
            avatar.render(slide, left, top)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added avatar to slide {slide_index}"

        return await _add_avatar()

    @mcp.tool
    async def pptx_add_avatar_group(
        slide_index: int,
        initials_list: list[str],
        left: float,
        top: float,
        size: float = 0.5,
        max_visible: int = 3,
        theme: str | None = None,
    ) -> str:
        """
        Add a group of overlapping avatars.

        Avatar groups show multiple users in a compact space.

        Args:
            slide_index: Index of the slide (0-based)
            initials_list: List of initials for each avatar
            left: Left position in inches
            top: Top position in inches
            size: Avatar size in inches
            max_visible: Maximum avatars to show before "+N"
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_avatar_group(
                slide_index=0,
                initials_list=["JD", "SM", "RJ", "AL"],
                left=2.0,
                top=1.0,
                max_visible=3
            )
        """

        async def _add_avatar_group():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            # Convert initials list to members format
            members = [{"text": initials} for initials in initials_list]
            group = AvatarGroup(
                members=members, size=size, max_display=max_visible, theme=get_theme_dict(theme)
            )
            group.render(slide, left, top)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added avatar group with {len(initials_list)} avatars to slide {slide_index}"

        return await _add_avatar_group()

    # ============================================================================
    # BADGE COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_badge(
        slide_index: int,
        text: str,
        left: float,
        top: float,
        variant: str = "default",
        theme: str | None = None,
    ) -> str:
        """
        Add a badge component to a slide.

        Badges are small labels for status, categories, or counts.

        Args:
            slide_index: Index of the slide (0-based)
            text: Badge text
            left: Left position in inches
            top: Top position in inches
            variant: Badge style (default, primary, secondary, success, warning, error)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_badge(
                slide_index=0,
                text="New",
                left=3.0,
                top=1.0,
                variant="success"
            )
        """

        async def _add_badge():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            badge = Badge(text=text, variant=variant, theme=get_theme_dict(theme))
            badge.render(slide, left, top)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {variant} badge to slide {slide_index}"

        return await _add_badge()

    # ============================================================================
    # BUTTON COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_button(
        slide_index: int,
        text: str,
        left: float,
        top: float,
        variant: str = "default",
        size: str = "md",
        width: float | None = None,
        height: float | None = None,
        theme: str | None = None,
    ) -> str:
        """
        Add a button component to a slide.

        Buttons are interactive action elements with multiple variants and sizes.

        Args:
            slide_index: Index of the slide (0-based)
            text: Button text
            left: Left position in inches
            top: Top position in inches
            variant: Button style (default, secondary, outline, ghost, destructive)
            size: Button size (sm, md, lg)
            width: Optional width override in inches
            height: Optional height override in inches
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_button(
                slide_index=0,
                text="Get Started",
                left=4.0,
                top=3.0,
                variant="default",
                size="lg"
            )
        """

        async def _add_button():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            button = Button(text=text, variant=variant, size=size, theme=get_theme_dict(theme))
            button.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {variant} button to slide {slide_index}"

        return await _add_button()

    # ============================================================================
    # CARD COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_card(
        slide_index: int,
        left: float,
        top: float,
        width: float = 3.0,
        height: float = 2.0,
        title: str | None = None,
        description: str | None = None,
        variant: str = "default",
        theme: str | None = None,
    ) -> str:
        """
        Add a card container component to a slide.

        Cards are versatile containers for grouping related content.

        Args:
            slide_index: Index of the slide (0-based)
            left: Left position in inches
            top: Top position in inches
            width: Card width in inches
            height: Card height in inches
            title: Optional card title
            description: Optional card description
            variant: Card style (default, bordered, elevated)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_card(
                slide_index=0,
                left=2.0,
                top=2.0,
                title="Features",
                description="Key capabilities",
                variant="elevated"
            )
        """

        async def _add_card():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            card = Card(variant=variant, theme=get_theme_dict(theme))
            if title:
                card.add_child(Card.Title(title))
            if description:
                card.add_child(Card.Description(description))
            card.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {variant} card to slide {slide_index}"

        return await _add_card()

    @mcp.tool
    async def pptx_add_metric_card(
        slide_index: int,
        label: str,
        value: str,
        left: float,
        top: float,
        change: str | None = None,
        trend: str | None = None,
        width: float = 2.0,
        height: float = 1.5,
        theme: str | None = None,
    ) -> str:
        """
        Add a metric/KPI card component to a slide.

        Metric cards display key performance indicators with optional trends.

        Args:
            slide_index: Index of the slide (0-based)
            label: Metric label (e.g., "Revenue")
            value: Metric value (e.g., "$1.2M")
            left: Left position in inches
            top: Top position in inches
            change: Optional change value (e.g., "+12%")
            trend: Trend direction (up, down, neutral)
            width: Card width in inches
            height: Card height in inches
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_metric_card(
                slide_index=0,
                label="Monthly Revenue",
                value="$45.2K",
                left=2.0,
                top=2.0,
                change="+12%",
                trend="up"
            )
        """

        async def _add_metric():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            metric = MetricCard(
                label=label, value=value, change=change, trend=trend, theme=get_theme_dict(theme)
            )
            metric.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added metric card '{label}' to slide {slide_index}"

        return await _add_metric()

    # ============================================================================
    # ICON COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_icon(
        slide_index: int,
        icon_type: str,
        left: float,
        top: float,
        size: float = 0.5,
        variant: str = "default",
        theme: str | None = None,
    ) -> str:
        """
        Add an icon component to a slide.

        Icons are visual indicators and symbolic representations.

        Args:
            slide_index: Index of the slide (0-based)
            icon_type: Icon type (check, cross, arrow, info, warning, etc.)
            left: Left position in inches
            top: Top position in inches
            size: Icon size in inches
            variant: Icon style (default, filled, outlined)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_icon(
                slide_index=0,
                icon_type="check",
                left=1.0,
                top=1.0,
                size=0.5,
                variant="filled"
            )
        """

        async def _add_icon():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            icon = Icon(icon=icon_type, size=size, variant=variant, theme=get_theme_dict(theme))
            icon.render(slide, left, top)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {icon_type} icon to slide {slide_index}"

        return await _add_icon()

    # ============================================================================
    # PROGRESS COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_progress_bar(
        slide_index: int,
        value: float,
        left: float,
        top: float,
        width: float = 4.0,
        height: float = 0.3,
        variant: str = "default",
        show_label: bool = True,
        theme: str | None = None,
    ) -> str:
        """
        Add a progress bar component to a slide.

        Progress bars visualize completion or loading states.

        Args:
            slide_index: Index of the slide (0-based)
            value: Progress value (0-100)
            left: Left position in inches
            top: Top position in inches
            width: Bar width in inches
            height: Bar height in inches
            variant: Bar style (default, success, warning, error)
            show_label: Whether to show percentage label
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_progress_bar(
                slide_index=0,
                value=75,
                left=2.0,
                top=3.0,
                variant="success"
            )
        """

        async def _add_progress():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            progress = ProgressBar(
                value=value,
                variant=variant,
                show_percentage=show_label,
                theme=get_theme_dict(theme),
            )
            progress.render(slide, left, top, width)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added progress bar ({value}%) to slide {slide_index}"

        return await _add_progress()

    # ============================================================================
    # TILE COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_tile(
        slide_index: int,
        label: str,
        value: str,
        left: float,
        top: float,
        width: float = 2.0,
        height: float = 1.5,
        variant: str = "default",
        theme: str | None = None,
    ) -> str:
        """
        Add a data tile component to a slide.

        Tiles display data values with labels in a compact format.

        Args:
            slide_index: Index of the slide (0-based)
            label: Tile label
            value: Tile value
            left: Left position in inches
            top: Top position in inches
            width: Tile width in inches
            height: Tile height in inches
            variant: Tile style (default, primary, secondary, accent)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_tile(
                slide_index=0,
                label="Active Users",
                value="1,234",
                left=1.0,
                top=2.0,
                variant="primary"
            )
        """

        async def _add_tile():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            tile = Tile(text=value, label=label, variant=variant, theme=get_theme_dict(theme))
            tile.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added tile '{label}' to slide {slide_index}"

        return await _add_tile()

    # ============================================================================
    # SHAPE COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_shape(
        slide_index: int,
        shape_type: str,
        left: float,
        top: float,
        width: float = 2.0,
        height: float = 2.0,
        fill_color: str | None = None,
        text: str | None = None,
        theme: str | None = None,
    ) -> str:
        """
        Add a shape component to a slide.

        Shapes include rectangles, circles, triangles, arrows, and more.

        Args:
            slide_index: Index of the slide (0-based)
            shape_type: Shape type (rectangle, circle, triangle, arrow, etc.)
            left: Left position in inches
            top: Top position in inches
            width: Shape width in inches
            height: Shape height in inches
            fill_color: Optional fill color (hex or semantic token)
            text: Optional text inside shape
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_shape(
                slide_index=0,
                shape_type="rectangle",
                left=2.0,
                top=2.0,
                width=3.0,
                height=2.0,
                text="Click here"
            )
        """

        async def _add_shape():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            shape = Shape(
                shape_type=shape_type, fill_color=fill_color, text=text, theme=get_theme_dict(theme)
            )
            shape.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {shape_type} shape to slide {slide_index}"

        return await _add_shape()

    # ============================================================================
    # CONNECTOR COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_connector(
        slide_index: int,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        connector_type: str = "straight",
        theme: str | None = None,
    ) -> str:
        """
        Add a connector line/arrow between two points.

        Connectors create visual relationships between elements.

        Args:
            slide_index: Index of the slide (0-based)
            start_x: Starting X position in inches
            start_y: Starting Y position in inches
            end_x: Ending X position in inches
            end_y: Ending Y position in inches
            connector_type: Connector style (straight, elbow, curved)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_connector(
                slide_index=0,
                start_x=2.0,
                start_y=2.0,
                end_x=5.0,
                end_y=3.0,
                connector_type="arrow"
            )
        """

        async def _add_connector():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            connector = Connector(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                connector_type=connector_type,
                theme=get_theme_dict(theme),
            )
            connector.render(slide)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added {connector_type} connector to slide {slide_index}"

        return await _add_connector()

    # ============================================================================
    # SMARTART COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_process_flow(
        slide_index: int,
        steps: list[str],
        left: float,
        top: float,
        width: float = 8.0,
        height: float = 2.0,
        orientation: str = "horizontal",
        theme: str | None = None,
    ) -> str:
        """
        Add a process flow diagram to a slide.

        Process flows show sequential steps with arrows.

        Args:
            slide_index: Index of the slide (0-based)
            steps: List of step descriptions
            left: Left position in inches
            top: Top position in inches
            width: Diagram width in inches
            height: Diagram height in inches
            orientation: Flow direction (horizontal, vertical)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_process_flow(
                slide_index=0,
                steps=["Research", "Design", "Develop", "Test", "Deploy"],
                left=1.0,
                top=2.0,
                orientation="horizontal"
            )
        """

        async def _add_flow():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            flow = ProcessFlow(items=steps, theme=get_theme_dict(theme))
            flow.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added process flow with {len(steps)} steps to slide {slide_index}"

        return await _add_flow()

    # ============================================================================
    # TIMELINE COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_timeline(
        slide_index: int,
        events: list[dict[str, str]],
        left: float,
        top: float,
        width: float = 8.0,
        height: float = 2.0,
        orientation: str = "horizontal",
        theme: str | None = None,
    ) -> str:
        """
        Add a timeline component to a slide.

        Timelines display chronological events with dates.

        Args:
            slide_index: Index of the slide (0-based)
            events: List of event dicts with 'date' and 'description' keys
            left: Left position in inches
            top: Top position in inches
            width: Timeline width in inches
            height: Timeline height in inches
            orientation: Timeline direction (horizontal, vertical)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_timeline(
                slide_index=0,
                events=[
                    {"date": "Q1 2024", "description": "Launch"},
                    {"date": "Q2 2024", "description": "Expansion"},
                    {"date": "Q3 2024", "description": "Scale"}
                ],
                left=1.0,
                top=2.0
            )
        """

        async def _add_timeline():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            timeline = Timeline(events=events, theme=get_theme_dict(theme))
            timeline.render(slide, left, top, width)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added timeline with {len(events)} events to slide {slide_index}"

        return await _add_timeline()

    # ============================================================================
    # TEXT COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_textbox(
        slide_index: int,
        text: str,
        left: float,
        top: float,
        width: float = 4.0,
        height: float = 1.0,
        font_size: int = 14,
        alignment: str = "left",
        theme: str | None = None,
    ) -> str:
        """
        Add a text box component to a slide.

        Text boxes display formatted text content.

        Args:
            slide_index: Index of the slide (0-based)
            text: Text content
            left: Left position in inches
            top: Top position in inches
            width: Text box width in inches
            height: Text box height in inches
            font_size: Font size in points
            alignment: Text alignment (left, center, right)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_textbox(
                slide_index=0,
                text="Important message here",
                left=2.0,
                top=3.0,
                font_size=18,
                alignment="center"
            )
        """

        async def _add_textbox():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            textbox = TextBox(
                text=text, font_size=font_size, alignment=alignment, theme=get_theme_dict(theme)
            )
            textbox.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added text box to slide {slide_index}"

        return await _add_textbox()

    @mcp.tool
    async def pptx_add_bullet_list(
        slide_index: int,
        items: list[str],
        left: float,
        top: float,
        width: float = 5.0,
        height: float = 3.0,
        theme: str | None = None,
    ) -> str:
        """
        Add a bullet list component to a slide.

        Bullet lists display items in a structured list format.

        Args:
            slide_index: Index of the slide (0-based)
            items: List of bullet point items
            left: Left position in inches
            top: Top position in inches
            width: List width in inches
            height: List height in inches
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_bullet_list(
                slide_index=0,
                items=["First point", "Second point", "Third point"],
                left=2.0,
                top=2.0
            )
        """

        async def _add_bullets():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            bullets = BulletList(items=items, theme=get_theme_dict(theme))
            bullets.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added bullet list with {len(items)} items to slide {slide_index}"

        return await _add_bullets()

    # ============================================================================
    # TABLE COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_table_component(
        slide_index: int,
        headers: list[str],
        rows: list[list[str]],
        left: float,
        top: float,
        width: float = 6.0,
        height: float = 3.0,
        variant: str = "default",
        theme: str | None = None,
    ) -> str:
        """
        Add a table component to a slide.

        Tables display structured data with headers and rows.

        Args:
            slide_index: Index of the slide (0-based)
            headers: Column headers
            rows: Data rows (list of lists)
            left: Left position in inches
            top: Top position in inches
            width: Table width in inches
            height: Table height in inches
            variant: Table style (default, striped, bordered)
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_table_component(
                slide_index=0,
                headers=["Product", "Q1", "Q2"],
                rows=[
                    ["Widget A", "$100K", "$120K"],
                    ["Widget B", "$80K", "$95K"]
                ],
                left=1.0,
                top=2.0
            )
        """

        async def _add_table():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            table = Table(headers=headers, data=rows, variant=variant, theme=get_theme_dict(theme))
            table.render(slide, left, top, width, height)

            # Apply presentation theme to the slide
            if metadata and metadata.theme:
                theme_obj = theme_manager.get_theme(metadata.theme)
                if theme_obj:
                    theme_obj.apply_to_slide(slide)

            # Update in VFS
            await manager.update()

            return f"Added table with {len(rows)} rows to slide {slide_index}"

        return await _add_table()

    # ============================================================================
    # IMAGE COMPONENTS
    # ============================================================================

    @mcp.tool
    async def pptx_add_image_component(
        slide_index: int,
        image_path: str,
        left: float,
        top: float,
        width: float | None = None,
        height: float | None = None,
        maintain_aspect: bool = True,
        theme: str | None = None,
    ) -> str:
        """
        Add an image component to a slide.

        Images display pictures with optional aspect ratio preservation.

        Args:
            slide_index: Index of the slide (0-based)
            image_path: Path to image file or base64 data URL
            left: Left position in inches
            top: Top position in inches
            width: Optional width in inches
            height: Optional height in inches
            maintain_aspect: Whether to preserve aspect ratio
            theme: Theme name to use

        Returns:
            Success message

        Example:
            await pptx_add_image_component(
                slide_index=0,
                image_path="path/to/image.png",
                left=2.0,
                top=2.0,
                width=4.0
            )
        """

        async def _add_image():
            result = await manager.get()
            if not result:
                raise ValueError("No presentation found. Create one first.")

            prs, metadata = result
            if slide_index >= len(prs.slides):
                raise ValueError(f"Slide index {slide_index} out of range")

            slide = prs.slides[slide_index]
            try:
                image = Image(image_source=image_path, theme=get_theme_dict(theme))
                await image.render(slide, left, top, width, height)

                # Apply presentation theme to the slide
                if metadata and metadata.theme:
                    theme_obj = theme_manager.get_theme(metadata.theme)
                    if theme_obj:
                        theme_obj.apply_to_slide(slide)

                # Update in VFS
                await manager.update()

                return f"Added image to slide {slide_index}"
            except FileNotFoundError as e:
                return f"Error adding image: {str(e)}"

        return await _add_image()

    # ============================================================================
    # THEME MANAGEMENT
    # ============================================================================
    # Theme tools have been moved to tools/theme_tools.py for better organization
    # Use: pptx_apply_theme, pptx_list_themes, pptx_create_custom_theme,
    #      pptx_apply_component_theme, pptx_list_component_themes

    # Store all tools for return
    tools.update(
        {
            # Alert
            "pptx_add_alert": pptx_add_alert,
            # Avatar
            "pptx_add_avatar": pptx_add_avatar,
            "pptx_add_avatar_group": pptx_add_avatar_group,
            # Badge
            "pptx_add_badge": pptx_add_badge,
            # Button
            "pptx_add_button": pptx_add_button,
            # Card
            "pptx_add_card": pptx_add_card,
            "pptx_add_metric_card": pptx_add_metric_card,
            # Icon
            "pptx_add_icon": pptx_add_icon,
            # Progress
            "pptx_add_progress_bar": pptx_add_progress_bar,
            # Tile
            "pptx_add_tile": pptx_add_tile,
            # Shape
            "pptx_add_shape": pptx_add_shape,
            # Connector
            "pptx_add_connector": pptx_add_connector,
            # SmartArt
            "pptx_add_process_flow": pptx_add_process_flow,
            # Timeline
            "pptx_add_timeline": pptx_add_timeline,
            # Text
            "pptx_add_textbox": pptx_add_textbox,
            "pptx_add_bullet_list": pptx_add_bullet_list,
            # Table
            "pptx_add_table_component": pptx_add_table_component,
            # Image
            "pptx_add_image_component": pptx_add_image_component,
        }
    )

    return tools
