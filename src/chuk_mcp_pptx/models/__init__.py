"""
Pydantic Models for PowerPoint MCP Server

All data structures are Pydantic models for type safety and validation.
"""

from .responses import (
    # Enums
    TargetType,
    LayoutType,
    # Response models
    ErrorResponse,
    SuccessResponse,
    PresentationResponse,
    SlideResponse,
    ChartResponse,
    ComponentResponse,
    ComponentListResponse,
    ComponentInfo,
    ComponentPosition,
    ComponentTarget,
    PlaceholderStatus,
    ImageStatus,
    ValidationWarning,
    ListPresentationsResponse,
    PresentationInfo,
    ExportResponse,
    ImportResponse,
    StatusResponse,
    DownloadUrlResponse,
    TemplateInfo,
    TemplateListResponse,
    AnalysisResponse,
)
from .presentation import (
    PresentationMetadata,
    SlideMetadata,
)

__all__ = [
    # Enums
    "TargetType",
    "LayoutType",
    # Response models
    "ErrorResponse",
    "SuccessResponse",
    "PresentationResponse",
    "SlideResponse",
    "ChartResponse",
    "ComponentResponse",
    "ComponentListResponse",
    "ComponentInfo",
    "ComponentPosition",
    "ComponentTarget",
    "PlaceholderStatus",
    "ImageStatus",
    "ValidationWarning",
    "ListPresentationsResponse",
    "PresentationInfo",
    "ExportResponse",
    "ImportResponse",
    "StatusResponse",
    "DownloadUrlResponse",
    "TemplateInfo",
    "TemplateListResponse",
    "AnalysisResponse",
    # Metadata models
    "PresentationMetadata",
    "SlideMetadata",
]
