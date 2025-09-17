# Charts & Data Visualization Capabilities

The PowerPoint MCP Server provides comprehensive charting and data visualization tools for creating professional, data-driven presentations.

## Supported Chart Types (16 Total)

### 1. Column Charts
- **Regular Column**: Vertical bars comparing values across categories
- **Stacked Column**: Shows cumulative values with segments stacked vertically
- **Use Cases**: Quarterly sales, performance comparisons, time-series data

### 2. Bar Charts  
- **Regular Bar**: Horizontal bars for better label readability
- **Stacked Bar**: Shows composition of each category horizontally
- **Use Cases**: Product comparisons, ranking data, long category names

### 3. Line Charts
- **Regular Line**: Shows trends and changes over time
- **Line with Markers**: Highlights individual data points
- **Use Cases**: Growth trends, KPI tracking, time-series analysis

### 4. Pie & Doughnut Charts
- **Pie Chart**: Shows proportional distribution with percentage labels
- **Doughnut Chart**: Similar to pie with hollow center for modern look
- **Use Cases**: Market share, budget allocation, composition analysis

### 5. Area Charts
- **Regular Area**: Emphasizes magnitude of change over time
- **Stacked Area**: Shows how components contribute to total over time
- **Use Cases**: Cumulative growth, traffic sources, resource utilization

### 6. Scatter (XY) Charts
- **Scatter Plot**: Shows relationships between two continuous variables
- **Correlation Analysis**: Identify patterns and trends in data relationships
- **Use Cases**: Price vs sales analysis, performance correlations, data clustering

### 7. Bubble Charts
- **3D Data Visualization**: X/Y position plus size dimension
- **Market Positioning**: Compare products across three metrics
- **Use Cases**: Market analysis, portfolio management, competitive positioning

### 8. Radar (Spider) Charts  
- **Regular Radar**: Multi-axis comparison with lines
- **Filled Radar**: Filled area for visual impact
- **Use Cases**: Performance reviews, feature comparisons, skill assessments

### 9. Waterfall Charts
- **Financial Analysis**: Shows incremental changes
- **Bridge Charts**: Visualize how initial value changes through additions/subtractions
- **Use Cases**: Profit analysis, budget variance, cash flow visualization

## Chart Creation Tools

### Basic Chart Addition
```python
await pptx_add_chart(
    slide_index=1,
    chart_type="column",
    categories=["Q1", "Q2", "Q3", "Q4"],
    series_data={
        "Product A": [45, 52, 48, 58],
        "Product B": [38, 41, 44, 49]
    },
    title="Quarterly Sales Performance"
)
```

### Specialized Pie Chart
```python
await pptx_add_pie_chart(
    slide_index=2,
    categories=["Enterprise", "SMB", "Consumer"],
    values=[45, 35, 20],
    title="Market Segments",
    show_percentages=True
)
```

### Scatter Chart for Correlations
```python
await pptx_add_scatter_chart(
    slide_index=3,
    series_data=[
        {
            "name": "Product A",
            "x_values": [10, 20, 30, 40, 50],
            "y_values": [15, 25, 45, 35, 55]
        }
    ],
    title="Price vs Sales Correlation"
)
```

### Bubble Chart for 3D Analysis
```python
await pptx_add_bubble_chart(
    slide_index=4,
    series_data=[
        {
            "name": "Market Segments",
            "data_points": [
                (10, 20, 5),   # x=price, y=quality, size=market_share
                (15, 25, 8),
                (20, 30, 12)
            ]
        }
    ],
    title="Market Positioning"
)
```

### Radar Chart for Multi-Criteria
```python
await pptx_add_radar_chart(
    slide_index=5,
    categories=["Speed", "Reliability", "Comfort", "Design", "Economy"],
    series_data={
        "Model A": [8, 7, 9, 8, 6],
        "Model B": [7, 9, 7, 6, 8]
    },
    title="Product Comparison",
    filled=True
)
```

### Waterfall for Financial Analysis
```python
await pptx_add_waterfall_chart(
    slide_index=6,
    categories=["Start", "Sales", "+Service", "-Costs", "-Tax", "Profit"],
    values=[100, 50, 20, -30, -10, 130],
    title="Profit Analysis"
)
```

