"""
Theme system for PowerPoint presentations.
"""

from .theme_manager import ThemeManager, Theme
from .design_system import (
    ResolvedDesignSystem,
    resolve_design_system,
    extract_template_design_system,
    extract_placeholder_styles,
)

__all__ = [
    "ThemeManager",
    "Theme",
    "ResolvedDesignSystem",
    "resolve_design_system",
    "extract_template_design_system",
    "extract_placeholder_styles",
]
