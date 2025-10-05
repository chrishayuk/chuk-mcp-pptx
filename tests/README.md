# PowerPoint MCP Server Test Suite

Comprehensive test coverage for the PowerPoint MCP Server components using pytest.

## Test Structure

```
tests/
├── conftest.py                 # Shared fixtures and test utilities
├── components/
│   ├── charts/                 # Chart component tests
│   │   ├── test_column_bar.py  # Column, Bar, Waterfall charts
│   │   ├── test_line_area.py   # Line, Area, Sparkline charts
│   │   ├── test_pie_doughnut.py # Pie, Doughnut, Sunburst charts
│   │   └── test_funnel.py      # Funnel, Gantt, Heatmap charts
│   └── ui/                     # UI component tests
│       └── test_card.py        # Card components
└── themes/
    └── test_theme_manager.py   # Theme system tests
```

## Running Tests

```bash
# Install test dependencies
uv pip install pytest pytest-asyncio pytest-mock

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/components/charts/test_column_bar.py

# Run tests matching pattern
uv run pytest -k "test_column"

# Run with coverage
uv run pytest --cov=chuk_mcp_pptx --cov-report=html
```

## Test Coverage

### Chart Components ✅
- **ColumnChart**: Initialization, validation, rendering, variants
- **BarChart**: All variants, stacking options
- **WaterfallChart**: Positive/negative values, connectors
- **LineChart**: Smooth/markers variants, multiple series
- **AreaChart**: Filled/stacked variants, transparency
- **SparklineChart**: Minimal charts, markers
- **PieChart**: Standard/exploded, percentages
- **DoughnutChart**: Hole size, center text
- **SunburstChart**: Hierarchical data, validation
- **FunnelChart**: Conversion rates, dimensions
- **GanttChart**: Tasks, dependencies, milestones
- **HeatmapChart**: Data matrix, color scales

### UI Components ✅
- **Card**: Basic rendering, variants, themes
- **MetricCard**: Values, trends, formatting (needs implementation)
- **FeatureCard**: Lists, icons, limits (needs implementation)

### Theme System ✅
- **ThemeManager**: Theme loading, listing, registration
- **Theme**: Colors, application, variants

## Test Fixtures

### Mock Objects
- `mock_slide`: Mocked PowerPoint slide
- `mock_presentation`: Mocked presentation
- `mock_chart_data`: Chart data helper

### Sample Data
- `sample_chart_data`: Pre-configured chart data for all types
- `sample_component_data`: UI component test data
- `dark_theme` / `light_theme`: Theme configurations

### Utilities
- `assert_color_valid()`: Validate hex colors
- `assert_chart_renders()`: Test chart rendering
- `assert_component_renders()`: Test component rendering

## Current Test Status

- **Total Tests**: 102
- **Passing**: 54 (53%)
- **Failing**: 48 (47%)

### Known Issues
1. Some chart classes missing `validate()` method
2. MetricCard and FeatureCard components need implementation
3. Theme object structure needs alignment with tests

## Adding New Tests

1. Create test file in appropriate directory
2. Import component and fixtures
3. Write test classes with descriptive names
4. Use fixtures for mock objects and data
5. Test initialization, validation, rendering, and edge cases

Example:
```python
class TestNewComponent:
    def test_init(self, dark_theme):
        component = NewComponent(param="value", theme=dark_theme)
        assert component.param == "value"
    
    def test_render(self, mock_slide, dark_theme):
        component = NewComponent(theme=dark_theme)
        component.render(mock_slide, left=1, top=1)
        assert mock_slide.shapes.add_shape.called
```

## CI/CD Integration

Add to GitHub Actions:
```yaml
- name: Run tests
  run: |
    uv pip install pytest pytest-asyncio pytest-mock
    uv run pytest --tb=short
```