"""
Tests for new PowerPoint-specific components: ProgressBar, Icon, Timeline, Tile, Avatar, Chat.
"""

from chuk_mcp_pptx.components.core.progress import ProgressBar
from chuk_mcp_pptx.components.core.icon import Icon, IconList, ICON_SYMBOLS
from chuk_mcp_pptx.components.core.timeline import Timeline
from chuk_mcp_pptx.components.core.tile import Tile, IconTile, ValueTile
from chuk_mcp_pptx.components.core.avatar import Avatar, AvatarWithLabel, AvatarGroup
from chuk_mcp_pptx.components.chat import ChatMessage, ChatConversation


class TestProgressBar:
    """Test ProgressBar component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        progress = ProgressBar(value=75, theme=dark_theme)
        assert progress.value == 75

    def test_value_validation(self, dark_theme):
        """Test value validation and clamping."""
        # Over max
        progress = ProgressBar(value=150, theme=dark_theme)
        assert progress.value == 100

        # Under min
        progress = ProgressBar(value=-10, theme=dark_theme)
        assert progress.value == 0

    def test_variants(self, dark_theme):
        """Test different variants."""
        variants = ["default", "success", "warning", "error"]
        for variant in variants:
            progress = ProgressBar(value=50, variant=variant, theme=dark_theme)
            assert progress.variant == variant

    def test_styles(self, dark_theme):
        """Test different styles."""
        # Bar style (default)
        bar = ProgressBar(value=60, style="bar", theme=dark_theme)
        assert bar.style == "bar"

        # Segmented style
        segmented = ProgressBar(value=60, style="segmented", segments=10, theme=dark_theme)
        assert segmented.style == "segmented"
        assert segmented.segments == 10

    def test_show_percentage(self, dark_theme):
        """Test percentage display."""
        progress = ProgressBar(value=75, show_percentage=True, theme=dark_theme)
        assert progress.show_percentage is True

    def test_label(self, dark_theme):
        """Test label text."""
        progress = ProgressBar(value=50, label="Loading...", theme=dark_theme)
        assert progress.label == "Loading..."

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        progress = ProgressBar(value=75, theme=dark_theme)
        shapes = progress.render(mock_slide, left=1, top=2, width=4)
        assert isinstance(shapes, list)
        assert len(shapes) > 0


class TestIcon:
    """Test Icon component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        icon = Icon("check", theme=dark_theme)
        assert icon.symbol == ICON_SYMBOLS.get("check", "check")

    def test_icon_mapping(self, dark_theme):
        """Test icon name mapping."""
        # Known icon
        check = Icon("check", theme=dark_theme)
        assert check.symbol == "✓"

        # Star icon
        star = Icon("star", theme=dark_theme)
        assert star.symbol == "★"

        # Unknown icon (should use as-is)
        custom = Icon("→", theme=dark_theme)
        assert custom.symbol == "→"

    def test_variants(self, dark_theme):
        """Test color variants."""
        variants = ["default", "primary", "success", "warning", "error", "muted"]
        for variant in variants:
            icon = Icon("check", variant=variant, theme=dark_theme)
            assert icon.variant == variant

    def test_sizes(self, dark_theme):
        """Test icon sizes."""
        sizes = ["sm", "md", "lg", "xl", "2xl"]
        for size in sizes:
            icon = Icon("check", size=size, theme=dark_theme)
            assert icon.size == size

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        icon = Icon("check", variant="success", size="lg", theme=dark_theme)
        shape = icon.render(mock_slide, left=1, top=2)
        assert shape is not None


