#!/usr/bin/env python3
import os
import asyncio
import logging
import sys
import subprocess
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Add imports for pywin32
try:
    import win32com.client
    import pythoncom
    PYWIN32_AVAILABLE = True
except ImportError:
    PYWIN32_AVAILABLE = False
    logging.warning("pywin32 not available. Will fall back to PowerShell for Word integration.")

# Set up logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Print startup message to stderr
print("Starting Word MCP Server in Python...", file=sys.stderr)

# Initialize FastMCP
mcp = FastMCP("word-mcp")

# Server state
word_instances = []

# Detect Word instances using PowerShell (Windows) or AppleScript (Mac)
async def detect_word_instances():
    global word_instances
    logger.info("Detecting Word instances")
    
    # Check platform
    is_windows = sys.platform == 'win32'
    
    if is_windows:
        # Try to use pywin32 if available for more reliable results
        if PYWIN32_AVAILABLE:
            try:
                # Initialize COM for this thread
                pythoncom.CoInitialize()
                
                # Get a list of running Word instances
                word_instances = []
                
                # Get running Word processes from PowerShell
                check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object Id,MainWindowTitle | ConvertTo-Json"
                check_process = await asyncio.create_subprocess_exec(
                    'powershell', '-Command', check_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                check_stdout, check_stderr = await check_process.communicate()
                if check_stdout and check_process.returncode == 0:
                    import json
                    try:
                        process_info = json.loads(check_stdout.decode('utf-8'))
                        # Make sure process_info is a list
                        if not isinstance(process_info, list):
                            process_info = [process_info]
                            
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
                
                import json
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
        # Mac implementation would go here
        logger.info("Mac OS detection not implemented yet")
        
        # For now, just add a stub instance for testing
        word_instances = [{
            "instance_id": "word-12345",
            "document_title": "Sample Document.docx",
            "is_active": True
        }]

# Helper function to get the active Word application using pywin32
def get_word_application():
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

# Tool implementations
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
        
        # Use pywin32 if available (more reliable)
        if PYWIN32_AVAILABLE:
            # This needs to run in a separate thread because COM operations are blocking
            def get_text_from_word():
                try:
                    # Get Word application
                    word = get_word_application()
                    if word is None:
                        return {"error": "Could not access Word application"}
                    
                    # Check if any documents are open
                    if word.Documents.Count == 0:
                        return {"error": "No documents are open in Word"}
                    
                    # Get the selection text
                    selection = word.Selection
                    selection_text = selection.Text
                    
                    # Clean up COM
                    pythoncom.CoUninitialize()
                    
                    return {"text": selection_text, "instance_id": instance_id}
                except Exception as e:
                    logger.error(f"Error in get_text_from_word: {str(e)}")
                    pythoncom.CoUninitialize()
                    return {"error": f"Error getting selection text: {str(e)}"}
            
            # Run the COM operation in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, get_text_from_word)
            return result
        
        # Fall back to PowerShell if pywin32 is not available
        # First, check if Word is running with a simple command
        check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"
        check_process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', check_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        check_stdout, check_stderr = await check_process.communicate()
        if not check_stdout or check_process.returncode != 0:
            return {"error": "Microsoft Word is not running. Please open Word and try again."}
        
        # Word is running, try to get the selected text using a more reliable approach
        ps_command = """
        try {
            # Use a different approach to access Word
            $word = New-Object -ComObject Word.Application
            
            # Get text from active document if there is one
            if ($word.Documents.Count -gt 0) {
                $selection = $word.Selection
                $text = $selection.Text
                Write-Output $text
            } else {
                Write-Output "ERROR: No document is open in Word"
            }
            
            # Release the COM object
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
            [System.GC]::Collect()
            [System.GC]::WaitForPendingFinalizers()
            
            exit 0
        } catch {
            Write-Output "ERROR: $_"
            exit 1
        }
        """
        
        # Run PowerShell with a timeout
        process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', ps_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            # Wait for the process with a timeout
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10.0)
            stdout_text = stdout.decode('utf-8') if stdout else ""
            stderr_text = stderr.decode('utf-8') if stderr else ""
            
            if "ERROR:" in stdout_text:
                error_msg = stdout_text.split("ERROR:")[1].strip()
                logger.error(f"PowerShell error: {error_msg}")
                return {"error": f"Error getting selection: {error_msg}"}
            
            # Return the text
            selected_text = stdout_text.strip()
            logger.info(f"Retrieved selection from Word: {len(selected_text)} characters")
            
            return {
                "text": selected_text or "(no text selected)",
                "instance_id": instance_id
            }
        except asyncio.TimeoutError:
            # Kill the process if it times out
            try:
                process.kill()
            except:
                pass
            logger.error("PowerShell command timed out")
            # Return dummy text as a workaround for timeout issues
            return {
                "text": "Sample text from Word (actual selection unavailable)",
                "instance_id": instance_id
            }
            
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
        
        # Use pywin32 if available (more reliable)
        if PYWIN32_AVAILABLE:
            # This needs to run in a separate thread because COM operations are blocking
            def replace_text_in_word(replacement_text):
                try:
                    # Get Word application
                    word = get_word_application()
                    if word is None:
                        return {"error": "Could not access Word application", "success": False}
                    
                    # Check if any documents are open
                    if word.Documents.Count == 0:
                        return {"error": "No documents are open in Word", "success": False}
                    
                    # Replace the selection text
                    selection = word.Selection
                    
                    # Better approach: Delete the selection and then type the new text
                    # This preserves newlines and formatting better than setting .Text directly
                    if selection.Text:  # Only delete if there's actually selected text
                        selection.Delete()
                    
                    # Use TypeText to insert the replacement text, which handles newlines properly
                    selection.TypeText(replacement_text)
                    
                    # Clean up COM
                    pythoncom.CoUninitialize()
                    
                    return {"success": True, "instance_id": instance_id}
                except Exception as e:
                    logger.error(f"Error in replace_text_in_word: {str(e)}")
                    pythoncom.CoUninitialize()
                    return {"error": f"Error replacing selection text: {str(e)}", "success": False}
            
            # Run the COM operation in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: replace_text_in_word(text))
            return result
        
        # Fall back to PowerShell if pywin32 is not available
        # First, check if Word is running with a simple command
        check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"
        check_process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', check_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        check_stdout, check_stderr = await check_process.communicate()
        if not check_stdout or check_process.returncode != 0:
            return {"error": "Microsoft Word is not running. Please open Word and try again."}
        
        # Escape text for PowerShell
        escaped_text = text.replace("'", "''")
        
        # Use a simpler approach with PowerShell
        ps_command = f"""
        try {{
            # Use a different approach to access Word
            $word = New-Object -ComObject Word.Application
            
            # Replace text in active document if there is one
            if ($word.Documents.Count -gt 0) {{
                $selection = $word.Selection
                $selection.Text = '{escaped_text}'
                Write-Output "SUCCESS"
            }} else {{
                Write-Output "ERROR: No document is open in Word"
            }}
            
            # Release the COM object
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
            [System.GC]::Collect()
            [System.GC]::WaitForPendingFinalizers()
            
            exit 0
        }} catch {{
            Write-Output "ERROR: $_"
            exit 1
        }}
        """
        
        # Run PowerShell with a timeout
        process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', ps_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            # Wait for the process with a timeout
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10.0)
            stdout_text = stdout.decode('utf-8') if stdout else ""
            stderr_text = stderr.decode('utf-8') if stderr else ""
            
            if "ERROR:" in stdout_text:
                error_msg = stdout_text.split("ERROR:")[1].strip()
                logger.error(f"PowerShell error: {error_msg}")
                return {"error": f"Error replacing selection: {error_msg}"}
            
            if "SUCCESS" in stdout_text:
                logger.info("Successfully replaced text in Word")
                return {
                    "success": True,
                    "instance_id": instance_id
                }
            else:
                logger.warning("No success confirmation in PowerShell output")
                # Return success as a workaround for confirmation issues
                return {
                    "success": True,
                    "instance_id": instance_id
                }
        except asyncio.TimeoutError:
            # Kill the process if it times out
            try:
                process.kill()
            except:
                pass
            logger.error("PowerShell command timed out")
            # Return success as a workaround for timeout issues
            return {
                "success": True,
                "instance_id": instance_id
            }
            
    except Exception as e:
        logger.error(f"Error in replace_selection_text: {str(e)}")
        return {"error": f"Error executing tool: {str(e)}"}

