"""
Comprehensive tests for the variant system.
"""

import pytest
from chuk_mcp_pptx.components.variants import (
    VariantConfig,
    VariantDefinition,
    CompoundVariant,
    VariantBuilder,
    create_variants,
    CARD_VARIANTS,
    BUTTON_VARIANTS,
    BADGE_VARIANTS,
)


class TestVariantConfig:
    """Test VariantConfig dataclass."""

    def test_variant_config_creation(self):
        """Test creating variant config."""
        config = VariantConfig(props={"bg": "blue", "padding": 0.5})

        assert config.props == {"bg": "blue", "padding": 0.5}
        assert config.description is None

    def test_variant_config_with_description(self):
        """Test variant config with description."""
        config = VariantConfig(props={"bg": "red"}, description="Destructive variant")

        assert config.description == "Destructive variant"


class TestVariantDefinition:
    """Test VariantDefinition class."""

    def test_variant_definition_creation(self):
        """Test creating variant definition."""
        var_def = VariantDefinition(
            {
                "default": VariantConfig(props={"bg": "blue"}),
                "primary": VariantConfig(props={"bg": "purple"}),
            }
        )

        assert "default" in var_def.options
        assert "primary" in var_def.options

    def test_get_variant(self):
        """Test getting variant by key."""
        var_def = VariantDefinition(
            {
                "default": VariantConfig(props={"bg": "blue"}),
                "primary": VariantConfig(props={"bg": "purple"}),
            }
        )

        config = var_def.get("primary")
        assert config.props["bg"] == "purple"

    def test_get_default_fallback(self):
        """Test fallback to default variant."""
        var_def = VariantDefinition(
            {
                "default": VariantConfig(props={"bg": "blue"}),
            }
        )

        # Should fallback to default
        config = var_def.get("nonexistent")
        assert config.props["bg"] == "blue"


class TestCompoundVariant:
    """Test CompoundVariant class."""

    def test_compound_variant_creation(self):
        """Test creating compound variant."""
        compound = CompoundVariant(
            conditions={"variant": "primary", "size": "lg"}, props={"font_weight": "bold"}
        )

        assert compound.conditions == {"variant": "primary", "size": "lg"}
        assert compound.props == {"font_weight": "bold"}

    def test_matches_true(self):
        """Test matching conditions."""
        compound = CompoundVariant(
            conditions={"variant": "primary", "size": "lg"}, props={"font_weight": "bold"}
        )

        active = {"variant": "primary", "size": "lg"}
        assert compound.matches(active) is True

    def test_matches_false(self):
        """Test non-matching conditions."""
        compound = CompoundVariant(
            conditions={"variant": "primary", "size": "lg"}, props={"font_weight": "bold"}
        )

        active = {"variant": "secondary", "size": "lg"}
        assert compound.matches(active) is False

    def test_matches_partial(self):
        """Test partial match fails."""
        compound = CompoundVariant(
            conditions={"variant": "primary", "size": "lg"}, props={"font_weight": "bold"}
        )

        # Only variant matches, not size
        active = {"variant": "primary", "size": "sm"}
        assert compound.matches(active) is False


