"""
Chat components for PowerPoint presentations.

Provides both generic and platform-specific chat interfaces.
"""

from .generic import ChatMessage, ChatConversation
from .ios import iMessageBubble, iMessageConversation
from .android import AndroidMessageBubble, AndroidConversation
from .whatsapp import WhatsAppBubble, WhatsAppConversation
from .chatgpt import ChatGPTMessage, ChatGPTConversation
from .slack import SlackMessage, SlackConversation
from .teams import TeamsMessage, TeamsConversation
from .facebook import FacebookMessengerBubble, FacebookMessengerConversation
from .aol import AIMBubble, AIMConversation
from .msn import MSNBubble, MSNConversation

__all__ = [
    # Generic chat
    "ChatMessage",
    "ChatConversation",
    # Modern platforms
    "iMessageBubble",
    "iMessageConversation",
    "AndroidMessageBubble",
    "AndroidConversation",
    "WhatsAppBubble",
    "WhatsAppConversation",
    "ChatGPTMessage",
    "ChatGPTConversation",
    # Workplace platforms
    "SlackMessage",
    "SlackConversation",
    "TeamsMessage",
    "TeamsConversation",
    # Social platforms
    "FacebookMessengerBubble",
    "FacebookMessengerConversation",
    # Legacy/nostalgic platforms
    "AIMBubble",
    "AIMConversation",
    "MSNBubble",
    "MSNConversation",
]
