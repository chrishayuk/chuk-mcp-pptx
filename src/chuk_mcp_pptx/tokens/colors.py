# src/chuk_mcp_pptx/tokens/colors.py
"""
Design tokens for colors - the foundation of our theme system.
Similar to CSS variables in shadcn/ui.
"""

from typing import Dict, Any

# Base color palette - raw colors that themes can reference
PALETTE = {
    # Neutrals
    "slate": {
        50: "#f8fafc",
        100: "#f1f5f9",
        200: "#e2e8f0",
        300: "#cbd5e1",
        400: "#94a3b8",
        500: "#64748b",
        600: "#475569",
        700: "#334155",
        800: "#1e293b",
        900: "#0f172a",
        950: "#020617",
    },
    "zinc": {
        50: "#fafafa",
        100: "#f4f4f5",
        200: "#e4e4e7",
        300: "#d4d4d8",
        400: "#a1a1aa",
        500: "#71717a",
        600: "#52525b",
        700: "#3f3f46",
        800: "#27272a",
        900: "#18181b",
        950: "#09090b",
    },
    # Colors
    "red": {
        50: "#fef2f2",
        100: "#fee2e2",
        200: "#fecaca",
        300: "#fca5a5",
        400: "#f87171",
        500: "#ef4444",
        600: "#dc2626",
        700: "#b91c1c",
        800: "#991b1b",
        900: "#7f1d1d",
        950: "#450a0a",
    },
    "orange": {
        50: "#fff7ed",
        100: "#ffedd5",
        200: "#fed7aa",
        300: "#fdba74",
        400: "#fb923c",
        500: "#f97316",
        600: "#ea580c",
        700: "#c2410c",
        800: "#9a3412",
        900: "#7c2d12",
        950: "#431407",
    },
    "amber": {
        50: "#fffbeb",
        100: "#fef3c7",
        200: "#fde68a",
        300: "#fcd34d",
        400: "#fbbf24",
        500: "#f59e0b",
        600: "#d97706",
        700: "#b45309",
        800: "#92400e",
        900: "#78350f",
        950: "#451a03",
    },
    "yellow": {
        50: "#fefce8",
        100: "#fef9c3",
        200: "#fef08a",
        300: "#fde047",
        400: "#facc15",
        500: "#eab308",
        600: "#ca8a04",
        700: "#a16207",
        800: "#854d0e",
        900: "#713f12",
        950: "#422006",
    },
    "lime": {
        50: "#f7fee7",
        100: "#ecfccb",
        200: "#d9f99d",
        300: "#bef264",
        400: "#a3e635",
        500: "#84cc16",
        600: "#65a30d",
        700: "#4d7c0f",
        800: "#3f6212",
        900: "#365314",
        950: "#1a2e05",
    },
    "green": {
        50: "#f0fdf4",
        100: "#dcfce7",
        200: "#bbf7d0",
        300: "#86efac",
        400: "#4ade80",
        500: "#22c55e",
        600: "#16a34a",
        700: "#15803d",
        800: "#166534",
        900: "#14532d",
        950: "#052e16",
    },
    "emerald": {
        50: "#ecfdf5",
        100: "#d1fae5",
        200: "#a7f3d0",
        300: "#6ee7b7",
        400: "#34d399",
        500: "#10b981",
        600: "#059669",
        700: "#047857",
        800: "#065f46",
        900: "#064e3b",
        950: "#022c22",
    },
    "teal": {
        50: "#f0fdfa",
        100: "#ccfbf1",
        200: "#99f6e4",
        300: "#5eead4",
        400: "#2dd4bf",
        500: "#14b8a6",
        600: "#0d9488",
        700: "#0f766e",
        800: "#115e59",
        900: "#134e4a",
        950: "#042f2e",
    },
    "cyan": {
        50: "#ecfeff",
        100: "#cffafe",
        200: "#a5f3fc",
        300: "#67e8f9",
        400: "#22d3ee",
        500: "#06b6d4",
        600: "#0891b2",
        700: "#0e7490",
        800: "#155e75",
        900: "#164e63",
        950: "#083344",
    },
    "sky": {
        50: "#f0f9ff",
        100: "#e0f2fe",
        200: "#bae6fd",
        300: "#7dd3fc",
        400: "#38bdf8",
        500: "#0ea5e9",
        600: "#0284c7",
        700: "#0369a1",
        800: "#075985",
        900: "#0c4a6e",
        950: "#082f49",
    },
    "blue": {
        50: "#eff6ff",
        100: "#dbeafe",
        200: "#bfdbfe",
        300: "#93c5fd",
        400: "#60a5fa",
        500: "#3b82f6",
        600: "#2563eb",
        700: "#1d4ed8",
        800: "#1e40af",
        900: "#1e3a8a",
        950: "#172554",
    },
    "indigo": {
        50: "#eef2ff",
        100: "#e0e7ff",
        200: "#c7d2fe",
        300: "#a5b4fc",
        400: "#818cf8",
        500: "#6366f1",
        600: "#4f46e5",
        700: "#4338ca",
        800: "#3730a3",
        900: "#312e81",
        950: "#1e1b4b",
    },
    "violet": {
        50: "#f5f3ff",
        100: "#ede9fe",
        200: "#ddd6fe",
        300: "#c4b5fd",
        400: "#a78bfa",
        500: "#8b5cf6",
        600: "#7c3aed",
        700: "#6d28d9",
        800: "#5b21b6",
        900: "#4c1d95",
        950: "#2e1065",
    },
    "purple": {
        50: "#faf5ff",
        100: "#f3e8ff",
        200: "#e9d5ff",
        300: "#d8b4fe",
        400: "#c084fc",
        500: "#a855f7",
        600: "#9333ea",
        700: "#7e22ce",
        800: "#6b21a8",
        900: "#581c87",
        950: "#3b0764",
    },
    "fuchsia": {
        50: "#fdf4ff",
        100: "#fae8ff",
        200: "#f5d0fe",
        300: "#f0abfc",
        400: "#e879f9",
        500: "#d946ef",
        600: "#c026d3",
        700: "#a21caf",
        800: "#86198f",
        900: "#701a75",
        950: "#4a044e",
    },
    "pink": {
        50: "#fdf2f8",
        100: "#fce7f3",
        200: "#fbcfe8",
        300: "#f9a8d4",
        400: "#f472b6",
        500: "#ec4899",
        600: "#db2777",
        700: "#be185d",
        800: "#9f1239",
        900: "#831843",
        950: "#500724",
    },
    "rose": {
        50: "#fff1f2",
        100: "#ffe4e6",
        200: "#fecdd3",
        300: "#fda4af",
        400: "#fb7185",
        500: "#f43f5e",
        600: "#e11d48",
        700: "#be123c",
        800: "#9f1239",
        900: "#881337",
        950: "#4c0519",
    },
}