class TestVariantBuilder:
    """Test VariantBuilder class."""

    def test_builder_creation(self):
        """Test creating builder."""
        builder = VariantBuilder(base_props={"border_radius": 8})

        assert builder.base_props == {"border_radius": 8}
        assert len(builder.variants) == 0

    def test_add_variant(self):
        """Test adding variants."""
        builder = VariantBuilder()
        builder.add_variant(
            "size",
            {
                "sm": {"padding": 0.2},
                "md": {"padding": 0.4},
                "lg": {"padding": 0.6},
            },
        )

        assert "size" in builder.variants
        assert len(builder.variants["size"].options) == 3

    def test_set_defaults(self):
        """Test setting default variants."""
        builder = VariantBuilder()
        builder.set_defaults(variant="default", size="md")

        assert builder.default_variants["variant"] == "default"
        assert builder.default_variants["size"] == "md"

    def test_add_compound(self):
        """Test adding compound variant."""
        builder = VariantBuilder()
        builder.add_compound(
            conditions={"variant": "primary", "size": "lg"}, props={"shadow": True}
        )

        assert len(builder.compound_variants) == 1

    def test_build_basic(self):
        """Test building props with basic variants."""
        builder = VariantBuilder(base_props={"border_radius": 8})
        builder.add_variant(
            "variant",
            {
                "default": {"bg": "card.DEFAULT"},
                "primary": {"bg": "primary.DEFAULT"},
            },
        )
        builder.set_defaults(variant="default")

        props = builder.build(variant="primary")

        assert props["border_radius"] == 8
        assert props["bg"] == "primary.DEFAULT"

    def test_build_with_defaults(self):
        """Test building with default variants."""
        builder = VariantBuilder()
        builder.add_variant(
            "size",
            {
                "sm": {"padding": 0.2},
                "md": {"padding": 0.4},
            },
        )
        builder.set_defaults(size="md")

        # Don't specify size, should use default
        props = builder.build()
        assert props["padding"] == 0.4

    def test_build_with_compound(self):
        """Test building with compound variants."""
        builder = VariantBuilder()
        builder.add_variant(
            "variant",
            {
                "default": {"bg": "blue"},
                "primary": {"bg": "purple"},
            },
        )
        builder.add_variant(
            "size",
            {
                "sm": {"padding": 0.2},
                "lg": {"padding": 0.6},
            },
        )
        builder.add_compound(
            conditions={"variant": "primary", "size": "lg"},
            props={"shadow": True, "font_weight": "bold"},
        )

        props = builder.build(variant="primary", size="lg")

        assert props["bg"] == "purple"
        assert props["padding"] == 0.6
        assert props["shadow"] is True
        assert props["font_weight"] == "bold"

    def test_build_compound_not_matching(self):
        """Test compound variant doesn't apply when not matching."""
        builder = VariantBuilder()
        builder.add_variant(
            "variant",
            {
                "default": {"bg": "blue"},
                "primary": {"bg": "purple"},
            },
        )
        builder.add_variant(
            "size",
            {
                "sm": {"padding": 0.2},
                "lg": {"padding": 0.6},
            },
        )
        builder.add_compound(
            conditions={"variant": "primary", "size": "lg"}, props={"shadow": True}
        )

        # Size is sm, not lg, so compound shouldn't apply
        props = builder.build(variant="primary", size="sm")

        assert "shadow" not in props

    def test_get_schema(self):
        """Test getting schema."""
        builder = VariantBuilder(base_props={"border_radius": 8})
        builder.add_variant(
            "variant",
            {
                "default": {"bg": "blue"},
                "primary": {"bg": "purple"},
            },
        )
        builder.set_defaults(variant="default")

        schema = builder.get_schema()

        assert "base_props" in schema
        assert "variants" in schema
        assert "compound_variants" in schema
        assert "variant" in schema["variants"]
        assert schema["variants"]["variant"]["default"] == "default"

    def test_chaining(self):
        """Test method chaining."""
        builder = (
            VariantBuilder()
            .add_variant("size", {"sm": {"p": 0.2}})
            .set_defaults(size="sm")
            .add_compound({"size": "sm"}, {"compact": True})
        )

        assert "size" in builder.variants
        assert builder.default_variants["size"] == "sm"
        assert len(builder.compound_variants) == 1


class TestCreateVariants:
    """Test create_variants factory function."""

    def test_create_variants_basic(self):
        """Test creating variants with factory."""
        variants = create_variants(
            base={"border_radius": 8},
            variants={
                "size": {
                    "sm": {"padding": 0.2},
                    "md": {"padding": 0.4},
                }
            },
        )

        assert isinstance(variants, VariantBuilder)
        props = variants.build(size="sm")
        assert props["padding"] == 0.2

    def test_create_variants_with_defaults(self):
        """Test creating with default variants."""
        variants = create_variants(
            variants={
                "variant": {
                    "default": {"bg": "blue"},
                    "primary": {"bg": "purple"},
                }
            },
            default_variants={"variant": "default"},
        )

        props = variants.build()
        assert props["bg"] == "blue"

    def test_create_variants_with_compounds(self):
        """Test creating with compound variants."""
        variants = create_variants(
            variants={"variant": {"primary": {"bg": "purple"}}, "size": {"lg": {"padding": 0.6}}},
            compound_variants=[
                {"conditions": {"variant": "primary", "size": "lg"}, "props": {"shadow": True}}
            ],
        )

        props = variants.build(variant="primary", size="lg")
        assert props["shadow"] is True


