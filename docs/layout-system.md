# Layout System

The layout system provides a comprehensive grid and spacing framework for building structured PowerPoint presentations, inspired by modern UI frameworks like Tailwind CSS and Bootstrap.

## Overview

The layout system consists of:
- **12-Column Grid** - Flexible grid system for responsive layouts with boundary management
- **Container** - Centered content containers with preset widths
- **Stack** - Vertical/horizontal layout with consistent spacing
- **Spacer** - Invisible spacing elements
- **Divider** - Visual separator lines
- **Boundary System** - Automatic boundary validation and positioning

## Design Philosophy

The layout system follows a clear hierarchy:

```
Container → Grid → Components
```

1. **Container** establishes safe content boundaries
2. **Grid** subdivides space and manages positioning
3. **Components** auto-size within grid cells

This approach eliminates manual calculations and ensures consistent, responsive layouts.

## Grid System

### Modern Grid Pattern (Recommended)

The modern approach uses Container + Grid with stored bounds:

```python
from chuk_mcp_pptx.layout import Container, Grid
from chuk_mcp_pptx.components import Card

# 1. Container establishes boundaries
container = Container(size="lg", padding="sm", center=True)
bounds = container.render(slide, top=1.8)

# 2. Grid uses container bounds - no repetition needed
grid = Grid(columns=12, rows=2, gap="md", bounds=bounds)

# 3. Get cells - grid remembers its bounds
metrics_pos = grid.get_cell(col_span=4, col_start=0, row_start=0)
main_pos = grid.get_cell(col_span=8, col_start=0, row_start=1)
sidebar_pos = grid.get_cell(col_span=4, col_start=8, row_start=1)

# 4. Components auto-size within cells
MetricCard(...).render(slide, **metrics_pos)  # Only left, top, width
Card(...).render(slide, **main_pos)  # Height auto-calculated
```

**Key Benefits:**
- ✅ No manual boundary calculations
- ✅ No repetitive bound parameters
- ✅ Components auto-size based on content
- ✅ Grid handles all spacing

### Legacy Grid Pattern

The original approach still works for simple cases:

```python
# Create a 3-column grid
grid = Grid(columns=3, gap="md")
cells = grid.get_cell_positions(slide, left=0.5, top=2.0, width=9.0, height=3.0)

# Render content in each cell
for i, cell in enumerate(cells):
    card = Card(variant="elevated", theme=theme)
    card.add_child(Card.Title(f"Column {i+1}"))
    card.render(slide, **cell)
```

### Grid with Auto-Height Components

Use `get_cell()` for components that calculate their own height:

```python
# Auto-height (default) - component calculates height based on content
pos = grid.get_cell(col_span=8, col_start=0, row_start=1)  # No height in result
card.render(slide, **pos)  # Card auto-sizes

# Fixed-height - when you need explicit dimensions
pos = grid.get_cell(col_span=4, col_start=0, auto_height=False)  # Includes height
chart.render(slide, **pos)  # Chart uses grid height
```

### Grid Parameters

- `columns` (int): Number of columns (default: 12)
- `gap` (str): Gap size between columns ("none", "xs", "sm", "md", "lg", "xl")
- `rows` (int): Number of rows (default: 1)

### Common Grid Patterns

```python
# Full width (12 columns)
grid.get_span(col_span=12, col_start=0)

# Half width (6 columns)
grid.get_span(col_span=6, col_start=0)
grid.get_span(col_span=6, col_start=6)

# Third width (4 columns)
grid.get_span(col_span=4, col_start=0)
grid.get_span(col_span=4, col_start=4)
grid.get_span(col_span=4, col_start=8)

# Main + Sidebar (8 + 4)
grid.get_span(col_span=8, col_start=0)  # Main content
grid.get_span(col_span=4, col_start=8)  # Sidebar
```

## Container

### Basic Container

Containers center and constrain content width:

```python
from chuk_mcp_pptx.layout import Container

# Create centered container
container = Container(size="lg", padding="md", center=True)
bounds = container.render(slide, top=2.0, height=3.0)

# Render content within container
card.render(slide, **bounds)
```

### Container Sizes

```python
# Small container (8 inches)
Container(size="sm")

# Medium container (9 inches)
Container(size="md")

# Large container (10 inches) - default
Container(size="lg")

# Extra large (11 inches)
Container(size="xl")

# 2XL (12 inches)
Container(size="2xl")

# Full width (13.333 inches)
Container(size="full")
```

