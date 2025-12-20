# Golden Path Prompts for chuk-mcp-pptx

These canonical prompts demonstrate the optimal workflow for generating professional presentations. Use these as examples in demos, videos, and documentation.

---

## The Template-First Workflow

Every successful presentation generation follows this pattern:

```
1. Discover → 2. Analyze → 3. Build → 4. Verify → 5. Save
```

The key insight: **Templates have 20-50+ layouts**. Using variety creates engaging presentations.

---

## Demo 1: Startup Pitch Deck (8 slides)

### The Prompt

```
Create an 8-slide pitch deck for "CheeseStack" - a marketplace connecting
artisanal cheese lovers with small-batch producers.

Include:
1. Title slide with company name and tagline
2. Problem statement (fragmented discovery, quality verification, logistics)
3. Solution overview (AI matching, cold chain, subscriptions)
4. Market opportunity with chart showing $50B specialty cheese market growth
5. Traction metrics (ARR, subscribers, retention)
6. Business model (subscriptions, marketplace commission, experiences)
7. Team slide with leadership and advisors
8. The ask - $8M Series A with use of funds

Use the brand_proposal template and apply the dark-violet theme.
```

### Expected Tool-Call Sequence

```python
# Step 1: Discover templates
pptx_list_templates()

# Step 2: Create from template
pptx_create(name="cheesestack_pitch", template_name="brand_proposal")

# Step 3: CRITICAL - Analyze template to see all 55 layouts
pptx_analyze_template("brand_proposal")
# → Returns layouts like: "Title Slide" (0), "Title and Content" (1),
#   "Two Content" (3), "Comparison" (4), "Title Only" (5), etc.

# Step 4: Build slides with variety
# Slide 0: Title
pptx_add_slide_from_template(layout_index=0)
pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="CheeseStack")
pptx_populate_placeholder(slide_index=0, placeholder_idx=1, content="The Future of Artisanal Cheese Discovery")
pptx_list_slide_components(slide_index=0)  # VERIFY

# Slide 1: Problem (Title + Content layout)
pptx_add_slide_from_template(layout_index=1)
pptx_populate_placeholder(slide_index=1, placeholder_idx=0, content="The Problem")
pptx_populate_placeholder(slide_index=1, placeholder_idx=1, content="Three key challenges...")
pptx_list_slide_components(slide_index=1)  # VERIFY

# Slide 2: Solution
pptx_add_slide_from_template(layout_index=1)
# ... populate placeholders ...

# Slide 3: Market (with chart)
pptx_add_slide_from_template(layout_index=5)  # Title Only
pptx_populate_placeholder(slide_index=3, placeholder_idx=0, content="Market Opportunity")
# Add chart to content area
pptx_add_component(
    slide_index=3,
    component="ColumnChart",
    left=1.0, top=1.8, width=8.0, height=4.5,  # Free-form OK for Title Only layout
    params={
        "categories": ["2023", "2024", "2025", "2026", "2027"],
        "series": {
            "US Market": [12.5, 14.2, 16.1, 18.3, 20.8],
            "EU Market": [22.0, 23.5, 25.2, 27.0, 29.0]
        },
        "title": "Specialty Cheese Market ($B)"
    }
)
pptx_list_slide_components(slide_index=3)

# Slide 4: Traction (Two Content layout - side by side)
pptx_add_slide_from_template(layout_index=3)  # Two Content
pptx_populate_placeholder(slide_index=4, placeholder_idx=0, content="Traction")
pptx_populate_placeholder(slide_index=4, placeholder_idx=1, content="Key Metrics:\n- $1.2M ARR\n- 15K subscribers")
pptx_populate_placeholder(slide_index=4, placeholder_idx=2, content="Milestones:\n- Featured in Food & Wine\n- Series A oversubscribed")
pptx_list_slide_components(slide_index=4)

# Continue for remaining slides...

# Step 5: Apply theme
pptx_apply_theme(theme="dark-violet")

# Step 6: Save
pptx_save(path="cheesestack_pitch.pptx")
```

---

## Demo 2: Quarterly Business Review (10 slides)

### The Prompt

```
Create a Q3 2024 quarterly business review for "Acme Corp" with:

1. Title slide with quarter and company name
2. Executive summary (3 key highlights)
3. Revenue performance with line chart (Q1-Q4 actual vs forecast)
4. Customer metrics with table (new, churned, net, NPS by segment)
5. Product updates (shipped features vs roadmap)
6. Competitive landscape comparison
7. Challenges and risks
8. Q4 priorities
9. Team updates and hiring
10. Q&A / Discussion slide

Use corporate styling with a professional color theme.
```

### Expected Tool-Call Sequence

