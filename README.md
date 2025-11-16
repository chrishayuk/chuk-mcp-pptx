# Chuk MCP PowerPoint Server

A powerful, LLM-friendly PowerPoint design system with MCP server integration. Built with shadcn-inspired component architecture, featuring variants, composition patterns, and comprehensive theming.

## ✨ Highlights

- **🎨 Design System** - shadcn/ui-inspired component architecture
- **🎭 Theme System** - 15+ built-in themes with dark/light modes
- **🧩 Variant System** - Type-safe, composable variants (cva-inspired)
- **🔧 Composition Patterns** - Build complex UIs from subcomponents
- **📋 Component Registry** - LLM-friendly schemas and discovery
- **🎯 Design Tokens** - Consistent colors, typography, spacing
- **🤖 MCP Integration** - Full Model Context Protocol support
- **✅ Fully Tested** - 1387 tests with comprehensive coverage

## Project Structure

```
chuk-mcp-pptx/
├── src/chuk_mcp_pptx/
│   ├── components/        # Component library
│   │   ├── core/         # Core components (Card, Button, Badge, etc.)
│   │   ├── charts/       # Chart components (Bar, Line, Pie, etc.)
│   │   ├── code.py       # Code block components
│   │   └── base.py       # Base component class
│   ├── tokens/           # Design tokens (colors, typography, spacing)
│   ├── themes/           # Theme system and manager (15+ themes)
│   ├── layout/           # Layout system (Grid, Stack, Container, etc.)
│   ├── tools/            # MCP tool implementations
│   │   ├── component_tools.py  # Component creation tools
│   │   ├── chart_tools.py      # Chart creation tools
│   │   ├── shape_tools.py      # Shape and SmartArt tools
│   │   ├── text_tools.py       # Text manipulation tools
│   │   ├── image_tools.py      # Image handling tools
│   │   ├── layout_tools.py     # Layout management tools
│   │   ├── table_tools.py      # Table creation tools
│   │   ├── theme_tools.py      # Theme application tools
│   │   └── ...                 # And more specialized tools
│   ├── registry.py       # Component registry
│   ├── async_server.py   # Async MCP server
│   └── server.py         # Server entry point
├── docs/                 # Comprehensive documentation
├── examples/             # Examples and demos
├── tests/                # 1387 comprehensive tests
└── outputs/              # Generated presentations
```

## Features

### Core Features
- Create and manage multiple PowerPoint presentations
- Add various slide types (title, content, text, images, charts)
- Save/load presentations to/from disk
- Import/export as base64 for easy transfer
- Virtual Filesystem Integration
- Auto-save to VFS

### Design System Features ✨
- **Variant System** - cva-inspired composable variants
- **Composition Patterns** - shadcn-style component composition
- **Component Registry** - Discovery and documentation for LLMs
- **Design Tokens** - Colors, typography, spacing tokens
- **Theme System** - 15+ themes with export/import
- **Type Safety** - Pydantic schemas for validation

## Installation

```bash
# Using uv
uv sync
uv run chuk-mcp-pptx

# Or using pip
pip install -e .
```

## Usage

The server provides comprehensive MCP tools organized by category:

### Presentation Management
- `pptx_create` - Create a new presentation
- `pptx_list` - List all open presentations
- `pptx_switch` - Switch between presentations
- `pptx_get_info` - Get detailed info about a presentation
- `pptx_close` - Close a presentation
- `pptx_clear_all` - Clear all presentations from memory
- `pptx_status` - Get server status and VFS configuration

### Component Tools (50+ components)
- `pptx_add_card` - Add card component with variants
- `pptx_add_button` - Add button component
- `pptx_add_badge` - Add badge component
- `pptx_add_alert` - Add alert component
- `pptx_add_metric_card` - Add metric card with trend indicator
- `pptx_add_avatar` - Add avatar component
- `pptx_add_progress_bar` - Add progress bar
- `pptx_add_icon` - Add icon component
- And 40+ more shadcn-inspired components...

### Chart Tools (15+ chart types)
- `pptx_add_bar_chart` - Add bar/column charts
- `pptx_add_line_chart` - Add line/area charts
- `pptx_add_pie_chart` - Add pie/doughnut charts
- `pptx_add_scatter_chart` - Add scatter/bubble charts
- `pptx_add_radar_chart` - Add radar charts
- `pptx_add_combo_chart` - Add combination charts
- `pptx_add_funnel_chart` - Add funnel charts
- `pptx_add_gauge_chart` - Add gauge charts
- And more specialized visualization types...

