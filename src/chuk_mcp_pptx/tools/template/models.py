"""
Pydantic models for template tools.

All template tool responses use these type-safe models.
No dict goop, only Pydantic models.
"""

from pydantic import BaseModel, Field


class BuiltinTemplateInfo(BaseModel):
    """Information about a built-in presentation template."""

    name: str = Field(..., description="Template identifier (e.g., 'brand_proposal')")
    display_name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Template description")
    category: str = Field(
        ..., description="Template category (business, basic, technology, education)"
    )
    layout_count: int = Field(..., description="Number of slide layouts", ge=0)
    tags: list[str] = Field(default_factory=list, description="Search tags")
    is_builtin: bool = Field(default=True, description="Always true for builtin templates")

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "name": "brand_proposal",
                "display_name": "Brand Proposal",
                "description": "Professional brand proposal template with 55 layouts",
                "category": "business",
                "layout_count": 55,
                "tags": ["brand", "proposal", "marketing", "business", "professional"],
                "is_builtin": True,
            }
        }


class CustomTemplateInfo(BaseModel):
    """Information about a custom/imported presentation template."""

    name: str = Field(..., description="Template name")
    slide_count: int = Field(..., description="Number of slides", ge=0)
    namespace_id: str = Field(..., description="Artifact store namespace ID")
    is_builtin: bool = Field(default=False, description="Always false for custom templates")
    category: str = Field(default="custom", description="Always 'custom'")

    class Config:
        extra = "forbid"


class PresentationTemplateListResponse(BaseModel):
    """Response from listing presentation templates."""

    builtin_templates: list[BuiltinTemplateInfo] = Field(
        default_factory=list, description="Built-in templates from template manager"
    )
    custom_templates: list[CustomTemplateInfo] = Field(
        default_factory=list, description="Custom templates from artifact store"
    )
    total: int = Field(..., description="Total number of templates", ge=0)

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "builtin_templates": [
                    {
                        "name": "brand_proposal",
                        "display_name": "Brand Proposal",
                        "description": "Professional brand proposal template",
                        "category": "business",
                        "layout_count": 55,
                        "tags": ["brand", "proposal"],
                        "is_builtin": True,
                    }
                ],
                "custom_templates": [],
                "total": 1,
            }
        }


class LayoutPlaceholderInfo(BaseModel):
    """Information about a placeholder in a layout."""

    idx: int = Field(..., description="Placeholder index")
    type: str = Field(..., description="Placeholder type")
    name: str = Field(..., description="Placeholder name")

    class Config:
        extra = "forbid"


class LayoutInfo(BaseModel):
    """Information about a slide layout."""

    index: int = Field(..., description="Layout index", ge=0)
    name: str = Field(..., description="Layout name")
    placeholder_count: int = Field(default=0, description="Number of placeholders", ge=0)
    placeholders: list[LayoutPlaceholderInfo] = Field(
        default_factory=list, description="Placeholder details"
    )

    class Config:
        extra = "forbid"


class PresentationTemplateAnalysis(BaseModel):
    """Analysis of a presentation template's structure."""

    name: str = Field(..., description="Template name")
    slide_count: int = Field(..., description="Number of slides in template", ge=0)
    layout_count: int = Field(..., description="Number of slide layouts", ge=0)
    layouts: list[LayoutInfo] = Field(default_factory=list, description="Available slide layouts")
    master_count: int = Field(default=1, description="Number of slide masters", ge=1)
    has_theme: bool = Field(default=False, description="Whether template has custom theme")

    class Config:
        extra = "forbid"


class LayoutVariant(BaseModel):
    """A variant of a base layout."""

    index: int = Field(..., description="Layout index")
    name: str = Field(..., description="Layout name")
    variant_number: int | None = Field(None, description="Variant number if detected from name")
    placeholder_count: int = Field(..., description="Number of placeholders")
    original_slide_number: int | None = Field(
        None, description="Original slide number in template (1-indexed)"
    )

    class Config:
        extra = "forbid"


class LayoutGroup(BaseModel):
    """Group of similar layouts (base + variants)."""

    base_name: str = Field(..., description="Base layout name without variant number")
    base_layout: LayoutVariant = Field(..., description="Primary/base layout")
    variants: list[LayoutVariant] = Field(default_factory=list, description="Layout variants")
    total_count: int = Field(..., description="Total layouts in group (base + variants)")
    placeholder_signature: str = Field(..., description="Placeholder pattern signature")

    class Config:
        extra = "forbid"


class TemplateLayoutVariantsAnalysis(BaseModel):
    """Analysis of template layouts with variant detection."""

    total_layouts: int = Field(..., description="Total number of layouts")
    unique_groups: int = Field(..., description="Number of unique layout groups")
    layout_groups: list[LayoutGroup] = Field(default_factory=list, description="Grouped layouts")
    ungrouped_layouts: list[LayoutVariant] = Field(
        default_factory=list, description="Layouts that don't fit any group"
    )

    class Config:
        extra = "forbid"


class TemplateImportResponse(BaseModel):
    """Response from importing a template."""

    name: str = Field(..., description="Template name")
    slide_count: int = Field(..., description="Number of slides imported", ge=0)
    layout_count: int = Field(..., description="Number of layouts imported", ge=0)
    namespace_id: str = Field(..., description="Artifact store namespace ID")
    message: str = Field(..., description="Success message")

    class Config:
        extra = "forbid"


# Alias for backward compatibility
TemplateInfo = PresentationTemplateAnalysis
