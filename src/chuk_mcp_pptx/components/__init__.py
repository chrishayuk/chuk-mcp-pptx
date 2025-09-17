"""
PowerPoint components library.
Provides reusable, theme-aware components for presentations.
"""

from .base import Component, AsyncComponent
from .button import Button, IconButton
from .card import Card, MetricCard, FeatureCard
from .chart import Chart, BarChart, LineChart, PieChart
from .code import CodeBlock, Terminal

__all__ = [
    # Base
    'Component',
    'AsyncComponent',
    
    # Buttons
    'Button',
    'IconButton',
    
    # Cards
    'Card',
    'MetricCard', 
    'FeatureCard',
    
    # Charts
    'Chart',
    'BarChart',
    'LineChart',
    'PieChart',
    
    # Code
    'CodeBlock',
    'Terminal',
]