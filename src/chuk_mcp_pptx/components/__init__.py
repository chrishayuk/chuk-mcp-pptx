"""
PowerPoint components library.
Provides reusable, theme-aware components for presentations.
"""

from .base import Component, AsyncComponent
from .code import CodeBlock, InlineCode, Terminal

# Component infrastructure
from .registry import ComponentRegistry, registry, get_component_class
from .tracking import ComponentTracker, component_tracker, ComponentInstance

# Core UI components
from .core import (
    Alert,
    Avatar,
    AvatarWithLabel,
    AvatarGroup,
    Badge,
    DotBadge,
    CountBadge,
    Button,
    IconButton,
    ButtonGroup,
    Card,
    MetricCard,
    Icon,
    IconList,
    Image,
    Video,
    ProgressBar,
    Tile,
    IconTile,
    ValueTile,
    Timeline,
)
from .chat import (
    ChatMessage,
    ChatConversation,
    iMessageBubble,
    iMessageConversation,
    AndroidMessageBubble,
    AndroidConversation,
    WhatsAppBubble,
    WhatsAppConversation,
    ChatGPTMessage,
    ChatGPTConversation,
    SlackMessage,
    SlackConversation,
    TeamsMessage,
    TeamsConversation,
    FacebookMessengerBubble,
    FacebookMessengerConversation,
    AIMBubble,
    AIMConversation,
    MSNBubble,
    MSNConversation,
)
from .containers import (
    iPhoneContainer,
    SamsungContainer,
    BrowserWindow,
    MacOSWindow,
    WindowsWindow,
    ChatContainer,
)

# Chart components - import to register with decorator
from .charts import (
    ColumnChart,
    BarChart,
    WaterfallChart,
    LineChart,
    AreaChart,
    SparklineChart,
    PieChart,
    DoughnutChart,
)

__all__ = [
    # Base
    "Component",
    "AsyncComponent",
    # Infrastructure
    "ComponentRegistry",
    "registry",
    "get_component_class",
    "ComponentTracker",
    "component_tracker",
    "ComponentInstance",
    # Buttons
    "Button",
    "IconButton",
    "ButtonGroup",
    # Cards
    "Card",
    "MetricCard",
    # Badges
    "Badge",
    "DotBadge",
    "CountBadge",
    # Alerts
    "Alert",
    # Code
    "CodeBlock",
    "InlineCode",
    "Terminal",
    # Progress
    "ProgressBar",
    # Icons
    "Icon",
    "IconList",
    # Media
    "Image",
    "Video",
    # Timeline
    "Timeline",
    # Tiles
    "Tile",
    "IconTile",
    "ValueTile",
    # Avatars
    "Avatar",
    "AvatarWithLabel",
    "AvatarGroup",
    # Chat - Generic
    "ChatMessage",
    "ChatConversation",
    # Chat - Mobile Platforms
    "iMessageBubble",
    "iMessageConversation",
    "AndroidMessageBubble",
    "AndroidConversation",
    "WhatsAppBubble",
    "WhatsAppConversation",
    "FacebookMessengerBubble",
    "FacebookMessengerConversation",
    # Chat - AI & Workplace
    "ChatGPTMessage",
    "ChatGPTConversation",
    "SlackMessage",
    "SlackConversation",
    "TeamsMessage",
    "TeamsConversation",
    # Chat - Legacy/Nostalgic
    "AIMBubble",
    "AIMConversation",
    "MSNBubble",
    "MSNConversation",
    # Containers - Mobile
    "iPhoneContainer",
    "SamsungContainer",
    # Containers - Desktop/Windows
    "BrowserWindow",
    "MacOSWindow",
    "WindowsWindow",
    # Containers - Generic
    "ChatContainer",
    # Charts
    "ColumnChart",
    "BarChart",
    "WaterfallChart",
    "LineChart",
    "AreaChart",
    "SparklineChart",
    "PieChart",
    "DoughnutChart",
]
