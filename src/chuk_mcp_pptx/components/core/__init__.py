# src/chuk_mcp_pptx/components/core/__init__.py
"""
Core UI Components
=================

Fundamental UI building blocks for presentations.

Components:
- Alert: Notification and message components
- Avatar: User profile and identity components
- Badge: Status indicators and labels
- Button: Interactive action buttons
- Card: Container components with structured content
- Icon: Icon and visual indicators
- Progress: Progress bars and loading indicators
- Tile: Data display tiles
- Timeline: Timeline and sequence components
"""

from .alert import Alert
from .avatar import Avatar, AvatarWithLabel, AvatarGroup
from .badge import Badge, DotBadge, CountBadge
from .button import Button, IconButton, ButtonGroup
from .card import Card, MetricCard
from .icon import Icon, IconList
from .progress import ProgressBar
from .tile import Tile, IconTile, ValueTile
from .timeline import Timeline

__all__ = [
    # Alert
    "Alert",

    # Avatar
    "Avatar",
    "AvatarWithLabel",
    "AvatarGroup",

    # Badge
    "Badge",
    "DotBadge",
    "CountBadge",

    # Button
    "Button",
    "IconButton",
    "ButtonGroup",

    # Card
    "Card",
    "MetricCard",

    # Icon
    "Icon",
    "IconList",

    # Progress
    "ProgressBar",

    # Tile
    "Tile",
    "IconTile",
    "ValueTile",

    # Timeline
    "Timeline",
]
