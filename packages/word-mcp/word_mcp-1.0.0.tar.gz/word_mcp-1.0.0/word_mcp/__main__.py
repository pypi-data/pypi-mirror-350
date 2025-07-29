#!/usr/bin/env python3
"""
Main entry point for the word_mcp package.

This allows the package to be executed as a module with:
    python -m word_mcp
    uvx word-mcp
    uvx wordmcp
"""

from .server import main

if __name__ == "__main__":
    main() 