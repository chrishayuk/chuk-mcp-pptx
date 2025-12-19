"""
Response Models for PowerPoint MCP Server Tools

All tool responses are Pydantic models for type safety and consistent API.
"""

from pydantic import BaseModel, Field
from typing import Literal, Any
from enum import Enum


class TargetType(str, Enum):
    """Component target types for placement."""

    PLACEHOLDER = "placeholder"
    COMPONENT = "component"
    LAYOUT = "layout"
    FREE_FORM = "free-form"


class LayoutType(str, Enum):
    """Layout region types."""

    GRID = "grid"
    FLEX_ROW = "flex-row"
    FLEX_COLUMN = "flex-column"


class ErrorResponse(BaseModel):
    """Error response model for tool failures."""

    error: str = Field(..., description="Error message describing what went wrong")

    class Config:
        extra = "forbid"


class SuccessResponse(BaseModel):
    """Generic success response for simple operations."""

    message: str = Field(..., description="Success message")

    class Config:
        extra = "forbid"


class TemplateInfo(BaseModel):
    """Information about template used to create presentation."""

    template_name: str = Field(..., description="Name of template used")
    layout_count: int = Field(..., description="Number of layouts available", ge=0)
    message: str = Field(..., description="Guidance message for using template layouts")

    class Config:
        extra = "forbid"


class PresentationResponse(BaseModel):
    """Response model for presentation creation/modification operations."""

    name: str = Field(..., description="Presentation name", min_length=1)
    message: str = Field(..., description="Operation result message")
    slide_count: int = Field(..., description="Total number of slides", ge=0)
    is_current: bool = Field(
        default=True, description="Whether this is now the current active presentation"
    )
    template_info: TemplateInfo | None = Field(
        None, description="Template information if presentation was created from a template"
    )

    class Config:
        extra = "forbid"


class PlaceholderInfo(BaseModel):
    """Information about a placeholder in a layout."""

    idx: int = Field(..., description="Placeholder index", ge=0)
    type: str = Field(..., description="Placeholder type (e.g., TITLE, BODY, PICTURE)")
    name: str = Field(..., description="Placeholder name")

    class Config:
        extra = "forbid"


class LayoutInfo(BaseModel):
    """Information about a slide layout."""

    layout_index: int = Field(..., description="Layout index used", ge=0)
    layout_name: str = Field(..., description="Name of the layout")
    placeholders: list[PlaceholderInfo] = Field(
        default_factory=list, description="Available placeholders in this layout"
    )
    message: str = Field(..., description="Guidance message for using this layout")

    class Config:
        extra = "forbid"


class SlideResponse(BaseModel):
    """Response model for slide operations."""

    presentation: str = Field(..., description="Presentation name", min_length=1)
    slide_index: int = Field(..., description="Index of the slide (0-based)", ge=0)
    message: str = Field(..., description="Operation result message")
    slide_count: int = Field(..., description="Total slides in presentation", ge=0)
    layout_info: LayoutInfo | None = Field(
        None, description="Layout information if slide was created from template layout"
    )

    class Config:
        extra = "forbid"


class ChartResponse(BaseModel):
    """Response model for chart addition operations."""

    presentation: str = Field(..., description="Presentation name", min_length=1)
    slide_index: int = Field(..., description="Slide where chart was added", ge=0)
    chart_type: str = Field(..., description="Type of chart added", min_length=1)
    message: str = Field(..., description="Operation result message")
    data_points: int | None = Field(None, description="Number of data points in chart", ge=0)

    class Config:
        extra = "forbid"


class ComponentResponse(BaseModel):
    """Response model for component addition operations."""

    presentation: str = Field(..., description="Presentation name", min_length=1)
    slide_index: int = Field(..., description="Slide where component was added", ge=0)
    component: str = Field(..., description="Component type added", min_length=1)
    message: str = Field(..., description="Operation result message")
    variant: str | None = Field(None, description="Component variant used")

    class Config:
        extra = "forbid"


