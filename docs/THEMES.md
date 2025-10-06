# Theme Management

The theme system provides a centralized way to manage colors, fonts, and styling across your PowerPoint presentations.

## Table of Contents

1. [Overview](#overview)
2. [ThemeManager](#thememanager)
3. [Theme Class](#theme-class)
4. [Built-in Themes](#built-in-themes)
5. [Custom Themes](#custom-themes)
6. [Using Themes](#using-themes)
7. [Exporting/Importing](#exportingimporting)

---

## Overview

The theme system provides:
- **Consistent styling** across presentations
- **Dark and light mode support**
- **Multiple color schemes** (blue, violet, green, etc.)
- **Special themes** (cyberpunk, minimal, corporate, gradient)
- **Custom theme creation**
- **Export/import** for sharing

### Quick Example

```python
from chuk_mcp_pptx.themes import ThemeManager

# Get theme manager
mgr = ThemeManager()

# List available themes
themes = mgr.list_themes()
# ["dark", "dark-blue", "dark-violet", "light", "cyberpunk", ...]

# Get and use a theme
theme = mgr.get_theme("dark-violet")
theme.apply_to_slide(slide)
```

---

## ThemeManager

The `ThemeManager` is the central registry for themes.

### Creating a ThemeManager

```python
from chuk_mcp_pptx.themes import ThemeManager

mgr = ThemeManager()
# Automatically includes all built-in themes
```

### Listing Themes

```python
# List all themes
all_themes = mgr.list_themes()
# ["dark", "dark-blue", "dark-violet", "dark-green", "dark-orange",
#  "light", "light-blue", "light-violet", "cyberpunk", "minimal", ...]

# List themes by mode
dark_themes = mgr.list_themes_by_mode("dark")
light_themes = mgr.list_themes_by_mode("light")
```

### Getting Themes

```python
# Get a specific theme
theme = mgr.get_theme("dark-violet")

if theme:
    print(f"Theme: {theme.name}")
    print(f"Mode: {theme.mode}")
    print(f"Primary hue: {theme.primary_hue}")
else:
    print("Theme not found")
```

### Setting Current Theme

```python
# Set active theme
mgr.set_current_theme("dark-green")

# Access current theme
current = mgr.current_theme
print(f"Current theme: {current.name}")
```

### Registering Custom Themes

```python
from chuk_mcp_pptx.themes import Theme

# Create custom theme
custom = Theme(
    name="my-theme",
    primary_hue="emerald",
    mode="dark",
    font_family="Helvetica"
)

# Register it
mgr.register_theme(custom)

# Now available
theme = mgr.get_theme("my-theme")
```

### Getting Theme Information

```python
# Get theme info as dictionary
info = mgr.get_theme_info("dark-violet")
# {
#   "name": "dark-violet",
#   "mode": "dark",
#   "primary_hue": "violet",
#   "font_family": "Inter",
#   "colors": {
#     "background": {...},
#     "foreground": {...},
#     "primary": {...},
#     ...
#   }
# }
```

### Applying Themes to Slides

```python
# Apply theme to a slide
mgr.apply_to_slide(slide, "dark-blue")

# Or use current theme
mgr.set_current_theme("cyberpunk")
mgr.apply_to_slide(slide)  # Uses current theme
```

---

## Theme Class

The `Theme` class represents an individual theme.

### Creating a Theme

```python
from chuk_mcp_pptx.themes import Theme

theme = Theme(
    name="custom",
    primary_hue="emerald",  # Color from PALETTE
    mode="dark",             # "dark" or "light"
    font_family="Inter"      # Font family name
)
```

### Theme Properties

#### Direct Properties

```python
theme.name          # "custom"
theme.primary_hue   # "emerald"
theme.mode          # "dark"
theme.font_family   # "Inter"
```

#### Token Properties

Themes automatically generate semantic color tokens:

```python
# Background colors
theme.background["DEFAULT"]
theme.background["secondary"]
theme.background["tertiary"]

# Foreground colors
theme.foreground["DEFAULT"]
theme.foreground["secondary"]
theme.foreground["muted"]

# Primary colors
theme.primary["DEFAULT"]
theme.primary["foreground"]
theme.primary["hover"]
theme.primary["active"]

# Secondary colors
theme.secondary["DEFAULT"]
theme.secondary["foreground"]

# Other categories
theme.accent
theme.muted
theme.card
theme.border
```

#### Chart Colors

```python
# Get chart colors as RGBColor list
chart_colors = theme.get_chart_colors()
# [RGBColor(59, 130, 246), RGBColor(6, 182, 212), ...]

# Or access raw values
theme.chart  # ["#3b82f6", "#06b6d4", "#8b5cf6", ...]
```

### Color Methods

```python
# Convert hex to RGB
rgb = theme.hex_to_rgb("#ff0000")  # (255, 0, 0)

# Get color from token path
from pptx.dml.color import RGBColor
color = theme.get_color("primary.DEFAULT")  # Returns RGBColor
```

### Applying Themes

#### To Slides

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Apply theme background
theme.apply_to_slide(slide)
```

#### To Shapes

```python
# Create a shape
shape = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(3), Inches(1))

# Apply theme styling
theme.apply_to_shape(shape, "primary")  # Style types: card, primary, secondary, accent, muted
```

### Serialization

#### To Dictionary

```python
# Convert to dict
data = theme.to_dict()
# {
#   "name": "custom",
#   "mode": "dark",
#   "primary_hue": "emerald",
#   "font_family": "Inter"
# }
```

#### To JSON

```python
# Export as JSON string
json_str = theme.export_json()
```

#### From Dictionary

```python
# Create theme from dict
config = {
    "name": "imported",
    "primary_hue": "violet",
    "mode": "light",
    "font_family": "Arial"
}

theme = Theme.from_dict(config)
```

---

## Built-in Themes

### Dark Themes

```python
mgr.get_theme("dark")         # Default dark theme (blue)
mgr.get_theme("dark-blue")    # Dark with blue primary
mgr.get_theme("dark-violet")  # Dark with violet primary
mgr.get_theme("dark-green")   # Dark with emerald primary
mgr.get_theme("dark-orange")  # Dark with orange primary
mgr.get_theme("dark-red")     # Dark with red primary
mgr.get_theme("dark-pink")    # Dark with pink primary
mgr.get_theme("dark-purple")  # Dark with purple primary
```

#### Dark Theme Characteristics
- Dark background (`#09090b` - zinc-950)
- Light foreground text
- Suitable for modern, tech-focused presentations
- Reduced eye strain in low-light environments

### Light Themes

```python
mgr.get_theme("light")        # Default light theme (blue)
mgr.get_theme("light-blue")   # Light with blue primary
mgr.get_theme("light-violet") # Light with violet primary
mgr.get_theme("light-green")  # Light with emerald primary
mgr.get_theme("light-orange") # Light with orange primary
mgr.get_theme("light-warm")   # Light with amber primary
```

#### Light Theme Characteristics
- White or very light background
- Dark text for readability
- Professional, traditional presentation style
- Works well in well-lit environments

### Special Themes

#### Cyberpunk

```python
theme = mgr.get_theme("cyberpunk")
# - Black background (#0a0014)
# - Neon cyan foreground (#00ffff)
# - Magenta primary (#ff00ff)
# - Yellow accent (#ffff00)
# - Orbitron font family
```

Perfect for: Tech demos, gaming, futuristic content

#### Minimal

```python
theme = mgr.get_theme("minimal")
# - Pure white background (#ffffff)
# - Pure black text (#000000)
# - Grayscale palette
# - Helvetica Neue font
# - No colors, maximum simplicity
```

Perfect for: Clean presentations, academic content, minimalist design

#### Corporate

```python
theme = mgr.get_theme("corporate")
# - Light background (#f7f9fb)
# - Professional blue primary (#2b6cb0)
# - Green accent (#48bb78)
# - Segoe UI font
```

Perfect for: Business presentations, corporate decks, formal meetings

#### Gradient Themes

```python
mgr.get_theme("sunset")  # Warm gradient colors
mgr.get_theme("ocean")   # Cool blue-purple gradient
mgr.get_theme("aurora")  # Cyan-green-pink gradient
```

These themes use gradient color schemes for backgrounds and accents.

---

## Custom Themes

### Basic Custom Theme

```python
from chuk_mcp_pptx.themes import Theme

custom = Theme(
    name="brand",
    primary_hue="teal",
    mode="light",
    font_family="Roboto"
)
```

### Advanced Custom Theme

Subclass `Theme` for complete customization:

```python
from chuk_mcp_pptx.themes import Theme

class BrandTheme(Theme):
    """Custom brand theme with specific colors."""

    def __init__(self):
        super().__init__(
            name="brand",
            primary_hue="blue",
            mode="light"
        )

        # Override specific colors
        self.tokens.update({
            "background": {
                "DEFAULT": "#f8f9fa"  # Custom background
            },
            "primary": {
                "DEFAULT": "#0066cc",  # Brand blue
                "foreground": "#ffffff"
            },
            "accent": {
                "DEFAULT": "#ff6b35",  # Brand orange
                "foreground": "#000000"
            }
        })

        self.font_family = "Montserrat"

# Use custom theme
brand = BrandTheme()
mgr.register_theme(brand)
```

### Gradient Custom Theme

```python
from chuk_mcp_pptx.themes import GradientTheme

gradient = GradientTheme(
    name="custom-gradient",
    gradient_colors=["#667eea", "#764ba2", "#f093fb"]
)

mgr.register_theme(gradient)
```

---

## Using Themes

### In a Presentation

```python
from pptx import Presentation
from pptx.util import Inches
from chuk_mcp_pptx.themes import ThemeManager

# Setup
prs = Presentation()
mgr = ThemeManager()
theme = mgr.get_theme("dark-violet")

# Apply to all slides
for slide_layout in prs.slide_layouts:
    slide = prs.slides.add_slide(slide_layout)
    theme.apply_to_slide(slide)

# Or apply to specific slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
theme.apply_to_slide(slide)
```

### With Components

```python
from chuk_mcp_pptx.components.card_v2 import Card

# Convert theme to dict for component
theme_dict = theme.to_dict()

# Create component with theme
card = Card(variant="elevated", padding="lg", theme=theme_dict)
card.render(slide, left=1, top=1)
```

### Dynamic Theme Switching

```python
# Create presentation with theme A
theme_a = mgr.get_theme("dark-blue")
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
theme_a.apply_to_slide(slide1)

# Switch to theme B for next slides
theme_b = mgr.get_theme("light-green")
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
theme_b.apply_to_slide(slide2)
```

### Accessing Theme Colors in Code

```python
# Get theme
theme = mgr.get_theme("dark-violet")

# Use colors
from pptx.dml.color import RGBColor

bg_color = theme.get_color("background.DEFAULT")
primary_color = theme.get_color("primary.DEFAULT")
text_color = theme.get_color("foreground.DEFAULT")

# Apply to shape
shape.fill.solid()
shape.fill.fore_color.rgb = bg_color

# Apply to text
paragraph.font.color.rgb = text_color
```

---

## Exporting/Importing

### Export Single Theme

```python
# Get theme manager
mgr = ThemeManager()

# Export as JSON
json_str = mgr.export_theme("dark-violet")

# Save to file
with open("my-theme.json", "w") as f:
    f.write(json_str)
```

### Export All Themes

```python
# Export entire theme library
all_themes_json = mgr.export_all_themes()

# Save to file
with open("all-themes.json", "w") as f:
    f.write(all_themes_json)
```

### Import Theme

```python
import json

# Load from file
with open("my-theme.json", "r") as f:
    theme_data = json.load(f)

# Create theme from data
custom_theme = Theme.from_dict(theme_data)

# Register
mgr.register_theme(custom_theme)
```

### Share Themes

```python
# Export theme for sharing
theme = mgr.get_theme("dark-violet")
export_data = theme.export_json()

# ... send to colleague ...

# Colleague imports
import json
data = json.loads(export_data)
imported_theme = Theme.from_dict(data)
mgr.register_theme(imported_theme)
```

---

## Best Practices

### 1. Consistent Theme Usage

```python
# Good: Use one theme per presentation
theme = mgr.get_theme("corporate")
for slide in prs.slides:
    theme.apply_to_slide(slide)

# Avoid: Mixing too many themes
```

### 2. Theme-Aware Components

```python
# Good: Pass theme to components
theme_dict = theme.to_dict()
card = Card(theme=theme_dict)

# Components automatically use theme colors
```

### 3. Semantic Color Usage

```python
# Good: Use semantic tokens
bg = theme.get_color("background.DEFAULT")
primary = theme.get_color("primary.DEFAULT")

# Avoid: Hardcoded colors
# bg = RGBColor(0, 0, 0)  # Not theme-aware
```

### 4. Mode Selection

```python
# Consider your presentation environment
if presenting_in_dark_room:
    theme = mgr.get_theme("dark-violet")
else:
    theme = mgr.get_theme("light")
```

### 5. Custom Branding

```python
# Create a brand theme and reuse it
class CompanyTheme(Theme):
    def __init__(self):
        super().__init__("company", "blue", "light")
        self.tokens["primary"]["DEFAULT"] = "#company-blue"
        self.font_family = "CompanyFont"

# Register once, use everywhere
mgr.register_theme(CompanyTheme())
```

---

## See Also

- [Design Tokens](TOKENS.md) - Token system used by themes
- [Enhanced Components](ENHANCED_COMPONENTS.md) - Using themes with components
- [Improvements](../IMPROVEMENTS.md) - System overview