### Container Padding

```python
# No padding
Container(padding="none")

# Small padding
Container(padding="sm")

# Medium padding (default)
Container(padding="md")

# Large padding
Container(padding="lg")

# Extra large padding
Container(padding="xl")
```

## Stack

### Vertical Stack

Stack elements vertically with consistent spacing:

```python
from chuk_mcp_pptx.layout import Stack

# Vertical stack
stack = Stack(direction="vertical", gap="lg", align="start")
positions = stack.distribute(
    num_items=3,
    item_height=1.0,
    top=2.0
)

for i, pos in enumerate(positions):
    card = Card(variant="default", theme=theme)
    card.add_child(Card.Title(f"Item {i+1}"))
    card.render(slide, **pos)
```

### Horizontal Stack

Stack elements horizontally:

```python
# Horizontal stack
stack = Stack(direction="horizontal", gap="md", align="center")
positions = stack.distribute(
    num_items=4,
    item_width=2.0,
    left=0.5,
    top=3.0
)

for pos in positions:
    button = Button(text="Action", variant="default")
    button.render(slide, **pos)
```

### Stack with Auto-Rendering (New)

Use `render_children()` for automatic positioning:

```python
# Create components
buttons = [
    Button("Export", variant="outline", size="sm"),
    Button("Refresh", variant="secondary", size="sm"),
    Button("Settings", variant="ghost", size="sm")
]

# Stack handles positioning automatically
stack = Stack(direction="vertical", gap="sm")
stack.render_children(
    slide,
    buttons,
    left=sidebar_pos['left'] + 0.1,
    top=sidebar_pos['top'] + 0.5,
    item_width=sidebar_pos['width'] - 0.2,
    item_height=0.4
)
```

**When to use:**
- ✅ Fixed-height components (buttons, badges)
- ✅ Known dimensions
- ❌ Auto-height components (cards with variable content) - use `distribute()` instead

### Stack Alignment

```python
# Align to start (left/top)
Stack(align="start")

# Center alignment
Stack(align="center")

# Align to end (right/bottom)
Stack(align="end")

# Stretch to fill
Stack(align="stretch")
```

### Stack Gap Sizes

```python
Stack(gap="xs")   # Extra small gap
Stack(gap="sm")   # Small gap
Stack(gap="md")   # Medium gap (default)
Stack(gap="lg")   # Large gap
Stack(gap="xl")   # Extra large gap
Stack(gap="2xl")  # 2X large gap
```

## Spacer

### Basic Spacer

Add spacing between elements:

```python
from chuk_mcp_pptx.layout import Spacer

# Vertical spacer
spacer = Spacer(size="lg", direction="vertical")
spacing = spacer.get_size()  # Returns inches

# Horizontal spacer
spacer = Spacer(size="md", direction="horizontal")
```

### Spacer Sizes

```python
Spacer(size="xs")   # 0.25 inches
Spacer(size="sm")   # 0.375 inches
Spacer(size="md")   # 0.5 inches (default)
Spacer(size="lg")   # 0.75 inches
Spacer(size="xl")   # 1.0 inches
Spacer(size="2xl")  # 1.5 inches
```

## Divider

### Horizontal Divider

Create horizontal separator lines:

```python
from chuk_mcp_pptx.layout import Divider

# Horizontal divider
divider = Divider(
    orientation="horizontal",
    thickness=1,
    color="border.DEFAULT"
)
divider.render(slide, left=0.5, top=3.0, width=9.0)
```

### Vertical Divider

Create vertical separator lines:

```python
# Vertical divider
divider = Divider(
    orientation="vertical",
    thickness=2,
    color="border.DEFAULT"
)
divider.render(slide, left=5.0, top=2.0, height=4.0)
```

### Divider Customization

```python
# Thick divider
Divider(thickness=3)

# Custom color
Divider(color="primary.DEFAULT")

# Subtle divider
Divider(thickness=0.5, color="border.subtle")
```

## Spacing Tokens

The layout system uses consistent spacing tokens:

