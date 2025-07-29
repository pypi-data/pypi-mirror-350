"""
Word MCP Server - A Model Context Protocol server for Microsoft Word integration.

This package provides MCP tools for interacting with Microsoft Word documents
across different platforms (Windows and macOS), enabling document automation
and AI-powered workflows.
"""

__version__ = "1.0.0"
__author__ = "Word MCP Team"
__email__ = "support@wordmcp.com"

from .server import main

__all__ = ["main", "__version__"] 