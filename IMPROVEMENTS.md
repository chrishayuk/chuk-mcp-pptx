# PowerPoint Design System Improvements

## Overview

This project now includes **shadcn/ui-inspired improvements** to make it a more powerful, LLM-friendly PowerPoint design system. The enhancements focus on three core areas:

1. **Variant System** - Type-safe, composable variants (inspired by cva)
2. **Composition Patterns** - Component composition API (like Card.Header, Card.Content)
3. **Component Registry** - LLM-friendly schemas and component discovery

---

## 🎨 What's New

### 1. Variant System (`src/chuk_mcp_pptx/variants.py`)

Inspired by `class-variance-authority`, provides a powerful way to manage component variations:

```python
from chuk_mcp_pptx.variants import create_variants

card_variants = create_variants(
    base={"border_radius": 12},
    variants={
        "variant": {
            "default": {"bg_color": "card.DEFAULT"},
            "outlined": {"bg_color": "card.DEFAULT", "border_width": 1},
            "elevated": {"bg_color": "card.DEFAULT", "shadow": True},
        },
        "padding": {
            "sm": {"padding": 0.25},
            "md": {"padding": 0.5},
            "lg": {"padding": 0.75},
        }
    },
    default_variants={"variant": "default", "padding": "md"}
)

# Build props
props = card_variants.build(variant="elevated", padding="lg")
```

**Features:**
- Base props + variant overrides
- Compound variants (apply props when multiple conditions match)
- Default variants
- JSON schema export for LLM consumption
- Preset variants: `CARD_VARIANTS`, `BUTTON_VARIANTS`, `BADGE_VARIANTS`

### 2. Composition Patterns (`src/chuk_mcp_pptx/composition.py`)

Build complex components from smaller subcomponents, shadcn-style:

```python
from chuk_mcp_pptx.components.card_v2 import Card
from chuk_mcp_pptx.composition import CompositionBuilder

# Method 1: Direct composition (shadcn-style class attributes)
card = Card(variant="outlined")
card.add_child(Card.Header("Dashboard", "Real-time analytics"))
card.add_child(Card.Content("Your data here"))
card.add_child(Card.Footer("Updated now"))

# Method 2: Fluent builder pattern
builder = CompositionBuilder(theme)
children = (builder
    .header("Title", "Subtitle")
    .separator()
    .content("Main content")
    .badge("New", "success")
    .footer("Footer text")
    .build())

card = Card()
for child in children:
    card.add_child(child)
```

**Subcomponents:**
- `CardHeader` - Header with title and description
- `CardTitle` - Standalone title
- `CardDescription` - Standalone description
- `CardContent` - Main content area
- `CardFooter` - Footer with alignment
- `Badge` - Inline badge/label
- `Separator` - Visual divider
- `Stack` - Vertical layout

**Helper Functions:**
- `compose()` - Combine subcomponents
- `with_separator()` - Auto-add separators between items
- `CompositionBuilder` - Fluent API

### 3. Component Registry (`src/chuk_mcp_pptx/registry.py`)

LLM-friendly component discovery and documentation:

```python
from chuk_mcp_pptx.registry import registry, component, ComponentCategory, prop

# Register components
@component(
    name="Card",
    category=ComponentCategory.CONTAINER,
    description="Versatile container component",
    props=[
        prop("variant", "string", "Visual variant",
             options=["default", "outlined", "elevated"]),
        prop("padding", "string", "Padding size", default="md"),
    ],
    variants={"variant": ["default", "outlined", "elevated"]},
    tags=["container", "layout"]
)
class Card(Component):
    ...

# Use registry
components = registry.list_components()  # ["Card", "MetricCard", ...]
schema = registry.get_schema("Card")     # Full JSON schema
results = registry.search("metric")       # Search by keyword
llm_docs = registry.export_for_llm()     # Export for LLM consumption
```

**Features:**
- Automatic schema generation (Pydantic)
- Component metadata (props, variants, examples)
- Search and discovery
- Category organization
- LLM-friendly JSON export
- Usage examples

---

## 📦 New Components

### Enhanced Card (`src/chuk_mcp_pptx/components/card_v2.py`)

```python
from chuk_mcp_pptx.components.card_v2 import Card, MetricCard

# Basic card with variants
card = Card(variant="outlined", padding="lg")
card.render(slide, left=1, top=1, width=4, height=3)

# Metric card
metric = MetricCard(
    label="Revenue",
    value="$1.2M",
    change="+12%",
    trend="up",
    variant="elevated"
)
metric.render(slide, left=1, top=1)
```

**Variants:**
- `variant`: `default`, `outlined`, `elevated`, `ghost`
- `padding`: `none`, `sm`, `md`, `lg`, `xl`

