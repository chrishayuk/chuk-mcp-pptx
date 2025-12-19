"""
Presentation Metadata Models

Pydantic models for tracking presentation and slide metadata.
"""

from pydantic import BaseModel, Field
from datetime import datetime


class SlideMetadata(BaseModel):
    """Metadata for a single slide."""

    index: int = Field(..., description="Slide index (0-based)", ge=0)
    layout: str = Field(default="Blank", description="Slide layout name")
    has_title: bool = Field(default=False, description="Whether slide has a title")
    title_text: str | None = Field(default=None, description="Title text if present")
    shape_count: int = Field(default=0, description="Number of shapes on slide", ge=0)
    has_chart: bool = Field(default=False, description="Whether slide contains charts")
    has_table: bool = Field(default=False, description="Whether slide contains tables")
    has_images: bool = Field(default=False, description="Whether slide contains images")
    component_types: list[str] = Field(
        default_factory=list, description="List of component types on this slide"
    )

    class Config:
        extra = "forbid"


class PresentationMetadata(BaseModel):
    """Metadata for a presentation."""

    name: str = Field(..., description="Presentation name", min_length=1)
    slide_count: int = Field(default=0, description="Number of slides", ge=0)
    created_at: datetime = Field(
        default_factory=datetime.now, description="When presentation was created"
    )
    modified_at: datetime = Field(
        default_factory=datetime.now, description="Last modification time"
    )
    theme: str | None = Field(default=None, description="Applied theme name if any")
    vfs_path: str | None = Field(default=None, description="Artifact URI for storage")
    namespace_id: str | None = Field(default=None, description="Namespace ID in artifact store")
    is_saved: bool = Field(default=False, description="Whether saved to artifact store")
    template_path: str | None = Field(
        default=None, description="Path to template file if created from template"
    )
    slides: list[SlideMetadata] = Field(default_factory=list, description="Metadata for each slide")

    class Config:
        extra = "forbid"

    def update_modified(self) -> None:
        """Update the modified timestamp."""
        self.modified_at = datetime.now()

    def add_slide_metadata(self, slide_meta: SlideMetadata) -> None:
        """Add metadata for a new slide."""
        self.slides.append(slide_meta)
        self.slide_count = len(self.slides)
        self.update_modified()

    def get_slide_metadata(self, index: int) -> SlideMetadata | None:
        """Get metadata for a specific slide."""
        if 0 <= index < len(self.slides):
            return self.slides[index]
        return None
