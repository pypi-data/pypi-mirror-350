#!/usr/bin/env python3
"""
Word MCP Server - Main server module.

This module provides the FastMCP server implementation with tools for 
interacting with Microsoft Word documents across different platforms.
"""

import asyncio
import logging
import sys
from typing import Dict, Optional
from pydantic import Field

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise ImportError("mcp package is required. Install with: pip install mcp")

from .backends import get_word_backend
from .backends.factory import is_platform_supported, get_platform_name

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


def create_server(name: str = "word-mcp") -> FastMCP:
    """Create and configure the Word MCP server."""
    # Check platform support
    if not is_platform_supported():
        raise RuntimeError(f"Platform {get_platform_name()} is not supported.")
    
    # Initialize FastMCP
    mcp = FastMCP(name)
    
    # Initialize the Word backend for the current platform
    try:
        word_backend = get_word_backend()
        logger.info(f"Initialized {get_platform_name()} Word backend")
    except Exception as e:
        logger.error(f"Failed to initialize Word backend: {str(e)}")
        raise
    
    @mcp.tool()
    async def get_selection_text(
        instance_id: Optional[str] = Field(None, description="Optional identifier for the specific Word instance to target. If not provided, uses the most recently active instance.")
    ) -> Dict:
        """Retrieves the currently selected text from the active Microsoft Word document"""
        logger.info(f"Handling get_selection_text with instance_id: {instance_id}")
        
        try:
            result = await word_backend.get_selection_text(instance_id)
            return result
        except Exception as e:
            logger.error(f"Error in get_selection_text: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}"}

    @mcp.tool()
    async def replace_selection_text(
        text: str = Field(..., description="The new text to replace the current selection"),
        instance_id: Optional[str] = Field(None, description="Optional identifier for the specific Word instance to target. If not provided, uses the most recently active instance.")
    ) -> Dict:
        """Replaces the currently selected text in the active Microsoft Word document with new text"""
        logger.info(f"Handling replace_selection_text with text: {text}, instance_id: {instance_id}")
        
        try:
            result = await word_backend.replace_selection_text(text, instance_id)
            return result
        except Exception as e:
            logger.error(f"Error in replace_selection_text: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}"}

    @mcp.tool()
    async def list_word_instances() -> Dict:
        """Lists all available Microsoft Word instances currently running"""
        logger.info("Handling list_word_instances request")
        
        try:
            result = await word_backend.list_instances()
            return result
        except Exception as e:
            logger.error(f"Error in list_word_instances: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}"}

    @mcp.tool()
    async def find_and_select_section(
        keywords: str = Field(..., description="The keywords to search for (exact match, case insensitive)"),
        section_type: str = Field("any", description="Type of section to search in. 'heading' searches in heading styles (H1-H6), 'paragraph' searches in all paragraphs, 'bookmark' searches in bookmark names, 'any' searches in all types. Default is 'any'."),
        instance_id: Optional[str] = Field(None, description="Optional identifier for the specific Word instance to target. If not provided, uses the most recently active instance.")
    ) -> Dict:
        """Finds and selects the first section in the document that contains the specified keywords (exact match, case insensitive)"""
        logger.info(f"Handling find_and_select_section with keywords: {keywords}, section_type: {section_type}, instance_id: {instance_id}")
        
        try:
            result = await word_backend.find_and_select_section(keywords, section_type, instance_id)
            return result
        except Exception as e:
            logger.error(f"Error in find_and_select_section: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}", "found": False}

    @mcp.tool()
    async def select_next_section(
        section_type: str = Field("any", description="Type of section to search for next. 'heading' searches for next heading styles (H1-H6), 'paragraph' searches for next paragraph, 'bookmark' searches for next bookmark, 'any' searches for any next section type. Default is 'any'."),
        instance_id: Optional[str] = Field(None, description="Optional identifier for the specific Word instance to target. If not provided, uses the most recently active instance.")
    ) -> Dict:
        """Selects the next section in the document after the current selection"""
        logger.info(f"Handling select_next_section with section_type: {section_type}, instance_id: {instance_id}")
        
        try:
            result = await word_backend.select_next_section(section_type, instance_id)
            return result
        except Exception as e:
            logger.error(f"Error in select_next_section: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}", "found": False}

    return mcp


async def initialize_server(mcp: FastMCP):
    """Initialize the server and detect Word instances."""
    try:
        word_backend = get_word_backend()
        await word_backend.detect_instances()
        logger.info("Word MCP Server initialization complete")
    except Exception as e:
        logger.error(f"Error during server initialization: {str(e)}")


def run_server(name: str = "word-mcp"):
    """Create and run the Word MCP server."""
    print(f"Starting Word MCP Server for {get_platform_name()}...", file=sys.stderr)
    print("Starting MCP server with stdio transport...", file=sys.stderr)
    
    try:
        # Create the server
        mcp = create_server(name)
        
        # Initialize the server
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_server(mcp))
        
        # Run the FastMCP server
        logger.info("Word MCP Server ready")
        mcp.run()
        print("MCP server started successfully", file=sys.stderr)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the command line interface."""
    run_server()


if __name__ == "__main__":
    main() 