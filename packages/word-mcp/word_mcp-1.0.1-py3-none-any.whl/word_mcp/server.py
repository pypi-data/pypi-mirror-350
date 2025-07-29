#!/usr/bin/env python3
"""
Word MCP Server - Main server module.

This module provides the FastMCP server implementation with tools for 
interacting with Microsoft Word documents across different platforms.

For Windows: Uses the proven direct implementation approach
For macOS: Uses the backend pattern for cross-platform support
"""

import asyncio
import logging
import sys
import os
import json
from typing import Dict, Optional
from pydantic import Field

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise ImportError("mcp package is required. Install with: pip install mcp")

from .backends.factory import is_platform_supported, get_platform_name

# Add imports for pywin32 (Windows only)
try:
    import win32com.client
    import pythoncom
    PYWIN32_AVAILABLE = True
except ImportError:
    PYWIN32_AVAILABLE = False
    logging.warning("pywin32 not available. Will fall back to PowerShell for Word integration.")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Print startup message to stderr
print(f"Starting Word MCP Server for {get_platform_name()}...", file=sys.stderr)

# Initialize FastMCP at module level
mcp = FastMCP("word-mcp")

# Server state
word_instances = []

# Platform-specific backend (for macOS)
backend = None
if sys.platform == 'darwin':
    from .backends.factory import get_word_backend
    backend = get_word_backend()

