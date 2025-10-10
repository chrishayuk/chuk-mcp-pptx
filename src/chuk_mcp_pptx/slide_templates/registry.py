"""
Template Registry System

Provides decorator-based registration for slide templates, similar to the
component registry. Templates are self-documenting with metadata including
props, examples, and tags for LLM discovery.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


class TemplateCategory(Enum):
    """Categories for organizing slide templates."""
    OPENING = "opening"        # Title slides, intro slides
    CONTENT = "content"        # Content, bullet points
    DASHBOARD = "dashboard"    # Metrics, KPIs
    COMPARISON = "comparison"  # Side-by-side comparisons
    TIMELINE = "timeline"      # Timelines, roadmaps
    CLOSING = "closing"        # Thank you, contact slides
    LAYOUT = "layout"          # Generic layouts


@dataclass
class TemplateProp:
    """Metadata for a template property."""
    name: str
    type: str  # "string", "array", "object", "number", "boolean"
    description: str
    required: bool = True
    options: Optional[List[str]] = None
    default: Any = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required,
            "options": self.options,
            "default": self.default
        }


@dataclass
class TemplateMetadata:
    """Complete metadata for a registered template."""
    name: str
    category: TemplateCategory
    description: str
    props: List[TemplateProp]
    examples: List[Dict[str, Any]]
    tags: List[str]
    class_ref: type

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "props": [prop.to_dict() for prop in self.props],
            "examples": self.examples,
            "tags": self.tags
        }


# Global template registry
_TEMPLATE_REGISTRY: Dict[str, TemplateMetadata] = {}


def template(
    name: str,
    category: TemplateCategory,
    description: str,
    props: List[TemplateProp],
    examples: Optional[List[Dict[str, Any]]] = None,
    tags: Optional[List[str]] = None
):
    """
    Decorator to register a slide template.

    Args:
        name: Template name (used for lookup)
        category: Template category
        description: Human-readable description
        props: List of template properties
        examples: Example usage
        tags: Search tags

    Example:
        @template(
            name="MetricsDashboard",
            category=TemplateCategory.DASHBOARD,
            description="Dashboard with metric cards",
            props=[
                TemplateProp("title", "string", "Slide title"),
                TemplateProp("metrics", "array", "List of metrics")
            ],
            tags=["dashboard", "metrics"]
        )
        class MetricsDashboard(SlideTemplate):
            def render(self, prs):
                # Implementation
                pass
    """
    def decorator(cls):
        metadata = TemplateMetadata(
            name=name,
            category=category,
            description=description,
            props=props,
            examples=examples or [],
            tags=tags or [],
            class_ref=cls
        )
        _TEMPLATE_REGISTRY[name] = metadata
        cls._template_metadata = metadata
        return cls
    return decorator


def list_templates(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all registered templates.

    Args:
        category: Optional category filter

    Returns:
        List of template metadata dictionaries
    """
    templates = []

    for metadata in _TEMPLATE_REGISTRY.values():
        # Filter by category if specified
        if category and metadata.category.value != category:
            continue

        templates.append(metadata.to_dict())

    return templates


def get_template_info(name: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific template.

    Args:
        name: Template name

    Returns:
        Template metadata dictionary or None if not found
    """
    metadata = _TEMPLATE_REGISTRY.get(name)
    if not metadata:
        return None

    return metadata.to_dict()


def get_template(name: str) -> Optional[type]:
    """
    Get the template class by name.

    Args:
        name: Template name

    Returns:
        Template class or None if not found
    """
    metadata = _TEMPLATE_REGISTRY.get(name)
    if not metadata:
        return None

    return metadata.class_ref


def get_all_categories() -> List[str]:
    """
    Get list of all template categories.

    Returns:
        List of category values
    """
    return [cat.value for cat in TemplateCategory]
