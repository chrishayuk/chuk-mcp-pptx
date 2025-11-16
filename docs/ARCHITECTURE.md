# Pydantic-Native Architecture

## Overview

chuk-mcp-pptx follows a **Pydantic-first** design philosophy inspired by chuk-motion. Every data structure is a Pydantic `BaseModel` for type safety, validation, and maintainability.

## Core Principles

1. **No Dictionary Goop**: Never pass raw dictionaries. All data is typed and validated.
2. **Async Native**: All I/O operations are async using `AsyncVirtualFileSystem`
3. **Constants Over Strings**: Magic strings/numbers are defined as enums/constants
4. **Model-Based Responses**: All tool responses return `model_dump_json()`
5. **Virtual Filesystem**: Flexible storage with file/memory/sqlite/s3 providers

## Architecture Layers

```
┌──────────────────────────────────────────┐
│         MCP Tools (async_server.py)      │
│  - Pydantic Response Models              │
│  - Constants for Messages & Types        │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│     PresentationManager                  │
│  - Manages Presentation Objects          │
│  - Tracks PresentationMetadata (Pydantic)│
│  - VFS Integration (async)               │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│      AsyncVirtualFileSystem              │
│  - File Provider (default)               │
│  - Memory/SQLite/S3 Providers            │
└──────────────────────────────────────────┘
```

## Pydantic Models

### Response Models (`models/responses.py`)

All MCP tool responses are Pydantic models:

```python
from pydantic import BaseModel, Field

class PresentationResponse(BaseModel):
    """Response for presentation operations."""
    name: str = Field(..., description="Presentation name", min_length=1)
    message: str = Field(..., description="Operation result")
    slide_count: int = Field(..., description="Total slides", ge=0)
    is_current: bool = Field(default=True, description="Is active presentation")

    class Config:
        extra = "forbid"  # Prevents typos/extra fields
```

**Key Features:**
- Field-level validation (`min_length`, `ge`, `gt`)
- Descriptive metadata for LLMs
- `extra = "forbid"` prevents typos
- Type hints using `str | None` instead of `Optional[str]`

### Metadata Models (`models/presentation.py`)

Track presentation state with Pydantic:

```python
class PresentationMetadata(BaseModel):
    """Metadata for a presentation."""
    name: str = Field(..., min_length=1)
    slide_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    theme: str | None = None
    vfs_path: str | None = None
    is_saved: bool = Field(default=False)
    slides: list[SlideMetadata] = Field(default_factory=list)

    def update_modified(self) -> None:
        """Update the modified timestamp."""
        self.modified_at = datetime.now()
```

**Benefits:**
- Automatic timestamp management
- Type-safe slide metadata tracking
- Methods for common operations

## Constants & Enums (`constants.py`)

All magic strings and numbers are defined as constants:

```python
from enum import IntEnum
from typing import Literal

# Enums for numbered constants
class SlideLayoutIndex(IntEnum):
    """Standard slide layout indices."""
    TITLE = 0
    TITLE_AND_CONTENT = 1
    SECTION_HEADER = 2
    BLANK = 6

class ShapeType(IntEnum):
    """Microsoft Office shape type constants."""
    CHART = 3
    PICTURE = 13
    TABLE = 19

# Literal types for string constants
ChartType = Literal[
    "bar", "column", "line", "pie",
    "doughnut", "scatter", "bubble"
]

# Message templates
class ErrorMessages:
    """Standard error message templates."""
    NO_PRESENTATION = "No presentation found. Create one first with pptx_create()"
    PRESENTATION_NOT_FOUND = "Presentation '{name}' not found"

class SuccessMessages:
    """Standard success message templates."""
    PRESENTATION_CREATED = "Created presentation '{name}'"
    SLIDE_ADDED = "Added {slide_type} slide to '{presentation}'"
```

**Usage in Tools:**

```python
# ❌ BAD - Magic strings
slide_layout = prs.slide_layouts[0]
error = "No presentation found"

# ✅ GOOD - Constants
slide_layout = prs.slide_layouts[SlideLayoutIndex.TITLE]
error = ErrorMessages.NO_PRESENTATION
```

## Tool Response Pattern

Every MCP tool follows this pattern:

```python
from .models import ErrorResponse, PresentationResponse
from .constants import ErrorMessages, SuccessMessages

@mcp.tool
async def pptx_create(name: str, theme: str | None = None) -> str:
    """
    Create a new PowerPoint presentation.

    Returns:
        JSON string with PresentationResponse model
    """
    try:
        # Business logic - returns Pydantic model
        metadata = await manager.create(name=name, theme=theme)

        # Return Pydantic model as JSON
        return PresentationResponse(
            name=metadata.name,
            message=SuccessMessages.PRESENTATION_CREATED.format(name=metadata.name),
            slide_count=metadata.slide_count,
            is_current=True,
        ).model_dump_json()

    except Exception as e:
        logger.error(f"Failed to create presentation: {e}")
        return ErrorResponse(error=str(e)).model_dump_json()
```

**Key Points:**
1. All tools return `str` (JSON)
2. Success returns `SomeResponse.model_dump_json()`
3. Errors return `ErrorResponse(error=...).model_dump_json()`
4. Use constants for messages
5. Try/except wraps all business logic

## Virtual Filesystem Integration

### AsyncVirtualFileSystem Pattern

Following chuk-motion, all file I/O uses VFS:

```python
from chuk_virtual_fs import AsyncVirtualFileSystem

# Initialize VFS with provider
vfs = AsyncVirtualFileSystem(provider="file")  # or "memory", "sqlite", "s3"

# Pass to manager
manager = PresentationManager(vfs=vfs, base_path="presentations")
```

