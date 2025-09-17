# PowerPoint MCP Server Examples

This folder contains example scripts demonstrating the PowerPoint MCP Server capabilities.
All generated presentations are saved to the `../outputs/` folder.

## Available Examples

### 1. simple_example.py
**Basic presentation creation example**
- Creates a simple presentation with title and content slides
- Demonstrates basic text slides and bullet points
- Shows how to save presentations
- Output: `outputs/simple_demo.pptx`

### 2. chart_demo.py
**Sales analytics dashboard demo**
- Creates a professional sales presentation
- Includes metrics dashboard with KPIs
- Demonstrates column and pie charts using unified API
- Shows template usage and color schemes
- Output: `outputs/sales_analytics_2024.pptx`

### 3. chart_gallery.py
**Comprehensive chart showcase**
- Demonstrates all 15 supported chart types
- Uses the unified `pptx_add_chart()` API for all charts
- Includes examples of:
  - Column & Bar charts (regular and stacked)
  - Line & Area charts (with variants)
  - Pie & Doughnut charts
  - Scatter (XY) plots for correlations
  - Bubble charts for 3D data visualization
  - Radar charts for multi-criteria comparison
  - Waterfall charts for financial analysis
- Shows proper data structure for each chart type
- Output: `outputs/chart_gallery.pptx`

### 4. image_demo.py
**Basic image handling demonstration**
- Creates a simple presentation with various image features
- Demonstrates basic image operations:
  - Adding image slides with titles
  - Images with captions
  - Logo positioning in standard locations
  - Multiple images on a single slide
- Uses base64 data URLs for demo (no external files needed)
- Shows how to work with both file paths and base64 images
- Output: `outputs/image_demo.pptx`

### 5. table_gallery.py
**Comprehensive table showcase**
- Complete demonstration of data table capabilities
- Table types demonstrated:
  - Basic data tables with headers and rows
  - Financial reports with formatting
  - Product comparison matrices
  - Project timelines and schedules
  - Performance metrics and KPIs
  - Budget allocation tables
  - Risk assessment matrices
  - Employee rosters
  - Pricing tiers
  - Inventory status reports
- Features:
  - Three table styles (light, medium, dark)
  - Custom positioning and sizing
  - Support for emojis and status indicators
  - Professional business formatting
- Output: `outputs/table_gallery.pptx`

### 6. image_gallery.py
**Comprehensive image gallery showcase**
- Complete demonstration of all image handling capabilities
- Features demonstrated:
  - Basic image slides
  - Custom positioning and sizing with layout validation
  - Automatic gallery grids with smart spacing
  - Images with captions
  - Logo positioning (9 standard positions)
  - Background images for slides
  - Image replacement with position retention
  - Mixed layouts with featured and supporting images
- Includes automatic layout helpers for proper positioning
- Uses generated colored rectangles for demo purposes
- Supports both file paths and base64 data URLs
- Output: `outputs/image_gallery.pptx`

## Unified APIs

### Chart API

All chart examples use the simplified unified chart API:

```python
await pptx_add_chart(
    slide_index=0,
    chart_type="column",  # or "pie", "scatter", "bubble", etc.
    data={
        # Structure depends on chart_type
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": {"Revenue": [100, 120, 140, 160]}
    },
    title="Chart Title"
)
```

### Image API

Image handling uses specialized tools for different purposes:

```python
# Add image to slide with precise positioning
await pptx_add_image(
    slide_index=1,
    image_path="/path/to/image.png",  # or base64 data URL
    left=2.0,
    top=1.5,
    width=4.0,
    height=3.0
)

# Create image gallery grid
await pptx_add_image_gallery(
    slide_index=2,
    image_paths=[img1, img2, img3, img4],
    columns=2,
    spacing=0.2
)

# Add logo in standard position
await pptx_add_logo(
    slide_index=0,
    logo_path="/path/to/logo.png",
    position="top-right",
    size=1.5
)
```

### 6. layout_inspection_demo.py
**Layout inspection and automatic fixes**
- Demonstrates slide inspection capabilities
- Features:
  - Detailed slide content inspection
  - Overlap detection between elements
  - Out-of-bounds element detection
  - Automatic layout fixes
  - Presentation-wide analysis
- Shows AI workflow for quality assurance
- Output: `outputs/layout_demo.pptx`

## Layout and Positioning

All examples now include automatic layout validation to ensure:
- Images and charts fit within slide boundaries
- Proper spacing and margins are maintained
- Overlapping placeholders are automatically removed
- Content stays within safe areas (accounting for titles)

The layout helpers use standard PowerPoint dimensions:
- Slide width: 10.0 inches
- Slide height: 5.625 inches (16:9 aspect ratio)
- Safe content margins from edges

## Running Examples

All examples use async/await and can be run with:

```bash
cd examples
uv run python example_name.py
```

## Output Location

All generated PowerPoint files are saved to the `../outputs/` folder to keep the examples directory clean.