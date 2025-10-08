# PowerPoint MCP Server Examples

This directory contains examples demonstrating the PowerPoint MCP Server's capabilities, organized by category.

## 🎨 Design System Showcases (Start Here!)

Our "shadcn for PowerPoint" design system - comprehensive demonstrations:

### Core Design System
- **`tokens_showcase.py`** - Design tokens: colors, typography, spacing, semantic colors
- **`layout_system_showcase.py`** - Grid system, containers, stacks, spacing scale
- **`themes_showcase.py`** - All available themes with components and charts
- **`core_components_showcase.py`** - Complete UI component library:
  - Buttons, badges, alerts, cards
  - Progress bars, icons, timeline
  - Tiles, avatars
  - **Shapes** (25+ geometric shapes)
  - **Connectors & Arrows** (straight, elbow, curved)
  - **SmartArt Diagrams** (process, cycle, hierarchy)
  - **Text** (text boxes, bullet lists, formatting)
  - **Images** (layouts, effects, aspect ratios, filters)

### Business-Focused Galleries
- **`theme_showcase_by_domain.py`** - Business domain-specific charts across all themes (48 presentations!)
- **`complete_chart_showcase.py`** - Comprehensive showcase of all chart types with modern themes

## 📊 Chart & Data Galleries

### Chart Galleries
- **`theme_chart_galleries.py`** - 🆕 Individual chart galleries for each theme (12 galleries)
  - Creates one gallery per theme showing all chart types
  - Demonstrates consistent styling across themes
  - 7 slides per gallery with professional layouts
  - All charts use component-based architecture

### Data Tables
- **`table_gallery.py`** - 🆕 Professional table components (3 themed galleries)
  - Financial reports, product comparisons, project timelines
  - Performance metrics, budget allocations
  - 4 table variants: default, bordered, striped, minimal
  - Creates galleries for corporate, dark, and ocean themes

### Chat Interfaces
- **`chat_conversation_showcase.py`** - Chat message components and layouts
- **`container_chat_showcase.py`** - Chat interfaces with containers
- **`platform_chat_showcase.py`** - Platform-style chat designs

## 🚀 Quick Start Examples

- **`simple_example.py`** - Minimal working example
- **`code_examples.py`** - Code syntax highlighting in slides

## 📁 Output Structure

Running these examples will create presentations in the `../outputs/` directory:

```
outputs/
├── complete_chart_showcase.pptx       # Main comprehensive chart gallery
├── theme_galleries/                   # Individual theme chart galleries
│   ├── chart_gallery_dark.pptx       # Dark theme charts
│   ├── chart_gallery_dark_blue.pptx  # Dark blue theme
│   ├── chart_gallery_dark_violet.pptx
│   ├── chart_gallery_dark_green.pptx
│   ├── chart_gallery_dark_purple.pptx
│   ├── chart_gallery_light.pptx      # Light theme charts
│   ├── chart_gallery_corporate.pptx  # Corporate theme
│   ├── chart_gallery_light_warm.pptx
│   ├── chart_gallery_cyberpunk.pptx  # Special themes
│   ├── chart_gallery_sunset.pptx
│   ├── chart_gallery_ocean.pptx
│   └── chart_gallery_minimal.pptx
├── table_gallery_corporate.pptx       # Corporate theme tables
├── table_gallery_dark.pptx            # Dark theme tables
├── table_gallery_ocean.pptx           # Ocean theme tables
├── domain_galleries/                  # Domain-specific themed charts
│   ├── general_business_*.pptx       # Business analytics (8 themes)
│   ├── tech_teams_*.pptx             # Engineering metrics (8 themes)
│   ├── finance_*.pptx                # Financial dashboards (8 themes)
│   ├── hr_*.pptx                     # People analytics (8 themes)
│   ├── project_mgmt_*.pptx           # Project management (8 themes)
│   └── stock_market_*.pptx           # Trading analytics (8 themes)
└── [other output files]
```

## 🎯 Recommended Examples to Start

1. **Design System Basics**: Run `tokens_showcase.py` to see design tokens in action
2. **Layout System**: Run `layout_system_showcase.py` to see grid and layout capabilities
3. **Themes**: Run `themes_showcase.py` to explore all available themes
4. **Components**: Run `core_components_showcase.py` to see all UI components
5. **Charts**: Run `theme_chart_galleries.py` to see charts across all themes (12 galleries!)
6. **Tables**: Run `table_gallery.py` to see professional table components (3 themes)
7. **Business Focus**: Run `theme_showcase_by_domain.py` for domain-specific galleries (48 presentations!)