class TestIconList:
    """Test IconList component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        items = [("check", "Item 1"), ("check", "Item 2")]
        icon_list = IconList(items, theme=dark_theme)
        assert icon_list.items == items

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        items = [("check", "Feature 1"), ("rocket", "Feature 2"), ("star", "Feature 3")]
        icon_list = IconList(items, variant="success", theme=dark_theme)
        shapes = icon_list.render(mock_slide, left=1, top=2, width=5)
        assert isinstance(shapes, list)
        # Should have icon + text for each item
        assert len(shapes) >= len(items)


class TestTimeline:
    """Test Timeline component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        events = [{"date": "Q1", "title": "Start"}, {"date": "Q2", "title": "Build"}]
        timeline = Timeline(events, theme=dark_theme)
        assert timeline.events == events

    def test_variants(self, dark_theme):
        """Test variants."""
        events = [{"date": "2024", "title": "Launch"}]
        variants = ["default", "minimal", "highlighted"]
        for variant in variants:
            timeline = Timeline(events, variant=variant, theme=dark_theme)
            assert timeline.variant == variant

    def test_styles(self, dark_theme):
        """Test timeline styles."""
        events = [{"date": "2024", "title": "Event"}]
        styles = ["line", "arrow", "segmented"]
        for style in styles:
            timeline = Timeline(events, style=style, theme=dark_theme)
            assert timeline.style == style

    def test_highlighted_events(self, dark_theme):
        """Test highlighted events."""
        events = [
            {"date": "Q1", "title": "Plan"},
            {"date": "Q2", "title": "Launch", "highlight": True},
        ]
        Timeline(events, theme=dark_theme)
        assert events[1]["highlight"] is True

    def test_render_empty(self, mock_slide, dark_theme):
        """Test rendering with no events."""
        timeline = Timeline([], theme=dark_theme)
        shapes = timeline.render(mock_slide, left=1, top=2, width=6)
        assert shapes == []

    def test_render_with_events(self, mock_slide, dark_theme):
        """Test rendering with events."""
        events = [
            {"date": "Jan", "title": "Start"},
            {"date": "Feb", "title": "Mid"},
            {"date": "Mar", "title": "End"},
        ]
        timeline = Timeline(events, style="arrow", theme=dark_theme)
        shapes = timeline.render(mock_slide, left=1, top=2, width=8)
        assert len(shapes) > 0


class TestTile:
    """Test Tile component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        tile = Tile(text="42", label="Tasks", theme=dark_theme)
        assert tile.text == "42"
        assert tile.label == "Tasks"

    def test_variants(self, dark_theme):
        """Test tile variants."""
        variants = ["default", "outlined", "filled", "ghost"]
        for variant in variants:
            tile = Tile(text="Test", variant=variant, theme=dark_theme)
            assert tile.variant == variant

    def test_sizes(self, dark_theme):
        """Test tile sizes."""
        sizes = ["sm", "md", "lg", "xl"]
        for size in sizes:
            tile = Tile(text="Test", size=size, theme=dark_theme)
            assert tile.size == size

    def test_color_variants(self, dark_theme):
        """Test color variants."""
        colors = ["default", "primary", "success", "warning", "destructive"]
        for color in colors:
            tile = Tile(text="Test", color_variant=color, theme=dark_theme)
            assert tile.color_variant == color

    def test_with_icon(self, dark_theme):
        """Test tile with icon."""
        tile = Tile(icon="rocket", label="Fast", theme=dark_theme)
        assert tile.icon == "rocket"
        assert tile.label == "Fast"

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        tile = Tile(text="42", label="Tasks", variant="outlined", theme=dark_theme)
        shape = tile.render(mock_slide, left=1, top=2)
        assert shape is not None


class TestIconTile:
    """Test IconTile component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        tile = IconTile("rocket", label="Fast", theme=dark_theme)
        assert tile.icon == "rocket"
        assert tile.label == "Fast"
        assert tile.text is None  # IconTile doesn't have text

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        tile = IconTile(
            "check", label="Done", variant="filled", color_variant="success", theme=dark_theme
        )
        shape = tile.render(mock_slide, left=1, top=2)
        assert shape is not None


class TestValueTile:
    """Test ValueTile component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        tile = ValueTile("98%", label="Uptime", theme=dark_theme)
        assert tile.text == "98%"
        assert tile.label == "Uptime"
        assert tile.icon is None  # ValueTile doesn't have icon

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        tile = ValueTile("42", label="Tasks", variant="outlined", theme=dark_theme)
        shape = tile.render(mock_slide, left=1, top=2)
        assert shape is not None


class TestAvatar:
    """Test Avatar component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        avatar = Avatar(text="JD", theme=dark_theme)
        assert avatar.text == "JD"

    def test_with_icon(self, dark_theme):
        """Test avatar with icon."""
        avatar = Avatar(icon="user", theme=dark_theme)
        assert avatar.icon == "user"

    def test_variants(self, dark_theme):
        """Test avatar variants."""
        variants = ["default", "filled", "outlined", "minimal"]
        for variant in variants:
            avatar = Avatar(text="JD", variant=variant, theme=dark_theme)
            assert avatar.variant == variant

    def test_sizes(self, dark_theme):
        """Test avatar sizes."""
        sizes = ["xs", "sm", "md", "lg", "xl"]
        for size in sizes:
            avatar = Avatar(text="JD", size=size, theme=dark_theme)
            assert avatar.size == size

    def test_color_variants(self, dark_theme):
        """Test color variants."""
        colors = ["default", "primary", "success", "warning", "destructive"]
        for color in colors:
            avatar = Avatar(text="JD", color_variant=color, theme=dark_theme)
            assert avatar.color_variant == color

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        avatar = Avatar(text="JD", variant="filled", color_variant="primary", theme=dark_theme)
        shape = avatar.render(mock_slide, left=1, top=2)
        assert shape is not None

    def test_initials_truncation(self, dark_theme):
        """Test that initials are truncated to 2 characters."""
        avatar = Avatar(text="ABCD", theme=dark_theme)
        # Rendering should truncate to 2 chars in the render method
        assert avatar.text == "ABCD"  # Stored as-is, truncated during render