# Semantic token definitions
def get_semantic_tokens(primary_hue: str = "blue", mode: str = "dark") -> Dict[str, Any]:
    """
    Get semantic color tokens based on primary hue and mode.

    Args:
        primary_hue: Primary color from palette (e.g., "blue", "violet")
        mode: "dark" or "light"

    Returns:
        Dictionary of semantic color tokens
    """
    is_dark = mode == "dark"

    return {
        # Background tokens
        "background": {
            "DEFAULT": PALETTE["zinc"][950] if is_dark else "#ffffff",
            "secondary": PALETTE["zinc"][900] if is_dark else PALETTE["zinc"][50],
            "tertiary": PALETTE["zinc"][800] if is_dark else PALETTE["zinc"][100],
        },
        # Foreground tokens
        "foreground": {
            "DEFAULT": PALETTE["zinc"][50] if is_dark else PALETTE["zinc"][900],
            "secondary": PALETTE["zinc"][200] if is_dark else PALETTE["zinc"][700],
            "muted": PALETTE["zinc"][400] if is_dark else PALETTE["zinc"][500],
        },
        # Primary colors
        "primary": {
            "DEFAULT": PALETTE[primary_hue][500 if is_dark else 600],
            "foreground": "#ffffff" if is_dark else "#ffffff",
            "hover": PALETTE[primary_hue][400 if is_dark else 700],
            "active": PALETTE[primary_hue][300 if is_dark else 800],
        },
        # Secondary colors
        "secondary": {
            "DEFAULT": PALETTE["zinc"][800 if is_dark else 200],
            "foreground": PALETTE["zinc"][50 if is_dark else 900],
            "hover": PALETTE["zinc"][700 if is_dark else 300],
            "active": PALETTE["zinc"][600 if is_dark else 400],
        },
        # Accent colors
        "accent": {
            "DEFAULT": PALETTE[primary_hue][400 if is_dark else 500],
            "foreground": PALETTE["zinc"][950] if is_dark else "#ffffff",
            "hover": PALETTE[primary_hue][300 if is_dark else 600],
            "active": PALETTE[primary_hue][200 if is_dark else 700],
        },
        # Muted colors
        "muted": {
            "DEFAULT": PALETTE["zinc"][800 if is_dark else 100],
            "foreground": PALETTE["zinc"][400 if is_dark else 600],
        },
        # Card colors
        "card": {
            "DEFAULT": PALETTE["zinc"][900 if is_dark else 50],
            "foreground": PALETTE["zinc"][50 if is_dark else 900],
            "hover": PALETTE["zinc"][800 if is_dark else 100],
        },
        # Border colors
        "border": {
            "DEFAULT": PALETTE["zinc"][800 if is_dark else 200],
            "secondary": PALETTE["zinc"][700 if is_dark else 300],
        },
        # Status colors
        "destructive": {
            "DEFAULT": PALETTE["red"][600 if is_dark else 500],
            "foreground": "#ffffff",
        },
        "success": {
            "DEFAULT": PALETTE["green"][600 if is_dark else 500],
            "foreground": "#ffffff",
        },
        "warning": {
            "DEFAULT": PALETTE["amber"][600 if is_dark else 500],
            "foreground": PALETTE["zinc"][950],
        },
        "info": {
            "DEFAULT": PALETTE["blue"][600 if is_dark else 500],
            "foreground": "#ffffff",
        },
        # Chart colors (for data visualization)
        "chart": [
            PALETTE[primary_hue][500],
            PALETTE["cyan"][500],
            PALETTE["violet"][500],
            PALETTE["emerald"][500],
            PALETTE["orange"][500],
            PALETTE["pink"][500],
            PALETTE["yellow"][500],
            PALETTE["indigo"][500],
        ],
    }