## Data Table Support

Create formatted data tables for detailed information display:

```python
await pptx_add_data_table(
    slide_index=3,
    data=[
        ["Product", "Q1", "Q2", "Q3", "Q4"],
        ["Widget A", "100", "120", "135", "145"],
        ["Widget B", "85", "90", "95", "102"]
    ],
    has_header_row=True
)
```

## Professional Templates

### Metrics Dashboard
Display KPIs with visual impact:
```python
await pptx_create_metrics_slide(
    title="Executive Summary",
    metrics=[
        {"value": "$12.4M", "label": "Total Revenue"},
        {"value": "94%", "label": "Target Achievement"},
        {"value": "+28%", "label": "YoY Growth"}
    ]
)
```

### Comparison Slides
Side-by-side comparisons with visual elements:
```python
await pptx_create_comparison_slide(
    title="Product Comparison",
    left_title="Standard Plan",
    left_content=["Basic features", "$9.99/month"],
    right_title="Premium Plan",
    right_content=["All features", "$19.99/month"]
)
```

## SmartArt Diagrams

Create professional diagrams for processes and hierarchies:

```python
await pptx_add_smart_art(
    slide_index=4,
    diagram_type="process",  # process, hierarchy, or cycle
    items=["Plan", "Execute", "Review", "Improve"]
)
```

## Advanced Features

### Custom Positioning
All charts support precise positioning and sizing:
- `left`, `top`: Position in inches from slide edges
- `width`, `height`: Chart dimensions in inches
- Default: Optimized for standard slide layouts

### Multiple Data Series
Support for complex multi-series visualizations:
- Up to 10 series per chart
- Automatic color differentiation
- Legend positioning options

### Formatting Options
- Custom chart titles
- Percentage labels for pie charts
- Data labels and markers
- Grid lines and axis formatting

## Color Schemes

Professional color schemes available:
- `modern_blue`: Contemporary blue gradient
- `corporate_gray`: Professional grayscale
- `vibrant`: Bold, high-contrast colors
- `pastel`: Soft, muted tones
- `dark_mode`: Dark background themes

## Performance Optimization

- **Async Processing**: All chart operations run asynchronously
- **Batch Operations**: Create multiple charts efficiently
- **Memory Management**: Automatic cleanup of chart data
- **File Size Optimization**: Efficient XML structure

## Example Workflow

```python
# Create presentation
await pptx_create(name="sales_report")

# Add title slide
await pptx_create_title_slide(
    title="Q4 Sales Report",
    subtitle="Performance Analysis"
)

# Add metrics dashboard
await pptx_create_metrics_slide(
    title="Key Metrics",
    metrics=[
        {"value": "$5.2M", "label": "Revenue"},
        {"value": "112%", "label": "Target"}
    ]
)

# Add trend chart
await pptx_add_slide(title="Revenue Trend")
await pptx_add_chart(
    slide_index=2,
    chart_type="line_markers",
    categories=["Jan", "Feb", "Mar", "Apr"],
    series_data={"Revenue": [1.2, 1.4, 1.3, 1.5]},
    title="Monthly Revenue ($M)"
)

# Save presentation
await pptx_save(path="q4_sales.pptx")
```

## Compatibility

- **PowerPoint**: Full compatibility (2007 and later)
- **LibreOffice**: Full support for all chart types
- **Google Slides**: Basic chart support
- **Keynote**: Limited support (see KEYNOTE_COMPATIBILITY.md)

## Best Practices

1. **Data Organization**: Structure data clearly with categories and series
2. **Chart Selection**: Choose appropriate chart type for data story
3. **Visual Hierarchy**: Use titles and labels effectively
4. **Color Consistency**: Maintain color scheme throughout presentation
5. **Performance**: Use async operations for large datasets

## Limitations

- Maximum 255 categories per chart
- Maximum 255 data points per series
- Complex 3D charts not supported
- Animation effects not available via API

## Future Enhancements

- Waterfall charts for financial analysis
- Scatter plots for correlation analysis
- Bubble charts for three-dimensional data
- Custom chart templates
- Real-time data connections