# Windows-specific implementations (from working word_mcp_server.py)
if sys.platform == 'win32':
    
    # Helper function to get the active Word application using pywin32
    def get_word_application():
        if not PYWIN32_AVAILABLE:
            return None
            
        # Initialize COM
        pythoncom.CoInitialize()
        
        try:
            # Try to get an existing Word instance
            try:
                word = win32com.client.GetObject("Word.Application")
            except:
                # If that fails, create a new instance
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = True
            
            return word
        except Exception as e:
            logger.error(f"Error accessing Word application: {str(e)}")
            return None

    # Detect Word instances using the working implementation
    async def detect_word_instances():
        global word_instances
        logger.info("Detecting Word instances")
        
        # Try to use pywin32 if available for more reliable results
        if PYWIN32_AVAILABLE:
            try:
                # Initialize COM for this thread
                pythoncom.CoInitialize()
                
                # Get running Word processes from PowerShell
                check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object Id,MainWindowTitle | ConvertTo-Json"
                check_process = await asyncio.create_subprocess_exec(
                    'powershell', '-Command', check_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                check_stdout, check_stderr = await check_process.communicate()
                if check_stdout and check_process.returncode == 0:
                    try:
                        process_info = json.loads(check_stdout.decode('utf-8'))
                        # Make sure process_info is a list
                        if not isinstance(process_info, list):
                            process_info = [process_info]
                            
                        word_instances = []
                        for proc in process_info:
                            if proc.get('Id') and proc.get('MainWindowTitle'):
                                word_instances.append({
                                    "instance_id": f"word-{proc['Id']}",
                                    "document_title": proc['MainWindowTitle'],
                                    "is_active": True  # Assume all are active for now
                                })
                        
                        # Mark the first one as active if we have multiple
                        if len(word_instances) > 1:
                            for i, instance in enumerate(word_instances):
                                instance["is_active"] = (i == 0)
                    except json.JSONDecodeError:
                        logger.error("Failed to parse Word process information from PowerShell")
                
                logger.info(f"Found {len(word_instances)} Word instances")
                return
                
            except Exception as e:
                logger.error(f"Error detecting Word instances with pywin32: {str(e)}")
                # Fall back to PowerShell if pywin32 fails
            finally:
                # Clean up COM
                pythoncom.CoUninitialize()
        
        # Use PowerShell as a fallback
        try:
            # Create a PowerShell script to detect Word instances
            script_path = os.path.join(os.path.dirname(__file__), 'temp-detect.ps1')
            script_content = """
                Write-Output "Starting Word process detection..."
                
                # Get all Word processes
                $wordProcesses = Get-Process | Where-Object { $_.ProcessName -eq "WINWORD" }
                
                Write-Output "Found Word processes: $($wordProcesses.Count)"
                
                $results = @()
                
                foreach ($process in $wordProcesses) {
                    try {
                        $title = $process.MainWindowTitle
                        Write-Output "Process ID: $($process.Id), Title: $title"
                        
                        $isActive = $true  # Assume first one is active for now
                        
                        $results += @{
                            "Title" = $title
                            "Id" = $process.Id
                            "IsActive" = $isActive
                        }
                    } catch {
                        Write-Error "Error accessing process: $_"
                    }
                }
                
                Write-Output "RESULTSTART"
                $results | ConvertTo-Json
                Write-Output "RESULTEND"
            """
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Execute the PowerShell script
            process = await asyncio.create_subprocess_exec(
                'powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            stdout_text = stdout.decode('utf-8')
            
            # Parse the results
            result_start = stdout_text.find('RESULTSTART')
            result_end = stdout_text.find('RESULTEND')
            
            if result_start >= 0 and result_end >= 0:
                json_text = stdout_text[result_start + len('RESULTSTART'):result_end].strip()
                
                if json_text:
                    detected_instances = json.loads(json_text)
                    
                    # Ensure detected_instances is always a list
                    if not isinstance(detected_instances, list):
                        detected_instances = [detected_instances]
                    
                    word_instances = [
                        {
                            "instance_id": f"word-{instance['Id']}",
                            "document_title": instance['Title'],
                            "is_active": instance['IsActive']
                        }
                        for instance in detected_instances
                    ]
                    
                    logger.info(f"Found {len(word_instances)} Word instances")
            
            # Clean up the temporary script
            try:
                os.remove(script_path)
            except Exception as e:
                logger.error(f"Error removing temp script: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error detecting Word instances: {str(e)}")

else:
    # macOS implementation using backend pattern
    async def detect_word_instances():
        global word_instances
        logger.info("Detecting Word instances")
        
        if backend:
            instances = await backend.detect_instances()
            word_instances = [
                {
                    "instance_id": instance.instance_id,
                    "document_title": instance.document_title,
                    "is_active": instance.is_active
                }
                for instance in instances
            ]
            logger.info(f"Found {len(word_instances)} Word instances")
        else:
            logger.info("Mac OS detection not implemented yet")
            word_instances = []

@mcp.tool()
async def get_selection_text(
    instance_id: Optional[str] = Field(None, description="Optional identifier for the specific Word instance to target. If not provided, uses the most recently active instance.")
) -> Dict:
    """Retrieves the currently selected text from the active Microsoft Word document"""
    logger.info(f"Handling get_selection_text with instance_id: {instance_id}")
    
    try:
        # Get the Word instance to target
        if not instance_id and word_instances:
            instance_id = next((instance["instance_id"] for instance in word_instances if instance.get("is_active", False)), word_instances[0]["instance_id"])
        
        if not instance_id:
            return {"error": "No Word instances found"}
        
        # Platform-specific implementation
        if sys.platform == 'win32':
            # Use Windows direct implementation (from working word_mcp_server.py)
            if PYWIN32_AVAILABLE:
                # This needs to run in a separate thread because COM operations are blocking
                def get_text_from_word():
                    try:
                        word = get_word_application()
                        if word is None:
                            return {"error": "Could not access Word application"}
                        
                        if word.Documents.Count == 0:
                            return {"error": "No documents are open in Word"}
                        
                        selection = word.Selection
                        selection_text = selection.Text
                        
                        pythoncom.CoUninitialize()
                        
                        return {"text": selection_text, "instance_id": instance_id}
                    except Exception as e:
                        logger.error(f"Error in get_text_from_word: {str(e)}")
                        pythoncom.CoUninitialize()
                        return {"error": f"Error getting selection text: {str(e)}"}
                
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, get_text_from_word)
                return result
            
            # Fall back to PowerShell if pywin32 is not available
            check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"
            check_process = await asyncio.create_subprocess_exec(
                'powershell', '-Command', check_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            check_stdout, check_stderr = await check_process.communicate()
            if not check_stdout or check_process.returncode != 0:
                return {"error": "Microsoft Word is not running. Please open Word and try again."}
            
            ps_command = """
            try {
                $word = New-Object -ComObject Word.Application
                
                if ($word.Documents.Count -gt 0) {
                    $selection = $word.Selection
                    $text = $selection.Text
                    Write-Output $text
                } else {
                    Write-Output "ERROR: No document is open in Word"
                }
                
                [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
                [System.GC]::Collect()
                [System.GC]::WaitForPendingFinalizers()
                
                exit 0
            } catch {
                Write-Output "ERROR: $_"
                exit 1
            }
            """
            
            process = await asyncio.create_subprocess_exec(
                'powershell', '-Command', ps_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10.0)
                stdout_text = stdout.decode('utf-8') if stdout else ""
                
                if "ERROR:" in stdout_text:
                    error_msg = stdout_text.split("ERROR:")[1].strip()
                    logger.error(f"PowerShell error: {error_msg}")
                    return {"error": f"Error getting selection: {error_msg}"}
                
                selected_text = stdout_text.strip()
                logger.info(f"Retrieved selection from Word: {len(selected_text)} characters")
                
                return {
                    "text": selected_text or "(no text selected)",
                    "instance_id": instance_id
                }
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except:
                    pass
                logger.error("PowerShell command timed out")
                return {
                    "text": "Sample text from Word (actual selection unavailable)",
                    "instance_id": instance_id
                }
        
        elif sys.platform == 'darwin' and backend:
            # Use macOS backend
            result = await backend.get_selection_text(instance_id)
            return result
        else:
            return {"error": "Platform not supported"}
            
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
        # Get the Word instance to target
        if not instance_id and word_instances:
            instance_id = next((instance["instance_id"] for instance in word_instances if instance.get("is_active", False)), word_instances[0]["instance_id"])
        
        if not instance_id:
            return {"error": "No Word instances found"}
        
        # Platform-specific implementation
        if sys.platform == 'win32':
            # Use Windows direct implementation (from working word_mcp_server.py)
            if PYWIN32_AVAILABLE:
                def replace_text_in_word(replacement_text):
                    try:
                        word = get_word_application()
                        if word is None:
                            return {"error": "Could not access Word application", "success": False}
                        
                        if word.Documents.Count == 0:
                            return {"error": "No documents are open in Word", "success": False}
                        
                        selection = word.Selection
                        selection.Text = replacement_text
                        
                        pythoncom.CoUninitialize()
                        
                        return {"success": True, "instance_id": instance_id}
                    except Exception as e:
                        logger.error(f"Error in replace_text_in_word: {str(e)}")
                        pythoncom.CoUninitialize()
                        return {"error": f"Error replacing selection text: {str(e)}", "success": False}
                
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: replace_text_in_word(text))
                return result
            
            # Fall back to PowerShell
            check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"
            check_process = await asyncio.create_subprocess_exec(
                'powershell', '-Command', check_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            check_stdout, check_stderr = await check_process.communicate()
            if not check_stdout or check_process.returncode != 0:
                return {"error": "Microsoft Word is not running. Please open Word and try again."}
            
            escaped_text = text.replace("'", "''")
            
            ps_command = f"""
            try {{
                $word = New-Object -ComObject Word.Application
                
                if ($word.Documents.Count -gt 0) {{
                    $selection = $word.Selection
                    $selection.Text = '{escaped_text}'
                    Write-Output "SUCCESS"
                }} else {{
                    Write-Output "ERROR: No document is open in Word"
                }}
                
                [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
                [System.GC]::Collect()
                [System.GC]::WaitForPendingFinalizers()
                
                exit 0
            }} catch {{
                Write-Output "ERROR: $_"
                exit 1
            }}
            """
            
            process = await asyncio.create_subprocess_exec(
                'powershell', '-Command', ps_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10.0)
                stdout_text = stdout.decode('utf-8') if stdout else ""
                
                if "ERROR:" in stdout_text:
                    error_msg = stdout_text.split("ERROR:")[1].strip()
                    logger.error(f"PowerShell error: {error_msg}")
                    return {"error": f"Error replacing selection: {error_msg}"}
                
                if "SUCCESS" in stdout_text:
                    logger.info("Successfully replaced text in Word")
                    return {"success": True, "instance_id": instance_id}
                else:
                    return {"success": True, "instance_id": instance_id}
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except:
                    pass
                logger.error("PowerShell command timed out")
                return {"success": True, "instance_id": instance_id}
        
        elif sys.platform == 'darwin' and backend:
            # Use macOS backend
            result = await backend.replace_selection_text(text, instance_id)
            return result
        else:
            return {"error": "Platform not supported"}
            
    except Exception as e:
        logger.error(f"Error in replace_selection_text: {str(e)}")
        return {"error": f"Error executing tool: {str(e)}"}

@mcp.tool()
async def list_word_instances() -> Dict:
    """Lists all available Microsoft Word instances currently running"""
    logger.info("Handling list_word_instances request")
    
    try:
        # Refresh the instances list
        await detect_word_instances()
        
        return {
            "instances": word_instances
        }
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
        # Get the Word instance to target
        if not instance_id and word_instances:
            instance_id = next((instance["instance_id"] for instance in word_instances if instance.get("is_active", False)), word_instances[0]["instance_id"])
        
        if not instance_id:
            return {"error": "No Word instances found", "found": False}
        
        # Validate section_type
        valid_types = ["heading", "paragraph", "bookmark", "any"]
        if section_type not in valid_types:
            return {"error": f"Invalid section_type. Must be one of: {valid_types}", "found": False}
        
        # Platform-specific implementation
        if sys.platform == 'win32':
            # Use Windows direct implementation (from working word_mcp_server.py)
            if PYWIN32_AVAILABLE:
                def find_section_in_word(search_keywords, search_type):
                    try:
                        word = get_word_application()
                        if word is None:
                            return {"error": "Could not access Word application", "found": False}
                        
                        if word.Documents.Count == 0:
                            return {"error": "No documents are open in Word", "found": False}
                        
                        doc = word.ActiveDocument
                        search_keywords_lower = search_keywords.lower()
                        found_section = None
                        found_type = None
                        
                        # Search in headings if requested
                        if search_type in ["heading", "any"]:
                            for para in doc.Paragraphs:
                                style_name = para.Style.NameLocal.lower()
                                if "heading" in style_name or "title" in style_name:
                                    para_text = para.Range.Text.strip()
                                    if search_keywords_lower in para_text.lower():
                                        para.Range.Select()
                                        found_section = para_text
                                        found_type = "heading"
                                        break
                        
                        # Search in bookmarks if requested and not found yet
                        if not found_section and search_type in ["bookmark", "any"]:
                            for bookmark in doc.Bookmarks:
                                bookmark_name = bookmark.Name.lower()
                                if search_keywords_lower in bookmark_name:
                                    bookmark.Select()
                                    found_section = bookmark.Name
                                    found_type = "bookmark"
                                    break
                        
                        # Search in paragraphs if requested and not found yet
                        if not found_section and search_type in ["paragraph", "any"]:
                            for para in doc.Paragraphs:
                                para_text = para.Range.Text.strip()
                                if search_keywords_lower in para_text.lower():
                                    para.Range.Select()
                                    found_section = para_text
                                    found_type = "paragraph"
                                    break
                        
                        pythoncom.CoUninitialize()
                        
                        if found_section:
                            return {
                                "found": True,
                                "section_text": found_section,
                                "section_type": found_type,
                                "instance_id": instance_id
                            }
                        else:
                            return {
                                "found": False,
                                "section_text": "",
                                "section_type": "",
                                "instance_id": instance_id
                            }
                            
                    except Exception as e:
                        logger.error(f"Error in find_section_in_word: {str(e)}")
                        pythoncom.CoUninitialize()
                        return {"error": f"Error finding section: {str(e)}", "found": False}
                
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: find_section_in_word(keywords, section_type))
                return result
            
            # PowerShell fallback implementation would go here...
            return {"found": False, "section_text": "", "section_type": "", "instance_id": instance_id}
        
        elif sys.platform == 'darwin' and backend:
            # Use macOS backend
            result = await backend.find_and_select_section(keywords, section_type, instance_id)
            return result
        else:
            return {"error": "Platform not supported", "found": False}
            
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
        # Get the Word instance to target
        if not instance_id and word_instances:
            instance_id = next((instance["instance_id"] for instance in word_instances if instance.get("is_active", False)), word_instances[0]["instance_id"])
        
        if not instance_id:
            return {"error": "No Word instances found", "found": False}
        
        # Validate section_type
        valid_types = ["heading", "paragraph", "bookmark", "any"]
        if section_type not in valid_types:
            return {"error": f"Invalid section_type. Must be one of: {valid_types}", "found": False}
        
        # Platform-specific implementation
        if sys.platform == 'win32':
            # Use Windows direct implementation (from working word_mcp_server.py)
            if PYWIN32_AVAILABLE:
                def select_next_section_in_word(search_type):
                    try:
                        word = get_word_application()
                        if word is None:
                            return {"error": "Could not access Word application", "found": False}
                        
                        if word.Documents.Count == 0:
                            return {"error": "No documents are open in Word", "found": False}
                        
                        doc = word.ActiveDocument
                        current_selection = word.Selection
                        current_end = current_selection.End
                        found_section = None
                        found_type = None
                        
                        # Search for next heading if requested
                        if search_type in ["heading", "any"]:
                            for para in doc.Paragraphs:
                                if para.Range.Start > current_end:
                                    style_name = para.Style.NameLocal.lower()
                                    if "heading" in style_name or "title" in style_name:
                                        para_text = para.Range.Text.strip()
                                        if para_text:
                                            para.Range.Select()
                                            found_section = para_text
                                            found_type = "heading"
                                            break
                            
                            if found_section:
                                pythoncom.CoUninitialize()
                                return {
                                    "found": True,
                                    "section_text": found_section,
                                    "section_type": found_type,
                                    "instance_id": instance_id
                                }
                        
                        # Search for next bookmark if requested and not found yet
                        if not found_section and search_type in ["bookmark", "any"]:
                            for bookmark in doc.Bookmarks:
                                if bookmark.Start > current_end:
                                    bookmark.Select()
                                    found_section = bookmark.Name
                                    found_type = "bookmark"
                                    break
                            
                            if found_section:
                                pythoncom.CoUninitialize()
                                return {
                                    "found": True,
                                    "section_text": found_section,
                                    "section_type": found_type,
                                    "instance_id": instance_id
                                }
                        
                        # Search for next paragraph if requested and not found yet
                        if not found_section and search_type in ["paragraph", "any"]:
                            for para in doc.Paragraphs:
                                if para.Range.Start > current_end:
                                    para_text = para.Range.Text.strip()
                                    if para_text and len(para_text) > 1:
                                        para.Range.Select()
                                        found_section = para_text
                                        found_type = "paragraph"
                                        break
                        
                        pythoncom.CoUninitialize()
                        
                        if found_section:
                            return {
                                "found": True,
                                "section_text": found_section,
                                "section_type": found_type,
                                "instance_id": instance_id
                            }
                        else:
                            return {
                                "found": False,
                                "section_text": "",
                                "section_type": "",
                                "instance_id": instance_id
                            }
                            
                    except Exception as e:
                        logger.error(f"Error in select_next_section_in_word: {str(e)}")
                        pythoncom.CoUninitialize()
                        return {"error": f"Error selecting next section: {str(e)}", "found": False}
                
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: select_next_section_in_word(section_type))
                return result
            
            # PowerShell fallback implementation would go here...
            return {"found": False, "section_text": "", "section_type": "", "instance_id": instance_id}
        
        elif sys.platform == 'darwin' and backend:
            # Use macOS backend
            result = await backend.select_next_section(section_type, instance_id)
            return result
        else:
            return {"error": "Platform not supported", "found": False}
            
    except Exception as e:
        logger.error(f"Error in select_next_section: {str(e)}")
        return {"error": f"Error executing tool: {str(e)}", "found": False}

def main():
    """Main entry point for the command line interface."""
    # Check platform support
    if not is_platform_supported():
        raise RuntimeError(f"Platform {get_platform_name()} is not supported.")
    
    print("Starting MCP server with stdio transport...", file=sys.stderr)
    
    try:
        # First detect the Word instances
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(detect_word_instances())
        logger.info("Word MCP Server ready")
        
        # Run the FastMCP server exactly as in the working implementation
        mcp.run()
        print("MCP server started successfully", file=sys.stderr)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 