# Chuk MCP PowerPoint Server

A powerful, LLM-friendly PowerPoint design system with MCP server integration. Built with a template-first architecture, universal component API, and comprehensive theming for creating professional presentations.

## Highlights

- **Template-First Workflow** - Professional templates with 50+ layouts each
- **Universal Component API** - Single tool for all components (charts, tables, images, etc.)
- **Design System** - shadcn/ui-inspired component architecture with variants
- **Theme System** - 15+ built-in themes with dark/light modes
- **Component Registry** - LLM-friendly schemas and discovery
- **Design Tokens** - Consistent colors, typography, spacing
- **MCP Integration** - Full Model Context Protocol support
- **Fully Tested** - 2395+ tests with comprehensive coverage
- **Cloud Ready** - Deploy to Fly.io with Tigris S3 and Redis

## Project Structure

```
chuk-mcp-pptx/
├── src/chuk_mcp_pptx/
│   ├── components/           # Component library
│   │   ├── core/            # Core components (Card, Badge, Table, Image, etc.)
│   │   ├── charts/          # Chart components (Column, Line, Pie, Gauge, etc.)
│   │   ├── tracking.py      # Component tracking system
│   │   ├── registry.py      # Component registry with schemas
│   │   └── base.py          # Base component class
│   ├── tools/               # MCP tool implementations
│   │   ├── universal/       # Universal component API
│   │   │   ├── api.py       # pptx_add_component, pptx_update_component
│   │   │   ├── registry.py  # Component discovery tools
│   │   │   └── semantic.py  # Semantic slide tools
│   │   ├── template/        # Template tools
│   │   │   ├── workflow.py  # pptx_add_slide_from_template
│   │   │   ├── analyze.py   # pptx_analyze_template
│   │   │   └── list.py      # pptx_list_templates
│   │   ├── core/            # Core tools (placeholder population)
│   │   ├── theme/           # Theme management tools
│   │   ├── layout/          # Slide layout tools
│   │   └── inspection/      # Slide inspection tools
│   ├── templates/           # Template manager
│   ├── themes/              # Theme system (15+ themes)
│   ├── tokens/              # Design tokens
│   ├── layout/              # Layout helpers
│   ├── slide_templates/     # Pre-built slide templates
│   ├── async_server.py      # Async MCP server
│   └── server.py            # Server entry point
├── docs/                    # Documentation
├── examples/                # Examples and demos (see Golden Path)
├── tests/                   # 2395+ comprehensive tests
└── outputs/                 # Generated presentations
```

## Features

### Core Features
- Create presentations from professional templates (50+ layouts)
- Universal component API for all content types
- Smart placeholder population with automatic content handling
- Template-aware design system resolution
- Save/load presentations, import/export as base64
- Cloud storage with presigned download URLs

### Design System Features
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

## MCP Tools Reference

The server provides MCP tools organized into logical groups:

### Presentation Management
- `pptx_create` - Create presentation (optionally from template)
- `pptx_list` - List all open presentations
- `pptx_switch` - Switch between presentations
- `pptx_get_info` - Get presentation metadata
- `pptx_delete` - Delete a presentation
- `pptx_status` - Get server status

### Template Workflow (Recommended)
- `pptx_analyze_template` - Analyze template layouts and placeholders
- `pptx_analyze_template_variants` - Group similar layouts
- `pptx_add_slide_from_template` - Add slide using template layout
- `pptx_populate_placeholder` - Populate placeholders with content
- `pptx_list_templates` - List available templates
- `pptx_get_builtin_template` - Get built-in template info

### Universal Component API
- `pptx_add_component` - Add any component (charts, tables, images, etc.)
- `pptx_update_component` - Update existing component
- `pptx_list_slide_components` - List and validate slide components

### Component Registry
- `pptx_list_components` - List all available components
- `pptx_search_components` - Search components by keyword
- `pptx_get_component_schema` - Get component schema/props
- `pptx_get_component_variants` - Get variant options
- `pptx_get_component_examples` - Get usage examples
- `pptx_export_registry_docs` - Export full registry docs

### Layout Management
- `pptx_list_layouts` - List available slide layouts
- `pptx_add_slide_with_layout` - Add slide with specific layout
- `pptx_customize_layout` - Customize slide appearance
- `pptx_apply_master_layout` - Apply master formatting
- `pptx_duplicate_slide` - Duplicate existing slide
- `pptx_reorder_slides` - Reorder slides