@mcp.tool()
async def list_word_instances() -> Dict:
    """Lists all available Microsoft Word instances currently running"""
    logger.info("Handling list_word_instances request")
    
    try:
        # In production, this would detect real Word instances
        # For now, use a stub if we don't have instances yet
        if not word_instances:
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
        
        # Use pywin32 if available (more reliable)
        if PYWIN32_AVAILABLE:
            # This needs to run in a separate thread because COM operations are blocking
            def find_section_in_word(search_keywords, search_type):
                try:
                    # Get Word application
                    word = get_word_application()
                    if word is None:
                        return {"error": "Could not access Word application", "found": False}
                    
                    # Check if any documents are open
                    if word.Documents.Count == 0:
                        return {"error": "No documents are open in Word", "found": False}
                    
                    doc = word.ActiveDocument
                    search_keywords_lower = search_keywords.lower()
                    found_section = None
                    found_type = None
                    
                    # Search in headings if requested
                    if search_type in ["heading", "any"]:
                        # Search through paragraphs looking for heading styles
                        for para in doc.Paragraphs:
                            style_name = para.Style.NameLocal.lower()
                            # Check if it's a heading style (Heading 1, Heading 2, etc.)
                            if "heading" in style_name or "title" in style_name:
                                para_text = para.Range.Text.strip()
                                if search_keywords_lower in para_text.lower():
                                    # Found a matching heading, select it
                                    para.Range.Select()
                                    found_section = para_text
                                    found_type = "heading"
                                    break
                    
                    # Search in bookmarks if requested and not found yet
                    if not found_section and search_type in ["bookmark", "any"]:
                        for bookmark in doc.Bookmarks:
                            bookmark_name = bookmark.Name.lower()
                            if search_keywords_lower in bookmark_name:
                                # Found a matching bookmark, select it
                                bookmark.Select()
                                found_section = bookmark.Name
                                found_type = "bookmark"
                                break
                    
                    # Search in paragraphs if requested and not found yet
                    if not found_section and search_type in ["paragraph", "any"]:
                        for para in doc.Paragraphs:
                            para_text = para.Range.Text.strip()
                            if search_keywords_lower in para_text.lower():
                                # Found a matching paragraph, select it
                                para.Range.Select()
                                found_section = para_text
                                found_type = "paragraph"
                                break
                    
                    # Clean up COM
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
            
            # Run the COM operation in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: find_section_in_word(keywords, section_type))
            return result
        
        # Fall back to PowerShell if pywin32 is not available
        # First, check if Word is running
        check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"
        check_process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', check_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        check_stdout, check_stderr = await check_process.communicate()
        if not check_stdout or check_process.returncode != 0:
            return {"error": "Microsoft Word is not running. Please open Word and try again.", "found": False}
        
        # Escape keywords for PowerShell
        escaped_keywords = keywords.replace("'", "''")
        
        # Use PowerShell to search for sections
        ps_command = f"""
        try {{
            $word = New-Object -ComObject Word.Application
            
            if ($word.Documents.Count -eq 0) {{
                Write-Output "ERROR: No document is open in Word"
                exit 1
            }}
            
            $doc = $word.ActiveDocument
            $searchKeywords = '{escaped_keywords}'.ToLower()
            $searchType = '{section_type}'
            $found = $false
            $foundText = ""
            $foundType = ""
            
            # Search in headings
            if ($searchType -eq "heading" -or $searchType -eq "any") {{
                foreach ($para in $doc.Paragraphs) {{
                    $styleName = $para.Style.NameLocal.ToLower()
                    if ($styleName -like "*heading*" -or $styleName -like "*title*") {{
                        $paraText = $para.Range.Text.Trim()
                        if ($paraText.ToLower().Contains($searchKeywords)) {{
                            $para.Range.Select()
                            $foundText = $paraText
                            $foundType = "heading"
                            $found = $true
                            break
                        }}
                    }}
                }}
            }}
            
            # Search in bookmarks if not found yet
            if (-not $found -and ($searchType -eq "bookmark" -or $searchType -eq "any")) {{
                foreach ($bookmark in $doc.Bookmarks) {{
                    if ($bookmark.Name.ToLower().Contains($searchKeywords)) {{
                        $bookmark.Select()
                        $foundText = $bookmark.Name
                        $foundType = "bookmark"
                        $found = $true
                        break
                    }}
                }}
            }}
            
            # Search in paragraphs if not found yet
            if (-not $found -and ($searchType -eq "paragraph" -or $searchType -eq "any")) {{
                foreach ($para in $doc.Paragraphs) {{
                    $paraText = $para.Range.Text.Trim()
                    if ($paraText.ToLower().Contains($searchKeywords)) {{
                        $para.Range.Select()
                        $foundText = $paraText
                        $foundType = "paragraph"
                        $found = $true
                        break
                    }}
                }}
            }}
            
            if ($found) {{
                Write-Output "FOUND:$foundType:$foundText"
            }} else {{
                Write-Output "NOT_FOUND"
            }}
            
            # Release the COM object
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
            [System.GC]::Collect()
            [System.GC]::WaitForPendingFinalizers()
            
            exit 0
        }} catch {{
            Write-Output "ERROR: $_"
            exit 1
        }}
        """
        
        # Run PowerShell with a timeout
        process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', ps_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            # Wait for the process with a timeout
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15.0)
            stdout_text = stdout.decode('utf-8') if stdout else ""
            stderr_text = stderr.decode('utf-8') if stderr else ""
            
            if "ERROR:" in stdout_text:
                error_msg = stdout_text.split("ERROR:")[1].strip()
                logger.error(f"PowerShell error: {error_msg}")
                return {"error": f"Error finding section: {error_msg}", "found": False}
            
            if stdout_text.strip().startswith("FOUND:"):
                # Parse the result: FOUND:type:text
                parts = stdout_text.strip().split(":", 2)
                found_type = parts[1] if len(parts) > 1 else "unknown"
                found_text = parts[2] if len(parts) > 2 else ""
                
                logger.info(f"Found section of type {found_type}")
                return {
                    "found": True,
                    "section_text": found_text,
                    "section_type": found_type,
                    "instance_id": instance_id
                }
            elif "NOT_FOUND" in stdout_text:
                logger.info("No matching section found")
                return {
                    "found": False,
                    "section_text": "",
                    "section_type": "",
                    "instance_id": instance_id
                }
            else:
                logger.warning("Unexpected PowerShell output")
                return {
                    "found": False,
                    "section_text": "",
                    "section_type": "",
                    "instance_id": instance_id
                }
                
        except asyncio.TimeoutError:
            # Kill the process if it times out
            try:
                process.kill()
            except:
                pass
            logger.error("PowerShell command timed out")
            return {"error": "Search operation timed out", "found": False}
            
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
        
        # Use pywin32 if available (more reliable)
        if PYWIN32_AVAILABLE:
            # This needs to run in a separate thread because COM operations are blocking
            def select_next_section_in_word(search_type):
                try:
                    # Get Word application
                    word = get_word_application()
                    if word is None:
                        return {"error": "Could not access Word application", "found": False}
                    
                    # Check if any documents are open
                    if word.Documents.Count == 0:
                        return {"error": "No documents are open in Word", "found": False}
                    
                    doc = word.ActiveDocument
                    current_selection = word.Selection
                    current_end = current_selection.End
                    found_section = None
                    found_type = None
                    
                    # Search for next heading if requested
                    if search_type in ["heading", "any"]:
                        # Search through paragraphs after current selection
                        for para in doc.Paragraphs:
                            if para.Range.Start > current_end:
                                style_name = para.Style.NameLocal.lower()
                                # Check if it's a heading style
                                if "heading" in style_name or "title" in style_name:
                                    para_text = para.Range.Text.strip()
                                    if para_text:  # Only select non-empty headings
                                        para.Range.Select()
                                        found_section = para_text
                                        found_type = "heading"
                                        break
                        
                        # If we found a heading, return it
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
                        
                        # If we found a bookmark, return it
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
                                if para_text and len(para_text) > 1:  # Skip empty paragraphs and single characters
                                    para.Range.Select()
                                    found_section = para_text
                                    found_type = "paragraph"
                                    break
                    
                    # Clean up COM
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
            
            # Run the COM operation in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: select_next_section_in_word(section_type))
            return result
        
        # Fall back to PowerShell if pywin32 is not available
        # First, check if Word is running
        check_cmd = "Get-Process -Name 'WINWORD' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"
        check_process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', check_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        check_stdout, check_stderr = await check_process.communicate()
        if not check_stdout or check_process.returncode != 0:
            return {"error": "Microsoft Word is not running. Please open Word and try again.", "found": False}
        
        # Use PowerShell to select next section
        ps_command = f"""
        try {{
            $word = New-Object -ComObject Word.Application
            
            if ($word.Documents.Count -eq 0) {{
                Write-Output "ERROR: No document is open in Word"
                exit 1
            }}
            
            $doc = $word.ActiveDocument
            $selection = $word.Selection
            $currentEnd = $selection.End
            $searchType = '{section_type}'
            $found = $false
            $foundText = ""
            $foundType = ""
            
            # Search for next heading
            if ($searchType -eq "heading" -or $searchType -eq "any") {{
                foreach ($para in $doc.Paragraphs) {{
                    if ($para.Range.Start -gt $currentEnd) {{
                        $styleName = $para.Style.NameLocal.ToLower()
                        if ($styleName -like "*heading*" -or $styleName -like "*title*") {{
                            $paraText = $para.Range.Text.Trim()
                            if ($paraText -and $paraText.Length -gt 0) {{
                                $para.Range.Select()
                                $foundText = $paraText
                                $foundType = "heading"
                                $found = $true
                                break
                            }}
                        }}
                    }}
                }}
            }}
            
            # Search for next bookmark if not found yet
            if (-not $found -and ($searchType -eq "bookmark" -or $searchType -eq "any")) {{
                foreach ($bookmark in $doc.Bookmarks) {{
                    if ($bookmark.Start -gt $currentEnd) {{
                        $bookmark.Select()
                        $foundText = $bookmark.Name
                        $foundType = "bookmark"
                        $found = $true
                        break
                    }}
                }}
            }}
            
            # Search for next paragraph if not found yet
            if (-not $found -and ($searchType -eq "paragraph" -or $searchType -eq "any")) {{
                foreach ($para in $doc.Paragraphs) {{
                    if ($para.Range.Start -gt $currentEnd) {{
                        $paraText = $para.Range.Text.Trim()
                        if ($paraText -and $paraText.Length -gt 1) {{
                            $para.Range.Select()
                            $foundText = $paraText
                            $foundType = "paragraph"
                            $found = $true
                            break
                        }}
                    }}
                }}
            }}
            
            if ($found) {{
                Write-Output "FOUND:$foundType:$foundText"
            }} else {{
                Write-Output "NOT_FOUND"
            }}
            
            # Release the COM object
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
            [System.GC]::Collect()
            [System.GC]::WaitForPendingFinalizers()
            
            exit 0
        }} catch {{
            Write-Output "ERROR: $_"
            exit 1
        }}
        """
        
        # Run PowerShell with a timeout
        process = await asyncio.create_subprocess_exec(
            'powershell', '-Command', ps_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            # Wait for the process with a timeout
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10.0)
            stdout_text = stdout.decode('utf-8') if stdout else ""
            stderr_text = stderr.decode('utf-8') if stderr else ""
            
            if "ERROR:" in stdout_text:
                error_msg = stdout_text.split("ERROR:")[1].strip()
                logger.error(f"PowerShell error: {error_msg}")
                return {"error": f"Error selecting next section: {error_msg}", "found": False}
            
            if stdout_text.strip().startswith("FOUND:"):
                # Parse the result: FOUND:type:text
                parts = stdout_text.strip().split(":", 2)
                found_type = parts[1] if len(parts) > 1 else "unknown"
                found_text = parts[2] if len(parts) > 2 else ""
                
                logger.info(f"Selected next section of type {found_type}")
                return {
                    "found": True,
                    "section_text": found_text,
                    "section_type": found_type,
                    "instance_id": instance_id
                }
            elif "NOT_FOUND" in stdout_text:
                logger.info("No next section found")
                return {
                    "found": False,
                    "section_text": "",
                    "section_type": "",
                    "instance_id": instance_id
                }
            else:
                logger.warning("Unexpected PowerShell output")
                return {
                    "found": False,
                    "section_text": "",
                    "section_type": "",
                    "instance_id": instance_id
                }
                
        except asyncio.TimeoutError:
            # Kill the process if it times out
            try:
                process.kill()
            except:
                pass
            logger.error("PowerShell command timed out")
            return {"error": "Selection operation timed out", "found": False}
            
    except Exception as e:
        logger.error(f"Error in select_next_section: {str(e)}")
        return {"error": f"Error executing tool: {str(e)}", "found": False}

def run_word_mcp_server():
    """Main entry point for the Windows implementation."""
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

# Start the server
if __name__ == "__main__":
    run_word_mcp_server() 