"""Useful Enums"""

from enum import Enum

class Roles(str, Enum):
    """ChatGPT roles"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