```python
# Setup
pptx_create(name="q3_qbr", template_name="brand_proposal")
pptx_analyze_template("brand_proposal")

# Title
pptx_add_slide_from_template(layout_index=0)
pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="Q3 2024 Business Review")
pptx_populate_placeholder(slide_index=0, placeholder_idx=1, content="Acme Corp | October 2024")

# Executive Summary
pptx_add_slide_from_template(layout_index=1)
pptx_populate_placeholder(slide_index=1, placeholder_idx=0, content="Executive Summary")
pptx_populate_placeholder(slide_index=1, placeholder_idx=1,
    content="1. Revenue up 23% YoY, exceeding forecast\n2. Customer NPS improved to 72 (+8)\n3. Launched 3 major product features")

# Revenue with Chart
pptx_add_slide_from_template(layout_index=5)  # Layout with chart placeholder
pptx_populate_placeholder(slide_index=2, placeholder_idx=0, content="Revenue Performance")
# If layout has CHART placeholder at idx 2:
pptx_populate_placeholder(slide_index=2, placeholder_idx=2, content={
    "type": "LineChart",
    "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": {
        "Actual": [2.1, 2.4, 2.8, None],
        "Forecast": [2.0, 2.3, 2.6, 3.0]
    },
    "title": "Revenue ($M)"
})
pptx_list_slide_components(slide_index=2)

# Customer Metrics with Table
pptx_add_slide_from_template(layout_index=1)
pptx_populate_placeholder(slide_index=3, placeholder_idx=0, content="Customer Metrics")
# Add table via component
pptx_add_component(
    slide_index=3,
    component="Table",
    left=0.5, top=1.5, width=9.0, height=3.0,
    params={
        "headers": ["Segment", "New", "Churned", "Net", "NPS"],
        "data": [
            ["Enterprise", "12", "2", "+10", "78"],
            ["Mid-Market", "45", "8", "+37", "71"],
            ["SMB", "156", "24", "+132", "68"]
        ],
        "variant": "striped"
    }
)

# Comparison slide for competitive landscape
pptx_add_slide_from_template(layout_index=4)  # Comparison layout
pptx_populate_placeholder(slide_index=5, placeholder_idx=0, content="Competitive Landscape")
pptx_populate_placeholder(slide_index=5, placeholder_idx=1, content="Our Strengths:\n- Best-in-class UX\n- Enterprise security\n- 24/7 support")
pptx_populate_placeholder(slide_index=5, placeholder_idx=2, content="Competitor Focus:\n- Lower pricing\n- More integrations\n- Faster releases")

# ... continue for remaining slides ...

pptx_save(path="q3_qbr_acme.pptx")
```

---

## Demo 3: Technical Tutorial (6 slides)

### The Prompt

```
Create a technical tutorial presentation on "Building REST APIs with FastAPI":

1. Title slide with topic and speaker info
2. What is FastAPI? (overview with key features)
3. Code example: Basic endpoint (show Python code)
4. Code example: Request validation with Pydantic
5. Architecture diagram (conceptual - placeholder for diagram)
6. Resources and next steps

Keep it clean and developer-focused.
```

### Expected Tool-Call Sequence

```python
pptx_create(name="fastapi_tutorial", template_name="tech")
pptx_analyze_template("tech")

# Title
pptx_add_slide_from_template(layout_index=0)
pptx_populate_placeholder(slide_index=0, placeholder_idx=0, content="Building REST APIs with FastAPI")
pptx_populate_placeholder(slide_index=0, placeholder_idx=1, content="A Practical Tutorial | @yourhandle")

# Overview
pptx_add_slide_from_template(layout_index=1)
pptx_populate_placeholder(slide_index=1, placeholder_idx=0, content="What is FastAPI?")
pptx_populate_placeholder(slide_index=1, placeholder_idx=1,
    content="Modern, fast Python web framework:\n- Automatic OpenAPI documentation\n- Type hints for validation\n- Async support out of the box\n- Comparable performance to Node.js/Go")

# Code Example 1
pptx_add_slide_from_template(layout_index=5)  # Title only for code
pptx_populate_placeholder(slide_index=2, placeholder_idx=0, content="Basic Endpoint")
pptx_add_component(
    slide_index=2,
    component="Text",
    left=0.5, top=1.5, width=9.0, height=4.0,
    params={
        "text": """from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}""",
        "font_family": "Consolas",
        "font_size": 18,
        "bg_color": "#1e1e1e",
        "text_color": "#d4d4d4"
    }
)

# Code Example 2
pptx_add_slide_from_template(layout_index=5)
pptx_populate_placeholder(slide_index=3, placeholder_idx=0, content="Request Validation")
pptx_add_component(
    slide_index=3,
    component="Text",
    left=0.5, top=1.5, width=9.0, height=4.0,
    params={
        "text": """from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
async def create_item(item: Item):
    return item""",
        "font_family": "Consolas",
        "font_size": 18,
        "bg_color": "#1e1e1e",
        "text_color": "#d4d4d4"
    }
)

# Architecture (placeholder for diagram)
pptx_add_slide_from_template(layout_index=6)  # Blank for custom layout
pptx_add_component(
    slide_index=4,
    component="Text",
    left=3.5, top=0.5, width=3.0, height=0.5,
    params={"text": "Architecture Overview", "font_size": 24, "bold": True}
)
# Add boxes for architecture diagram
pptx_add_component(slide_index=4, component="Shape", left=1.0, top=2.0, width=2.0, height=1.0,
    params={"shape_type": "rectangle", "text": "Client", "bg_color": "#3b82f6"})
pptx_add_component(slide_index=4, component="Shape", left=4.0, top=2.0, width=2.0, height=1.0,
    params={"shape_type": "rectangle", "text": "FastAPI", "bg_color": "#10b981"})
pptx_add_component(slide_index=4, component="Shape", left=7.0, top=2.0, width=2.0, height=1.0,
    params={"shape_type": "rectangle", "text": "Database", "bg_color": "#8b5cf6"})

# Resources
pptx_add_slide_from_template(layout_index=1)
pptx_populate_placeholder(slide_index=5, placeholder_idx=0, content="Resources & Next Steps")
pptx_populate_placeholder(slide_index=5, placeholder_idx=1,
    content="Documentation: fastapi.tiangolo.com\nTutorial repo: github.com/user/fastapi-demo\nCommunity: discord.gg/fastapi\n\nNext: Authentication, Database integration, Deployment")

pptx_save(path="fastapi_tutorial.pptx")
```

