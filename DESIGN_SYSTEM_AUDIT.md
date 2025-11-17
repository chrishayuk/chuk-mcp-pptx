# Design System Audit Report

**Date:** 2025-11-16
**Status:** Analysis Complete - Pending Refactor

## Executive Summary

Out of **51 component files** in the components directory, significant violations were found across multiple categories. Components are not consistently using the design system for colors, typography, and fonts. Hardcoded strings exist throughout that should be constants/enums.

---

## 1. Design System Files Location

The project has a well-structured design system located in `src/chuk_mcp_pptx/`:

### Core Design System Files:
- `tokens/colors.py` - Color palette and semantic color tokens
- `tokens/typography.py` - Font families, sizes, weights, and text styles
- `tokens/spacing.py` - Spacing scale, margins, padding, gaps, border radius, shadows
- `constants.py` - General constants and enums
- `variants.py` - Variant system for component composition
- `themes/theme_manager.py` - Theme management system

---

## 2. Components NOT Using Design System Properly

### Chat Components (HIGH Priority - 11 files)

1. `components/chat/android.py` - Hardcoded colors throughout
2. `components/chat/aol.py` - Multiple hardcoded RGB values
3. `components/chat/chatgpt.py` - ChatGPT-specific colors hardcoded
4. `components/chat/facebook.py` - Facebook blue hardcoded
5. `components/chat/generic.py` - Generic chat with hardcoded values
6. `components/chat/ios.py` - iOS blue hardcoded (some using tokens)
7. `components/chat/msn.py` - MSN messenger colors hardcoded
8. `components/chat/slack.py` - Slack purple and colors hardcoded
9. `components/chat/teams.py` - Teams purple colors hardcoded
10. `components/chat/whatsapp.py` - WhatsApp green hardcoded
11. `components/chat/base.py` - Base chat component

### Container Components (HIGH Priority - 6 files)

12. `components/containers/browser.py` - Browser chrome colors hardcoded
13. `components/containers/generic.py` - Generic container colors hardcoded
14. `components/containers/iphone.py` - iPhone bezel colors hardcoded
15. `components/containers/macos.py` - macOS window colors hardcoded
16. `components/containers/samsung.py` - Samsung bezel colors hardcoded
17. `components/containers/windows.py` - Windows window colors hardcoded

### Code Component (MEDIUM Priority - 1 file)

18. `components/code.py` - Language colors and styling hardcoded

### Chart Components (MEDIUM Priority - 6 files)

19. `components/charts/column_bar.py` - Chart colors hardcoded
20. `components/charts/funnel.py` - Funnel stage colors hardcoded
21. `components/charts/line_area.py` - Area/line chart colors hardcoded
22. `components/charts/pie_doughnut.py` - Pie chart colors hardcoded
23. `components/charts/radar_combo.py` - Radar/combo colors hardcoded
24. `components/charts/scatter_bubble.py` - Scatter plot colors hardcoded

---

## 3. Specific Violations with Examples

### A. Hardcoded RGB Colors

#### `components/chat/chatgpt.py`
- Line 65: `RGBColor(247, 247, 248)` - User message background
- Line 67: `RGBColor(236, 236, 241)` - System message background
- Line 70: `RGBColor(255, 255, 255)` - Assistant message background
- Line 74: `RGBColor(52, 53, 65)` - ChatGPT dark text color
- Line 121: `RGBColor(16, 163, 127)` - ChatGPT green avatar color

#### `components/chat/android.py`
- Line 74: `RGBColor(11, 87, 208)` - RCS blue for sent messages
- Line 77: `RGBColor(231, 237, 243)` - Material gray for received messages
- Line 82: `RGBColor(255, 255, 255)` - White text
- Line 84: `RGBColor(32, 33, 36)` - Material dark gray
- Line 150: `RGBColor(95, 99, 104)` - Material medium gray

#### `components/code.py`
- Lines 27-46: `LANGUAGE_COLORS` dictionary with hardcoded hex values
- Line 86: `self.LANGUAGE_COLORS.get(self.language, "#666666")` - Fallback gray
- Line 117: `RGBColor(*self.hex_to_rgb("#1e1e1e"))` - Code background (dark)
- Line 150: `RGBColor(*self.hex_to_rgb("#e0e0e0"))` - Code text (light)
- Line 268: `RGBColor(*self.hex_to_rgb("#000000"))` - Terminal black background
- Line 271: `RGBColor(*self.hex_to_rgb("#00ff00"))` - Terminal green border
- Line 301: `RGBColor(*self.hex_to_rgb("#00ff00"))` - Terminal green text

