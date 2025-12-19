"""
Slide Templates Module

Provides a registry-based system for creating complete slides with automatic
layout using the Grid system and design system components.

Templates are discovered via decorators and can be:
- Queried by LLMs for available options
- Used directly in Python code
- Invoked via MCP semantic tools

All templates use Grid-based positioning (no hardcoded inches).
"""

from .registry import (
    template,
    TemplateCategory,
    TemplateProp,
    TemplateMetadata,
    list_templates,
    get_template_info,
    get_template,
)
from .base import SlideTemplate

# Import templates to trigger registration
from .dashboard import MetricsDashboard
from .comparison import ComparisonSlide
from .timeline import TimelineSlide
from .content_grid import ContentGridSlide

__all__ = [
    # Registry
    "template",
    "TemplateCategory",
    "TemplateProp",
    "TemplateMetadata",
    "list_templates",
    "get_template_info",
    "get_template",
    # Base
    "SlideTemplate",
    # Templates
    "MetricsDashboard",
    "ComparisonSlide",
    "TimelineSlide",
    "ContentGridSlide",
]