### Theme Tools
- `pptx_list_themes` - List available themes
- `pptx_get_theme_info` - Get theme details
- `pptx_apply_theme` - Apply theme to presentation
- `pptx_create_custom_theme` - Create custom theme
- `pptx_apply_component_theme` - Apply theme to component
- `pptx_list_component_themes` - List component-specific themes

### Inspection Tools
- `pptx_inspect_slide` - Detailed slide inspection
- `pptx_fix_slide_layout` - Auto-fix layout issues
- `pptx_analyze_presentation_layout` - Full presentation analysis

### Semantic Tools
- `pptx_add_title_slide` - Add title slide (deprecated, use templates)
- `pptx_add_slide` - Add content slide (deprecated, use templates)

### File Operations
- `pptx_save` - Save presentation to disk
- `pptx_export_base64` - Export as base64 data
- `pptx_import_base64` - Import from base64 data
- `pptx_get_download_url` - Get presigned download URL

## Recommended Workflow

### Template-Based Presentations (Recommended)

The recommended approach uses professional templates for consistent, high-quality presentations:

```python
# 1. Create presentation from a template
await pptx_create(name="quarterly_report", template_name="brand_proposal")

# 2. Analyze template to see ALL available layouts (CRITICAL!)
await pptx_analyze_template("brand_proposal")
# Returns 50+ layouts: Title, Content, Comparison, Quote, Charts, etc.

# 3. Add slides using specific layouts
result = await pptx_add_slide_from_template(layout_index=0)  # Title slide
# Response shows: placeholder 0 (TITLE), placeholder 1 (SUBTITLE)

# 4. Populate text placeholders
await pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="Q4 Report")
await pptx_populate_placeholder(slide_index=0, placeholder_idx=1, content="Financial Results")

# 5. Add content slide with chart
result = await pptx_add_slide_from_template(layout_index=40)  # Chart layout
# Response shows: placeholder 2 (CHART)

# 6. Populate chart placeholder with structured data
await pptx_populate_placeholder(
    slide_index=1,
    placeholder_idx=2,
    content={
        'type': 'ColumnChart',
        'title': 'Revenue by Quarter',
        'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
        'series': {'Revenue': [100, 120, 140, 180]}
    }
)

# 7. Verify slide components
await pptx_list_slide_components(slide_index=1)
# Validates all placeholders are populated, no empty "Click to add" text

# 8. Save presentation
await pptx_save(path="quarterly_report.pptx")
```

### Universal Component API

For adding components anywhere (free-form or into placeholders):

```python
# Add chart into placeholder (template-aware)
await pptx_add_component(
    slide_index=1,
    component="ColumnChart",
    target_placeholder=2,
    params={
        "title": "Sales Growth",
        "categories": ["Jan", "Feb", "Mar"],
        "series": {"Sales": [100, 150, 200]}
    }
)

# Add table into placeholder
await pptx_add_component(
    slide_index=2,
    component="Table",
    target_placeholder=14,
    params={
        "headers": ["Product", "Q1", "Q2"],
        "data": [["Widget A", "$10K", "$15K"], ["Widget B", "$8K", "$12K"]]
    }
)

# Free-form positioning (for blank slides)
await pptx_add_component(
    slide_index=3,
    component="Badge",
    left=2.0, top=3.0, width=1.5, height=0.5,
    params={"text": "New", "variant": "success"}
)
```

## Running the Server

The server can run in different transport modes:

```bash
# Auto-detect mode (stdio for Claude Desktop, HTTP otherwise)
uv run python -m chuk_mcp_pptx.server

# Force stdio mode
uv run python -m chuk_mcp_pptx.server stdio

# Force HTTP mode on specific port
uv run python -m chuk_mcp_pptx.server http --port 8080
```

## Cloud Deployment (Fly.io)

Deploy the PowerPoint MCP Server to Fly.io with Tigris S3 storage and Redis for production use.

### Quick Deploy

