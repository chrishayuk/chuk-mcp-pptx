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
- Connector: Arrows and connector lines
- Icon: Icon and visual indicators
- Image: Picture and image components
- Progress: Progress bars and loading indicators
- Shape: Geometric shapes and basic elements
- SmartArt: Diagram components (ProcessFlow, CycleDiagram, HierarchyDiagram)
- Table: Data tables with headers and rows
- Text: Text boxes and bullet lists
- Tile: Data display tiles
- Timeline: Timeline and sequence components
"""

from .alert import Alert
from .avatar import Avatar, AvatarWithLabel, AvatarGroup
from .badge import Badge, DotBadge, CountBadge
from .button import Button, IconButton, ButtonGroup
from .card import Card, MetricCard
from .connector import Connector
from .icon import Icon, IconList
from .image import Image
from .progress import ProgressBar
from .shape import Shape
from .smart_art import ProcessFlow, CycleDiagram, HierarchyDiagram
from .table import Table
from .text import TextBox, BulletList
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

    # Connector
    "Connector",

    # Icon
    "Icon",
    "IconList",

    # Image
    "Image",

    # Progress
    "ProgressBar",

    # Shape
    "Shape",

    # SmartArt
    "ProcessFlow",
    "CycleDiagram",
    "HierarchyDiagram",

    # Table
    "Table",

    # Text
    "TextBox",
    "BulletList",

    # Tile
    "Tile",
    "IconTile",
    "ValueTile",

    # Timeline
    "Timeline",
]
