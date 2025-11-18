# src/chuk_mcp_pptx/tokens/platform_colors.py
"""
Platform-specific brand colors for chat, container, and application UI components.
These colors represent authentic brand identities for platforms like iOS, Android, WhatsApp, etc.
"""

# Chat Platform Colors
CHAT_COLORS = {
    "ios": {
        "sent": "#0B93F6",  # iOS Messages blue
        "received": "#E8E8ED",  # iOS Messages gray
        "text_sent": "#FFFFFF",
        "text_received": "#000000",
    },
    "android": {
        "sent": "#0B57D0",  # Material Design RCS blue
        "received": "#E7EDF3",  # Material Design light gray
        "text_sent": "#FFFFFF",
        "text_received": "#202124",
        "timestamp": "#5F6368",  # Material medium gray
    },
    "whatsapp": {
        "sent": "#DCF8C6",  # WhatsApp green (light)
        "received": "#FFFFFF",
        "background": "#ECE5DD",  # WhatsApp chat background
        "text": "#000000",
    },
    "chatgpt": {
        "user": "#F7F7F8",  # ChatGPT user message
        "assistant": "#FFFFFF",  # ChatGPT assistant message
        "system": "#ECECF1",  # ChatGPT system message
        "text": "#343541",  # ChatGPT dark text
        "avatar": "#10A37F",  # ChatGPT green
    },
    "slack": {
        "background": "#FFFFFF",
        "hover": "#F8F8F8",
        "avatar": "#611F69",  # Slack purple
        "text": "#1D1C1D",  # Slack dark text
        "secondary_text": "#616061",  # Slack medium gray
        "link": "#1D9BD1",  # Slack blue
    },
    "teams": {
        "purple": "#6264A7",  # Microsoft Teams purple
        "text": "#252423",  # Teams dark gray
        "secondary_text": "#605E5C",  # Teams medium gray
        "background": "#FFFFFF",
    },
    "facebook": {
        "sent": "#0084FF",  # Facebook Messenger blue
        "received": "#E4E6EB",  # Facebook gray
        "text": "#000000",
    },
    "msn": {
        "header": "#0078D7",  # MSN/Windows blue
        "sent": "#CCE4FF",  # MSN light blue
        "received": "#E8E8E8",  # MSN gray
    },
    "aol": {
        "header": "#FFCC00",  # AOL yellow
        "sent": "#FFFFCC",  # AOL light yellow
        "received": "#E8E8E8",
    },
    "generic": {
        "sent": "#007AFF",  # Generic blue
        "received": "#E5E5EA",  # Generic gray
        "text": "#000000",
    },
}

# Browser Chrome Colors
BROWSER_COLORS = {
    "chrome": {
        "light": {
            "chrome": "#F0F0F0",
            "text": "#323232",
            "border": "#DADCE0",
        },
        "dark": {
            "chrome": "#323232",
            "text": "#E8EAED",
            "border": "#5F6368",
        },
    },
    "safari": {
        "light": {
            "chrome": "#F5F5F5",
            "text": "#000000",
            "border": "#D1D1D6",
        },
        "dark": {
            "chrome": "#2C2C2C",
            "text": "#FFFFFF",
            "border": "#48484A",
        },
    },
    "firefox": {
        "light": {
            "chrome": "#F0F0F4",
            "text": "#15141A",
            "border": "#CFCFD8",
        },
        "dark": {
            "chrome": "#2B2A33",
            "text": "#FBFBFE",
            "border": "#52525E",
        },
    },
}

# macOS Window Controls (traffic lights)
MACOS_CONTROLS = {
    "close": "#FF5F56",
    "minimize": "#FFBD2E",
    "maximize": "#28C940",
}

# Windows Window Controls
WINDOWS_CONTROLS = {
    "close": "#E81123",
    "minimize": "#000000",
    "maximize": "#000000",
}

# Terminal Colors
TERMINAL_COLORS = {
    "background": "#1E1E1E",  # VS Code dark background
    "text": "#00FF00",  # Classic terminal green
    "border": "#00FF00",
    "prompt": "#00FF00",
}

