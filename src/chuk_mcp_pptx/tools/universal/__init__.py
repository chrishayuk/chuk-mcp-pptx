"""
Universal Component API

Single unified API for adding components anywhere:
- Free-form positioning
- Into placeholders (template-aware)
- Into other components (composition)
- Into layout regions (grid/flex)
"""

from .api import register_universal_component_api
from .registry import register_registry_tools
from .semantic import register_semantic_tools

__all__ = [
    "register_universal_component_api",
    "register_registry_tools",
    "register_semantic_tools",
]
