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
- Container: Responsive container for centering and constraining content
- Divider: Visual divider line for separating content
- Grid: 12-column grid layout system
- Icon: Icon and visual indicators
- Image: Picture and image components
- Progress: Progress bars and loading indicators
- Video: Video and multimedia components
- Shape: Geometric shapes and basic elements
- SmartArt: Diagram components (ProcessFlow, CycleDiagram, HierarchyDiagram)
- Spacer: Invisible spacer for adding spacing between elements
- Stack: Stack elements vertically or horizontally with consistent spacing
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
from .container import Container
from .content_grid import ContentGrid
from .divider import Divider
from .grid import Grid
from .icon import Icon, IconList
from .image import Image
from .progress import ProgressBar
from .video import Video
from .shape import Shape
from .smart_art import ProcessFlow, CycleDiagram, HierarchyDiagram
from .spacer import Spacer
from .stack import Stack
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
    # Container
    "Container",
    # ContentGrid
    "ContentGrid",
    # Divider
    "Divider",
    # Grid
    "Grid",
    # Icon
    "Icon",
    "IconList",
    # Image
    "Image",
    # Progress
    "ProgressBar",
    # Video
    "Video",
    # Shape
    "Shape",
    # SmartArt
    "ProcessFlow",
    "CycleDiagram",
    "HierarchyDiagram",
    # Spacer
    "Spacer",
    # Stack
    "Stack",
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