# Device Bezel/Frame Colors
DEVICE_COLORS = {
    "iphone": {
        "bezel": "#1C1C1E",  # iPhone Pro graphite
        "screen": "#000000",
    },
    "samsung": {
        "bezel": "#2C2C2E",  # Samsung phantom black
        "screen": "#000000",
    },
}

# Code Language Brand Colors
LANGUAGE_COLORS = {
    "python": "#3776AB",
    "javascript": "#F7DF1E",
    "typescript": "#3178C6",
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
    "text": "#666666",  # Default fallback
}


# Container UI Colors (OS-specific window chrome)
# These colors represent actual OS UI elements in light/dark modes
CONTAINER_UI_COLORS = {
    "macos": {
        "light": {
            "titlebar": "#ECECEC",
            "text": "#000000",
            "content_bg": "#FFFFFF",
            "toolbar": "#F6F6F6",
            "border": "#B4B4B4",
        },
        "dark": {
            "titlebar": "#323232",
            "text": "#FFFFFF",
            "content_bg": "#FFFFFF",
            "toolbar": "#3C3C3C",
            "border": "#B4B4B4",
        },
    },
    "windows": {
        "light": {
            "titlebar": "#FFFFFF",
            "text": "#000000",
            "menubar": "#F0F0F0",
            "border": "#B4B4B4",
        },
        "dark": {
            "titlebar": "#202020",
            "text": "#FFFFFF",
            "menubar": "#1E1E1E",
            "border": "#B4B4B4",
        },
    },
    "browser": {
        "light": {
            "text": "#000000",
            "addressbar": "#FFFFFF",
            "placeholder": "#B4B4B4",
            "border": "#B4B4B4",
        },
        "dark": {
            "text": "#FFFFFF",
            "addressbar": "#464646",
            "placeholder": "#B4B4B4",
            "border": "#B4B4B4",
        },
    },
    "generic": {
        "light": {
            "header_bg": "#DCDCDC",
            "header_text": "#000000",
            "titlebar_bg": "#F5F5F5",
            "content_bg": "#FFFFFF",
            "border": "#B4B4B4",
        },
        "dark": {
            "header_bg": "#3C3C3C",
            "header_text": "#FFFFFF",
            "titlebar_bg": "#323232",
            "content_bg": "#FFFFFF",
            "border": "#B4B4B4",
        },
    },
}


def get_chat_color(platform: str, variant: str, theme: str = "light") -> str:
    """
    Get brand-accurate chat bubble color for a platform.

    Args:
        platform: Chat platform (e.g., "ios", "android", "whatsapp")
        variant: Message variant (e.g., "sent", "received")
        theme: "light" or "dark" mode

    Returns:
        Hex color string
    """
    platform_colors = CHAT_COLORS.get(platform, CHAT_COLORS["generic"])
    return platform_colors.get(variant, platform_colors.get("sent", "#007AFF"))


def get_browser_color(browser: str, element: str, theme: str = "light") -> str:
    """
    Get browser chrome color.

    Args:
        browser: Browser type ("chrome", "safari", "firefox")
        element: Element type ("chrome", "text", "border")
        theme: "light" or "dark"

    Returns:
        Hex color string
    """
    browser_colors = BROWSER_COLORS.get(browser, BROWSER_COLORS["chrome"])
    theme_colors = browser_colors.get(theme, browser_colors["light"])
    return theme_colors.get(element, "#F0F0F0")


def get_language_color(language: str) -> str:
    """
    Get programming language brand color.

    Args:
        language: Programming language name (lowercase)

    Returns:
        Hex color string
    """
    return LANGUAGE_COLORS.get(language.lower(), LANGUAGE_COLORS["text"])


def get_container_ui_color(platform: str, element: str, theme: str = "light") -> str:
    """
    Get OS-specific container UI color.

    Args:
        platform: OS platform ("macos", "windows", "browser", "generic")
        element: UI element (e.g., "titlebar", "text", "border")
        theme: "light" or "dark" mode

    Returns:
        Hex color string
    """
    platform_colors = CONTAINER_UI_COLORS.get(platform, CONTAINER_UI_COLORS["generic"])
    theme_colors = platform_colors.get(theme, platform_colors["light"])
    return theme_colors.get(element, "#FFFFFF")