#### `components/containers/browser.py`
- Lines 79-88: Chrome/Safari/Firefox hardcoded chrome colors
- Line 84: `RGBColor(50, 50, 50)` and `RGBColor(240, 240, 240)`
- Line 180: `RGBColor(255, 95, 86)` - Close button (macOS red)
- Line 181: `RGBColor(255, 189, 46)` - Minimize button (macOS yellow)
- Line 182: `RGBColor(40, 201, 64)` - Maximize button (macOS green)

#### `components/containers/windows.py`
- Line 154: `RGBColor(232, 17, 35)` - Windows red close button

#### `components/chat/slack.py`
- Line 101: `RGBColor(97, 31, 105)` - Slack purple avatar
- Line 117: `RGBColor(29, 28, 29)` - Slack dark text
- Line 121: `RGBColor(97, 96, 97)` - Slack medium gray
- Line 131: `RGBColor(29, 155, 209)` - Slack blue

#### `components/chat/teams.py`
- Line 49: `RGBColor(98, 100, 167)` - Teams purple
- Line 60: `RGBColor(37, 36, 35)` - Teams dark gray
- Line 66: `RGBColor(96, 94, 92)` - Teams medium gray

### B. Hardcoded Font Sizes

#### `components/code.py`
- Line 137: `p.font.size = Pt(10)` - Language label font size
- Line 146: `p.font.size = Pt(11)` - Code font size
- Line 227: `p.font.size = Pt(12)` - Inline code font size
- Line 286: `p.font.size = Pt(10)` - Terminal header font size
- Line 300: `p.font.size = Pt(11)` - Terminal output font size

#### `components/chat/chatgpt.py`
- Line 130: `av_p.font.size = Pt(12)` - Avatar text
- Line 165: `p.font.size = Pt(14)` - Message text

#### `components/chat/android.py`
- Line 148: `current_p.font.size = Pt(11)` - Sender name
- Line 157: `current_p.font.size = Pt(14)` - Message text
- Line 181: `ts_p.font.size = Pt(10)` - Timestamp

#### `components/chat/facebook.py`
- Line 134: `av_p.font.size = Pt(11)` - Avatar
- Line 169: `p.font.size = Pt(15)` - Message text

#### `components/charts/funnel.py`
- Line 129: `Pt(18)` - Funnel title font size
- Line 218: `Pt(stage_font_size)` - Stage font size
- Line 362: `Pt(16)` - Funnel header font size
- Lines 514, 522, 530: `Pt(9)` and `Pt(8)` - Table cell font sizes

#### `components/charts/line_area.py`
- Line 427: `Pt(11)` - Label font size
- Line 445: `Pt(10)` - Value font size

### C. Hardcoded Font Families

#### `components/code.py`
- Line 136: `p.font.name = "Cascadia Code"` - Hardcoded monospace font
- Line 145: `p.font.name = "Cascadia Code"` - Repeated
- Line 226: `p.font.name = "Cascadia Code"` - Inline code font
- Line 285: `p.font.name = "Cascadia Code"` - Terminal font

#### `components/chat/chatgpt.py`
- Line 166: `p.font.name = "Söhne"` - ChatGPT proprietary font

#### `components/chat/android.py`
- Line 158: `p.font.name = "Roboto"` - Material Design font

#### Language Colors Dictionary (`components/code.py`)
```python
LANGUAGE_COLORS = {
    "python": "#3776ab",
    "javascript": "#f7df1e",
    "typescript": "#3178c6",
    "java": "#007396",
    "csharp": "#239120",
    "cpp": "#00599C",
    "go": "#00ADD8",
    "rust": "#000000",
    "ruby": "#CC342D",
    "php": "#777BB4",
    "swift": "#FA7343",
    "kotlin": "#7F52FF",
    "sql": "#336791",
    "html": "#E34C26",
    "css": "#1572B6",
    "shell": "#4EAA25",
    "yaml": "#CB171E",
    "json": "#000000",
}
```

### D. Hardcoded Spacing/Dimensions

#### `components/chat/chatgpt.py`
- Line 78: `chars_per_line = int(width * 8)` - Hardcoded character calculation
- Line 80: `line_height = 0.2` - Hardcoded line height
- Line 81: `padding = 0.4 if self.variant == "user" else 0.5` - Hardcoded padding
- Line 108: `avatar_left = left + 0.35` - Hardcoded offset
- Line 137: `text_left = left + 0.35 + avatar_size + 0.2` - Multiple hardcoded offsets

