# Enhanced Component System

This document describes the shadcn-inspired enhancements to the PowerPoint design system, including variants, composition patterns, and component registry.

## Table of Contents

1. [Variant System](#variant-system)
2. [Composition Patterns](#composition-patterns)
3. [Component Registry](#component-registry)
4. [Migration Guide](#migration-guide)

---

## Variant System

The variant system is inspired by `class-variance-authority` (cva) from shadcn/ui. It provides a type-safe way to define component variations.

### Basic Usage

```python
from chuk_mcp_pptx.variants import create_variants

# Define variants
button_variants = create_variants(
    base={"border_radius": 8, "font_weight": 500},
    variants={
        "variant": {
            "default": {"bg_color": "primary.DEFAULT"},
            "secondary": {"bg_color": "secondary.DEFAULT"},
            "outline": {"bg_color": "transparent", "border_width": 1},
        },
        "size": {
            "sm": {"padding": 0.2, "font_size": 12},
            "md": {"padding": 0.3, "font_size": 14},
            "lg": {"padding": 0.4, "font_size": 16},
        }
    },
    default_variants={"variant": "default", "size": "md"}
)

# Use variants
props = button_variants.build(variant="outline", size="lg")
# Returns: {
#   "border_radius": 8,
#   "font_weight": 500,
#   "bg_color": "transparent",
#   "border_width": 1,
#   "padding": 0.4,
#   "font_size": 16
# }
```

### Compound Variants

Compound variants apply props when multiple conditions are met:

```python
button_variants = create_variants(
    base={"border_radius": 8},
    variants={
        "variant": {"primary": {...}, "secondary": {...}},
        "size": {"sm": {...}, "lg": {...}}
    },
    compound_variants=[
        {
            "conditions": {"variant": "primary", "size": "lg"},
            "props": {"font_weight": "bold", "shadow": True}
        }
    ]
)

# When variant="primary" AND size="lg", adds font_weight and shadow
props = button_variants.build(variant="primary", size="lg")
```

### Preset Variants

Pre-built variant configurations are available:

```python
from chuk_mcp_pptx.variants import CARD_VARIANTS, BUTTON_VARIANTS, BADGE_VARIANTS

# Card variants
card_props = CARD_VARIANTS.build(variant="elevated", padding="lg")

# Button variants
button_props = BUTTON_VARIANTS.build(variant="destructive", size="sm")

# Badge variants
badge_props = BADGE_VARIANTS.build(variant="success")
```

### Variant Schema

Get JSON schema for LLM consumption:

```python
schema = CARD_VARIANTS.get_schema()
# {
#   "base_props": {...},
#   "variants": {
#     "variant": {
#       "options": ["default", "outlined", "elevated", "ghost"],
#       "default": "default"
#     },
#     "padding": {...}
#   },
#   "compound_variants": [...]
# }
```

---

## Composition Patterns

Composition patterns allow building complex components from smaller pieces, inspired by shadcn/ui's compositional API.

### Pattern 1: Direct Composition

```python
from chuk_mcp_pptx.components.card_v2 import Card
from chuk_mcp_pptx.composition import CardHeader, CardContent, CardFooter

card = Card(variant="outlined", padding="md")
card.add_child(CardHeader("Dashboard", "Real-time analytics"))
card.add_child(CardContent("Your metrics are trending upward"))
card.add_child(CardFooter("Updated 5 min ago"))
card.render(slide, left=1, top=1)
```

### Pattern 2: Class Attributes (shadcn style)

```python
card = Card(variant="elevated")
card.add_child(Card.Header("Features", "What we offer"))
card.add_child(Card.Content("Feature description"))
card.add_child(Card.Footer("Learn more →", align="right"))
card.render(slide, left=1, top=1)
```

### Pattern 3: Composition Builder

Fluent API for building compositions:

```python
from chuk_mcp_pptx.composition import CompositionBuilder

builder = CompositionBuilder(theme)
children = (builder
    .header("Analytics", "Real-time insights")
    .separator()
    .content("Your metrics show strong growth")
    .badge("New", "success")
    .footer("View details")
    .build())

card = Card(variant="default")
for child in children:
    card.add_child(child)
```

### Pattern 4: Compose Helpers

```python
from chuk_mcp_pptx.composition import compose, with_separator

# Manual composition
card._children = compose(
    CardTitle("Welcome"),
    CardDescription("Get started"),
    CardContent("Follow these steps")
)

# With automatic separators
card._children = with_separator(
    CardTitle("Section 1"),
    CardContent("Content 1"),
    CardTitle("Section 2"),
    CardContent("Content 2")
)
```

### Available Subcomponents

- `CardHeader(title, description?)` - Card header with title and optional subtitle
- `CardTitle(text)` - Standalone title
- `CardDescription(text)` - Standalone description
- `CardContent(text)` - Main content area
- `CardFooter(text, align?)` - Footer with alignment (left/center/right)
- `Badge(text, variant?)` - Inline badge/label
- `Separator()` - Visual separator line
- `Stack(children, spacing?)` - Vertical stack layout

### Creating Custom Subcomponents

```python
from chuk_mcp_pptx.composition import SubComponent

class CustomSection(SubComponent):
    def __init__(self, icon: str, text: str, theme=None):
        super().__init__(theme)
        self.icon = icon
        self.text = text

    def render_into(self, text_frame, theme=None):
        p = text_frame.add_paragraph()
        p.text = f"{self.icon} {self.text}"
        # Apply styling...
        return p
```

---

## Component Registry

The component registry provides LLM-friendly schemas and discovery.

### Registering Components

```python
from chuk_mcp_pptx.registry import component, ComponentCategory, prop, example

@component(
    name="MyCard",
    category=ComponentCategory.CONTAINER,
    description="Custom card component",
    props=[
        prop("title", "string", "Card title", required=True),
        prop("variant", "string", "Visual variant",
             options=["default", "primary"], default="default"),
        prop("size", "number", "Card size in inches", default=3.0)
    ],
    variants={
        "variant": ["default", "primary"],
    },
    examples=[
        example(
            "Basic card",
            'MyCard(title="Hello", variant="primary")',
            title="Hello",
            variant="primary"
        )
    ],
    tags=["card", "container"]
)
class MyCard(Component):
    ...
```

### Using the Registry

```python
from chuk_mcp_pptx.registry import registry

# List all components
components = registry.list_components()
# ["Card", "MetricCard", "MyCard", ...]

# Get component metadata
card_meta = registry.get("Card")
print(card_meta.description)
print(card_meta.props)

# Get JSON schema
schema = registry.get_schema("Card")
# {
#   "name": "Card",
#   "description": "...",
#   "schema": {...},  # Pydantic JSON schema
#   "variants": {...},
#   "examples": [...]
# }

# Search components
results = registry.search("metric")
for r in results:
    print(f"{r.name}: {r.description}")

# List by category
ui_components = registry.list_by_category(ComponentCategory.UI)

# Get usage examples
examples = registry.get_examples("Card")
```

### LLM Export

Export entire registry for LLM consumption:

```python
llm_docs = registry.export_for_llm()
# Returns JSON string with:
# - All component schemas
# - Variants and props
# - Usage examples
# - Categorization
# - Search indices
```

### Component Metadata

The registry stores rich metadata for each component:

```python
@dataclass
class ComponentMetadata:
    name: str                           # Unique identifier
    component_class: Type               # Python class
    category: ComponentCategory         # Category enum
    description: str                    # Human-readable description
    props: List[PropDefinition]        # Property definitions
    examples: List[Dict[str, Any]]     # Usage examples
    variants: Dict[str, List[str]]     # Available variants
    composition: Dict[str, Any]         # Composition support info
    tags: List[str]                     # Searchable tags
    version: str                        # Semantic version
```

---

## Migration Guide

### From Old Card to New Card

**Before:**
```python
from chuk_mcp_pptx.components.card import Card

card = Card(title="Hello", description="World", variant="default")
card.render(slide, left=1, top=1, width=3, height=2)
```

**After:**
```python
from chuk_mcp_pptx.components.card_v2 import Card

# Option 1: Same as before (still works)
card = Card(variant="default", padding="md")
card.add_child(Card.Header("Hello", "World"))
card.render(slide, left=1, top=1, width=3, height=2)

# Option 2: With builder pattern
builder = CompositionBuilder(theme)
children = builder.header("Hello", "World").build()

card = Card(variant="outlined")
for child in children:
    card.add_child(child)
card.render(slide, left=1, top=1)

# Option 3: Full variants
card = Card(variant="elevated", padding="lg")  # More options!
```

### Benefits of Migration

1. **More Variants**: `default`, `outlined`, `elevated`, `ghost`
2. **Flexible Padding**: `none`, `sm`, `md`, `lg`, `xl`
3. **Better Composition**: Mix and match subcomponents
4. **Type Safety**: Pydantic schemas for validation
5. **LLM-Friendly**: Full schema export for AI assistance

---

## Text Components

The Text components provide formatted text boxes and bullet lists with theme integration.

### TextBox Component

Create formatted text boxes with custom styling:

```python
from chuk_mcp_pptx.components.core import TextBox

# Simple text box
text = TextBox(text="Hello World")
text.render(slide, left=2, top=2, width=4, height=1)

# Formatted text
text = TextBox(
    text="Important Notice",
    font_size=24,
    bold=True,
    alignment="center",
    color="primary.DEFAULT"
)
text.render(slide, left=1, top=3, width=8, height=1.5)

# Auto-fit text
text = TextBox(
    text="This text will auto-fit to the shape",
    auto_fit=True
)
text.render(slide, left=2, top=2, width=4, height=1)
```

**Features:**
- Custom font family, size, and styling (bold, italic)
- Text alignment (left, center, right, justify)
- Semantic or hex color support
- Auto-fit text option
- Word wrapping

**Parameters:**
- `text` (required): Text content
- `font_name`: Font family (default: "Calibri")
- `font_size`: Font size in points (default: 18)
- `bold`: Bold text (default: False)
- `italic`: Italic text (default: False)
- `color`: Text color - semantic ("primary.DEFAULT") or hex ("#FF0000")
- `alignment`: "left", "center", "right", or "justify"
- `auto_fit`: Auto-fit text to shape (default: False)

### BulletList Component

Create formatted bullet lists:

```python
from chuk_mcp_pptx.components.core import BulletList

# Simple bullet list
bullets = BulletList(items=["Item 1", "Item 2", "Item 3"])
bullets.render(slide, left=1, top=2, width=8, height=4)

# Styled bullet list
bullets = BulletList(
    items=["Increase revenue", "Reduce costs", "Improve quality"],
    font_size=18,
    color="primary.DEFAULT",
    bullet_char="→"
)
bullets.render(slide, left=1, top=2, width=8, height=3)

# Custom bullet characters
bullets = BulletList(
    items=["Complete", "In Progress", "Pending"],
    bullet_char="✓"
)
bullets.render(slide, left=1, top=2, width=8, height=3)
```

**Features:**
- Custom bullet characters (•, →, ✓, etc.)
- Font size and color control
- Adjustable item spacing
- Semantic color support
- Word wrapping

**Parameters:**
- `items` (required): List of items to display
- `font_size`: Font size in points (default: 16)
- `color`: Text color - semantic or hex
- `bullet_char`: Bullet character (default: "•")
- `spacing`: Space after each item in points (default: 6)

---

## Image Component with Filters

The Image component supports advanced image processing filters using PIL (Pillow).

### Basic Usage

```python
from chuk_mcp_pptx.components.core import Image

# Simple image
image = Image(image_source="photo.jpg")
image.render(slide, left=2, top=2, width=4)

# With shadow effect
image = Image(image_source="photo.jpg", shadow=True)
image.render(slide, left=2, top=2, width=4)
```

### Available Filters

#### Blur
Apply Gaussian blur with adjustable radius:
```python
image = Image(image_source="photo.jpg", blur_radius=10)
image.render(slide, left=2, top=2, width=4)
```

#### Grayscale
Convert image to grayscale:
```python
image = Image(image_source="photo.jpg", grayscale=True)
image.render(slide, left=2, top=2, width=4)
```

#### Sepia
Apply vintage sepia tone effect:
```python
image = Image(image_source="photo.jpg", sepia=True)
image.render(slide, left=2, top=2, width=4)
```

#### Brightness
Adjust brightness (1.0 = normal, <1 = darker, >1 = brighter):
```python
# Brighten image by 50%
image = Image(image_source="photo.jpg", brightness=1.5)

# Darken image by 30%
image = Image(image_source="photo.jpg", brightness=0.7)
```

#### Contrast
Adjust contrast (1.0 = normal, <1 = less, >1 = more):
```python
image = Image(image_source="photo.jpg", contrast=1.8)
```

#### Saturation
Adjust color saturation (1.0 = normal, 0 = grayscale, >1 = vibrant):
```python
# Increase saturation
image = Image(image_source="photo.jpg", saturation=2.0)

# Decrease saturation
image = Image(image_source="photo.jpg", saturation=0.3)
```

#### Sharpen
Apply sharpening filter:
```python
image = Image(image_source="photo.jpg", sharpen=True)
```

#### Invert
Invert colors (negative effect):
```python
image = Image(image_source="photo.jpg", invert=True)
```

### Combining Filters

Multiple filters can be applied simultaneously:

```python
image = Image(
    image_source="photo.jpg",
    blur_radius=3,
    brightness=1.2,
    contrast=1.3,
    saturation=1.5,
    shadow=True
)
image.render(slide, left=1, top=1, width=5, height=3)
```

### Filter Processing Order

Filters are applied in the following order:
1. Blur
2. Sharpen
3. Brightness
4. Contrast
5. Saturation
6. Grayscale (overrides saturation)
7. Sepia
8. Invert

### Performance Note

When filters are applied, the image is processed using PIL before being added to the slide. This happens once during rendering. Images without filters are added directly without processing for optimal performance.

---

## Layout System Integration

Text and Image components work seamlessly with the Grid and Stack layout systems.

### Text Components with Grid Layout

```python
from chuk_mcp_pptx.layout import Grid
from chuk_mcp_pptx.components.core import TextBox, BulletList

# Use 12-column grid
grid = Grid(columns=12, gap="md")

# Full-width header (12 cols)
pos_header = grid.get_span(col_span=12, col_start=0, left=0.5, top=1.8, width=9.0, height=0.8)
header = TextBox(text="Title", font_size=24, bold=True, alignment="center")
header.render(slide, **pos_header)

# Two-column layout (6 + 6 cols) - bullet lists side by side
pos_left = grid.get_span(col_span=6, col_start=0, left=0.5, top=2.8, width=9.0, height=2.0)
bullets_left = BulletList(items=["Item 1", "Item 2"], bullet_char="→")
bullets_left.render(slide, **pos_left)

pos_right = grid.get_span(col_span=6, col_start=6, left=0.5, top=2.8, width=9.0, height=2.0)
bullets_right = BulletList(items=["Item 3", "Item 4"])
bullets_right.render(slide, **pos_right)
```

### Text Components with Stack Layout

```python
from chuk_mcp_pptx.layout import Stack
from chuk_mcp_pptx.components.core import TextBox

# Vertical stack of text boxes
text_boxes = [
    TextBox(text="Section 1", bold=True),
    TextBox(text="Section 2", bold=True),
    TextBox(text="Section 3", bold=True)
]

v_stack = Stack(direction="vertical", gap="md")
v_stack.render_children(slide, text_boxes, left=0.5, top=2.0, item_width=4.0, item_height=0.8)

# Horizontal stack of bullet lists
bullet_lists = [
    BulletList(items=["Q1", "Q2", "Q3"]),
    BulletList(items=["Jan", "Feb", "Mar"])
]

h_stack = Stack(direction="horizontal", gap="lg")
h_stack.render_children(slide, bullet_lists, left=5.0, top=2.0, item_width=2.0, item_height=2.0)
```

### Image Components with Grid Layout

```python
from chuk_mcp_pptx.layout import Grid
from chuk_mcp_pptx.components.core import Image

grid = Grid(columns=12, gap="sm")

# Two large images (6 + 6 columns)
for i in range(2):
    pos = grid.get_span(col_span=6, col_start=i*6, left=0.5, top=1.8, width=9.0, height=2.0)
    img = Image(image_source=f"photo{i}.jpg", shadow=True)
    img.render(slide, **pos)

# Four small images (3 + 3 + 3 + 3 columns)
for i in range(4):
    pos = grid.get_span(col_span=3, col_start=i*3, left=0.5, top=4.0, width=9.0, height=1.5)
    img = Image(image_source=f"photo{i+2}.jpg", grayscale=True)
    img.render(slide, **pos)
```

### Image Components with Stack Layout

```python
from chuk_mcp_pptx.layout import Stack
from chuk_mcp_pptx.components.core import Image

# Vertical stack of images
images = [
    Image(image_source="photo1.jpg", shadow=True),
    Image(image_source="photo2.jpg", shadow=True),
    Image(image_source="photo3.jpg", shadow=True)
]

v_stack = Stack(direction="vertical", gap="sm")
v_stack.render_children(slide, images, left=0.5, top=2.0, item_width=4.0, item_height=1.5)

# Horizontal stack with filters
filtered_images = [
    Image(image_source="photo.jpg", brightness=1.4),
    Image(image_source="photo.jpg", contrast=1.6),
    Image(image_source="photo.jpg", saturation=1.8)
]

h_stack = Stack(direction="horizontal", gap="sm")
h_stack.render_children(slide, filtered_images, left=5.0, top=2.5, item_width=1.4, item_height=1.8)
```

### Benefits of Layout Integration

- **Responsive Layouts**: 12-column grid system adapts to different content widths
- **Consistent Spacing**: Stack layouts maintain uniform gaps between components
- **Easy Alignment**: Grid and Stack handle positioning automatically
- **Flexible Composition**: Mix and match text, images, and other components

---

## Examples

See `examples/core_components_showcase.py` for a complete demonstration including:
- All component variants
- Composition patterns
- Shape and connector components
- Image filters showcase
- SmartArt diagrams
- **Text + Layout Integration** (Grid and Stack)
- **Images + Layout Integration** (Grid and Stack)

See also:
- `examples/layout_system_showcase.py` - Dedicated layout system examples
- `examples/enhanced_components_demo.py` - Variant system examples

Run the demos:
```bash
python examples/core_components_showcase.py
python examples/layout_system_showcase.py
python examples/enhanced_components_demo.py
```

This creates presentations showcasing:
- All variant combinations
- Composition patterns
- Metric cards with trends
- Component registry usage
- Image filters and effects
- Layout system integration with text and images