```bash
# 1. Create the app
fly apps create chuk-mcp-pptx

# 2. Create Tigris S3 bucket for artifact storage
fly storage create

# 3. Create Redis instance
fly redis create --name chuk-mcp-pptx-redis --region lhr --no-replicas --enable-eviction

# 4. Set Redis URL secret (from redis create output)
fly secrets set REDIS_URL="redis://default:password@fly-chuk-mcp-pptx-redis.upstash.io:6379"

# 5. Deploy
fly deploy
```

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Fly.io Edge                            │
│                   (chuk-mcp-pptx.fly.dev)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 PowerPoint MCP Server                       │
│                   (Python + FastMCP)                        │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │ Presentation    │  │ chuk-artifacts                  │  │
│  │ Manager         │──│ (S3 + Redis backend)            │  │
│  └─────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │                            │
          ▼                            ▼
┌─────────────────────┐  ┌─────────────────────────────────┐
│    Fly Redis        │  │       Tigris S3                 │
│  (Upstash managed)  │  │   (Object storage)              │
│                     │  │                                 │
│  • Session metadata │  │  • Presentation files (.pptx)   │
│  • Distributed lock │  │  • Exported artifacts           │
└─────────────────────┘  └─────────────────────────────────┘
```

### Environment Variables

| Variable | Description | Set Via |
|----------|-------------|---------|
| `CHUK_ARTIFACTS_PROVIDER` | Storage provider (`s3`) | fly.toml |
| `AWS_ACCESS_KEY_ID` | Tigris access key | secrets |
| `AWS_SECRET_ACCESS_KEY` | Tigris secret key | secrets |
| `AWS_ENDPOINT_URL_S3` | Tigris endpoint | secrets |
| `BUCKET_NAME` | S3 bucket name | secrets |
| `REDIS_URL` | Redis connection URL | secrets |

### GitHub Actions Auto-Deploy

Add `FLY_API_TOKEN` to your repository secrets for automatic deployment on push to main:

```bash
fly tokens create deploy -x 999999h
```

The included `.github/workflows/fly-deploy.yml` handles automatic deployment.

### Getting Download URLs

When deployed to Fly.io with S3 storage, use `pptx_get_download_url` to get presigned URLs:

```python
# Create and save a presentation
pptx_create(name="report")
pptx_add_title_slide(title="Q4 Report")

# Get a download URL (valid for 1 hour by default)
result = pptx_get_download_url()
# Returns: {"url": "https://fly.storage.tigris.dev/...", "expires_in": 3600}

# Custom expiration (2 hours)
result = pptx_get_download_url(expires_in=7200)
```

For detailed deployment instructions, see [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md).

## Storage Configuration

The server uses `chuk-artifacts` for flexible storage with support for multiple backends:

### Storage Providers

- **memory** (default): In-memory storage (for local development)
- **file**: Local filesystem storage
- **sqlite**: SQLite database storage
- **s3**: AWS S3 or S3-compatible storage (Tigris, MinIO, etc.)

### Environment-Based Configuration

Storage is configured via environment variables:

```bash
# S3/Tigris storage (production)
export CHUK_ARTIFACTS_PROVIDER=s3
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_ENDPOINT_URL_S3=https://fly.storage.tigris.dev
export BUCKET_NAME=your-bucket

# Redis for metadata (optional but recommended for S3)
export REDIS_URL=redis://localhost:6379
```

### Artifact Store Integration

The server automatically persists presentations to the configured artifact store:

1. **Auto-save**: Presentations are automatically saved when created or modified
2. **Auto-load**: Presentations are loaded from the store when accessed
3. **Multi-server**: Multiple server instances can share presentations via S3
4. **Presigned URLs**: Generate download URLs for cloud-stored presentations

### Storage Patterns

1. **Artifact Store**: All presentations use chuk-artifacts for persistence
2. **Base64 transfer**: Export/import presentations as base64 for transfer
3. **Presigned URLs**: Get direct download links from S3/Tigris storage
4. **Image support**: Add images via file path or base64 data URLs

## Available Components

Components available through `pptx_add_component` and `pptx_populate_placeholder`:

### Charts
- `ColumnChart`, `BarChart` - Bar/column charts with clustered, stacked, stacked100 variants
- `LineChart`, `AreaChart` - Line/area charts with smooth, markers variants
- `PieChart`, `DoughnutChart` - Pie/doughnut charts with exploded variant
- `ScatterChart`, `BubbleChart` - Scatter/bubble visualizations
- `RadarChart` - Spider/radar charts
- `WaterfallChart` - Waterfall charts for financial data
- `FunnelChart` - Sales funnel visualizations
- `GaugeChart` - Gauge/speedometer charts
- `GanttChart` - Project timeline charts
- `HeatmapChart` - Heat map visualizations
- `SparklineChart` - Inline mini charts
- `Matrix3DChart` - 3D matrix visualizations

### Data
- `Table` - Tables with striped, bordered, compact variants
- `ContentGrid` - Grid layout for multiple items

### UI Components
- `Card` - Container with header/footer
- `Badge` - Status badges (default, secondary, success, warning, destructive)
- `Alert` - Alert boxes (default, info, success, warning, error)
- `Button` - Buttons (default, secondary, outline, ghost, destructive)
- `Progress` - Progress bars
- `Avatar` - Avatar/profile images
- `Icon` - Icon components

### Media
- `Image` - Images with various fit modes
- `Video` - Video placeholders
- `CodeBlock` - Syntax-highlighted code

### Layout
- `Container` - Content containers
- `Stack` - Vertical/horizontal stacks
- `Timeline` - Timeline visualizations
- `SmartArt` - SmartArt-style diagrams

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

### Via MCP (Recommended)

When connected via MCP client (Claude Desktop, etc.):

```python
# Create from template
await pptx_create(name="my_deck", template_name="brand_proposal")

