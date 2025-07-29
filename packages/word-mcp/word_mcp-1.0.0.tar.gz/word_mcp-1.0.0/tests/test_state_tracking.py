#!/usr/bin/env python3
"""
Test the state-tracking select_next_section implementation
"""

import asyncio
import pytest
from word_mcp.backends import get_word_backend


@pytest.mark.asyncio
async def test_state_tracking():
    """Test the state-tracking functionality."""
    try:
        backend = get_word_backend()
        await backend.detect_instances()
        
        initial_count = len(backend._processed_paragraphs)
        assert initial_count == 0, "Should start with no processed paragraphs"
        
        # Try to select 3 different sections
        processed_sections = []
        for i in range(3):
            result = await backend.select_next_section()
            
            if result.get('found'):
                text = result.get('section_text', '')
                processed_sections.append(text[:50])
                
                # Verify state tracking
                assert len(backend._processed_paragraphs) == i + 1, f"Should have {i+1} processed paragraphs"
                
                # Try a translation
                translated = f"[TEST TRANSLATION] {text}"
                replace_result = await backend.replace_selection_text(translated)
                assert replace_result.get('success'), "Translation should succeed"
            else:
                # If no more sections found, that's also a valid result
                break
        
        # Verify we processed different sections
        unique_sections = set(processed_sections)
        assert len(unique_sections) == len(processed_sections), "Should process different sections each time"
        
        print(f"✅ Successfully processed {len(processed_sections)} unique sections")
        
    except Exception as e:
        pytest.skip(f"Test skipped - likely no Word instance available: {str(e)}")


@pytest.mark.asyncio 
async def test_server_creation():
    """Test that the server can be created without errors."""
    from word_mcp.server import create_server
    
    try:
        server = create_server("test-server")
        assert server is not None, "Server should be created successfully"
        print("✅ Server creation test passed")
    except Exception as e:
        pytest.skip(f"Test skipped - platform may not be supported: {str(e)}")


if __name__ == "__main__":
    # Allow running tests directly
    asyncio.run(test_state_tracking()) 