**Composition Support:**
- `Card.Header(title, description)`
- `Card.Title(text)`
- `Card.Description(text)`
- `Card.Content(text)`
- `Card.Footer(text, align)`

---

## 🚀 Quick Start

### Run the Demo

```bash
uv run python examples/enhanced_components_demo.py
```

This demonstrates:
- All variant combinations
- Composition patterns
- Component registry usage
- Creates `outputs/enhanced_components_showcase.pptx`

### Basic Example

```python
from pptx import Presentation
from chuk_mcp_pptx.components.card_v2 import Card, MetricCard
from chuk_mcp_pptx.composition import CompositionBuilder
from chuk_mcp_pptx.themes.theme_manager import ThemeManager

# Setup
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])
theme_mgr = ThemeManager()
theme = theme_mgr.get_theme("dark-violet")
theme.apply_to_slide(slide)

# Create composed card
card = Card(variant="elevated", padding="lg", theme=theme.__dict__)
builder = CompositionBuilder(theme.__dict__)
children = (builder
    .header("Dashboard", "Real-time Analytics")
    .separator()
    .content("Your metrics are trending upward")
    .badge("Live", "success")
    .build())

for child in children:
    card.add_child(child)

card.render(slide, left=1, top=1, width=5, height=3)

# Add metric cards
metrics = [
    MetricCard("Revenue", "$1.2M", "+12%", "up", theme=theme.__dict__),
    MetricCard("Users", "45K", "+8%", "up", theme=theme.__dict__),
]

for i, metric in enumerate(metrics):
    metric.render(slide, left=1 + i*3, top=4.5, width=2.5, height=1.5)

prs.save("output.pptx")
```

---

## 📚 Documentation

- **[Enhanced Components Guide](docs/ENHANCED_COMPONENTS.md)** - Complete documentation
- **[Examples](examples/enhanced_components_demo.py)** - Working examples
- **[Original README](README.md)** - Project overview

---

## 🎯 Benefits for LLM Integration

### 1. Schema-Driven
- Every component has a JSON schema
- Pydantic validation
- Clear prop types and defaults

### 2. Discoverable
- Search components by keyword
- Browse by category
- Get usage examples

### 3. Composable
- Mix and match subcomponents
- Builder patterns for complex UIs
- Reusable compositions

### 4. Type-Safe Variants
- Predefined variant options
- Compound variants for edge cases
- Schema export for LLM prompting

### 5. Self-Documenting
```python
# Get all component info for LLM
llm_docs = registry.export_for_llm()
# Returns comprehensive JSON with:
# - All components and schemas
# - Variants and options
# - Usage examples
# - Search indices
```

---

## 🔄 Migration from Old Components

Old components still work! New components are in `card_v2.py`:

```python
# Old way (still works)
from chuk_mcp_pptx.components.card import Card
card = Card(title="Hello", description="World")

# New way (more powerful)
from chuk_mcp_pptx.components.card_v2 import Card
card = Card(variant="elevated", padding="lg")
card.add_child(Card.Header("Hello", "World"))
```

---

## 🛠️ Architecture

```
src/chuk_mcp_pptx/
├── variants.py              # Variant system (cva-inspired)
├── composition.py           # Composition patterns
├── registry.py              # Component registry
├── components/
│   ├── base.py             # Base component class
│   ├── card.py             # Original card (legacy)
│   └── card_v2.py          # Enhanced card with variants
├── tokens/                 # Design tokens (existing)
│   ├── colors.py
│   ├── typography.py
│   └── spacing.py
└── themes/                 # Theme system (existing)
    └── theme_manager.py
```

---

## 📊 Comparison to shadcn/ui

| Feature | shadcn/ui | This System |
|---------|-----------|-------------|
| Variants (cva) | ✅ | ✅ Built with `create_variants()` |
| Composition | ✅ Card.Header | ✅ Card.Header, Card.Content, etc. |
| Theme tokens | ✅ CSS vars | ✅ Python design tokens |
| Component registry | ✅ CLI | ✅ Python registry + LLM export |
| Type safety | ✅ TypeScript | ✅ Pydantic schemas |
| Builder pattern | ✅ cn() utility | ✅ CompositionBuilder |

---

## 🎉 Next Steps

1. **Extend to More Components**
   - Apply variant system to Button, Badge, Alert, etc.
   - Add more composition patterns

2. **Layout Primitives**
   - Grid, Flex, Stack components
   - Auto-layout algorithms

3. **Animation Presets**
   - Entrance/exit animations
   - Motion design tokens

4. **CLI Tools**
   - Component scaffolding
   - Theme generator

5. **MCP Integration**
   - Expose registry via MCP tools
   - LLM-friendly component creation

---

## 📝 License

Same as main project.

---

**Built with inspiration from [shadcn/ui](https://ui.shadcn.com/) 🎨**