```python
from chuk_mcp_pptx.tokens.spacing import SPACING, GAPS, MARGINS, PADDING

# Spacing scale (in inches)
SPACING["4"]   # 0.25"
SPACING["6"]   # 0.375"
SPACING["8"]   # 0.5"
SPACING["12"]  # 0.75"
SPACING["16"]  # 1.0"

# Gap presets
GAPS["xs"]    # Extra small gap
GAPS["sm"]    # Small gap
GAPS["md"]    # Medium gap
GAPS["lg"]    # Large gap
GAPS["xl"]    # Extra large gap

# Margin presets
MARGINS["md"]  # Medium margin
MARGINS["lg"]  # Large margin

# Padding presets
PADDING["md"]  # Medium padding
PADDING["lg"]  # Large padding
```

## Layout Helpers

### Safe Content Area

Get the safe content area for placing elements:

```python
from chuk_mcp_pptx.layout import get_safe_content_area

# Get safe area with title
area = get_safe_content_area(has_title=True)
# Returns: {'left': 0.5, 'top': 1.0, 'width': 9.0, 'height': 4.125}

# Get safe area without title
area = get_safe_content_area(has_title=False)
```

### Centering Elements

Center elements on the slide:

```python
from chuk_mcp_pptx.layout import center_element

# Center horizontally and vertically
pos = center_element(width=4.0, height=2.0)

# Center horizontally only
pos = center_element(width=4.0, height=2.0, vertical=False)

# Center vertically only
pos = center_element(width=4.0, height=2.0, horizontal=False)
```

### Grid Layout Calculation

Calculate optimal grid layout:

```python
from chuk_mcp_pptx.layout import calculate_grid_layout

# Auto-calculate columns for 6 items
positions = calculate_grid_layout(num_items=6)

# Force 3 columns
positions = calculate_grid_layout(num_items=6, columns=3)

# Custom spacing
positions = calculate_grid_layout(
    num_items=6,
    columns=3,
    spacing=0.3
)
```

### Horizontal Distribution

Distribute items horizontally:

```python
from chuk_mcp_pptx.layout import distribute_horizontally

positions = distribute_horizontally(
    num_items=4,
    item_width=2.0,
    item_height=1.0,
    top=3.0
)

for pos in positions:
    # Render item at position
    button.render(slide, **pos)
```

## Responsive Patterns

### Dashboard Layout (Modern Pattern)

```python
# 1. Container establishes boundaries
container = Container(size="lg", padding="sm", center=True)
bounds = container.render(slide, top=1.8)

# 2. Grid with bounds - 2 rows for metrics + content
grid = Grid(columns=12, rows=2, gap="md", bounds=bounds)

# 3. Row 0: Metric cards (3 × 4 columns = 12 total)
metrics = [
    ("Revenue", "$1.2M", "+15%", "up", 0),
    ("Users", "45K", "+8%", "up", 4),
    ("Growth", "23%", "+3%", "up", 8),
]

for label, value, change, trend, col_start in metrics:
    pos = grid.get_cell(col_span=4, col_start=col_start, row_start=0)
    MetricCard(label, value, change, trend).render(slide, **pos)

# 4. Row 1: Main content (8 cols) + Sidebar (4 cols)
main_pos = grid.get_cell(col_span=8, col_start=0, row_start=1)
sidebar_pos = grid.get_cell(col_span=4, col_start=8, row_start=1)

# Main card auto-sizes
card = Card(variant="elevated")
card.add_child(Card.Title("Main Content (8/12 cols)"))
card.add_child(Card.Description("Primary content area"))
card.render(slide, **main_pos)

# Sidebar with stacked buttons
buttons = [Button("Export"), Button("Refresh"), Button("Settings")]
stack = Stack(direction="vertical", gap="sm")
stack.render_children(slide, buttons,
                      left=sidebar_pos['left'] + 0.1,
                      top=sidebar_pos['top'] + 0.5,
                      item_width=sidebar_pos['width'] - 0.2,
                      item_height=0.4)
```

**Key Points:**
- Container defines safe boundaries once
- Grid stores bounds, no repetition in get_cell() calls
- Components auto-size (metrics, cards)
- Stack handles button positioning
- No manual calculations!

### Card Grid

```python
# 3-column card grid
grid = Grid(columns=3, gap="lg")
cells = grid.get_cell_positions(slide, top=2.0, height=4.0)

for i, cell in enumerate(cells):
    card = Card(variant="elevated", theme=theme)
    card.add_child(Card.Title(f"Feature {i+1}"))
    card.render(slide, **cell)
```

### Stacked Content

