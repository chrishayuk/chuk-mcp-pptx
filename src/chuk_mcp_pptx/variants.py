"""
Variant system inspired by class-variance-authority (cva).
Provides composable variants for PowerPoint components.
"""

from __future__ import annotations


from typing import Any, TypeVar, Optional
from copy import deepcopy
from pydantic import BaseModel, field_validator
import re


T = TypeVar("T")


class VariantConfig(BaseModel):
    """Configuration for a single variant option."""

    props: dict[str, Any]
    description: str | None = None

    class Config:
        frozen = False
        arbitrary_types_allowed = True

    @field_validator("props")
    @classmethod
    def validate_props(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate prop values, especially color hex codes."""
        hex_pattern = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

        for key, value in v.items():
            # Validate color hex codes
            if isinstance(value, str) and value.startswith("#"):
                if not hex_pattern.match(value):
                    raise ValueError(f"Invalid hex color: {value}")

            # Validate numeric ranges for common props
            if key in ("font_size", "padding", "margin") and isinstance(value, (int, float)):
                if value < 0:
                    raise ValueError(f"{key} must be non-negative, got {value}")

            if key == "border_radius" and isinstance(value, (int, float)):
                if value < 0:
                    raise ValueError(f"border_radius must be non-negative, got {value}")

        return v


class VariantDefinition:
    """
    Defines variants for a component property.

    Example:
        variant_def = VariantDefinition({
            "default": VariantConfig(props={"bg": "card.DEFAULT"}),
            "primary": VariantConfig(props={"bg": "primary.DEFAULT"}),
        })
    """

    def __init__(self, options: dict[str, VariantConfig]):
        self.options = options

    def get(self, key: str, default: str = "default") -> Optional[VariantConfig]:
        """Get variant configuration by key."""
        return self.options.get(key, self.options.get(default))


class CompoundVariant:
    """
    Defines props that apply when multiple variants are active.

    Example:
        CompoundVariant(
            conditions={"variant": "primary", "size": "lg"},
            props={"font_size": 24}
        )
    """

    def __init__(self, conditions: dict[str, str], props: dict[str, Any]):
        self.conditions = conditions
        self.props = props

    def matches(self, active_variants: dict[str, str]) -> bool:
        """Check if conditions match active variants."""
        for key, value in self.conditions.items():
            if active_variants.get(key) != value:
                return False
        return True


class VariantBuilder:
    """
    Builder for creating variant configurations.
    Inspired by shadcn/ui's cva pattern.
    """

    def __init__(self, base_props: Optional[dict[str, Any | None]] = None):
        """
        Initialize variant builder.

        Args:
            base_props: Base properties applied to all variants
        """
        self.base_props = base_props or {}
        self.variants: dict[str, VariantDefinition] = {}
        self.default_variants: dict[str, str] = {}
        self.compound_variants: list[CompoundVariant] = []

    def add_variant(self, name: str, options: dict[str, dict[str, Any]]) -> "VariantBuilder":
        """
        Add a variant type.

        Args:
            name: Variant name (e.g., "variant", "size", "color")
            options: Dict of option_name -> props

        Returns:
            Self for chaining
        """
        variant_options = {
            key: VariantConfig(props=props) if isinstance(props, dict) else props
            for key, props in options.items()
        }
        self.variants[name] = VariantDefinition(variant_options)
        return self

    def set_defaults(self, **defaults) -> "VariantBuilder":
        """
        Set default variants.

        Example:
            builder.set_defaults(variant="default", size="md")
        """
        self.default_variants.update(defaults)
        return self

    def add_compound(self, conditions: dict[str, str], props: dict[str, Any]) -> "VariantBuilder":
        """
        Add compound variant.

        Args:
            conditions: Conditions that must match (e.g., {"variant": "primary", "size": "lg"})
            props: Props to apply when conditions match
        """
        self.compound_variants.append(CompoundVariant(conditions, props))
        return self

    def build(self, **selected_variants) -> dict[str, Any]:
        """
        Build final props based on selected variants.

        Args:
            **selected_variants: Selected variant values (e.g., variant="primary", size="lg")

        Returns:
            Merged props dictionary
        """
        # Start with base props
        result = deepcopy(self.base_props)

        # Apply defaults
        active_variants = {**self.default_variants}

        # Override with selected variants
        active_variants.update(selected_variants)

        # Apply variant props
        for variant_name, variant_value in active_variants.items():
            if variant_name in self.variants:
                variant_def = self.variants[variant_name]
                config = variant_def.get(variant_value)
                if config:
                    result.update(config.props)

        # Apply compound variants
        for compound in self.compound_variants:
            if compound.matches(active_variants):
                result.update(compound.props)

        return result

    def get_schema(self) -> dict[str, Any]:
        """
        Get JSON schema for this variant configuration.
        Useful for LLM consumption.
        """
        return {
            "base_props": self.base_props,
            "variants": {
                name: {
                    "options": list(variant.options.keys()),
                    "default": self.default_variants.get(name),
                }
                for name, variant in self.variants.items()
            },
            "compound_variants": [
                {"conditions": cv.conditions, "props": cv.props} for cv in self.compound_variants
            ],
        }


def create_variants(
    base: Optional[dict[str, Any | None]] = None,
    variants: Optional[dict[str, dict[str, dict[str, Any | None]]]] = None,
    default_variants: Optional[dict[str, str | None]] = None,
    compound_variants: Optional[list[dict[str, Any | None]]] = None,
) -> VariantBuilder:
    """
    Factory function for creating variant builders.
    Provides a more functional API similar to cva.

    Example:
        card_variants = create_variants(
            base={"border_radius": 8},
            variants={
                "variant": {
                    "default": {"bg_color": "card.DEFAULT"},
                    "primary": {"bg_color": "primary.DEFAULT"},
                    "destructive": {"bg_color": "destructive.DEFAULT"}
                },
                "size": {
                    "sm": {"padding": 0.25, "font_size": 12},
                    "md": {"padding": 0.5, "font_size": 14},
                    "lg": {"padding": 0.75, "font_size": 16}
                }
            },
            default_variants={
                "variant": "default",
                "size": "md"
            },
            compound_variants=[
                {
                    "conditions": {"variant": "primary", "size": "lg"},
                    "props": {"font_weight": "bold"}
                }
            ]
        )

        # Use it
        props = card_variants.build(variant="primary", size="lg")
    """
    builder = VariantBuilder(base)

    if variants:
        for name, options in variants.items():
            builder.add_variant(name, options)

    if default_variants:
        builder.set_defaults(**default_variants)

    if compound_variants:
        for cv in compound_variants:
            builder.add_compound(cv["conditions"], cv["props"])  # type: ignore[arg-type]

    return builder


# Preset variant builders for common patterns
BUTTON_VARIANTS = create_variants(
    base={
        "border_radius": 8,
        "font_weight": 500,
    },
    variants={
        "variant": {
            "default": {"bg_color": "primary.DEFAULT", "fg_color": "primary.foreground"},
            "secondary": {"bg_color": "secondary.DEFAULT", "fg_color": "secondary.foreground"},
            "outline": {
                "bg_color": "transparent",
                "fg_color": "primary.DEFAULT",
                "border_width": 1,
            },
            "ghost": {
                "bg_color": "transparent",
                "fg_color": "foreground.DEFAULT",
                "border_width": 0,
            },
            "destructive": {
                "bg_color": "destructive.DEFAULT",
                "fg_color": "destructive.foreground",
            },
        },
        "size": {
            "sm": {"padding": 0.2, "font_size": 12, "height": 0.6},
            "md": {"padding": 0.3, "font_size": 14, "height": 0.8},
            "lg": {"padding": 0.4, "font_size": 16, "height": 1.0},
        },
    },
    default_variants={"variant": "default", "size": "md"},
)

CARD_VARIANTS = create_variants(
    base={
        "border_radius": 12,
    },
    variants={
        "variant": {
            "default": {
                "bg_color": "card.DEFAULT",
                "fg_color": "card.foreground",
                "border_width": 0,
            },
            "outlined": {
                "bg_color": "card.DEFAULT",
                "fg_color": "card.foreground",
                "border_width": 1,
                "border_color": "border.DEFAULT",
            },
            "elevated": {"bg_color": "card.DEFAULT", "fg_color": "card.foreground", "shadow": True},
            "ghost": {
                "bg_color": "transparent",
                "fg_color": "foreground.DEFAULT",
                "border_width": 0,
            },
        },
        "padding": {
            "none": {"padding": 0},
            "sm": {"padding": 0.25},
            "md": {"padding": 0.5},
            "lg": {"padding": 0.75},
            "xl": {"padding": 1.0},
        },
    },
    default_variants={"variant": "default", "padding": "md"},
)

BADGE_VARIANTS = create_variants(
    base={
        "border_radius": 4,
        "font_size": 10,
        "font_weight": 600,
        "padding": 0.15,
    },
    variants={
        "variant": {
            "default": {"bg_color": "primary.DEFAULT", "fg_color": "primary.foreground"},
            "secondary": {"bg_color": "secondary.DEFAULT", "fg_color": "secondary.foreground"},
            "success": {"bg_color": "success.DEFAULT", "fg_color": "success.foreground"},
            "warning": {"bg_color": "warning.DEFAULT", "fg_color": "warning.foreground"},
            "destructive": {
                "bg_color": "destructive.DEFAULT",
                "fg_color": "destructive.foreground",
            },
            "outline": {
                "bg_color": "transparent",
                "fg_color": "foreground.DEFAULT",
                "border_width": 1,
            },
        }
    },
    default_variants={"variant": "default"},
)

# Chart variants
CHART_VARIANTS = create_variants(
    base={
        "show_legend": True,
        "legend_position": "right",
        "show_grid": True,
        "gap_width": 150,
    },
    variants={
        "style": {
            "default": {"show_values": False, "show_grid": True},
            "minimal": {"show_values": False, "show_grid": False, "legend_position": "bottom"},
            "detailed": {"show_values": True, "show_grid": True, "legend_position": "right"},
            "compact": {"show_values": False, "show_grid": False, "gap_width": 100},
        },
        "legend": {
            "right": {"legend_position": "right", "show_legend": True},
            "bottom": {"legend_position": "bottom", "show_legend": True},
            "top": {"legend_position": "top", "show_legend": True},
            "none": {"show_legend": False},
        },
    },
    default_variants={"style": "default", "legend": "right"},
)

COLUMN_CHART_VARIANTS = create_variants(
    base={
        "show_legend": True,
        "legend_position": "right",
        "show_grid": True,
        "gap_width": 150,
    },
    variants={
        "variant": {
            "clustered": {"gap_width": 150, "overlap": 0},
            "stacked": {"overlap": 100},
            "stacked100": {"overlap": 100},
        },
        "style": {
            "default": {"show_values": False},
            "minimal": {"show_values": False, "show_grid": False},
            "detailed": {"show_values": True},
        },
    },
    default_variants={"variant": "clustered", "style": "default"},
)

PIE_CHART_VARIANTS = create_variants(
    base={
        "show_legend": True,
        "legend_position": "right",
    },
    variants={
        "variant": {
            "pie": {"show_labels": True},
            "doughnut": {"show_labels": True, "hole_size": 0.5},
            "exploded": {"show_labels": True, "explosion": 0.1},
        },
        "style": {
            "default": {"show_percentages": True, "show_values": False},
            "detailed": {"show_percentages": True, "show_values": True},
            "minimal": {"show_percentages": False, "show_values": False},
        },
    },
    default_variants={"variant": "pie", "style": "default"},
)

LINE_CHART_VARIANTS = create_variants(
    base={
        "show_legend": True,
        "legend_position": "right",
        "show_grid": True,
        "smooth": False,
    },
    variants={
        "variant": {
            "line": {"smooth": False, "show_markers": True},
            "smooth": {"smooth": True, "show_markers": True},
            "area": {"fill_area": True, "smooth": False},
            "smooth_area": {"fill_area": True, "smooth": True},
        },
        "style": {
            "default": {"show_values": False, "show_grid": True},
            "minimal": {"show_values": False, "show_grid": False, "show_markers": False},
            "detailed": {"show_values": True, "show_grid": True},
        },
    },
    default_variants={"variant": "line", "style": "default"},
)
