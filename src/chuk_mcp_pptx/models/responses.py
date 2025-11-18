"""
Response Models for PowerPoint MCP Server Tools

All tool responses are Pydantic models for type safety and consistent API.
"""

from pydantic import BaseModel, Field
from typing import Literal


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


class PresentationResponse(BaseModel):
    """Response model for presentation creation/modification operations."""

    name: str = Field(..., description="Presentation name", min_length=1)
    message: str = Field(..., description="Operation result message")
    slide_count: int = Field(..., description="Total number of slides", ge=0)
    is_current: bool = Field(
        default=True, description="Whether this is now the current active presentation"
    )

    class Config:
        extra = "forbid"


class SlideResponse(BaseModel):
    """Response model for slide operations."""

    presentation: str = Field(..., description="Presentation name", min_length=1)
    slide_index: int = Field(..., description="Index of the slide (0-based)", ge=0)
    message: str = Field(..., description="Operation result message")
    slide_count: int = Field(..., description="Total slides in presentation", ge=0)

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


class PresentationInfo(BaseModel):
    """Information about a single presentation."""

    name: str = Field(..., description="Presentation name", min_length=1)
    slide_count: int = Field(..., description="Number of slides", ge=0)
    is_current: bool = Field(..., description="Whether this is the current active presentation")
    file_path: str | None = Field(None, description="VFS path if saved to filesystem")

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
    format: Literal["base64", "file", "vfs"] = Field(..., description="Export format")
    path: str | None = Field(None, description="File path or VFS path if applicable")
    size_bytes: int | None = Field(None, description="Size of exported data in bytes", ge=0)
    message: str = Field(..., description="Operation result message")

    class Config:
        extra = "forbid"


class ImportResponse(BaseModel):
    """Response model for presentation import operations."""

    name: str = Field(..., description="Imported presentation name", min_length=1)
    source: Literal["base64", "file", "vfs"] = Field(..., description="Import source")
    slide_count: int = Field(..., description="Number of slides imported", ge=0)
    message: str = Field(..., description="Operation result message")

    class Config:
        extra = "forbid"


class StatusResponse(BaseModel):
    """Response model for server status queries."""

    server: str = Field(default="chuk-mcp-pptx", description="Server name")
    version: str = Field(default="0.1.0", description="Server version")
    storage_provider: str = Field(
        ..., description="Active storage provider (file/memory/sqlite/s3)"
    )
    storage_path: str = Field(..., description="Base path for presentations in VFS")
    presentations_loaded: int = Field(..., description="Number of presentations in memory", ge=0)
    current_presentation: str | None = Field(None, description="Current active presentation")

    class Config:
        extra = "forbid"
