"""
Component registry with schema support for LLM consumption.
Provides discovery, documentation, and validation for PowerPoint components.
"""

from __future__ import annotations

from typing import Any, Type, List, Dict
from enum import Enum
import json
import inspect
from pydantic import BaseModel, Field, create_model
from collections import defaultdict


class ComponentCategory(str, Enum):
    """Component categories for organization."""

    LAYOUT = "layout"
    UI = "ui"
    CHART = "chart"
    DATA = "data"
    TEXT = "text"
    MEDIA = "media"
    CONTAINER = "container"


class PropDefinition(BaseModel):
    """Definition of a component property."""

    name: str = Field(..., description="Property name")
    type: str = Field(..., description="Property type")
    description: str = Field(..., description="Property description")
    required: bool = Field(default=False, description="Whether property is required")
    default: Any | None = Field(None, description="Default value if any")
    options: list[Any] | None = Field(None, description="Valid options/choices")
    example: Any | None = Field(None, description="Example value")

    class Config:
        extra = "forbid"


class ComponentMetadata(BaseModel):
    """Metadata for a registered component."""

    name: str = Field(..., description="Component name")
    component_class: Type = Field(..., description="Component class reference")
    category: ComponentCategory = Field(..., description="Component category")
    description: str = Field(..., description="Component description")
    props: list[PropDefinition] = Field(default_factory=list, description="Component properties")
    examples: list[dict[str, Any]] = Field(default_factory=list, description="Usage examples")
    variants: dict[str, list[str]] | None = Field(None, description="Available variants")
    composition: dict[str, Any] | None = Field(None, description="Composition patterns")
    tags: list[str] = Field(default_factory=list, description="Searchable tags")
    version: str = Field(default="1.0.0", description="Component version")

    class Config:
        extra = "forbid"
        arbitrary_types_allowed = True  # Allow Type in component_class


class ComponentRegistry:
    """
    Central registry for PowerPoint components.
    Provides LLM-friendly schemas and discovery.
    """

    def __init__(self):
        self._components: dict[str, ComponentMetadata] = {}
        self._categories: dict[ComponentCategory, list[str]] = defaultdict(list)
        self._tags: dict[str, list[str]] = defaultdict(list)

    def register(
        self,
        name: str,
        component_class: Type,
        category: ComponentCategory,
        description: str,
        props: list[PropDefinition],
        examples: list[dict[str, Any]] | None = None,
        variants: dict[str, list[str]] | None = None,
        composition: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        version: str = "1.0.0",
    ) -> ComponentMetadata:
        """
        Register a component with the registry.

        Args:
            name: Unique component name
            component_class: Component class
            category: Component category
            description: Human-readable description
            props: List of property definitions
            examples: Example usage
            variants: Available variants
            composition: Composition support info
            tags: Searchable tags
            version: Component version

        Returns:
            ComponentMetadata
        """
        metadata = ComponentMetadata(
            name=name,
            component_class=component_class,
            category=category,
            description=description,
            props=props,
            examples=examples or [],
            variants=variants,
            composition=composition,
            tags=tags or [],
            version=version,
        )

        self._components[name] = metadata
        self._categories[category].append(name)

        for tag in tags or []:
            self._tags[tag].append(name)

        return metadata

    def get(self, name: str) -> ComponentMetadata | None:
        """Get component metadata by name."""
        return self._components.get(name)

    def list_components(self) -> list[str]:
        """List all registered component names."""
        return list(self._components.keys())

    def list_by_category(self, category: ComponentCategory) -> list[str]:
        """List components in a category."""
        return self._categories.get(category, [])

    def search(self, query: str) -> list[ComponentMetadata]:
        """
        Search components by name, description, or tags.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching component metadata
        """
        query = query.lower()
        results = []

        for name, metadata in self._components.items():
            # Search in name
            if query in name.lower():
                results.append(metadata)
                continue

            # Search in description
            if query in metadata.description.lower():
                results.append(metadata)
                continue

            # Search in tags
            if any(query in tag.lower() for tag in metadata.tags):
                results.append(metadata)
                continue

        return results

    def get_schema(self, name: str) -> dict[str, Any] | None:
        """
        Get JSON schema for a component.

        Args:
            name: Component name

        Returns:
            JSON schema dict or None
        """
        metadata = self.get(name)
        if not metadata:
            return None

        # Build Pydantic model schema
        props_schema = {}
        required_fields = []

        for prop in metadata.props:
            field_info = Field(
                default=prop.default if not prop.required else ..., description=prop.description
            )

            # Map type strings to Python types
            type_map = {
                "string": str,
                "number": float,
                "integer": int,
                "boolean": bool,
                "array": List,
                "object": Dict,
            }

            prop_type = type_map.get(prop.type, Any)

            # Handle options (enum)
            if prop.options:
                from enum import Enum

                prop_type = Enum(f"{prop.name}Enum", {opt: opt for opt in prop.options})

            props_schema[prop.name] = (prop_type, field_info)

            if prop.required:
                required_fields.append(prop.name)

        # Create dynamic Pydantic model
        DynamicModel = create_model(f"{name}Props", **props_schema)

        return {
            "name": name,
            "description": metadata.description,
            "category": metadata.category.value,
            "version": metadata.version,
            "schema": DynamicModel.model_json_schema(),
            "variants": metadata.variants,
            "composition": metadata.composition,
            "examples": metadata.examples,
            "tags": metadata.tags,
        }

    def get_all_schemas(self) -> dict[str, Any]:
        """Get schemas for all components."""
        return {name: self.get_schema(name) for name in self._components.keys()}

    def export_for_llm(self) -> str:
        """
        Export registry as LLM-friendly JSON documentation.

        Returns:
            JSON string with all component docs
        """
        llm_docs = {
            "version": "1.0.0",
            "categories": {cat.value: self.list_by_category(cat) for cat in ComponentCategory},
            "components": self.get_all_schemas(),
            "index": {
                "by_category": {cat.value: self.list_by_category(cat) for cat in ComponentCategory},
                "by_tag": dict(self._tags),
                "all": self.list_components(),
            },
        }

        return json.dumps(llm_docs, indent=2)

    def get_component_signature(self, name: str) -> str | None:
        """
        Get the component's __init__ signature for LLM reference.

        Args:
            name: Component name

        Returns:
            Formatted signature string
        """
        metadata = self.get(name)
        if not metadata:
            return None

        try:
            sig = inspect.signature(metadata.component_class.__init__)
            return f"{name}{sig}"
        except Exception:
            return None

    def list_variants(self, name: str) -> dict[str, list[str]] | None:
        """Get available variants for a component."""
        metadata = self.get(name)
        return metadata.variants if metadata else None

    def get_examples(self, name: str) -> list[dict[str, Any]]:
        """Get usage examples for a component."""
        metadata = self.get(name)
        return metadata.examples if metadata else []


