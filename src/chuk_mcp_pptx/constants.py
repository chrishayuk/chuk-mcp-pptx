"""
Constants and Enums for PowerPoint MCP Server

All magic strings, numbers, and configuration values are defined here.
Uses Literal types and Enums for type safety.
"""
from enum import Enum, IntEnum
from typing import Literal


# Slide Layout Indices (python-pptx defaults)
class SlideLayoutIndex(IntEnum):
    """Standard slide layout indices in default PowerPoint templates."""

    TITLE = 0
    TITLE_AND_CONTENT = 1
    SECTION_HEADER = 2
    TWO_CONTENT = 3
    COMPARISON = 4
    TITLE_ONLY = 5
    BLANK = 6
    CONTENT_WITH_CAPTION = 7
    PICTURE_WITH_CAPTION = 8


# Chart Types
ChartType = Literal[
    "bar",
    "column",
    "line",
    "pie",
    "doughnut",
    "scatter",
    "bubble",
    "area",
    "radar",
    "combo",
    "funnel",
    "gauge",
    "waterfall",
    "treemap",
    "sunburst",
]


# Shape Types (MSO_SHAPE_TYPE enum values)
class ShapeType(IntEnum):
    """Microsoft Office shape type constants."""

    AUTO_SHAPE = 1
    CALLOUT = 2
    CANVAS = 20
    CHART = 3
    COMMENT = 4
    DIAGRAM = 21
    EMBEDDED_OLE_OBJECT = 7
    FORM_CONTROL = 8
    FREEFORM = 5
    GROUP = 6
    IGX_GRAPHIC = 24
    INK = 22
    INK_COMMENT = 23
    LINE = 9
    LINKED_OLE_OBJECT = 10
    LINKED_PICTURE = 11
    MEDIA = 16
    OLE_CONTROL_OBJECT = 12
    PICTURE = 13
    PLACEHOLDER = 14
    SCRIPT_ANCHOR = 18
    TABLE = 19
    TEXT_BOX = 17
    TEXT_EFFECT = 15
    THREE_D_MODEL = 30
    WEB_VIDEO = 26


# Component Types
ComponentType = Literal[
    "card",
    "button",
    "badge",
    "alert",
    "metric_card",
    "avatar",
    "progress_bar",
    "icon",
    "separator",
    "skeleton",
    "spinner",
    "tooltip",
    "breadcrumb",
    "pagination",
    "tabs",
    "accordion",
    "calendar",
    "timeline",
    "kanban",
    "chart",
    "table",
    "code_block",
]


# Chat Message Variants
MessageVariant = Literal["sent", "received", "user", "assistant", "system"]


# Chat Platform Types
ChatPlatform = Literal[
    "android",
    "ios",
    "chatgpt",
    "slack",
    "teams",
    "whatsapp",
    "facebook",
    "msn",
    "aol",
    "generic",
]


# Browser Types
BrowserType = Literal["chrome", "safari", "firefox"]


# Container Platform Types
ContainerPlatform = Literal["iphone", "samsung", "windows", "macos", "generic"]


# Device Variants
DeviceVariant = Literal["pro", "pro-max", "standard"]


# Code Language Types
CodeLanguage = Literal[
    "python",
    "javascript",
    "typescript",
    "java",
    "csharp",
    "cpp",
    "go",
    "rust",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "sql",
    "html",
    "css",
    "shell",
    "yaml",
    "json",
    "text",
]


# Text Alignment Types
TextAlignment = Literal["left", "center", "right", "justify"]


# Theme Mode
ThemeMode = Literal["light", "dark"]

# Theme Mode Constants
class Theme:
    """Theme mode constants to avoid hardcoded strings."""
    LIGHT = "light"
    DARK = "dark"


# Platform Name Constants
class Platform:
    """Platform name constants to avoid hardcoded strings."""

    # Chat Platforms
    IOS = "ios"
    ANDROID = "android"
    WHATSAPP = "whatsapp"
    CHATGPT = "chatgpt"
    SLACK = "slack"
    TEAMS = "teams"
    FACEBOOK = "facebook"
    MSN = "msn"
    AOL = "aol"
    GENERIC = "generic"

    # OS Platforms
    MACOS = "macos"
    WINDOWS = "windows"

    # Browser Platforms
    CHROME = "chrome"
    SAFARI = "safari"
    FIREFOX = "firefox"

    # Device Platforms
    IPHONE = "iphone"
    SAMSUNG = "samsung"