---

## Common Mistakes to Avoid

### 1. Skipping Template Analysis

```python
# WRONG - Jumping straight to slides without knowing layouts
pptx_create(name="deck", template_name="brand_proposal")
pptx_add_slide_from_template(layout_index=0)  # Only using layout 0

# RIGHT - Analyze first, then choose variety
pptx_create(name="deck", template_name="brand_proposal")
pptx_analyze_template("brand_proposal")  # See all 55 layouts!
# Now choose appropriate layouts: 0, 1, 3, 4, 5 for variety
```

### 2. Free-Form Positioning with Template Placeholders

```python
# WRONG - Creates overlay, placeholder "Click to add" still visible
pptx_add_slide_from_template(layout_index=40)  # Has CHART placeholder at idx 2
pptx_add_component(
    slide_index=5,
    component="ColumnChart",
    left=1.0, top=2.0, width=8.0, height=4.0,  # BAD!
    params={...}
)

# RIGHT - Use target_placeholder
pptx_add_slide_from_template(layout_index=40)
pptx_add_component(
    slide_index=5,
    component="ColumnChart",
    target_placeholder=2,  # GOOD!
    params={...}
)

# OR use pptx_populate_placeholder (simpler)
pptx_populate_placeholder(
    slide_index=5,
    placeholder_idx=2,
    content={"type": "ColumnChart", "series": {...}, "categories": [...]}
)
```

### 3. Skipping Verification

```python
# WRONG - Never verified, might have empty placeholders
pptx_add_slide_from_template(layout_index=3)
pptx_populate_placeholder(slide_index=4, placeholder_idx=0, content="Title")
# Forgot placeholder 1 and 2!

# RIGHT - Always verify
pptx_add_slide_from_template(layout_index=3)
pptx_populate_placeholder(slide_index=4, placeholder_idx=0, content="Title")
pptx_populate_placeholder(slide_index=4, placeholder_idx=1, content="Left content")
pptx_populate_placeholder(slide_index=4, placeholder_idx=2, content="Right content")
pptx_list_slide_components(slide_index=4)  # Check validation_passed=true
```

### 4. Repeating Same Layout

```python
# WRONG - Boring, wastes template variety
pptx_add_slide_from_template(layout_index=1)  # Title + Content
pptx_add_slide_from_template(layout_index=1)  # Title + Content again
pptx_add_slide_from_template(layout_index=1)  # Title + Content again
pptx_add_slide_from_template(layout_index=1)  # Title + Content again

# RIGHT - Use variety for engagement
pptx_add_slide_from_template(layout_index=0)  # Title slide
pptx_add_slide_from_template(layout_index=1)  # Title + Content
pptx_add_slide_from_template(layout_index=3)  # Two Content (side by side)
pptx_add_slide_from_template(layout_index=4)  # Comparison
pptx_add_slide_from_template(layout_index=5)  # Title Only (for charts/diagrams)
```

---

## Quick Reference: Layout Selection Guide

| Content Type | Recommended Layout | Notes |
|--------------|-------------------|-------|
| Title/Opening | Layout 0 (Title Slide) | Company name, tagline |
| Single topic | Layout 1 (Title + Content) | Most common |
| Side-by-side | Layout 3 (Two Content) | Comparison, pros/cons |
| Before/After | Layout 4 (Comparison) | Explicit comparison headers |
| Chart/Diagram | Layout 5 (Title Only) | Full space for visuals |
| Custom layout | Layout 6 (Blank) | Complete control |
| Quote | Look for Quote layout | Often index 10-20 |
| Section divider | Look for Section Header | Often index 2 |

---

## The One-Liner Summary

> **Analyze template first, choose layout variety, use target_placeholder for content, always verify with pptx_list_slide_components.**
