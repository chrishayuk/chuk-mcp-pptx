# PowerPoint MCP Server Examples

This directory contains examples demonstrating the PowerPoint MCP Server's capabilities, organized by category.

## 🎨 Beautiful Design System Examples

Our "shadcn for PowerPoint" design system - component-based charts with multiple themes:

### Core Galleries
- **`beautiful_chart_gallery.py`** - Comprehensive showcase of all chart types with modern themes
- **`theme_showcase_by_domain.py`** - Business domain-specific charts across all themes (48 presentations!)
- **`beautiful_themes_demo.py`** - Interactive theme demonstration

### Component Showcases
- **`component_showcase.py`** - All UI components (cards, badges, buttons)
- **`shapes_gallery.py`** - Shape components with theme variations
- **`table_gallery.py`** - Table and data grid components
- **`smartart_gallery.py`** - SmartArt and diagram components
- **`image_gallery.py`** - Image handling and layouts

## 📊 Chart Examples

### Basic Charts
- **`chart_demo.py`** - Simple chart creation examples
- **`chart_gallery.py`** - Basic chart types demonstration

### Advanced Charts
- **`comprehensive_chart_showcase.py`** - Advanced chart features
- **`theme_chart_galleries.py`** - Charts with theme variations

## 🚀 Quick Start Examples

- **`simple_example.py`** - Minimal working example
- **`code_examples.py`** - Code syntax highlighting in slides

## 🔧 Technical Demos

- **`connector_proof.py`** - Shape connector functionality
- **`image_demo.py`** - Image manipulation examples
- **`layout_inspection_demo.py`** - Layout analysis tools

## 📁 Output Structure

Running these examples will create presentations in the `../outputs/` directory:

```
outputs/
├── beautiful_chart_gallery.pptx      # Main chart gallery
├── theme_galleries/                  # Domain-specific themed charts
│   ├── general_business_*.pptx      # Business analytics (8 themes)
│   ├── tech_teams_*.pptx            # Engineering metrics (8 themes)
│   ├── finance_*.pptx               # Financial dashboards (8 themes)
│   ├── hr_*.pptx                    # People analytics (8 themes)
│   ├── project_mgmt_*.pptx          # Project management (8 themes)
│   └── stock_market_*.pptx          # Trading analytics (8 themes)
└── [other output files]
```

## 🎯 Recommended Examples to Start

1. **For Charts**: Run `beautiful_chart_gallery.py` to see all chart types
2. **For Themes**: Run `theme_showcase_by_domain.py` to generate business-specific galleries
3. **For Components**: Run `component_showcase.py` to see UI components
4. **For Quick Demo**: Run `simple_example.py` for a minimal example

## 💡 Design System Philosophy

Our examples demonstrate:
- **Component-based architecture** - Reusable chart and UI components
- **Theme consistency** - Same components, different visual styles
- **Business-appropriate** - Charts selected for specific business domains
- **Beautiful defaults** - Great looking presentations out of the box

## 🛠️ Running Examples

All examples can be run using uv:

```bash
# Run any example
uv run python examples/[example_name].py

# Generate all theme galleries (48 presentations!)
uv run python examples/theme_showcase_by_domain.py

# Create the beautiful chart gallery
uv run python examples/beautiful_chart_gallery.py
```

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

## 📚 Archive

Test and debug scripts have been moved to the `archive/` folder for reference.