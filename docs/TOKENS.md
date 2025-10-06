# Design Tokens

Design tokens are the foundation of the PowerPoint design system. They provide consistent values for colors, typography, spacing, and other design properties across your presentations.

## Table of Contents

1. [Overview](#overview)
2. [Color Tokens](#color-tokens)
3. [Typography Tokens](#typography-tokens)
4. [Spacing Tokens](#spacing-tokens)
5. [Usage](#usage)
6. [Exporting Tokens](#exporting-tokens)

---

## Overview

Design tokens are similar to CSS variables in web design. They allow you to:
- Maintain consistency across components
- Enable easy theming
- Provide semantic naming for design values
- Support LLM-friendly documentation

### Quick Example

```python
from chuk_mcp_pptx.tokens import PALETTE, FONT_SIZES, SPACING

# Access raw values
primary_color = PALETTE["blue"][500]  # "#3b82f6"
heading_size = FONT_SIZES["3xl"]      # 28
padding = SPACING["4"]                 # 0.25 inches
```

---

## Color Tokens

### Raw Color Palette

The palette includes 19 color families, each with 11 shades (50-950):

```python
from chuk_mcp_pptx.tokens import PALETTE

# Available colors
colors = [
    "slate", "zinc", "red", "orange", "amber", "yellow",
    "lime", "green", "emerald", "teal", "cyan", "sky",
    "blue", "indigo", "violet", "purple", "fuchsia", "pink", "rose"
]

# Each has shades: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
blue_500 = PALETTE["blue"][500]  # "#3b82f6"
blue_900 = PALETTE["blue"][900]  # "#1e3a8a"
```

### Semantic Color Tokens

Semantic tokens provide theme-aware colors that adapt to dark/light modes:

```python
from chuk_mcp_pptx.tokens import get_semantic_tokens

# Get tokens for a theme
tokens = get_semantic_tokens(primary_hue="blue", mode="dark")

# Available semantic categories:
tokens["background"]    # Background colors
tokens["foreground"]    # Text colors
tokens["primary"]       # Primary brand colors
tokens["secondary"]     # Secondary colors
tokens["accent"]        # Accent colors
tokens["muted"]         # Muted/subdued colors
tokens["card"]          # Card/container colors
tokens["border"]        # Border colors
tokens["destructive"]   # Error/danger colors
tokens["success"]       # Success colors
tokens["warning"]       # Warning colors
tokens["info"]          # Info colors
tokens["chart"]         # Chart visualization colors
```

#### Color Token Structure

Each color category has variants:

```python
# Primary color variants
tokens["primary"]["DEFAULT"]     # Main primary color
tokens["primary"]["foreground"]  # Text color on primary background
tokens["primary"]["hover"]       # Hover state
tokens["primary"]["active"]      # Active state
```

### Gradients

Pre-defined gradient color schemes:

```python
from chuk_mcp_pptx.tokens import GRADIENTS

GRADIENTS["sunset"]   # ["#ff6b6b", "#f7b731", "#5f27cd"]
GRADIENTS["ocean"]    # ["#667eea", "#764ba2", "#f093fb"]
GRADIENTS["forest"]   # ["#00b09b", "#96c93d", "#ffe000"]
GRADIENTS["flame"]    # ["#ff416c", "#ff4b2b", "#ffc837"]
GRADIENTS["aurora"]   # ["#00c9ff", "#92fe9d", "#fc00ff"]
GRADIENTS["cosmic"]   # ["#7303c0", "#ec38bc", "#03001e"]
GRADIENTS["mint"]     # ["#00b4d8", "#0077b6", "#03045e"]
GRADIENTS["lavender"] # ["#e0aaff", "#c77dff", "#7209b7"]
```

---

## Typography Tokens

### Font Families

```python
from chuk_mcp_pptx.tokens import FONT_FAMILIES

FONT_FAMILIES["sans"]    # ["Inter", "Segoe UI", "system-ui", ...]
FONT_FAMILIES["serif"]   # ["Playfair Display", "Georgia", ...]
FONT_FAMILIES["mono"]    # ["JetBrains Mono", "Cascadia Code", ...]
FONT_FAMILIES["display"] # ["Poppins", "Montserrat", ...]
```

### Font Sizes

Font sizes in points:

```python
from chuk_mcp_pptx.tokens import FONT_SIZES

FONT_SIZES["xs"]   # 10
FONT_SIZES["sm"]   # 12
FONT_SIZES["base"] # 14
FONT_SIZES["lg"]   # 16
FONT_SIZES["xl"]   # 18
FONT_SIZES["2xl"]  # 22
FONT_SIZES["3xl"]  # 28
FONT_SIZES["4xl"]  # 36
FONT_SIZES["5xl"]  # 48
FONT_SIZES["6xl"]  # 60
FONT_SIZES["7xl"]  # 72
FONT_SIZES["8xl"]  # 96
FONT_SIZES["9xl"]  # 128
```

### Font Weights

```python
from chuk_mcp_pptx.tokens import FONT_WEIGHTS

FONT_WEIGHTS["thin"]       # 100
FONT_WEIGHTS["extralight"] # 200
FONT_WEIGHTS["light"]      # 300
FONT_WEIGHTS["normal"]     # 400
FONT_WEIGHTS["medium"]     # 500
FONT_WEIGHTS["semibold"]   # 600
FONT_WEIGHTS["bold"]       # 700
FONT_WEIGHTS["extrabold"]  # 800
FONT_WEIGHTS["black"]      # 900
```

### Line Heights

Line height multipliers:

```python
from chuk_mcp_pptx.tokens import LINE_HEIGHTS

LINE_HEIGHTS["none"]    # 1
LINE_HEIGHTS["tight"]   # 1.25
LINE_HEIGHTS["snug"]    # 1.375
LINE_HEIGHTS["normal"]  # 1.5
LINE_HEIGHTS["relaxed"] # 1.625
LINE_HEIGHTS["loose"]   # 2
```

### Letter Spacing

Em units for letter spacing:

```python
from chuk_mcp_pptx.tokens import LETTER_SPACING

LETTER_SPACING["tighter"] # -0.05
LETTER_SPACING["tight"]   # -0.025
LETTER_SPACING["normal"]  # 0
LETTER_SPACING["wide"]    # 0.025
LETTER_SPACING["wider"]   # 0.05
LETTER_SPACING["widest"]  # 0.1
```

### Text Styles

Pre-defined text style combinations:

```python
from chuk_mcp_pptx.tokens import get_text_style

# Heading styles
h1 = get_text_style("h1")        # Display, 48pt, bold
h2 = get_text_style("h2")        # Display, 36pt, semibold
h3 = get_text_style("h3")        # Display, 28pt, semibold
h4 = get_text_style("h4")        # Sans, 22pt, medium
h5 = get_text_style("h5")        # Sans, 18pt, medium
h6 = get_text_style("h6")        # Sans, 16pt, medium

# Body styles
body = get_text_style("body")          # Sans, 14pt, relaxed
body_lg = get_text_style("body-lg")    # Sans, 16pt, relaxed
body_sm = get_text_style("body-sm")    # Sans, 12pt, relaxed

# Special styles
caption = get_text_style("caption")    # Sans, 10pt, wide
overline = get_text_style("overline")  # Sans, 10pt, uppercase
code = get_text_style("code")          # Mono, 12pt
quote = get_text_style("quote")        # Serif, 16pt, light
lead = get_text_style("lead")          # Sans, 18pt, light
```

### Typography Scale

Responsive typography for different contexts:

```python
from chuk_mcp_pptx.tokens import TYPOGRAPHY_SCALE

# Display scale (hero text)
TYPOGRAPHY_SCALE["display"]["2xl"]  # 128pt, tight
TYPOGRAPHY_SCALE["display"]["xl"]   # 96pt, tight
TYPOGRAPHY_SCALE["display"]["lg"]   # 72pt, tight

# Heading scale
TYPOGRAPHY_SCALE["heading"]["2xl"]  # 48pt, tight
TYPOGRAPHY_SCALE["heading"]["xl"]   # 36pt, tight
TYPOGRAPHY_SCALE["heading"]["lg"]   # 28pt, snug
```

---

## Spacing Tokens

All spacing values are in inches (PowerPoint native unit).

### Base Spacing Scale

```python
from chuk_mcp_pptx.tokens import SPACING

SPACING["0"]    # 0
SPACING["px"]   # 0.01
SPACING["1"]    # 0.0625
SPACING["2"]    # 0.125
SPACING["3"]    # 0.1875
SPACING["4"]    # 0.25    # Base unit
SPACING["6"]    # 0.375
SPACING["8"]    # 0.5
SPACING["12"]   # 0.75
SPACING["16"]   # 1.0
SPACING["24"]   # 1.5
SPACING["32"]   # 2.0
# ... up to 96
```

### Margin Presets

```python
from chuk_mcp_pptx.tokens import MARGINS

MARGINS["none"] # 0
MARGINS["xs"]   # 0.125
MARGINS["sm"]   # 0.25
MARGINS["md"]   # 0.375
MARGINS["lg"]   # 0.5
MARGINS["xl"]   # 0.75
MARGINS["2xl"]  # 1.0
MARGINS["3xl"]  # 1.5
```

### Padding Presets

```python
from chuk_mcp_pptx.tokens import PADDING

PADDING["none"] # 0
PADDING["xs"]   # 0.125
PADDING["sm"]   # 0.1875
PADDING["md"]   # 0.25
PADDING["lg"]   # 0.375
PADDING["xl"]   # 0.5
PADDING["2xl"]  # 0.75
PADDING["3xl"]  # 1.0
```

### Gap Presets

For spacing between elements:

```python
from chuk_mcp_pptx.tokens import GAPS

GAPS["none"] # 0
GAPS["xs"]   # 0.0625
GAPS["sm"]   # 0.125
GAPS["md"]   # 0.25
GAPS["lg"]   # 0.375
GAPS["xl"]   # 0.5
```

### Border Radius

Border radius values in points:

```python
from chuk_mcp_pptx.tokens import RADIUS

RADIUS["none"] # 0
RADIUS["sm"]   # 2
RADIUS["md"]   # 4
RADIUS["lg"]   # 6
RADIUS["xl"]   # 8
RADIUS["2xl"]  # 12
RADIUS["3xl"]  # 16
RADIUS["full"] # 9999  # Fully rounded
```

### Border Width

```python
from chuk_mcp_pptx.tokens import BORDER_WIDTH

BORDER_WIDTH["0"] # 0
BORDER_WIDTH["1"] # 0.5
BORDER_WIDTH["2"] # 1
BORDER_WIDTH["3"] # 1.5
BORDER_WIDTH["4"] # 2
BORDER_WIDTH["8"] # 4
```

### Shadows

Shadow definitions with offset, blur, and color:

```python
from chuk_mcp_pptx.tokens import SHADOWS

SHADOWS["none"]  # None
SHADOWS["sm"]    # Small shadow
SHADOWS["md"]    # Medium shadow
SHADOWS["lg"]    # Large shadow
SHADOWS["xl"]    # Extra large shadow
SHADOWS["2xl"]   # 2X large shadow
SHADOWS["inner"] # Inner shadow

# Shadow structure:
# {
#   "offset_x": 0,
#   "offset_y": 4,
#   "blur": 6,
#   "color": "rgba(0, 0, 0, 0.1)"
# }
```

### Grid System

```python
from chuk_mcp_pptx.tokens import GRID

GRID["cols"]   # 12  # Column count
GRID["gutter"] # 0.25 # Space between columns
GRID["margin"] # 0.5  # Outer margin
```

### Container Widths

```python
from chuk_mcp_pptx.tokens import CONTAINERS

CONTAINERS["sm"]   # 8 inches
CONTAINERS["md"]   # 9 inches
CONTAINERS["lg"]   # 10 inches (standard slide)
CONTAINERS["xl"]   # 11 inches
CONTAINERS["2xl"]  # 12 inches
CONTAINERS["full"] # 13.333 inches (full width)
```

### Aspect Ratios

```python
from chuk_mcp_pptx.tokens import ASPECT_RATIOS

ASPECT_RATIOS["square"]     # "1:1"
ASPECT_RATIOS["video"]      # "16:9"
ASPECT_RATIOS["photo"]      # "4:3"
ASPECT_RATIOS["portrait"]   # "3:4"
ASPECT_RATIOS["widescreen"] # "21:9"
ASPECT_RATIOS["golden"]     # "1.618:1"
```

### Layout Spacing Helper

Get complete spacing configuration for layout types:

```python
from chuk_mcp_pptx.tokens import get_layout_spacing

compact = get_layout_spacing("compact")
# {
#   "margin": 0.25,
#   "padding": 0.1875,
#   "gap": 0.125
# }

default = get_layout_spacing("default")
# {
#   "margin": 0.375,
#   "padding": 0.25,
#   "gap": 0.25
# }

comfortable = get_layout_spacing("comfortable")
# {
#   "margin": 0.5,
#   "padding": 0.375,
#   "gap": 0.375
# }

spacious = get_layout_spacing("spacious")
# {
#   "margin": 0.75,
#   "padding": 0.5,
#   "gap": 0.5
# }
```

---

## Usage

### In Components

```python
from chuk_mcp_pptx.tokens import get_semantic_tokens, FONT_SIZES, SPACING
from pptx.util import Pt, Inches

# Get theme tokens
tokens = get_semantic_tokens("violet", "dark")

# Use in component
shape.fill.fore_color.rgb = RGBColor(*hex_to_rgb(tokens["primary"]["DEFAULT"]))
shape.text_frame.margin_left = Inches(SPACING["4"])
paragraph.font.size = Pt(FONT_SIZES["xl"])
```

### With Theme System

```python
from chuk_mcp_pptx.themes import ThemeManager

mgr = ThemeManager()
theme = mgr.get_theme("dark-violet")

# Theme has semantic tokens built-in
bg_color = theme.tokens["background"]["DEFAULT"]
primary = theme.tokens["primary"]["DEFAULT"]
```

### Custom Token Usage

```python
from chuk_mcp_pptx.tokens import PALETTE, SPACING

# Build custom combinations
my_colors = {
    "primary": PALETTE["emerald"][600],
    "secondary": PALETTE["teal"][500],
    "accent": PALETTE["amber"][400]
}

my_spacing = {
    "tight": SPACING["2"],
    "normal": SPACING["4"],
    "loose": SPACING["8"]
}
```

---

## Exporting Tokens

### Get All Tokens

```python
from chuk_mcp_pptx.tokens import get_all_tokens

all_tokens = get_all_tokens(primary_hue="blue", mode="dark")
# {
#   "colors": {...},
#   "typography": {...},
#   "spacing": {...},
#   "borders": {...},
#   "shadows": {...},
#   "layout": {...}
# }
```

### Export as JSON

```python
from chuk_mcp_pptx.tokens import export_tokens_json

json_str = export_tokens_json(primary_hue="violet", mode="light")
# Returns formatted JSON string

# Save to file
with open("tokens.json", "w") as f:
    f.write(json_str)
```

### For LLM Consumption

Tokens are structured to be easily consumable by LLMs:

```python
# LLM can query: "What font sizes are available?"
from chuk_mcp_pptx.tokens import FONT_SIZES
print(list(FONT_SIZES.keys()))
# ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", ...]

# LLM can query: "What is the blue-500 color?"
from chuk_mcp_pptx.tokens import PALETTE
print(PALETTE["blue"][500])
# "#3b82f6"

# LLM can query: "Get all semantic colors for dark mode"
from chuk_mcp_pptx.tokens import get_semantic_tokens
tokens = get_semantic_tokens("blue", "dark")
print(tokens.keys())
# ["background", "foreground", "primary", "secondary", ...]
```

---

## Best Practices

1. **Use Semantic Tokens in Components**
   - Prefer `tokens["primary"]["DEFAULT"]` over `PALETTE["blue"][500]`
   - Semantic tokens adapt to themes automatically

2. **Consistent Spacing**
   - Use the spacing scale rather than arbitrary values
   - Prefer `SPACING["4"]` over `0.25`

3. **Typography Hierarchy**
   - Use `get_text_style()` for consistent text styling
   - Maintain visual hierarchy with the typography scale

4. **Theming**
   - Build components using semantic tokens
   - Components will automatically support all themes

5. **LLM Integration**
   - Export tokens as JSON for LLM documentation
   - Use descriptive names that LLMs can understand
   - Provide examples in documentation

---

## See Also

- [Theme Management](THEMES.md) - Using tokens with themes
- [Enhanced Components](ENHANCED_COMPONENTS.md) - Components using tokens
- [Variant System](../IMPROVEMENTS.md#variant-system) - Variants with token integration