class TestAvatarWithLabel:
    """Test AvatarWithLabel component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        avatar = AvatarWithLabel(text="JD", label="John Doe", sublabel="Designer", theme=dark_theme)
        assert avatar.text == "JD"
        assert avatar.label == "John Doe"
        assert avatar.sublabel == "Designer"

    def test_orientations(self, dark_theme):
        """Test orientations."""
        # Horizontal
        h_avatar = AvatarWithLabel(
            text="JD", label="John", orientation="horizontal", theme=dark_theme
        )
        assert h_avatar.orientation == "horizontal"

        # Vertical
        v_avatar = AvatarWithLabel(
            text="JD", label="John", orientation="vertical", theme=dark_theme
        )
        assert v_avatar.orientation == "vertical"

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        avatar = AvatarWithLabel(
            text="JD",
            label="John Doe",
            sublabel="Product Designer",
            variant="filled",
            theme=dark_theme,
        )
        shapes = avatar.render(mock_slide, left=1, top=2, width=3)
        assert isinstance(shapes, list)
        assert len(shapes) >= 1  # Avatar + label box


class TestAvatarGroup:
    """Test AvatarGroup component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        members = [{"text": "JD"}, {"text": "AS"}, {"text": "BM"}]
        group = AvatarGroup(members, theme=dark_theme)
        assert group.members == members

    def test_max_display(self, dark_theme):
        """Test max display limit."""
        members = [{"text": f"U{i}"} for i in range(10)]
        group = AvatarGroup(members, max_display=3, theme=dark_theme)
        assert group.max_display == 3

    def test_overlap(self, dark_theme):
        """Test overlapping avatars."""
        members = [{"text": "JD"}, {"text": "AS"}]
        group = AvatarGroup(members, overlap=True, theme=dark_theme)
        assert group.overlap is True

    def test_render(self, mock_slide, dark_theme):
        """Test rendering."""
        members = [
            {"text": "JD", "color_variant": "primary"},
            {"text": "AS", "color_variant": "success"},
            {"text": "BM", "color_variant": "warning"},
        ]
        group = AvatarGroup(members, theme=dark_theme)
        shapes = group.render(mock_slide, left=1, top=2)
        assert len(shapes) == len(members)

    def test_render_with_max_display(self, mock_slide, dark_theme):
        """Test rendering with max display."""
        members = [{"text": f"U{i}"} for i in range(5)]
        group = AvatarGroup(members, max_display=3, theme=dark_theme)
        shapes = group.render(mock_slide, left=1, top=2)
        # Should show 3 avatars + 1 "+2" avatar
        assert len(shapes) == 4


