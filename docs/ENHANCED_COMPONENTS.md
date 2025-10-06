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

## Examples

See `examples/enhanced_components_demo.py` for a complete demonstration.

Run the demo:
```bash
python examples/enhanced_components_demo.py
```

This creates a presentation showcasing:
- All variant combinations
- Composition patterns
- Metric cards with trends
- Component registry usage
