# Design System Refactoring Summary

## Completed Refactorings

### ✅ New Token Files Created
1. **`src/chuk_mcp_pptx/tokens/platform_colors.py`** - Platform-specific brand colors
   - `CHAT_COLORS` - All chat platform colors (iOS, Android, WhatsApp, ChatGPT, Slack, Teams, Facebook, MSN, AOL, Generic)
   - `BROWSER_COLORS` - Browser chrome colors (Chrome, Safari, Firefox)
   - `MACOS_CONTROLS` - macOS window traffic lights
   - `WINDOWS_CONTROLS` - Windows window controls
   - `TERMINAL_COLORS` - Terminal/console colors
   - `DEVICE_COLORS` - Device bezel colors
   - `LANGUAGE_COLORS` - Programming language brand colors
   - Helper functions: `get_chat_color()`, `get_browser_color()`, `get_language_color()`

### ✅ Constants/Enums Added (`src/chuk_mcp_pptx/constants.py`)
- `MessageVariant` - Literal type for message variants
- `ChatPlatform` - Chat platform types
- `BrowserType` - Browser types
- `ContainerPlatform` - Container platform types
- `DeviceVariant` - Device variants
- `CodeLanguage` - Programming language types
- `TextAlignment` - Text alignment types
- `ThemeMode` - Theme mode (light/dark)

### ✅ Components Refactored

#### 1. Code Component (`src/chuk_mcp_pptx/components/code.py`)
**Changes:**
- ❌ Removed hardcoded `LANGUAGE_COLORS` dictionary
- ✅ Now imports from `tokens.platform_colors.get_language_color()`
- ✅ Uses `FONT_FAMILIES["mono"][0]` instead of hardcoded `"Cascadia Code"`
- ✅ Uses `FONT_SIZES["xs"]`, `FONT_SIZES["sm"]` instead of `Pt(10)`, `Pt(11)`, `Pt(12)`
- ✅ Uses `TERMINAL_COLORS` for terminal background, border, text colors
- ✅ Uses design system `foreground.DEFAULT` instead of hardcoded `#e0e0e0`

**Before:**
```python
LANGUAGE_COLORS = {"python": "#3776ab", ...}
p.font.name = "Cascadia Code"
p.font.size = Pt(10)
container.fill.fore_color.rgb = RGBColor(*self.hex_to_rgb("#1e1e1e"))
```

**After:**
```python
from ..tokens.platform_colors import get_language_color, TERMINAL_COLORS
p.font.name = FONT_FAMILIES["mono"][0]
p.font.size = Pt(FONT_SIZES["xs"])
container.fill.fore_color.rgb = RGBColor(*self.hex_to_rgb(TERMINAL_COLORS["background"]))
```

#### 2. iOS Chat Component (`src/chuk_mcp_pptx/components/chat/ios.py`)
**Changes:**
- ✅ Uses `get_chat_color("ios", variant, "light")` instead of hardcoded `RGBColor(11, 147, 246)`
- ✅ Uses `CHAT_COLORS["ios"]["text_sent"]` / `"text_received"` for text colors
- ✅ Uses `FONT_FAMILIES["sans"][0]` instead of hardcoded `"SF Pro Text"`
- ✅ Uses `get_color("muted.foreground")` for timestamp instead of hardcoded `RGBColor(142, 142, 147)`

**Before:**
```python
return RGBColor(11, 147, 246)  # iOS blue
p.font.name = "SF Pro Text"
ts_p.font.color.rgb = RGBColor(142, 142, 147)
```

**After:**
```python
hex_color = get_chat_color("ios", self.variant, "light")
return RGBColor(*self.hex_to_rgb(hex_color))
p.font.name = FONT_FAMILIES["sans"][0]
ts_p.font.color.rgb = self.get_color("muted.foreground")
```

---

## Remaining Refactorings Needed

### 🔄 Chat Components (9 files remaining)

All chat components follow similar patterns and need the same refactorings:

#### Files to Update:
1. `android.py` - Android Messages
2. `whatsapp.py` - WhatsApp
3. `chatgpt.py` - ChatGPT
4. `facebook.py` - Facebook Messenger
5. `slack.py` - Slack
6. `teams.py` - Microsoft Teams
7. `msn.py` - MSN Messenger
8. `aol.py` - AOL Messenger
9. `generic.py` - Generic chat

#### Pattern to Apply:

**Import changes (add to each file):**
```python
from ...tokens.typography import FONT_SIZES, FONT_FAMILIES
from ...tokens.platform_colors import get_chat_color, CHAT_COLORS
from ...constants import MessageVariant
```