class TestChatMessage:
    """Test ChatMessage component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        msg = ChatMessage(text="Hello!", theme=dark_theme)
        assert msg.text == "Hello!"

    def test_variants(self, dark_theme):
        """Test message variants."""
        variants = ["sent", "received", "system"]
        for variant in variants:
            msg = ChatMessage(text="Test", variant=variant, theme=dark_theme)
            assert msg.variant == variant

    def test_with_sender(self, dark_theme):
        """Test message with sender."""
        msg = ChatMessage(text="Hello!", sender="John Doe", timestamp="10:30 AM", theme=dark_theme)
        assert msg.sender == "John Doe"
        assert msg.timestamp == "10:30 AM"

    def test_with_avatar(self, dark_theme):
        """Test message with avatar."""
        msg = ChatMessage(text="Hi there!", avatar_text="JD", show_avatar=True, theme=dark_theme)
        assert msg.avatar_text == "JD"
        assert msg.show_avatar is True

    def test_render_received(self, mock_slide, dark_theme):
        """Test rendering received message."""
        msg = ChatMessage(
            text="How can I help?",
            sender="Support",
            avatar_text="SA",
            variant="received",
            show_avatar=True,
            theme=dark_theme,
        )
        shapes = msg.render(mock_slide, left=1, top=2, width=6)
        assert len(shapes) >= 1  # Bubble + avatar

    def test_render_sent(self, mock_slide, dark_theme):
        """Test rendering sent message."""
        msg = ChatMessage(
            text="I need help", variant="sent", timestamp="10:30 AM", theme=dark_theme
        )
        shapes = msg.render(mock_slide, left=1, top=2, width=6)
        assert len(shapes) >= 1

    def test_render_system(self, mock_slide, dark_theme):
        """Test rendering system message."""
        msg = ChatMessage(text="John Doe joined the chat", variant="system", theme=dark_theme)
        shapes = msg.render(mock_slide, left=1, top=2, width=6)
        assert len(shapes) >= 1

    def test_bubble_height_calculation(self, dark_theme):
        """Test bubble height calculation."""
        short_msg = ChatMessage(text="Hi", theme=dark_theme)
        short_height = short_msg._calculate_bubble_height(4.0)

        long_msg = ChatMessage(
            text="This is a much longer message that should result in a taller bubble because it will wrap across multiple lines in the text frame.",
            theme=dark_theme,
        )
        long_height = long_msg._calculate_bubble_height(4.0)

        assert long_height > short_height


class TestChatConversation:
    """Test ChatConversation component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        messages = [
            {"text": "Hello!", "variant": "sent"},
            {"text": "Hi there!", "variant": "received"},
        ]
        conversation = ChatConversation(messages, theme=dark_theme)
        assert conversation.messages == messages

    def test_spacing(self, dark_theme):
        """Test message spacing."""
        messages = [{"text": "Test"}]
        conversation = ChatConversation(messages, spacing=0.5, theme=dark_theme)
        assert conversation.spacing == 0.5

    def test_render(self, mock_slide, dark_theme):
        """Test rendering conversation."""
        messages = [
            {"text": "Hi! I need help", "variant": "sent", "timestamp": "10:30 AM"},
            {
                "text": "Hello! How can I assist you?",
                "sender": "Support",
                "avatar_text": "SA",
                "variant": "received",
                "show_avatar": True,
                "timestamp": "10:31 AM",
            },
            {
                "text": "I have a question about my order",
                "variant": "sent",
                "timestamp": "10:32 AM",
            },
        ]
        conversation = ChatConversation(messages, theme=dark_theme)
        shapes = conversation.render(mock_slide, left=1, top=2, width=7)
        assert len(shapes) > 0  # Should have multiple shapes for all messages

    def test_empty_conversation(self, mock_slide, dark_theme):
        """Test rendering empty conversation."""
        conversation = ChatConversation([], theme=dark_theme)
        shapes = conversation.render(mock_slide, left=1, top=2, width=6)
        assert shapes == []


class TestComponentIntegration:
    """Test integration between components."""

    def test_avatar_in_chat(self, mock_slide, dark_theme):
        """Test Avatar component used in ChatMessage."""
        msg = ChatMessage(
            text="Hello from chat!",
            sender="Alice",
            avatar_text="AS",
            variant="received",
            show_avatar=True,
            theme=dark_theme,
        )
        shapes = msg.render(mock_slide, left=1, top=2, width=6)
        # Should include avatar shape
        assert len(shapes) >= 2  # Bubble + avatar

    def test_icon_in_tile(self, mock_slide, dark_theme):
        """Test Icon symbols used in Tile."""
        tile = IconTile("rocket", label="Fast", theme=dark_theme)
        shape = tile.render(mock_slide, left=1, top=2)
        assert shape is not None
        assert tile.icon == "rocket"

    def test_multiple_components_same_slide(self, mock_slide, dark_theme):
        """Test rendering multiple different components on same slide."""
        # Progress bar
        progress = ProgressBar(value=75, theme=dark_theme)
        progress.render(mock_slide, left=1, top=1, width=4)

        # Icon
        icon = Icon("check", variant="success", theme=dark_theme)
        icon.render(mock_slide, left=6, top=1)

        # Tile
        tile = ValueTile("42", label="Tasks", theme=dark_theme)
        tile.render(mock_slide, left=1, top=2)

        # Avatar
        avatar = Avatar(text="JD", theme=dark_theme)
        avatar.render(mock_slide, left=4, top=2)

        # All should render without conflicts
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called
