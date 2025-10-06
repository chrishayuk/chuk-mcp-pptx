# Component Enhancement Plan

## Current State Analysis

### Existing Components
- ✅ `card.py` - Legacy card component
- ✅ `card_v2.py` - Enhanced with variants/composition ✨
- 🔄 `button.py` - Good structure, needs variant integration
- 🔄 `code.py` - Good features, needs variant integration
- 🔄 `chart.py` - Needs enhancement
- 📁 `charts/` - Multiple chart types, need enhancement

### Legacy Code to Clean
- `legacy_themes.py` - Can be deprecated
- `card.py` - Mark as deprecated, point to card_v2.py

---

## Enhancement Strategy

### Phase 1: Core UI Components
1. **Button** → `button_v2.py`
   - Add variant system (BUTTON_VARIANTS already exists!)
   - Add composition support for icon+text
   - Register with component registry
   - Add tests

2. **Badge** → `badge.py` (new)
   - Use BADGE_VARIANTS
   - Simple, focused component
   - Register and test

3. **Alert** → `alert.py` (new)
   - Variants: info, success, warning, error
   - Composition: Alert.Title, Alert.Description
   - Register and test

### Phase 2: Enhanced Existing
4. **Code/Terminal** → `code_v2.py`
   - Add variant system
   - Better syntax highlighting simulation
   - Theme integration

5. **Progress** → `progress.py` (new)
   - Progress bars and indicators
   - Variants: default, accent, success
   - Animated appearance options

### Phase 3: Data Components
6. **Table** → `table.py` (enhance existing)
   - Variant system for styling
   - Header/body composition
   - Sortable appearance

7. **Stat/Metric** → (already have MetricCard in card_v2)
   - May just document well

### Phase 4: Layout Components
8. **Container** → `container.py` (new)
   - Grid layout helper
   - Flex-like positioning
   - Responsive sizing

9. **Separator** → (already in composition.py)
   - May enhance with variants

10. **Accordion** → `accordion.py` (new)
    - Expandable sections
    - Composition pattern

---

## New Component Ideas

### High Priority
1. **Tabs** - Tab navigation component
2. **List** - Ordered/unordered lists with variants
3. **Timeline** - Event timeline visualization
4. **Callout/Quote** - Highlighted text blocks

### Medium Priority
5. **Avatar** - User avatar circles
6. **Input/Form** - Input field appearance (non-interactive)
7. **Toggle/Switch** - Toggle appearance
8. **Slider** - Slider appearance

### Future/Advanced
9. **Carousel** - Multi-slide indicator
10. **Dialog/Modal** - Dialog box appearance
11. **Tooltip** - Tooltip appearance
12. **Breadcrumb** - Navigation breadcrumbs

---

## Implementation Checklist Per Component

For each component:
- [ ] Create `{component}_v2.py` or new file
- [ ] Implement with variant system
- [ ] Add composition support where applicable
- [ ] Register in component registry
- [ ] Write comprehensive tests (20+ tests)
- [ ] Create usage examples
- [ ] Update documentation
- [ ] Add to main `__init__.py`

---

## Testing Requirements

Each component needs:
1. **Creation tests** - Basic instantiation
2. **Variant tests** - All variant combinations
3. **Size tests** - All size options
4. **Rendering tests** - Actual slide rendering
5. **Theme integration tests** - Works with all themes
6. **Composition tests** - If composable
7. **Edge case tests** - Empty, long text, etc.
8. **Registry tests** - Schema and discovery

Target: **20-30 tests per component**

---

## Documentation Requirements

Each component needs:
1. **Inline docstrings** - Complete API documentation
2. **Component registry entry** - Props, variants, examples
3. **Usage examples** - Real-world scenarios
4. **Migration guide** - If replacing legacy

---

## Proposed File Structure

```
src/chuk_mcp_pptx/components/
├── __init__.py                 # Component exports
├── base.py                     # ✅ Base component class
├── card.py                     # ⚠️ Legacy (deprecated)
├── card_v2.py                  # ✅ Enhanced card
├── button_v2.py                # 🆕 Enhanced button
├── badge.py                    # 🆕 New badge
├── alert.py                    # 🆕 New alert
├── code_v2.py                  # 🆕 Enhanced code
├── progress.py                 # 🆕 New progress
├── table_v2.py                 # 🆕 Enhanced table
├── container.py                # 🆕 New container
├── list.py                     # 🆕 New list
├── tabs.py                     # 🆕 New tabs
├── timeline.py                 # 🆕 New timeline
├── callout.py                  # 🆕 New callout
└── charts/                     # 📁 Chart components
    ├── __init__.py
    ├── base.py                 # ✅ Base chart
    └── ... (existing charts)
```

---

## Priority Order

### Sprint 1 (Immediate)
1. Button v2 - Most commonly used
2. Badge - Simple, high value
3. Alert - Common pattern

### Sprint 2
4. Code v2 - Enhance existing
5. Progress - New, useful
6. List - Common need

### Sprint 3
7. Table v2 - Complex but important
8. Tabs - Navigation
9. Timeline - Visualization

### Sprint 4
10. Callout - Content highlight
11. Container - Layout helper
12. Remaining charts enhancement

---

## Success Metrics

- **Test Coverage**: 250+ → 500+ tests
- **Components**: 5 → 20+ components
- **Documentation**: All components documented
- **Registry**: All components registered
- **Examples**: Each component has 2-3 examples
- **Legacy**: All legacy code marked/deprecated

---

## Next Steps

1. Start with Button v2
2. Create comprehensive tests
3. Document and register
4. Create examples
5. Repeat for Badge and Alert
6. Review and iterate