**Color method refactoring:**
```python
# Before:
def _get_bubble_color(self) -> RGBColor:
    if self.variant == "sent":
        return RGBColor(11, 87, 208)  # Hardcoded
    else:
        return RGBColor(231, 237, 243)  # Hardcoded

# After:
def _get_bubble_color(self) -> RGBColor:
    hex_color = get_chat_color("android", self.variant, "light")  # Platform name changes per file
    return RGBColor(*self.hex_to_rgb(hex_color))
```

**Font refactoring:**
```python
# Before:
p.font.name = "Roboto"  # or other hardcoded fonts
p.font.size = Pt(14)

# After:
p.font.name = FONT_FAMILIES["sans"][0]
p.font.size = Pt(FONT_SIZES["base"])  # or "lg", "sm" depending on usage
```

**Specific color replacements needed:**
- `android.py`: `RGBColor(11, 87, 208)` → `get_chat_color("android", ...)`
- `whatsapp.py`: `RGBColor(220, 248, 198)` → `get_chat_color("whatsapp", ...)`
- `chatgpt.py`: `RGBColor(247, 247, 248)`, `RGBColor(16, 163, 127)` → platform_colors
- `facebook.py`: `RGBColor(0, 132, 255)` → `get_chat_color("facebook", ...)`
- `slack.py`: `RGBColor(97, 31, 105)` → `CHAT_COLORS["slack"]["avatar"]`
- `teams.py`: `RGBColor(98, 100, 167)` → `CHAT_COLORS["teams"]["purple"]`

---

### 🔄 Container Components (5 files)

#### Files to Update:
1. `browser.py` - Browser chrome
2. `windows.py` - Windows window
3. `macos.py` - macOS window
4. `iphone.py` - iPhone device frame
5. `samsung.py` - Samsung device frame

#### Pattern to Apply:

**Import changes:**
```python
from ...tokens.typography import FONT_SIZES, FONT_FAMILIES
from ...tokens.platform_colors import get_browser_color, MACOS_CONTROLS, WINDOWS_CONTROLS, DEVICE_COLORS
from ...tokens.spacing import SPACING
from ...constants import BrowserType, ContainerPlatform
```

**Browser color refactoring (`browser.py`):**
```python
# Before:
RGBColor(50, 50, 50)  # Chrome dark
RGBColor(240, 240, 240)  # Chrome light

# After:
hex_color = get_browser_color("chrome", "chrome", theme_mode)
RGBColor(*self.hex_to_rgb(hex_color))
```

**Window controls refactoring:**
```python
# Before (macos.py):
RGBColor(255, 95, 86)  # Close button red

# After:
RGBColor(*self.hex_to_rgb(MACOS_CONTROLS["close"]))
```

```python
# Before (windows.py):
RGBColor(232, 17, 35)  # Windows red

# After:
RGBColor(*self.hex_to_rgb(WINDOWS_CONTROLS["close"]))
```

**Font size refactoring:**
```python
# Before:
p.font.size = Pt(9)
p.font.size = Pt(10)

# After:
p.font.size = Pt(FONT_SIZES["xs"])  # for 10pt
# Note: 9pt doesn't have direct mapping, closest is xs (10pt)
```

**Spacing refactoring:**
```python
# Before (iphone.py):
screen_margin = 0.08
notch_height = 0.15
status_bar_height = 0.25

# After:
# These are custom device-specific - consider adding to constants
# Or keep as-is if they're truly device-specific dimensions
```

---

### 🔄 Core Components (3 files) - Minor Spacing Updates

#### Files to Update:
1. `button.py` - Character width estimations
2. `card.py` - Dimension calculations
3. `badge.py` - Character width and padding

#### Pattern to Apply:

**Create spacing constants (add to `constants.py`):**
```python
class ComponentSizing:
    """Component sizing constants for width/height calculations."""

    # Character width estimations (in inches)
    CHAR_WIDTH_SM = 0.06
    CHAR_WIDTH_MD = 0.07
    CHAR_WIDTH_LG = 0.08

    # Base widths for components
    BUTTON_BASE_WIDTH_SM = 1.5
    BUTTON_BASE_WIDTH_MD = 2.0
    BUTTON_BASE_WIDTH_LG = 2.5

    BADGE_CHAR_WIDTH = 0.08
    BADGE_PADDING = 0.5

    # Line height estimations
    LINE_HEIGHT_INCHES = 0.35
    PARAGRAPH_GAP = 0.08
    TITLE_GAP = 0.22
```