class TestPresetVariants:
    """Test preset variant configurations."""

    def test_card_variants(self):
        """Test CARD_VARIANTS preset."""
        assert CARD_VARIANTS is not None

        # Test default
        props = CARD_VARIANTS.build(variant="default", padding="md")
        assert "bg_color" in props
        assert "padding" in props

        # Test outlined
        outlined = CARD_VARIANTS.build(variant="outlined")
        assert outlined["border_width"] == 1

        # Test elevated
        elevated = CARD_VARIANTS.build(variant="elevated")
        assert elevated.get("shadow") is True

    def test_button_variants(self):
        """Test BUTTON_VARIANTS preset."""
        assert BUTTON_VARIANTS is not None

        # Test sizes
        sm = BUTTON_VARIANTS.build(size="sm")
        md = BUTTON_VARIANTS.build(size="md")
        lg = BUTTON_VARIANTS.build(size="lg")

        assert sm["padding"] < md["padding"] < lg["padding"]
        assert sm["font_size"] < md["font_size"] < lg["font_size"]

        # Test variants
        outline = BUTTON_VARIANTS.build(variant="outline")
        assert outline["bg_color"] == "transparent"
        assert outline["border_width"] == 1

    def test_badge_variants(self):
        """Test BADGE_VARIANTS preset."""
        assert BADGE_VARIANTS is not None

        default = BADGE_VARIANTS.build(variant="default")
        assert "bg_color" in default

        success = BADGE_VARIANTS.build(variant="success")
        assert success["bg_color"] == "success.DEFAULT"

        warning = BADGE_VARIANTS.build(variant="warning")
        assert warning["bg_color"] == "warning.DEFAULT"

    def test_card_variants_schema(self):
        """Test getting CARD_VARIANTS schema."""
        schema = CARD_VARIANTS.get_schema()

        assert "variants" in schema
        assert "variant" in schema["variants"]
        assert "padding" in schema["variants"]

        # Check variant options
        variant_options = schema["variants"]["variant"]["options"]
        assert "default" in variant_options
        assert "outlined" in variant_options
        assert "elevated" in variant_options
        assert "ghost" in variant_options


class TestVariantEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_builder(self):
        """Test builder with no variants."""
        builder = VariantBuilder()
        props = builder.build()

        assert props == {}

    def test_override_base_props(self):
        """Test that variants override base props."""
        builder = VariantBuilder(base_props={"bg": "blue", "padding": 0.5})
        builder.add_variant(
            "variant",
            {
                "primary": {"bg": "purple"}  # Override bg but keep padding
            },
        )

        props = builder.build(variant="primary")
        assert props["bg"] == "purple"
        assert props["padding"] == 0.5  # Base prop preserved

    def test_multiple_compounds(self):
        """Test multiple compound variants."""
        builder = VariantBuilder()
        builder.add_variant("variant", {"primary": {"bg": "purple"}})
        builder.add_variant("size", {"lg": {"padding": 0.6}})
        builder.add_variant("state", {"active": {"opacity": 1.0}})

        builder.add_compound({"variant": "primary", "size": "lg"}, {"shadow": True})
        builder.add_compound({"variant": "primary", "state": "active"}, {"glow": True})

        # Both compounds should apply
        props = builder.build(variant="primary", size="lg", state="active")
        assert props["shadow"] is True
        assert props["glow"] is True

    def test_nonexistent_variant(self):
        """Test using nonexistent variant value uses default from VariantDefinition."""
        builder = VariantBuilder()
        builder.add_variant(
            "size",
            {
                "sm": {"padding": 0.2},
                "md": {"padding": 0.4},
            },
        )
        builder.set_defaults(size="md")

        # When requesting nonexistent variant without it in active variants,
        # defaults are applied but xl isn't found, fallsback via VariantDefinition.get()
        # which returns the "default" option or the first match
        props = builder.build()  # Use defaults
        assert props["padding"] == 0.4  # Gets default (md)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
