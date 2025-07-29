"""
Word MCP Backend Package

This package contains platform-specific implementations for Microsoft Word integration.
"""

from .factory import get_word_backend

__all__ = ['get_word_backend'] 