# Component Sizing Constants
class ComponentSizing:
    """Component sizing constants for width/height calculations."""

    # Character width estimations (in inches) for text sizing
    CHAR_WIDTH_SM = 0.06
    CHAR_WIDTH_MD = 0.07
    CHAR_WIDTH_LG = 0.08

    # Base widths for button components
    BUTTON_BASE_WIDTH_SM = 1.5
    BUTTON_BASE_WIDTH_MD = 2.0
    BUTTON_BASE_WIDTH_LG = 2.5

    # Badge component sizing
    BADGE_CHAR_WIDTH = 0.08
    BADGE_PADDING = 0.5

    # Card component line heights
    LINE_HEIGHT_INCHES = 0.35
    PARAGRAPH_GAP = 0.08
    TITLE_GAP = 0.22

    # UI element sizing (in points)
    BORDER_WIDTH_THIN = 0.5
    BORDER_WIDTH_MEDIUM = 1
    BORDER_WIDTH_THICK = 2

    # Shadow properties (in points)
    SHADOW_BLUR_SM = 2
    SHADOW_BLUR_MD = 4
    SHADOW_BLUR_LG = 6
    SHADOW_DISTANCE_SM = 1
    SHADOW_DISTANCE_MD = 2
    SHADOW_DISTANCE_LG = 4

    # Spacing (in points)
    SPACE_XS = 2
    SPACE_SM = 3
    SPACE_MD = 4
    SPACE_LG = 6


# Theme Names
ThemeName = Literal[
    "default",
    "dark-violet",
    "tech-blue",
    "minimal",
    "vibrant",
    "corporate",
    "creative",
    "elegant",
    "modern",
    "professional",
]


# Export/Import Formats
ExportFormat = Literal["base64", "file", "vfs"]


# Storage Providers
StorageProvider = Literal["file", "memory", "sqlite", "s3"]


# File Extensions
class FileExtension:
    """File extension constants."""

    PPTX = ".pptx"
    JSON = ".json"
    PNG = ".png"
    JPG = ".jpg"
    JPEG = ".jpeg"
    GIF = ".gif"
    BMP = ".bmp"


# Default Values
class Defaults:
    """Default values for various operations."""

    PRESENTATION_NAME = "presentation"
    VFS_BASE_PATH = "presentations"
    CHART_WIDTH = 8.0  # inches
    CHART_HEIGHT = 5.0  # inches
    IMAGE_WIDTH = 6.0  # inches
    IMAGE_HEIGHT = 4.0  # inches
    FONT_SIZE_TITLE = 44
    FONT_SIZE_BODY = 18
    FONT_SIZE_CAPTION = 14


# Spacing and Layout Constants
class Spacing:
    """Spacing and layout constants for consistent positioning."""

    # Slide dimensions (standard 16:9)
    SLIDE_WIDTH = 10.0  # inches
    SLIDE_HEIGHT = 7.5  # inches

    # Safe areas and margins
    SLIDE_MARGIN = 0.5  # inches
    CONTENT_LEFT = 0.5  # inches
    CONTENT_TOP = 1.0  # inches
    CONTENT_RIGHT = 9.5  # inches
    CONTENT_BOTTOM = 7.0  # inches
    CONTENT_WIDTH = 9.0  # inches
    CONTENT_HEIGHT = 6.0  # inches

    # Title positioning
    TITLE_TOP = 0.5  # inches
    TITLE_HEIGHT = 1.0  # inches
    TITLE_SAFE_TOP = 1.6  # Space below title

    # Common spacing values
    SPACING_SMALL = 0.1  # inches
    SPACING_MEDIUM = 0.25  # inches
    SPACING_LARGE = 0.5  # inches
    SPACING_XLARGE = 1.0  # inches

    # Grid layout
    GRID_PADDING = 0.1  # inches between grid items

    # Logo positioning
    LOGO_SIZE_SMALL = 0.5  # inches
    LOGO_SIZE_MEDIUM = 1.0  # inches
    LOGO_SIZE_LARGE = 1.5  # inches


# Color Constants (RGB tuples)
class Colors:
    """Common color constants."""

    PRIMARY_BLUE = (0, 112, 192)
    ACCENT_ORANGE = (255, 127, 0)
    SUCCESS_GREEN = (84, 130, 53)
    WARNING_YELLOW = (255, 192, 0)
    ERROR_RED = (192, 0, 0)
    NEUTRAL_GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


# Server Configuration
class ServerConfig:
    """Server configuration constants."""

    NAME = "chuk-mcp-pptx"
    VERSION = "0.1.0"
    DEFAULT_PORT = 8000
    DEFAULT_HOST = "localhost"


# Error Messages
class ErrorMessages:
    """Standard error message templates."""

    NO_PRESENTATION = "No presentation found. Create one first with pptx_create()"
    PRESENTATION_NOT_FOUND = "Presentation '{name}' not found"
    SLIDE_NOT_FOUND = "Slide index {index} not found in presentation"
    INVALID_CHART_TYPE = "Invalid chart type: {chart_type}"
    INVALID_THEME = "Invalid theme: {theme}"
    FILE_NOT_FOUND = "File not found: {path}"
    SAVE_FAILED = "Failed to save presentation: {error}"
    LOAD_FAILED = "Failed to load presentation: {error}"


# Success Messages
class SuccessMessages:
    """Standard success message templates."""

    PRESENTATION_CREATED = "Created presentation '{name}'"
    SLIDE_ADDED = "Added {slide_type} slide to '{presentation}'"
    CHART_ADDED = "Added {chart_type} chart to slide {index}"
    COMPONENT_ADDED = "Added {component} component to slide {index}"
    PRESENTATION_SAVED = "Saved presentation to: {path}"
    PRESENTATION_LOADED = "Loaded presentation from: {path}"
    THEME_APPLIED = "Applied theme '{theme}' to presentation '{name}'"
