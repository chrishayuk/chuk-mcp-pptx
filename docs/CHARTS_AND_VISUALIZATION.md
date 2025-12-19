# Charts & Data Visualization

The PowerPoint MCP Server provides comprehensive charting through the Universal Component API.

## Chart Components

All charts are created using `pptx_add_component` or `pptx_populate_placeholder`:

| Component | Description | Variants |
|-----------|-------------|----------|
| `ColumnChart` | Vertical bar charts | clustered, stacked, stacked100 |
| `BarChart` | Horizontal bar charts | clustered, stacked, stacked100 |
| `LineChart` | Line/trend charts | default, smooth, markers |
| `AreaChart` | Area charts | default, stacked |
| `PieChart` | Pie charts | default, exploded |
| `DoughnutChart` | Doughnut charts | default, exploded |
| `ScatterChart` | Scatter/XY plots | default, lines |
| `BubbleChart` | Bubble charts | default |
| `RadarChart` | Spider/radar charts | default, filled |
| `WaterfallChart` | Waterfall/bridge charts | default |
| `FunnelChart` | Sales funnel charts | default |
| `GaugeChart` | Gauge/speedometer | default |
| `GanttChart` | Project timelines | default |
| `HeatmapChart` | Heat maps | default |
| `SparklineChart` | Inline mini charts | line, bar, area |
| `Matrix3DChart` | 3D matrix visualizations | default |

## Creating Charts

### Via pptx_add_component

```python
# Column chart with free positioning
await pptx_add_component(
    slide_index=1,
    component="ColumnChart",
    left=1.0, top=1.5, width=8.0, height=4.5,
    params={
        "title": "Quarterly Sales",
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": {
            "Product A": [45, 52, 48, 58],
            "Product B": [38, 41, 44, 49]
        }
    }
)

# Pie chart into template placeholder
await pptx_add_component(
    slide_index=2,
    component="PieChart",
    target_placeholder=2,
    params={
        "title": "Market Segments",
        "categories": ["Enterprise", "SMB", "Consumer"],
        "series": {"Share": [45, 35, 20]}
    }
)
```

### Via pptx_populate_placeholder

```python
# Populate CHART placeholder with data
await pptx_populate_placeholder(
    slide_index=1,
    placeholder_idx=2,
    content={
        "type": "ColumnChart",
        "title": "Revenue by Quarter",
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": {"Revenue": [100, 150, 200, 250]}
    }
)
```

## Chart Data Formats

### Category-Based Charts (Column, Bar, Line, Area, Pie)

```python
params={
    "title": "Chart Title",
    "categories": ["Cat1", "Cat2", "Cat3"],
    "series": {
        "Series A": [10, 20, 30],
        "Series B": [15, 25, 35]
    }
}
```

### Scatter/Bubble Charts

```python
params={
    "title": "Correlation Analysis",
    "series": {
        "Product A": {
            "x_values": [10, 20, 30, 40],
            "y_values": [15, 25, 45, 35]
        }
    }
}

# Bubble adds size dimension
params={
    "title": "Market Position",
    "series": {
        "Products": {
            "data_points": [
                {"x": 10, "y": 20, "size": 5},
                {"x": 15, "y": 25, "size": 8}
            ]
        }
    }
}
```

### Radar Charts

```python
params={
    "title": "Feature Comparison",
    "categories": ["Speed", "Reliability", "Cost", "Design"],
    "series": {
        "Model A": [8, 7, 9, 8],
        "Model B": [7, 9, 6, 8]
    },
    "variant": "filled"
}
```

### Gauge Chart

```python
params={
    "title": "Performance",
    "value": 75,
    "min_value": 0,
    "max_value": 100,
    "zones": [
        {"start": 0, "end": 30, "color": "#FF0000"},
        {"start": 30, "end": 70, "color": "#FFFF00"},
        {"start": 70, "end": 100, "color": "#00FF00"}
    ]
}
```

### Funnel Chart

```python
params={
    "title": "Sales Pipeline",
    "categories": ["Leads", "Qualified", "Proposal", "Closed"],
    "series": {"Count": [1000, 500, 200, 50]}
}
```

## Tables

Tables are also created via the Universal Component API:

```python
await pptx_add_component(
    slide_index=1,
    component="Table",
    target_placeholder=14,
    params={
        "headers": ["Product", "Q1", "Q2", "Q3", "Q4"],
        "data": [
            ["Widget A", "100", "120", "135", "145"],
            ["Widget B", "85", "90", "95", "102"]
        ],
        "variant": "striped"
    }
)
```

## Chart Positioning

### Into Template Placeholders (Recommended)

```python
# Use pptx_analyze_template to find CHART placeholder indices
# Then target them directly
await pptx_add_component(
    component="ColumnChart",
    target_placeholder=2,  # From template analysis
    ...
)
```

### Free Positioning

```python
await pptx_add_component(
    component="ColumnChart",
    left=1.0,    # inches from left
    top=1.5,     # inches from top
    width=8.0,   # chart width in inches
    height=4.5,  # chart height in inches
    ...
)
```

## Complete Workflow Example

```python
# 1. Create presentation from template
await pptx_create(name="sales_report", template_name="brand_proposal")

# 2. Analyze template to find chart layouts
await pptx_analyze_template("brand_proposal")
# Look for layouts with CHART placeholders

# 3. Add slide with chart layout
await pptx_add_slide_from_template(layout_index=40)
# Response shows: placeholder 2 (CHART)

# 4. Populate title
await pptx_populate_placeholder(
    slide_index=0, placeholder_idx=0,
    content="Q4 Sales Report"
)

# 5. Populate chart placeholder
await pptx_populate_placeholder(
    slide_index=0,
    placeholder_idx=2,
    content={
        "type": "ColumnChart",
        "title": "Revenue by Quarter",
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": {"Revenue": [1.2, 1.4, 1.3, 1.5]}
    }
)

# 6. Verify all components
await pptx_list_slide_components(slide_index=0)

# 7. Save presentation
await pptx_save(path="q4_sales.pptx")
```

## Compatibility

- **PowerPoint**: Full compatibility (2007 and later)
- **LibreOffice**: Full support for all chart types
- **Google Slides**: Basic chart support
- **Keynote**: Limited support

## Best Practices

1. **Use Templates**: Template placeholders ensure consistent sizing and positioning
2. **Analyze First**: Always run `pptx_analyze_template` before adding content
3. **Validate Components**: Use `pptx_list_slide_components` to verify population
4. **Match Chart to Data**: Choose appropriate chart types for your data story
5. **Keep It Simple**: Avoid too many series or categories per chart