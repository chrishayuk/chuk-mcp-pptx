"""
Container components for PowerPoint presentations.

Provides realistic device mockups and window containers for displaying
chat conversations and other content within authentic-looking frames.
"""

from .iphone import iPhoneContainer
from .samsung import SamsungContainer
from .browser import BrowserWindow
from .macos import MacOSWindow
from .windows import WindowsWindow
from .generic import ChatContainer

__all__ = [
    # Mobile device containers
    "iPhoneContainer",
    "SamsungContainer",
    # Desktop/Window containers
    "BrowserWindow",
    "MacOSWindow",
    "WindowsWindow",
    # Generic containers
    "ChatContainer",
]
