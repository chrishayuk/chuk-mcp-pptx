"""
PowerPoint components library.
Provides reusable, theme-aware components for presentations.
"""

from .base import Component, AsyncComponent
from .button import Button, IconButton, ButtonGroup
from .card import Card, MetricCard
from .badge import Badge, DotBadge, CountBadge
from .alert import Alert
from .code import CodeBlock, InlineCode, Terminal

__all__ = [
    # Base
    'Component',
    'AsyncComponent',

    # Buttons
    'Button',
    'IconButton',
    'ButtonGroup',

    # Cards
    'Card',
    'MetricCard',

    # Badges
    'Badge',
    'DotBadge',
    'CountBadge',

    # Alerts
    'Alert',

    # Code
    'CodeBlock',
    'InlineCode',
    'Terminal',
]