class ComponentPosition(BaseModel):
    """Position and size of a component."""

    left: float = Field(..., description="Left position in inches")
    top: float = Field(..., description="Top position in inches")
    width: float = Field(..., description="Width in inches")
    height: float = Field(..., description="Height in inches")

    class Config:
        extra = "forbid"


class ComponentTarget(BaseModel):
    """Target information for component placement."""

    type: TargetType = Field(..., description="Target type")
    id: int | str | None = Field(
        None, description="Target identifier (placeholder idx, component_id, or layout name)"
    )

    class Config:
        extra = "forbid"


class ComponentInfo(BaseModel):
    """Information about a component on a slide."""

    id: str = Field(..., description="Component ID", min_length=1)
    type: str = Field(..., description="Component type", min_length=1)
    position: ComponentPosition = Field(..., description="Position and size")
    target: ComponentTarget = Field(..., description="Target information")
    parent_id: str | None = Field(None, description="Parent component ID (for composition)")
    children: list[str] = Field(default_factory=list, description="Child component IDs")
    params: dict[str, Any] = Field(default_factory=dict, description="Component parameters")

    class Config:
        extra = "forbid"


class PlaceholderStatus(BaseModel):
    """Status of a placeholder on a slide."""

    idx: int = Field(..., description="Placeholder index", ge=0)
    type: str = Field(..., description="Placeholder type (e.g., TITLE, BODY, PICTURE)")
    name: str = Field(..., description="Placeholder name")
    is_empty: bool = Field(..., description="Whether placeholder has no content")
    has_text: bool = Field(default=False, description="Whether placeholder has text content")
    has_image: bool = Field(default=False, description="Whether placeholder has an image")
    content_preview: str | None = Field(None, description="Preview of content if available")

    class Config:
        extra = "forbid"


class ImageStatus(BaseModel):
    """Status of an image on a slide."""

    component_id: str = Field(..., description="Component ID of the image")
    placeholder_idx: int | None = Field(
        None, description="Placeholder index if image is in placeholder"
    )
    loaded_successfully: bool = Field(..., description="Whether image loaded without errors")
    error_message: str | None = Field(None, description="Error message if image failed to load")
    source: str | None = Field(None, description="Image source (path or URL)")

    class Config:
        extra = "forbid"


class ValidationWarning(BaseModel):
    """Validation warning for slide content."""

    type: Literal["empty_placeholder", "missing_image", "layout_mismatch"] = Field(
        ..., description="Warning type"
    )
    message: str = Field(..., description="Warning message")
    placeholder_idx: int | None = Field(None, description="Placeholder index if applicable")
    component_id: str | None = Field(None, description="Component ID if applicable")

    class Config:
        extra = "forbid"


class ComponentListResponse(BaseModel):
    """Response model for listing components on a slide."""

    slide_index: int = Field(..., description="Slide index", ge=0)
    component_count: int = Field(..., description="Number of components", ge=0)
    components: list[ComponentInfo] = Field(..., description="List of components")
    placeholders: list[PlaceholderStatus] = Field(
        default_factory=list, description="Status of all placeholders on slide"
    )
    images: list[ImageStatus] = Field(
        default_factory=list, description="Status of all images on slide"
    )
    warnings: list[ValidationWarning] = Field(
        default_factory=list, description="Validation warnings for this slide"
    )
    validation_passed: bool = Field(
        default=True, description="Whether slide passed all validation checks"
    )

    class Config:
        extra = "forbid"


class PresentationInfo(BaseModel):
    """Information about a single presentation."""

    name: str = Field(..., description="Presentation name", min_length=1)
    slide_count: int = Field(..., description="Number of slides", ge=0)
    is_current: bool = Field(..., description="Whether this is the current active presentation")
    file_path: str | None = Field(None, description="Artifact URI if saved to artifact store")
    namespace_id: str | None = Field(None, description="Namespace ID in artifact store")

    class Config:
        extra = "forbid"