#### `components/chat/android.py`
- Line 88: `chars_per_line = int(width * 11)` - Hardcoded calculation
- Line 90: `line_height = 0.2` - Hardcoded line height
- Line 91: `padding = 0.3` - Hardcoded padding
- Line 100: `bubble_width = min(width * 0.7, width - 1.0)` - Hardcoded width formula
- Line 136: `padding = 0.12` - Hardcoded text padding

### E. Hardcoded String Constants (Enum Candidates)

#### Message Variants (Not Centralized)
- `"sent"`, `"received"`, `"user"`, `"assistant"`, `"system"` - Scattered across chat components
- `"text"`, `"active"`, `"success"`, `"warning"`, `"error"` - Status indicators
- `"light"`, `"dark"` - Theme modes
- `"chrome"`, `"safari"`, `"firefox"` - Browser types (in containers)

#### Alignment Values
- `PP_ALIGN.LEFT`, `PP_ALIGN.CENTER`, `PP_ALIGN.RIGHT`, `PP_ALIGN.JUSTIFY` used
- But string variants like `"left"`, `"center"`, `"right"` hardcoded in some places

---

## 4. Patterns of Hardcoded Strings That Should Be Enums/Constants

### Message Variant Types
```python
# Currently scattered, should be centralized:
MessageVariant = Literal["sent", "received", "user", "assistant", "system"]
```

### Chat Platform Types
```python
# Scattered across chat components, should be enum:
ChatPlatform = Literal["android", "ios", "chatgpt", "slack", "teams", "whatsapp", "facebook", "msn", "aol", "generic"]
```

### Browser Types
```python
# In browser.py, should be enum:
BrowserType = Literal["chrome", "safari", "firefox"]
```

### Container Platform Types
```python
# Container components, should be enum:
ContainerPlatform = Literal["iphone", "samsung", "windows", "macos", "generic"]
```

### Code Language Types
```python
# In code.py, should be enum with associated design tokens:
CodeLanguage = Literal["python", "javascript", "typescript", "java", "csharp", "cpp", "go", "rust", "ruby", "php", "swift", "kotlin", "sql", "html", "css", "shell", "yaml", "json", "text"]
```

### Text Alignment
```python
# Used inconsistently:
TextAlignment = Literal["left", "center", "right", "justify"]
```

---

## 5. Summary Table

| Category | Files | Main Issues | Priority |
|----------|-------|------------|----------|
| **Chat Components** | 11 | Hardcoded RGB colors, fonts, spacing | HIGH |
| **Container Components** | 6 | Platform-specific colors not in tokens | HIGH |
| **Code Component** | 1 | Language colors, font family hardcoded | MEDIUM |
| **Chart Components** | 6 | Chart colors hardcoded | MEDIUM |
| **Core Components** | Text, Button, etc. | Some hardcoded values, but better usage of tokens | LOW |

---

## 6. Recommendations

### Phase 1: Create Missing Token Files
1. **Create Color System Constants** for platform-specific colors:
   - Extract ChatGPT, Slack, Teams, WhatsApp colors to design tokens
   - Create `tokens/platform_colors.py` for chat/app-specific colors
   - Create `tokens/languages.py` for code language colors

2. **Create Typography Constants**:
   - Move hardcoded font sizes from components to `tokens/typography.py`
   - Create size presets: `CHAT_SIZES`, `CODE_SIZES`, `CHART_SIZES`

3. **Centralize Platform-Specific Tokens**:
   - Create `tokens/platforms.py` for browser/OS types

### Phase 2: Create Missing Enums
1. **Create Message/Chat Enums**:
   - `MessageVariant` enum in constants.py
   - `ChatPlatform` enum for platform types
   - `BrowserType` enum for browsers
   - `ContainerPlatform` enum for OS containers
   - `CodeLanguage` enum for programming languages

### Phase 3: Refactor Components Systematically
1. **Chat Components** (11 files) - Highest impact
2. **Container Components** (6 files)
3. **Code Component** (1 file)
4. **Chart Components** (6 files)

### Phase 4: Standardize Spacing Values
- Extract magic numbers from chat components (0.2, 0.3, 0.5, etc.)
- Add to `SPACING` or create `COMPONENT_SPACING` in `tokens/spacing.py`

### Phase 5: Font Family Consolidation
- Move hardcoded font names to `FONT_FAMILIES` in typography
- Use design token references instead of literal strings

---

## Next Steps

1. Create new token files for platform-specific colors
2. Create missing enums for message variants, platforms, languages
3. Refactor components systematically starting with chat components
4. Update documentation with new design system usage patterns
5. Add linting/validation to prevent future violations