# Global registry instance
registry = ComponentRegistry()


# Helper functions for universal component API


def get_component_class(name: str) -> Type | None:
    """
    Get component class by name from the registry.

    This is a convenience function for the universal component API.

    Args:
        name: Component name (e.g., "metric_card", "badge", "button")

    Returns:
        Component class if found, None otherwise
    """
    metadata = registry.get(name)
    return metadata.component_class if metadata else None


# Registration helper decorators


def component(
    name: str, category: ComponentCategory, description: str, props: list[PropDefinition], **kwargs
):
    """
    Decorator to register a component.

    Example:
        @component(
            name="Card",
            category=ComponentCategory.CONTAINER,
            description="Container component with header/footer",
            props=[
                PropDefinition("title", "string", "Card title"),
                PropDefinition("variant", "string", "Visual variant",
                              options=["default", "outlined", "elevated"])
            ],
            variants={"variant": ["default", "outlined", "elevated"]},
            tags=["container", "layout"]
        )
        class Card(Component):
            ...
    """

    def decorator(cls):
        registry.register(
            name=name,
            component_class=cls,
            category=category,
            description=description,
            props=props,
            **kwargs,
        )
        return cls

    return decorator


# Convenience functions


def prop(name: str, type: str, description: str, **kwargs) -> PropDefinition:
    """Shorthand for creating PropDefinition."""
    return PropDefinition(name=name, type=type, description=description, **kwargs)


def example(description: str, code: str, **props) -> dict[str, Any]:
    """Create an example entry."""
    return {"description": description, "code": code, "props": props}


# Public API functions for accessing the registry


def get_component_schema(name: str) -> dict[str, Any] | None:
    """
    Get the schema for a registered component.

    Args:
        name: Component name

    Returns:
        Component schema dict or None if not found
    """
    metadata = registry.get(name)
    return registry.get_schema(name) if metadata else None


def list_components() -> list[str]:
    """
    List all registered component names.

    Returns:
        List of component names
    """
    return registry.list_components()