class ListPresentationsResponse(BaseModel):
    """Response model for listing all presentations."""

    presentations: list[PresentationInfo] = Field(
        ..., description="List of available presentations"
    )
    total: int = Field(..., description="Total number of presentations", ge=0)
    current: str | None = Field(None, description="Name of current active presentation")

    class Config:
        extra = "forbid"


class ExportResponse(BaseModel):
    """Response model for presentation export operations."""

    name: str = Field(..., description="Presentation name", min_length=1)
    format: Literal["base64", "file", "artifact"] = Field(..., description="Export format")
    path: str | None = Field(None, description="File path if applicable")
    artifact_uri: str | None = Field(None, description="Artifact URI if saved to artifact store")
    namespace_id: str | None = Field(None, description="Namespace ID in artifact store")
    download_url: str | None = Field(None, description="Presigned download URL (valid for 1 hour)")
    mime_type: str = Field(
        default="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        description="MIME type of the exported presentation",
    )
    size_bytes: int | None = Field(None, description="Size of exported data in bytes", ge=0)
    message: str = Field(..., description="Operation result message")

    class Config:
        extra = "forbid"


class ImportResponse(BaseModel):
    """Response model for presentation import operations."""

    name: str = Field(..., description="Imported presentation name", min_length=1)
    source: Literal["base64", "file", "artifact"] = Field(..., description="Import source")
    slide_count: int = Field(..., description="Number of slides imported", ge=0)
    artifact_uri: str | None = Field(None, description="Artifact URI in artifact store")
    namespace_id: str | None = Field(None, description="Namespace ID in artifact store")
    message: str = Field(..., description="Operation result message")

    class Config:
        extra = "forbid"


class StatusResponse(BaseModel):
    """Response model for server status queries."""

    server: str = Field(default="chuk-mcp-pptx", description="Server name")
    version: str = Field(default="0.1.0", description="Server version")
    storage_provider: str = Field(
        ..., description="Active storage provider (memory/filesystem/sqlite/s3)"
    )
    storage_path: str = Field(..., description="Base path for presentations")
    presentations_loaded: int = Field(..., description="Number of presentations in memory", ge=0)
    current_presentation: str | None = Field(None, description="Current active presentation")
    artifact_store_available: bool = Field(
        default=False, description="Whether artifact store is available"
    )

    class Config:
        extra = "forbid"


class DownloadUrlResponse(BaseModel):
    """Response model for download URL generation."""

    url: str = Field(..., description="Presigned download URL", min_length=1)
    presentation: str = Field(..., description="Presentation name", min_length=1)
    artifact_id: str = Field(..., description="Artifact ID in store", min_length=1)
    expires_in: int = Field(..., description="URL expiration time in seconds", gt=0)
    message: str = Field(..., description="Success message")

    class Config:
        extra = "forbid"


class TemplateMetadataResponse(BaseModel):
    """Information about a template (for listing templates)."""

    name: str = Field(..., description="Template name", min_length=1)
    description: str | None = Field(None, description="Template description")
    layout_count: int = Field(..., description="Number of layouts", ge=0)
    is_builtin: bool = Field(default=False, description="Whether this is a built-in template")
    file_path: str | None = Field(None, description="Template file path")

    class Config:
        extra = "forbid"


class TemplateListResponse(BaseModel):
    """Response model for listing templates."""

    templates: list[TemplateMetadataResponse] = Field(
        ..., description="List of available templates"
    )
    total: int = Field(..., description="Total number of templates", ge=0)
    builtin_count: int = Field(..., description="Number of built-in templates", ge=0)
    custom_count: int = Field(..., description="Number of custom templates", ge=0)

    class Config:
        extra = "forbid"


class AnalysisResponse(BaseModel):
    """Response model for presentation/slide analysis."""

    presentation: str = Field(..., description="Presentation name", min_length=1)
    slide_index: int | None = Field(None, description="Slide index if analyzing single slide", ge=0)
    analysis: dict[str, Any] = Field(..., description="Analysis results")
    message: str = Field(..., description="Analysis summary")

    class Config:
        extra = "forbid"
