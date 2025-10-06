"""
Variant system inspired by class-variance-authority (cva).
Provides composable variants for PowerPoint components.
"""

from typing import Dict, Any, Optional, List, Callable, TypeVar, Generic
from dataclasses import dataclass
from copy import deepcopy


T = TypeVar('T')


@dataclass
class VariantConfig:
    """Configuration for a single variant option."""
    props: Dict[str, Any]
    description: Optional[str] = None


class VariantDefinition:
    """
    Defines variants for a component property.

    Example:
        variant_def = VariantDefinition({
            "default": VariantConfig(props={"bg": "card.DEFAULT"}),
            "primary": VariantConfig(props={"bg": "primary.DEFAULT"}),
        })
    """

    def __init__(self, options: Dict[str, VariantConfig]):
        self.options = options

    def get(self, key: str, default: str = "default") -> VariantConfig:
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

    def __init__(self, conditions: Dict[str, str], props: Dict[str, Any]):
        self.conditions = conditions
        self.props = props

    def matches(self, active_variants: Dict[str, str]) -> bool:
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

    def __init__(self, base_props: Optional[Dict[str, Any]] = None):
        """
        Initialize variant builder.

        Args:
            base_props: Base properties applied to all variants
        """
        self.base_props = base_props or {}
        self.variants: Dict[str, VariantDefinition] = {}
        self.default_variants: Dict[str, str] = {}
        self.compound_variants: List[CompoundVariant] = []

    def add_variant(self, name: str, options: Dict[str, Dict[str, Any]]) -> 'VariantBuilder':
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

    def set_defaults(self, **defaults) -> 'VariantBuilder':
        """
        Set default variants.

        Example:
            builder.set_defaults(variant="default", size="md")
        """
        self.default_variants.update(defaults)
        return self

    def add_compound(self, conditions: Dict[str, str], props: Dict[str, Any]) -> 'VariantBuilder':
        """
        Add compound variant.

        Args:
            conditions: Conditions that must match (e.g., {"variant": "primary", "size": "lg"})
            props: Props to apply when conditions match
        """
        self.compound_variants.append(CompoundVariant(conditions, props))
        return self

    def build(self, **selected_variants) -> Dict[str, Any]:
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

    def get_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for this variant configuration.
        Useful for LLM consumption.
        """
        return {
            "base_props": self.base_props,
            "variants": {
                name: {
                    "options": list(variant.options.keys()),
                    "default": self.default_variants.get(name)
                }
                for name, variant in self.variants.items()
            },
            "compound_variants": [
                {
                    "conditions": cv.conditions,
                    "props": cv.props
                }
                for cv in self.compound_variants
            ]
        }


def create_variants(
    base: Optional[Dict[str, Any]] = None,
    variants: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None,
    default_variants: Optional[Dict[str, str]] = None,
    compound_variants: Optional[List[Dict[str, Any]]] = None
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
            builder.add_compound(cv["conditions"], cv["props"])

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
            "outline": {"bg_color": "transparent", "fg_color": "primary.DEFAULT", "border_width": 1},
            "ghost": {"bg_color": "transparent", "fg_color": "foreground.DEFAULT", "border_width": 0},
            "destructive": {"bg_color": "destructive.DEFAULT", "fg_color": "destructive.foreground"},
        },
        "size": {
            "sm": {"padding": 0.2, "font_size": 12, "height": 0.6},
            "md": {"padding": 0.3, "font_size": 14, "height": 0.8},
            "lg": {"padding": 0.4, "font_size": 16, "height": 1.0},
        }
    },
    default_variants={
        "variant": "default",
        "size": "md"
    }
)

CARD_VARIANTS = create_variants(
    base={
        "border_radius": 12,
    },
    variants={
        "variant": {
            "default": {"bg_color": "card.DEFAULT", "fg_color": "card.foreground", "border_width": 0},
            "outlined": {"bg_color": "card.DEFAULT", "fg_color": "card.foreground", "border_width": 1, "border_color": "border.DEFAULT"},
            "elevated": {"bg_color": "card.DEFAULT", "fg_color": "card.foreground", "shadow": True},
            "ghost": {"bg_color": "transparent", "fg_color": "foreground.DEFAULT", "border_width": 0},
        },
        "padding": {
            "none": {"padding": 0},
            "sm": {"padding": 0.25},
            "md": {"padding": 0.5},
            "lg": {"padding": 0.75},
            "xl": {"padding": 1.0},
        }
    },
    default_variants={
        "variant": "default",
        "padding": "md"
    }
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
            "destructive": {"bg_color": "destructive.DEFAULT", "fg_color": "destructive.foreground"},
            "outline": {"bg_color": "transparent", "fg_color": "foreground.DEFAULT", "border_width": 1},
        }
    },
    default_variants={
        "variant": "default"
    }
)
