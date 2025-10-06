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
- **✅ Fully Tested** - 249 tests with comprehensive coverage

## Project Structure

```
chuk-mcp-pptx/
├── src/chuk_mcp_pptx/
│   ├── components/        # Enhanced components (Card, MetricCard, etc.)
│   ├── tokens/            # Design tokens (colors, typography, spacing)
│   ├── themes/            # Theme system and manager
│   ├── variants.py        # Variant system (cva-inspired)
│   ├── composition.py     # Composition patterns
│   ├── registry.py        # Component registry
│   └── server.py          # MCP server
├── docs/                  # Comprehensive documentation
├── examples/              # Examples and demos
├── tests/                 # 249 comprehensive tests
└── outputs/               # Generated presentations
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

The server provides the following MCP tools:

### Presentation Management
- `pptx_create` - Create a new presentation
- `pptx_list` - List all open presentations
- `pptx_switch` - Switch between presentations
- `pptx_get_info` - Get detailed info about a presentation
- `pptx_close` - Close a presentation
- `pptx_clear_all` - Clear all presentations from memory
- `pptx_status` - Get server status and VFS configuration

### Slide Operations
- `pptx_add_title_slide` - Add a title slide
- `pptx_add_slide` - Add a content slide with bullet points
- `pptx_add_text_slide` - Add a slide with text content
- `pptx_add_image_slide` - Add a slide with an image

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

# Enable VFS persistence mode
PPTX_USE_VFS=true uv run python -m chuk_mcp_pptx.server

# VFS mode with custom path
PPTX_USE_VFS=true PPTX_VFS_PATH="vfs://my-presentations" uv run python -m chuk_mcp_pptx.server
```

### Environment Variables

- `PPTX_USE_VFS`: Set to "true" to enable VFS persistence (default: "false")
- `PPTX_VFS_PATH`: Base path in VFS for storing presentations (default: "vfs://presentations")

## Integration with Virtual Shell/Filesystem

The server supports multiple integration patterns:

1. **Direct file operations**: Save/load presentations directly to/from disk
2. **Base64 transfer**: Export/import presentations as base64 for transfer via virtual shell
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
from chuk_mcp_pptx.components.card_v2 import Card, MetricCard
from chuk_mcp_pptx.themes import ThemeManager

# Create presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Apply theme
mgr = ThemeManager()
theme = mgr.get_theme("dark-violet")
theme.apply_to_slide(slide)

# Add enhanced card with composition
card = Card(variant="elevated", padding="lg", theme=theme.to_dict())
card.add_child(Card.Header("Dashboard", "Real-time analytics"))
card.add_child(Card.Content("Your metrics are trending upward"))
card.render(slide, left=1, top=1, width=4, height=2.5)

# Add metric cards
metrics = [
    MetricCard("Revenue", "$1.2M", "+12%", "up", theme=theme.to_dict()),
    MetricCard("Users", "45K", "+8%", "up", theme=theme.to_dict()),
]

for i, metric in enumerate(metrics):
    metric.render(slide, left=1 + i*3, top=4, width=2.5, height=1.5)

prs.save("output.pptx")
```

### Run Examples

```bash
# Enhanced components demo
uv run python examples/enhanced_components_demo.py

# Theme showcase
uv run python examples/theme_showcase_by_domain.py

# Chart gallery
uv run python examples/beautiful_chart_gallery.py
```

## Documentation

- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Overview of enhancements
- **[docs/TOKENS.md](docs/TOKENS.md)** - Design token system
- **[docs/THEMES.md](docs/THEMES.md)** - Theme management
- **[docs/ENHANCED_COMPONENTS.md](docs/ENHANCED_COMPONENTS.md)** - Component system
- **[docs/CHARTS_AND_VISUALIZATION.md](docs/CHARTS_AND_VISUALIZATION.md)** - Charts

## Testing

### Run All Tests

```bash
# All 249 tests
uv run pytest tests/ -v

# Specific test suites
uv run pytest tests/tokens/test_tokens.py -v       # Token tests (29 tests)
uv run pytest tests/themes/test_themes.py -v       # Theme tests (34 tests)
uv run pytest tests/test_variants.py -v            # Variant tests (62 tests)
uv run pytest tests/test_composition.py -v         # Composition tests (37 tests)
```

### Test Coverage

- **Token System**: 29 tests - 100% pass ✅
- **Theme System**: 34 tests - 100% pass ✅
- **Variant System**: 62 tests - 100% pass ✅
- **Composition System**: 37 tests - 100% pass ✅
- **Component Tests**: 87 tests - 100% pass ✅

**Total: 249 tests, all passing** 🎉

## Dependencies

- `python-pptx` - PowerPoint file creation and manipulation
- `chuk-mcp-server` - MCP server framework
- `mcp` - Model Context Protocol implementation
- `pydantic` - Schema validation
- `pytest` - Testing framework