### Layout Tools
- `pptx_list_layouts` - List available slide layouts
- `pptx_add_slide_with_layout` - Add slide with specific layout
- `pptx_customize_layout` - Customize slide layout properties
- `pptx_apply_master_layout` - Apply master layout to slides
- `pptx_duplicate_slide` - Duplicate existing slide
- `pptx_reorder_slides` - Reorder slides in presentation

### Text Tools
- `pptx_add_text_slide` - Add a slide with text content
- `pptx_add_text_box` - Add formatted text box
- `pptx_add_bullet_list` - Add bullet list with formatting
- `pptx_extract_all_text` - Extract all text from presentation

### Image Tools
- `pptx_add_image_slide` - Add slide with image
- `pptx_add_image` - Add image to existing slide
- `pptx_add_background_image` - Set slide background image
- `pptx_add_image_gallery` - Add image grid/gallery
- `pptx_add_image_with_caption` - Add image with caption
- `pptx_add_logo` - Add logo to slide
- `pptx_replace_image` - Replace existing image
- `pptx_add_image_placeholder` - Add placeholder for mockups

### Shape & SmartArt Tools
- `pptx_add_shape` - Add shapes with text and styling
- `pptx_add_arrow` - Add connector arrows
- `pptx_add_smart_art` - Add SmartArt-style diagrams
- `pptx_add_code_block` - Add syntax-highlighted code blocks

### Table Tools
- `pptx_add_table` - Add formatted tables
- `pptx_update_table` - Update table content
- `pptx_format_table` - Apply table formatting
- `pptx_add_comparison_table` - Add comparison tables
- `pptx_add_data_table` - Add data tables with headers

### Theme Tools
- `pptx_apply_theme` - Apply theme to presentation
- `pptx_list_themes` - List available themes
- `pptx_create_custom_theme` - Create custom theme
- `pptx_export_theme` - Export theme configuration
- `pptx_get_theme_colors` - Get theme color palette

### Token Tools
- `pptx_list_color_tokens` - List available color tokens
- `pptx_list_typography_tokens` - List typography tokens
- `pptx_list_spacing_tokens` - List spacing tokens
- `pptx_get_semantic_colors` - Get semantic color scheme

### Registry Tools
- `pptx_list_components` - List all available components
- `pptx_search_components` - Search components by keyword
- `pptx_get_component_info` - Get component documentation
- `pptx_list_component_examples` - Get component usage examples

### File Operations
- `pptx_save` - Save presentation to disk
- `pptx_load` - Load presentation from disk
- `pptx_export_base64` - Export as base64 data
- `pptx_import_base64` - Import from base64 data

## Running the Server

The server can run in different transport modes:

```bash
# Auto-detect mode (stdio for Claude Desktop, HTTP otherwise)
uv run python -m chuk_mcp_pptx.server

# Force stdio mode
MCP_TRANSPORT=stdio uv run python -m chuk_mcp_pptx.server

# Force HTTP mode on specific port
MCP_TRANSPORT=http MCP_PORT=8080 uv run python -m chuk_mcp_pptx.server
```

## Storage Configuration

The server uses `chuk-virtual-fs` for flexible storage with support for multiple backends:

### Storage Providers

- **file** (default): Local filesystem storage
- **memory**: In-memory storage (fast, for testing)
- **sqlite**: SQLite database storage
- **s3**: AWS S3 or S3-compatible storage

### Configuring Storage Provider

Storage is configured in `async_server.py` (line 49):

```python
# Change provider here
vfs = AsyncVirtualFileSystem(provider="file")  # or "memory", "sqlite", "s3"
```

**Default Configuration**:
```python
# Uses local filesystem with presentations stored in ./presentations/
vfs = AsyncVirtualFileSystem(provider="file")
manager = PresentationManager(vfs=vfs, base_path="presentations")
```

**Example Configurations**:

```python
# In-memory storage (for testing)
vfs = AsyncVirtualFileSystem(provider="memory")

# SQLite storage
vfs = AsyncVirtualFileSystem(provider="sqlite", db_path="presentations.db")

# S3 storage
vfs = AsyncVirtualFileSystem(
    provider="s3",
    bucket="my-presentations",
    region="us-east-1"
)
```

### Virtual Filesystem Integration

The server automatically persists all presentations to the configured storage backend:

1. **Auto-save**: Presentations are automatically saved to VFS when created or modified
2. **Auto-load**: Presentations are loaded from VFS when accessed
3. **Multi-server**: Multiple server instances can share presentations via VFS
4. **Flexible storage**: Switch storage backends without code changes

### Storage Patterns

1. **Virtual Filesystem**: All presentations use VFS for persistence (flexible backends)
2. **Base64 transfer**: Export/import presentations as base64 for transfer
3. **Image support**: Add images via file path or base64 data URLs

## Example Usage

When connected via MCP, tools can be called like:

```python
# Create a presentation
pptx_create(name="quarterly_report")

# Add a title slide
pptx_add_title_slide(
    title="Q4 2024 Results",
    subtitle="Revenue and Growth Analysis"
)

# Add content slide with bullets
pptx_add_slide(
    title="Key Achievements",
    content=[
        "Revenue increased by 25%",
        "Launched 3 new products",
        "Expanded to 5 new markets"
    ]
)

# Save the presentation
pptx_save(path="q4_report.pptx")

# Export for transfer
pptx_export_base64()  # Returns base64 data
```

## MCP Configuration

For Claude Desktop, add to your MCP settings:

```json
{
  "mcpServers": {
    "chuk-mcp-pptx": {
      "command": "uv",
      "args": ["run", "python", "-m", "chuk_mcp_pptx.server"],
      "cwd": "/path/to/chuk-mcp-pptx"
    }
  }
}
```

## Quick Start

### Basic Usage

```python
from pptx import Presentation
from chuk_mcp_pptx.components.core import Card, MetricCard
from chuk_mcp_pptx.themes import ThemeManager

# Create presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Apply theme
mgr = ThemeManager()
theme = mgr.get_theme("dark-violet")
theme.apply_to_slide(slide)

# Add card with composition
card = Card(variant="elevated", theme=theme.__dict__)
card.add_child(Card.Title("Dashboard"))
card.add_child(Card.Description("Real-time analytics"))
card.render(slide, left=1, top=1, width=4, height=2.5)

# Add metric cards
metrics = [
    MetricCard(label="Revenue", value="$1.2M", change="+12%", trend="up", theme=theme.__dict__),
    MetricCard(label="Users", value="45K", change="+8%", trend="up", theme=theme.__dict__),
]

for i, metric in enumerate(metrics):
    metric.render(slide, left=1 + i*3, top=4, width=2.5, height=1.5)

prs.save("output.pptx")
```

### Run Examples

```bash
# Core components showcase
uv run python examples/core_components_showcase.py

# Layout system demo
uv run python examples/layout_system_showcase.py

# Theme showcase
uv run python examples/themes_showcase.py

# Token showcase
uv run python examples/tokens_showcase.py
```

## Documentation


## Testing

### Run All Tests

```bash
# All 1387 tests
uv run pytest tests/ -v

# Specific test suites
uv run pytest tests/components/ -v               # Component tests (900+ tests)
uv run pytest tests/layout/ -v                   # Layout tests (100+ tests)
uv run pytest tests/tools/ -v                    # MCP tools tests (350+ tests)
uv run pytest tests/themes/ -v                   # Theme tests (30+ tests)
uv run pytest tests/tokens/ -v                   # Token tests (10+ tests)
```

### Test Coverage

- **Component System**: 900+ tests - 100% pass ✅
- **Chart Components**: 300+ tests - 100% pass ✅
- **Layout System**: 100+ tests - 100% pass ✅
- **MCP Tools**: 350+ tests - 100% pass ✅
- **Theme System**: 30+ tests - 100% pass ✅
- **Token System**: 10+ tests - 100% pass ✅

**Total: 1387 tests, all passing** 🎉

## Dependencies

- `python-pptx` - PowerPoint file creation and manipulation
- `chuk-mcp-server` - MCP server framework
- `mcp` - Model Context Protocol implementation
- `pydantic` - Schema validation
- `pytest` - Testing framework