### Manager VFS Operations

```python
class PresentationManager:
    def __init__(self, vfs: "AsyncVirtualFileSystem", base_path: str):
        self.vfs = vfs
        self.base_path = base_path
        self._presentations: dict[str, Presentation] = {}
        self._metadata: dict[str, PresentationMetadata] = {}

    async def _save_to_vfs(self, name: str, prs: Presentation) -> bool:
        """Save presentation to VFS."""
        buffer = io.BytesIO()
        prs.save(buffer)
        buffer.seek(0)
        data = buffer.read()

        file_path = self._get_vfs_path(name)
        await self.vfs.write_file(file_path, data)
        return True

    async def _load_from_vfs(self, name: str) -> Presentation | None:
        """Load presentation from VFS."""
        file_path = self._get_vfs_path(name)

        if not await self.vfs.exists(file_path):
            return None

        data = await self.vfs.read_file(file_path)
        buffer = io.BytesIO(data)
        return Presentation(buffer)
```

## Type Hints

Use modern Python type hints throughout:

```python
# ❌ OLD STYLE
from typing import Optional, Dict, List

def get(name: Optional[str] = None) -> Optional[Presentation]:
    presentations: Dict[str, Presentation] = {}
    slides: List[str] = []

# ✅ NEW STYLE (Python 3.10+)
def get(name: str | None = None) -> Presentation | None:
    presentations: dict[str, Presentation] = {}
    slides: list[str] = []
```

## Validation Patterns

### Field Validation

```python
class PresentationInfo(BaseModel):
    name: str = Field(..., min_length=1, description="Presentation name")
    slide_count: int = Field(..., ge=0, description="Number of slides")

    class Config:
        extra = "forbid"
```

### Literal Types for Enums

```python
from typing import Literal

variant: Literal["minimal", "standard", "bold"] = "standard"
storage_provider: Literal["file", "memory", "sqlite", "s3"] = "file"
```

### Nested Models

```python
class SlideMetadata(BaseModel):
    index: int = Field(..., ge=0)
    has_chart: bool = False
    has_table: bool = False

class PresentationMetadata(BaseModel):
    name: str
    slides: list[SlideMetadata] = Field(default_factory=list)

    def add_slide_metadata(self, slide_meta: SlideMetadata) -> None:
        self.slides.append(slide_meta)
        self.slide_count = len(self.slides)
```

## Serialization

### To JSON

```python
# Pydantic model to JSON
response = PresentationResponse(name="demo", message="Success", slide_count=5)
json_str = response.model_dump_json()
```

### To Dict

```python
# For template rendering, etc.
response_dict = response.model_dump()
```

### From JSON/Dict

```python
# Parse from dict
data = {"name": "demo", "message": "Success", "slide_count": 5}
response = PresentationResponse(**data)

# Parse from JSON
json_str = '{"name": "demo", "message": "Success", "slide_count": 5}'
response = PresentationResponse.model_validate_json(json_str)
```

## Error Handling

```python
try:
    # Business logic
    result = await manager.create(name)
    return SuccessResponse(message="Created").model_dump_json()

except ValidationError as e:
    # Pydantic validation error
    return ErrorResponse(error=f"Validation failed: {e}").model_dump_json()

except Exception as e:
    # General error
    logger.error(f"Operation failed: {e}")
    return ErrorResponse(error=str(e)).model_dump_json()
```

## Testing Pattern

Use memory provider for fast, isolated tests:

```python
import pytest
from chuk_virtual_fs import AsyncVirtualFileSystem

@pytest.fixture
async def vfs():
    """VFS fixture with memory provider."""
    async with AsyncVirtualFileSystem(provider="memory") as fs:
        yield fs

@pytest.fixture
async def manager(vfs):
    """Manager fixture."""
    return PresentationManager(vfs=vfs)

async def test_create_presentation(manager):
    metadata = await manager.create("test")
    assert metadata.name == "test"
    assert metadata.slide_count == 0
    assert metadata.is_saved == True
```

## Migration Guide

### From Dict to Pydantic

**Before:**
```python
def list_presentations() -> dict[str, int]:
    return {"demo": 5, "report": 10}
```

**After:**
```python
def list_presentations() -> ListPresentationsResponse:
    presentations = [
        PresentationInfo(name="demo", slide_count=5, is_current=True),
        PresentationInfo(name="report", slide_count=10, is_current=False),
    ]
    return ListPresentationsResponse(
        presentations=presentations,
        total=len(presentations),
        current="demo",
    )
```

### From Strings to Constants

**Before:**
```python
if shape.shape_type == 13:  # Magic number!
    has_images = True

error = "No presentation found"  # Magic string!
```

**After:**
```python
if shape.shape_type == ShapeType.PICTURE:
    has_images = True

error = ErrorMessages.NO_PRESENTATION
```

## Best Practices

1. **Always use Pydantic models** for data structures
2. **Use constants** instead of magic strings/numbers
3. **Return `model_dump_json()`** from MCP tools
4. **Validate at boundaries** with Field constraints
5. **Use Literal types** for enums
6. **Document fields** with descriptions
7. **Set `extra = "forbid"`** to catch typos
8. **Use async VFS** for all file I/O
9. **Type hint everything** with modern syntax
10. **Handle errors consistently** with ErrorResponse

## Summary

The Pydantic-native architecture provides:
- ✅ Type safety throughout the codebase
- ✅ Automatic validation
- ✅ Self-documenting code
- ✅ Consistent error handling
- ✅ Easy testing with memory provider
- ✅ Flexible storage backends
- ✅ No magic strings or numbers
- ✅ LLM-friendly API responses