**Refactor components:**
```python
# Before (button.py):
base_widths = {"sm": 1.5, "md": 2.0, "lg": 2.5}
char_widths = {"sm": 0.06, "md": 0.07, "lg": 0.08}

# After:
from ...constants import ComponentSizing
base_width = ComponentSizing.BUTTON_BASE_WIDTH_SM  # or MD, LG
char_width = ComponentSizing.CHAR_WIDTH_SM  # or MD, LG
```

---

## Testing Strategy

After all refactorings are complete:

1. **Run existing demos** to verify visual output matches
2. **Create test script** that instantiates each component with default values
3. **Visual regression testing** - Compare before/after screenshots
4. **Check for import errors** - Ensure all imports resolve correctly
5. **Verify type annotations** - Ensure Literal types work with new constants

---

## Benefits of These Refactorings

### 1. **Centralized Color Management**
- All platform colors in one file
- Easy to update brand colors when platforms change their design
- Consistent color usage across components

### 2. **Type Safety**
- Literal types prevent typos (e.g., can't use "recieved" instead of "received")
- Better IDE autocomplete
- Catch errors at type-check time

### 3. **Design System Consistency**
- All components use same font families and sizes
- Typography changes cascade automatically
- Easier to maintain brand consistency

### 4. **Future-Proofing**
- Easy to add new platforms (just add to platform_colors.py)
- Easy to add new themes (tokens already structured)
- Reduces code duplication

### 5. **Better Documentation**
- Constants serve as documentation
- Clear naming (FONT_SIZES["xs"] vs Pt(10))
- Type hints improve code readability

---

## Quick Reference: Common Replacements

| Before | After | Location |
|--------|-------|----------|
| `"Cascadia Code"` | `FONT_FAMILIES["mono"][0]` | typography.py |
| `"SF Pro Text"` | `FONT_FAMILIES["sans"][0]` | typography.py |
| `"Roboto"` | `FONT_FAMILIES["sans"][0]` | typography.py |
| `Pt(10)` | `Pt(FONT_SIZES["xs"])` | typography.py |
| `Pt(11)` | `Pt(FONT_SIZES["sm"])` | typography.py |
| `Pt(12)` | `Pt(FONT_SIZES["sm"])` | typography.py |
| `Pt(14)` | `Pt(FONT_SIZES["base"])` | typography.py |
| `Pt(15)` | `Pt(FONT_SIZES["lg"])` | typography.py |
| `Pt(16)` | `Pt(FONT_SIZES["lg"])` | typography.py |
| `RGBColor(11, 147, 246)` | `get_chat_color("ios", "sent", "light")` | platform_colors.py |
| `RGBColor(220, 248, 198)` | `get_chat_color("whatsapp", "sent", "light")` | platform_colors.py |
| `"#00ff00"` | `TERMINAL_COLORS["text"]` | platform_colors.py |
| `"sent"`, `"received"` | Type: `MessageVariant` | constants.py |
| `"chrome"`, `"safari"` | Type: `BrowserType` | constants.py |
| `"python"`, `"javascript"` | Type: `CodeLanguage` | constants.py |

---

## Files Modified

### Created:
- ✅ `src/chuk_mcp_pptx/tokens/platform_colors.py`

### Updated:
- ✅ `src/chuk_mcp_pptx/constants.py` (added enums)
- ✅ `src/chuk_mcp_pptx/components/code.py` (full refactor)
- ✅ `src/chuk_mcp_pptx/components/chat/ios.py` (full refactor)

### Pending:
- ⏳ `src/chuk_mcp_pptx/components/chat/android.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/whatsapp.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/chatgpt.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/facebook.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/slack.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/teams.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/msn.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/aol.py`
- ⏳ `src/chuk_mcp_pptx/components/chat/generic.py`
- ⏳ `src/chuk_mcp_pptx/components/containers/browser.py`
- ⏳ `src/chuk_mcp_pptx/components/containers/windows.py`
- ⏳ `src/chuk_mcp_pptx/components/containers/macos.py`
- ⏳ `src/chuk_mcp_pptx/components/containers/iphone.py`
- ⏳ `src/chuk_mcp_pptx/components/containers/samsung.py`
- ⏳ `src/chuk_mcp_pptx/components/core/button.py`
- ⏳ `src/chuk_mcp_pptx/components/core/card.py`
- ⏳ `src/chuk_mcp_pptx/components/core/badge.py`

**Total:** 3 completed, 18 pending