# Analyze available layouts
await pptx_analyze_template("brand_proposal")

# Add and populate slides
await pptx_add_slide_from_template(layout_index=0)
await pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="Welcome")

# Save
await pptx_save(path="my_deck.pptx")
```

### Direct Python Usage

```python
from pptx import Presentation
from chuk_mcp_pptx.components.core import Card, Table
from chuk_mcp_pptx.components.charts import ColumnChart
from chuk_mcp_pptx.themes import ThemeManager

# Create presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Apply theme
theme_mgr = ThemeManager()
theme = theme_mgr.get_theme("dark-violet")
theme.apply_to_slide(slide)

# Add a chart
chart = ColumnChart(
    title="Revenue by Quarter",
    categories=["Q1", "Q2", "Q3", "Q4"],
    series={"Revenue": [100, 150, 200, 250]},
    theme=theme.__dict__
)
chart.render(slide, left=1, top=1.5, width=8, height=4)

# Add a table
table = Table(
    headers=["Product", "Sales", "Growth"],
    data=[
        ["Widget A", "$50K", "+15%"],
        ["Widget B", "$30K", "+8%"],
    ],
    variant="striped",
    theme=theme.__dict__
)
table.render(slide, left=1, top=5.5, width=8, height=1.5)

prs.save("output.pptx")
```

## Golden Path Examples

The `examples/` directory contains canonical demonstrations of the optimal workflow:

### Golden Path Pitch Deck

```bash
uv run python examples/golden_path_pitch_deck.py
```

Creates an 8-slide pitch deck demonstrating:
- Template-first workflow with `brand_proposal` template
- Chart components (Column, Line, Pie, Bar)
- Table components with variants
- Proper placeholder population
- Theme application

**Output:** `examples/output_pitch_deck.pptx`

### Golden Path Prompts

See `examples/GOLDEN_PATH_PROMPTS.md` for three canonical demo prompts:
1. **Startup Pitch Deck** (8 slides) - Full workflow example
2. **Quarterly Business Review** (10 slides) - Charts and tables
3. **Technical Tutorial** (6 slides) - Code examples and diagrams

These prompts show the expected MCP tool-call sequences for common presentation types.

## Documentation


## Testing

### Run All Tests

```bash
# All 2395+ tests
uv run pytest tests/ -v

# Or use make
make test

# Full check (lint, typecheck, security, tests)
make check
```

### Test Suites

```bash
uv run pytest tests/components/ -v               # Component tests
uv run pytest tests/components/charts/ -v        # Chart component tests
uv run pytest tests/tools/ -v                    # MCP tools tests
uv run pytest tests/layout/ -v                   # Layout tests
uv run pytest tests/themes/ -v                   # Theme tests
```

**Total: 2395+ tests, all passing**

## Dependencies

- `python-pptx` - PowerPoint file creation and manipulation
- `chuk-mcp-server` - MCP server framework
- `chuk-artifacts` - Flexible artifact storage (memory, file, sqlite, s3)
- `mcp` - Model Context Protocol implementation
- `pydantic` - Schema validation
- `aiobotocore` - Async S3 client (for cloud deployments)
- `redis` - Redis client (for distributed deployments)
- `pytest` - Testing framework