```python
# Vertical stack with dividers
stack = Stack(direction="vertical", gap="md")
positions = stack.distribute(num_items=4, item_height=1.0, top=2.0)

for i, pos in enumerate(positions):
    # Content
    Card(...).render(slide, **pos)

    # Divider (except last item)
    if i < len(positions) - 1:
        Divider(orientation="horizontal").render(
            slide,
            left=0.5,
            top=pos['top'] + pos['height'] + 0.1,
            width=9.0
        )
```

## Best Practices

### 1. Use Consistent Spacing

Always use spacing tokens instead of magic numbers:

```python
# Good
stack = Stack(gap="lg")

# Avoid
positions = [{'left': 0.5, 'top': 2.3}, {'left': 0.5, 'top': 3.7}]
```

### 2. Leverage Grid System

Use the grid for complex layouts:

```python
# Good - responsive layout
grid = Grid(columns=12, gap="md")
pos = grid.get_span(col_span=6, col_start=0)

# Avoid - hard-coded positioning
left = 0.5
width = 4.5
```

### 3. Container for Centering

Use containers to center content:

```python
# Good
container = Container(size="lg", center=True)
bounds = container.render(slide, top=2.0)

# Avoid
left = (10.0 - 5.0) / 2  # Manual centering
```

### 4. Stack for Lists

Use Stack for vertical/horizontal lists:

```python
# Good
stack = Stack(direction="vertical", gap="md")
positions = stack.distribute(num_items=5, item_height=0.8)

# Avoid
positions = []
top = 2.0
for i in range(5):
    positions.append({'top': top})
    top += 1.0
```

## Examples

See `examples/layout_system_showcase.py` for comprehensive examples of:
- 12-column grid layouts
- Container sizing
- Vertical and horizontal stacks
- Dividers and spacing
- Responsive dashboard pattern
- Spacing scale demonstration

## API Reference

### Grid

```python
Grid(
    columns: int = 12,
    gap: Literal["none", "xs", "sm", "md", "lg", "xl"] = "md",
    rows: int = 1,
    bounds: Optional[Dict[str, float]] = None,  # NEW!
    theme: Optional[Dict] = None
)
```

**Methods:**
- `get_cell()` - **NEW**: Get position with optional auto-height (recommended)
- `get_cell_positions()` - Get all cell positions
- `get_span()` - Get position for spanning cells

**New `get_cell()` Method:**
```python
grid.get_cell(
    col_span: int = 1,
    row_span: int = 1,
    col_start: int = 0,
    row_start: int = 0,
    left: Optional[float] = None,        # Uses bounds if not provided
    top: Optional[float] = None,         # Uses bounds if not provided
    width: Optional[float] = None,       # Uses bounds if not provided
    height: Optional[float] = None,      # Uses bounds if not provided
    auto_height: bool = True             # NEW: Omit height for auto-sizing
) -> Dict[str, float]
```

**Returns:**
- If `auto_height=True` (default): `{'left': ..., 'top': ..., 'width': ...}`
- If `auto_height=False`: `{'left': ..., 'top': ..., 'width': ..., 'height': ...}`

### Container

```python
Container(
    size: Literal["sm", "md", "lg", "xl", "2xl", "full"] = "lg",
    padding: Literal["none", "sm", "md", "lg", "xl"] = "md",
    center: bool = True,
    theme: Optional[Dict] = None
)
```

**Methods:**
- `render()` - Returns container bounds

### Stack

```python
Stack(
    direction: Literal["vertical", "horizontal"] = "vertical",
    gap: Literal["none", "xs", "sm", "md", "lg", "xl"] = "md",
    align: Literal["start", "center", "end", "stretch"] = "start",
    theme: Optional[Dict] = None
)
```

**Methods:**
- `distribute()` - Distribute items with spacing and return positions
- `render_children()` - **NEW**: Automatically render list of components with spacing

### Spacer

```python
Spacer(
    size: Literal["xs", "sm", "md", "lg", "xl", "2xl"] = "md",
    direction: Literal["vertical", "horizontal"] = "vertical",
    theme: Optional[Dict] = None
)
```

**Methods:**
- `get_size()` - Get spacer size in inches
- `render()` - Returns spacer dimensions

### Divider

```python
Divider(
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    thickness: float = 1,
    color: str = "border.DEFAULT",
    theme: Optional[Dict] = None
)
```

**Methods:**
- `render()` - Render divider line