## 💡 Design System Philosophy

Our examples demonstrate:
- **Component-based architecture** - Reusable chart and UI components
- **Theme consistency** - Same components, different visual styles
- **Business-appropriate** - Charts selected for specific business domains
- **Beautiful defaults** - Great looking presentations out of the box

## 🛠️ Running Examples

All examples can be run using uv:

```bash
# Design System showcases (recommended starting point)
uv run examples/tokens_showcase.py
uv run examples/layout_system_showcase.py
uv run examples/themes_showcase.py
uv run examples/core_components_showcase.py

# Chart galleries
uv run examples/theme_chart_galleries.py    # Creates 12 themed chart galleries!
uv run examples/complete_chart_showcase.py
uv run examples/theme_showcase_by_domain.py # Creates 48 domain presentations!

# Table galleries
uv run examples/table_gallery.py            # Creates 3 themed table galleries!

# Chat interfaces
uv run examples/chat_conversation_showcase.py
uv run examples/container_chat_showcase.py
uv run examples/platform_chat_showcase.py

# Quick start
uv run examples/simple_example.py
uv run examples/code_examples.py
```

## 📊 Chart Galleries

### Theme Chart Galleries (`theme_chart_galleries.py`)
Creates 12 individual galleries, one for each theme:

**Dark Themes:**
- dark, dark-blue, dark-violet, dark-green, dark-purple

**Light Themes:**
- light, corporate, light-warm

**Special Themes:**
- cyberpunk, sunset, ocean, minimal

Each gallery contains 7 slides:
1. Title slide
2. Column & Bar Charts (quarterly performance, technology trends)
3. Line & Area Charts (platform growth, customer segments)
4. Pie & Doughnut Charts (revenue by product, global distribution)
5. Scatter & Bubble Charts (performance correlation, market positioning)
6. Radar & Gauge Charts (product comparison, satisfaction/uptime metrics)
7. Sample Charts (multi-series column, color palette showcase)

### Table Gallery (`table_gallery.py`)
Creates 3 themed table galleries (corporate, dark, ocean):

Each gallery contains 7 slides:
1. Title slide
2. Financial Report (quarterly metrics)
3. Product Comparison (feature matrix)
4. Project Timeline (phases and milestones)
5. Performance Metrics (department KPIs)
6. Budget Allocation (quarterly budgets)
7. Table Variants (default, bordered, striped, minimal)

## 📊 Business Domain Charts

The `theme_showcase_by_domain.py` creates specialized charts for each business domain:

### General Business / Strategy
- Column/Bar Charts for revenue comparisons
- Waterfall Charts for profit analysis
- Line Charts for market trends
- Sunburst Charts for portfolio visualization
- Funnel Charts for sales pipeline

### Tech Teams / Engineering
- Burndown Charts for sprint tracking
- Velocity Charts for team performance
- Cumulative Flow Diagrams for workflow
- Stacked Bars for feature tracking

### Finance / CFO
- Waterfall Charts for EBITDA bridges
- Combo Charts for revenue & margins
- Stacked Columns for regional revenue
- Pie Charts for expense allocation

### HR / People Analytics
- Bar Charts for headcount analysis
- Radar Charts for engagement scores
- Line Charts for attrition trends
- Stacked Bars for diversity metrics

### Project Management
- Timeline Charts for milestones
- Resource Histograms for allocation
- Risk Matrices for assessment
- Progress Bars for phase tracking

### Stock Market / Trading
- Line Charts for index performance
- Column Charts for trading volumes
- Bubble Charts for risk/return analysis
- Waterfall Charts for P&L breakdown

## 🎨 Available Themes

All examples support these 12 built-in themes:

**Dark Themes:**
- `dark` - Default dark theme
- `dark-blue` - Blue accent dark theme
- `dark-violet` - Violet accent dark theme
- `dark-green` - Green accent dark theme
- `dark-purple` - Purple accent dark theme

**Light Themes:**
- `light` - Default light theme
- `corporate` - Professional corporate theme
- `light-warm` - Warm light theme

**Special Themes:**
- `cyberpunk` - High-contrast cyberpunk aesthetic
- `sunset` - Warm sunset colors
- `ocean` - Cool ocean blues
- `minimal` - Minimalist monochrome
