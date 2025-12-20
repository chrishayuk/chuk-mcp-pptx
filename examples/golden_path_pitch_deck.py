#!/usr/bin/env python3
"""
Golden Path: 8-Slide Startup Pitch Deck

This example demonstrates the OPTIMAL workflow for generating professional
presentations using the chuk-mcp-pptx MCP tools.

The key insight: Use layouts that have OBJECT placeholders (Layout 1, 13-19)
for charts/tables, not Title-only layouts (Layout 4-6).

Run with:
    uv run python examples/golden_path_pitch_deck.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_mcp_pptx.core.presentation_manager import PresentationManager
from chuk_mcp_pptx.components.charts import ColumnChart, LineChart, PieChart, BarChart
from chuk_mcp_pptx.components.core import Table
from chuk_mcp_pptx.themes import ThemeManager


async def main():
    print("=" * 70)
    print("GOLDEN PATH: Simulating MCP Tool Workflow")
    print("=" * 70)

    # These managers are what the MCP tools use internally
    manager = PresentationManager()
    theme_manager = ThemeManager()
    theme = theme_manager.get_theme("dark-violet")

    # =========================================================================
    # STEP 1: pptx_create(name="pitch_deck", template_name="brand_proposal")
    # =========================================================================
    print("\n[1] pptx_create(name='pitch_deck', template_name='brand_proposal')")
    metadata = await manager.create(name="pitch_deck", template_name="brand_proposal")
    result = await manager.get(metadata.name)
    prs, _ = result
    print(f"    Created presentation with {len(prs.slide_layouts)} layouts")

    # =========================================================================
    # STEP 2: pptx_analyze_template("brand_proposal")
    # This is what the tool returns - layouts with placeholders
    # =========================================================================
    print("\n[2] pptx_analyze_template('brand_proposal')")
    print("    Layouts with OBJECT placeholders for charts/tables:")

    for idx in range(min(20, len(prs.slide_layouts))):
        layout = prs.slide_layouts[idx]
        placeholders = []
        for shape in layout.placeholders:
            ph = shape.placeholder_format
            placeholders.append(
                {"idx": ph.idx, "type": ph.type.name if hasattr(ph.type, "name") else str(ph.type)}
            )

        has_object = any("OBJECT" in p["type"] for p in placeholders)
        if has_object:
            print(f"      Layout {idx}: {layout.name}")
            print(f"        Placeholders: {[(p['idx'], p['type']) for p in placeholders]}")

    # Helper functions to simulate MCP tool behavior
    def get_placeholder(slide, idx):
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == idx:
                return shape
        return None

    def populate_text(slide, idx, text):
        ph = get_placeholder(slide, idx)
        if ph and hasattr(ph, "text_frame"):
            ph.text_frame.text = text
            return True
        return False

    def populate_component(slide, idx, component, theme):
        """Populate a placeholder with a component - this is what pptx_populate_placeholder does."""
        ph = get_placeholder(slide, idx)
        if not ph:
            return False

        # Extract bounds
        left = ph.left.inches
        top = ph.top.inches
        width = ph.width.inches
        height = ph.height.inches

        # Delete placeholder (the MCP tool does this via _delete_placeholder_if_needed)
        try:
            ph.element.getparent().remove(ph.element)
        except Exception:
            pass

        # Render component at placeholder bounds
        component.render(slide, left=left, top=top, width=width, height=height)
        return True

    # =========================================================================
    # Build slides using the MCP workflow
    # =========================================================================
    print("\n[3] Building slides...")

    # SLIDE 0: Title (Layout 0)
    print("\n  pptx_add_slide_from_template(layout_index=0)")
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    populate_text(slide, 0, "CheeseStack")
    populate_text(slide, 1, "The Future of Artisanal Cheese Discovery")
    print("    pptx_populate_placeholder(0, 'CheeseStack')")
    print("    pptx_populate_placeholder(1, 'The Future of...')")

    # SLIDE 1: Problem (Layout 1 - Content)
    print("\n  pptx_add_slide_from_template(layout_index=1)")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "The Problem")
    populate_text(
        slide,
        1,
        "Artisanal cheese lovers face three key challenges:\n\n• Discovery is fragmented\n• Quality verification is impossible\n• Logistics are expensive",
    )
    print("    pptx_populate_placeholder(0, 'The Problem')")
    print("    pptx_populate_placeholder(1, '...')")

    # SLIDE 2: Solution with TABLE (Layout 1 - Content, stacked, full-width OBJECT at idx 1)
    # Layout 1 has OBJECT at idx=1, size 11.3x4.3 - perfect for tables
    print("\n  pptx_add_slide_from_template(layout_index=1)  # Content - stacked layout")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "Our Solution: CheeseStack Platform")

    table = Table(
        headers=["Feature", "Description", "Benefit"],
        data=[
            ["AI Matching", "Taste profile algorithm", "Perfect recommendations"],
            ["Cold Chain", "Temperature-controlled", "Fresh delivery"],
            ["Subscriptions", "Curated monthly boxes", "Discover favorites"],
            ["Virtual Tastings", "Live sessions", "Learn from experts"],
        ],
        variant="striped",
        theme=theme,
    )
    populate_component(slide, 1, table, theme)  # Layout 1 has OBJECT at idx=1
    print("    pptx_populate_placeholder(1, {type: 'Table', ...})")
    print('    -> TABLE in full-width OBJECT placeholder (11.3" wide)')

    # SLIDE 3: Market with COLUMN CHART (Layout 1 - Content, stacked)
    print("\n  pptx_add_slide_from_template(layout_index=1)  # Content - stacked layout")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "Market Opportunity: $50B Specialty Cheese")

    chart = ColumnChart(
        categories=["2023", "2024", "2025", "2026", "2027"],
        series={
            "US ($B)": [12.5, 14.2, 16.1, 18.3, 20.8],
            "EU ($B)": [22.0, 23.5, 25.2, 27.0, 29.0],
        },
        title="Market Growth",
        variant="clustered",
        theme=theme,
    )
    populate_component(slide, 1, chart, theme)
    print("    pptx_populate_placeholder(1, {type: 'ColumnChart', ...})")
    print("    -> CHART below title, no overlap!")

    # SLIDE 4: Traction with LINE CHART (Layout 1 - Content, stacked)
    print("\n  pptx_add_slide_from_template(layout_index=1)  # Content - stacked layout")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "Traction: Strong Monthly Growth")

    chart = LineChart(
        categories=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        series={"MRR ($K)": [45, 52, 61, 73, 82, 95, 108, 125, 142, 165, 188, 210]},
        title="Monthly Recurring Revenue",
        variant="line",
        theme=theme,
    )
    populate_component(slide, 1, chart, theme)
    print("    pptx_populate_placeholder(1, {type: 'LineChart', ...})")

    # SLIDE 5: Business Model with PIE CHART (Layout 1 - Content, stacked)
    print("\n  pptx_add_slide_from_template(layout_index=1)  # Content - stacked layout")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "Business Model: Three Revenue Streams")

    chart = PieChart(
        categories=["Subscriptions (65%)", "Marketplace (25%)", "Experiences (10%)"],
        values=[65, 25, 10],
        title="Revenue Mix",
        theme=theme,
    )
    populate_component(slide, 1, chart, theme)
    print("    pptx_populate_placeholder(1, {type: 'PieChart', ...})")

    # SLIDE 6: Team with TABLE (Layout 1 - Content, stacked)
    print("\n  pptx_add_slide_from_template(layout_index=1)  # Content - stacked layout")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "World-Class Team")

    table = Table(
        headers=["Name", "Role", "Background"],
        data=[
            ["Sarah Chen", "CEO", "Former VP at Blue Apron"],
            ["Marcus Williams", "CTO", "Ex-Google Maps"],
            ["Jean-Pierre Dubois", "CCO", "Master Fromager"],
            ["Lisa Park", "VP Marketing", "Former CMO Grubhub"],
        ],
        variant="bordered",
        theme=theme,
    )
    populate_component(slide, 1, table, theme)
    print("    pptx_populate_placeholder(1, {type: 'Table', ...})")

    # SLIDE 7: The Ask with BAR CHART (Layout 1 - Content, stacked)
    print("\n  pptx_add_slide_from_template(layout_index=1)  # Content - stacked layout")
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    populate_text(slide, 0, "The Ask: $8M Series A")

    chart = BarChart(
        categories=["Engineering (40%)", "Growth (30%)", "Operations (20%)", "G&A (10%)"],
        series={"Allocation ($M)": [3.2, 2.4, 1.6, 0.8]},
        title="Use of Funds",
        variant="clustered",
        theme=theme,
    )
    populate_component(slide, 1, chart, theme)
    print("    pptx_populate_placeholder(1, {type: 'BarChart', ...})")

    # =========================================================================
    # STEP 4: pptx_save()
    # =========================================================================
    print("\n[4] pptx_save(path='output_pitch_deck.pptx')")
    output_path = Path(__file__).parent / "output_pitch_deck.pptx"
    prs.save(str(output_path))
    print(f"    Saved to: {output_path}")
    print(f"    Slides: {len(prs.slides)}")

    # =========================================================================
    # Summary
    # =========================================================================
    print("\n" + "=" * 70)
    print("GOLDEN PATH SUMMARY")
    print("=" * 70)
    print("""
KEY INSIGHT: Use STACKED layouts where OBJECT is BELOW the title!

GOOD: Layout 1 (Content) - STACKED
  - TITLE at top (idx=0): top=0.92, height=1.34
  - OBJECT below (idx=1): top=2.59, size=11.3x4.3 (full width!)
  - No overlap - chart sits cleanly below title

BAD: Layout 13-17 (Content 2-6) - SIDE-BY-SIDE
  - TITLE on LEFT, OBJECT on RIGHT
  - Both start at same top position
  - Charts overlap with title area

WORKFLOW:
1. pptx_analyze_template() - Find STACKED layouts (Layout 1, 18, 19)
2. pptx_add_slide_from_template(layout_index=1) - Use Content layout
3. pptx_populate_placeholder(placeholder_idx=1, content={type: "ColumnChart"})
   - Chart renders INTO the OBJECT placeholder BELOW the title
   - No overlap issues!
""")
    print(f"\nOpen: open {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
