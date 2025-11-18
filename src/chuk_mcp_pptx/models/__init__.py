"""
Pydantic Models for PowerPoint MCP Server

All data structures are Pydantic models for type safety and validation.
"""

from .responses import (
    ErrorResponse,
    SuccessResponse,
    PresentationResponse,
    SlideResponse,
    ChartResponse,
    ComponentResponse,
    ListPresentationsResponse,
    PresentationInfo,
    ExportResponse,
    ImportResponse,
    StatusResponse,
)
from .presentation import (
    PresentationMetadata,
    SlideMetadata,
)

__all__ = [
    # Response models
    "ErrorResponse",
    "SuccessResponse",
    "PresentationResponse",
    "SlideResponse",
    "ChartResponse",
    "ComponentResponse",
    "ListPresentationsResponse",
    "PresentationInfo",
    "ExportResponse",
    "ImportResponse",
    "StatusResponse",
    # Metadata models
    "PresentationMetadata",
    "SlideMetadata",
]