# Gradient definitions
GRADIENTS = {
    "sunset": [PALETTE["red"][500], PALETTE["amber"][500], PALETTE["violet"][700]],
    "ocean": [PALETTE["blue"][500], PALETTE["purple"][500], PALETTE["pink"][300]],
    "forest": [PALETTE["teal"][500], PALETTE["lime"][500], PALETTE["yellow"][400]],
    "flame": [PALETTE["rose"][500], PALETTE["red"][500], PALETTE["amber"][400]],
    "aurora": [PALETTE["cyan"][400], PALETTE["green"][300], PALETTE["fuchsia"][500]],
    "cosmic": [PALETTE["purple"][700], PALETTE["fuchsia"][500], PALETTE["slate"][950]],
    "mint": [PALETTE["cyan"][500], PALETTE["blue"][700], PALETTE["indigo"][900]],
    "lavender": [PALETTE["purple"][300], PALETTE["purple"][500], PALETTE["purple"][800]],
}

# Utility color definitions for common UI patterns
UTILITY_COLORS = {
    # Chart default colors (colorful and distinct)
    "chart_defaults": [
        PALETTE["blue"][500],
        PALETTE["green"][500],
        PALETTE["orange"][500],
        PALETTE["violet"][500],
        PALETTE["pink"][500],
        PALETTE["cyan"][500],
        PALETTE["yellow"][500],
        PALETTE["red"][500],
    ],
    # Table colors
    "table": {
        "header": PALETTE["slate"][200],
        "header_text": PALETTE["slate"][900],
        "row_even": PALETTE["slate"][50],
        "row_odd": PALETTE["slate"][100],
        "row_text": PALETTE["slate"][900],
        "border": PALETTE["slate"][300],
    },
    # Status/feedback colors
    "status": {
        "success": PALETTE["green"][500],
        "success_light": PALETTE["green"][100],
        "warning": PALETTE["yellow"][500],
        "warning_light": PALETTE["yellow"][100],
        "error": PALETTE["red"][500],
        "error_light": PALETTE["red"][100],
        "info": PALETTE["blue"][500],
        "info_light": PALETTE["blue"][100],
    },
    # Device/platform specific colors
    "device": {
        "phantom_black": PALETTE["slate"][900],
        "phantom_white": PALETTE["slate"][50],
        "screen_dark": PALETTE["slate"][950],
        "button_dark": PALETTE["slate"][700],
        "button_darker": PALETTE["slate"][800],
    },
}
