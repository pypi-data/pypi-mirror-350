#!/usr/bin/env python3
"""
Main entry point for the word_mcp package.

This allows the package to be executed as a module with:
    python -m word_mcp
    uvx word-mcp
    uvx wordmcp
    
Platform-specific routing:
- Windows: Uses the proven working implementation (copied as word_mcp_server_windows.py)
- macOS: Uses the backend pattern implementation (server.py)
"""

import sys
import os

def main():
    """Main entry point with platform-specific routing."""
    
    # Print platform detection message
    platform = sys.platform
    print(f"Detected platform: {platform}", file=sys.stderr)
    
    if platform == 'win32':
        # Windows: Use the proven working implementation
        print("Loading proven Windows Word MCP implementation...", file=sys.stderr)
        
        try:
            # Import and run the copied working implementation
            from .word_mcp_server_windows import run_word_mcp_server
            
            print("Starting copied FastMCP implementation for Windows...", file=sys.stderr)
            run_word_mcp_server()
            
        except ImportError as e:
            print(f"❌ Could not import Windows implementation: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error running Windows implementation: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif platform == 'darwin':
        # macOS: Use the backend pattern implementation
        print("Loading macOS-specific Word MCP implementation...", file=sys.stderr)
        from .server import main as macos_main
        macos_main()
    else:
        # Unsupported platform
        print(f"❌ Platform {platform} is not supported", file=sys.stderr)
        print("Supported platforms: Windows (win32), macOS (darwin)", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 