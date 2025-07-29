"""
macOS-specific Word backend implementation using AppleScript.
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Optional, Any
from .base import WordBackend, WordInstance

logger = logging.getLogger(__name__)


class MacOSWordBackend(WordBackend):
    """macOS-specific implementation of Word backend using AppleScript."""
    
    def __init__(self):
        super().__init__()
        # Track which paragraphs have been processed to avoid infinite loops
        self._processed_paragraphs = set()
        self._last_document_hash = None
    
    async def _get_document_hash(self) -> str:
        """Get a simple hash of the document structure to detect document changes."""
        try:
            applescript = '''
            tell application "Microsoft Word"
                if (count of documents) > 0 then
                    tell active document
                        set docName to name of document 1
                        return docName
                    end tell
                else
                    return "NO_DOC"
                end if
            end tell
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', applescript,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                return stdout.decode('utf-8').strip()
            else:
                return "ERROR"
        except:
            return "ERROR"
    
    async def _reset_state_if_document_changed(self):
        """Reset processing state if document has changed."""
        current_hash = await self._get_document_hash()
        if current_hash != self._last_document_hash:
            self._processed_paragraphs.clear()
            self._last_document_hash = current_hash
            logger.info(f"Document changed, reset processing state. Hash: {current_hash}")
    
    async def detect_instances(self) -> List[WordInstance]:
        """Detect running Word instances using AppleScript."""
        logger.info("Detecting Word instances on macOS")
        
        self.instances = []
        
        try:
            # Use AppleScript to get Word document information
            applescript = '''
            tell application "System Events"
                set wordRunning to (name of processes) contains "Microsoft Word"
            end tell
            
            if wordRunning then
                tell application "Microsoft Word"
                    set docCount to count of documents
                    if docCount > 0 then
                        set docList to {}
                        repeat with i from 1 to docCount
                            set docName to name of document i
                            set end of docList to docName
                        end repeat
                        return docList as string
                    else
                        return "NO_DOCS"
                    end if
                end tell
            else
                return "NOT_RUNNING"
            end if
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', applescript,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            output = stdout.decode('utf-8').strip()
            
            if output == "NOT_RUNNING":
                logger.info("Microsoft Word is not running")
                return self.instances
            elif output == "NO_DOCS":
                logger.info("Microsoft Word is running but no documents are open")
                # Add a placeholder instance for the running application
                self.instances.append(WordInstance(
                    instance_id="word-macos-1",
                    document_title="Microsoft Word (no documents)",
                    is_active=True
                ))
                return self.instances
            else:
                # Parse document names (comma-separated)
                doc_names = [name.strip() for name in output.split(',') if name.strip()]
                for i, doc_name in enumerate(doc_names):
                    self.instances.append(WordInstance(
                        instance_id=f"word-macos-{i+1}",
                        document_title=doc_name,
                        is_active=(i == 0)  # Mark the first document as active
                    ))
                
                logger.info(f"Found {len(self.instances)} Word documents")
                return self.instances
        
        except Exception as e:
            logger.error(f"Error detecting Word instances on macOS: {str(e)}")
            return self.instances
    
    async def get_selection_text(self, instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Get the currently selected text from the specified Word instance."""
        logger.info(f"Getting selection text for instance: {instance_id}")
        
        target_instance_id = self.get_target_instance_id(instance_id)
        if not target_instance_id:
            return {"error": "No Word instances found"}
        
        try:
            # Use correct AppleScript syntax for Word selection
            applescript = '''
            tell application "Microsoft Word"
                if (count of documents) > 0 then
                    try
                        set currentSel to selection
                        set selectionText to content of text object of currentSel
                        
                        -- Handle missing value case
                        if selectionText is missing value then
                            return "(no text selected)"
                        else
                            return selectionText
                        end if
                    on error errMsg
                        return "ERROR: " & errMsg
                    end try
                else
                    return "ERROR: No document is open"
                end if
            end tell
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', applescript,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8').strip()
                logger.error(f"AppleScript error: {error_msg}")
                return {"error": f"Error getting selection text: {error_msg}"}
            
            selected_text = stdout.decode('utf-8').strip()
            
            if selected_text.startswith("ERROR:"):
                return {"error": selected_text}
            
            return {
                "text": selected_text,
                "instance_id": target_instance_id
            }
        
        except Exception as e:
            logger.error(f"Error getting selection text on macOS: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}"}
    
    async def replace_selection_text(self, text: str, instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Replace the currently selected text in the specified Word instance."""
        logger.info(f"Replacing selection text for instance: {instance_id}")
        
        target_instance_id = self.get_target_instance_id(instance_id)
        if not target_instance_id:
            return {"error": "No Word instances found"}
        
        try:
            # Escape the text for AppleScript
            escaped_text = text.replace('"', '\\"').replace('\\', '\\\\')
            
            # Use very simple AppleScript - just replace the text
            applescript = f'''
            tell application "Microsoft Word"
                if (count of documents) > 0 then
                    try
                        -- Better approach: Delete selection and type new text for proper newline handling
                        set currentSel to selection
                        if (content of text object of currentSel) is not missing value then
                            delete currentSel
                        end if
                        type text "{escaped_text}"
                        return "SUCCESS"
                    on error errMsg
                        return "ERROR:" & errMsg
                    end try
                else
                    return "ERROR: No document is open"
                end if
            end tell
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', applescript,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8').strip()
                logger.error(f"AppleScript error: {error_msg}")
                return {"error": f"Error replacing selection text: {error_msg}", "success": False}
            
            result = stdout.decode('utf-8').strip()
            
            if result.startswith("ERROR:"):
                return {"error": result, "success": False}
            elif result == "SUCCESS":
                # After successful replacement, ensure state consistency
                logger.info(f"Text replaced successfully. Processed paragraphs count: {len(self._processed_paragraphs)}")
                return {"success": True, "instance_id": target_instance_id}
            else:
                return {"success": True, "instance_id": target_instance_id}
        
        except Exception as e:
            logger.error(f"Error replacing selection text on macOS: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}", "success": False}
    
    async def find_and_select_section(self, keywords: str, section_type: str = "any", instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Find and select a section in the document that contains the specified keywords."""
        logger.info(f"Finding and selecting section with keywords: {keywords}, type: {section_type}")
        
        target_instance_id = self.get_target_instance_id(instance_id)
        if not target_instance_id:
            return {"error": "No Word instances found", "found": False}
        
        valid_types = ["heading", "paragraph", "bookmark", "any"]
        if section_type not in valid_types:
            return {"error": f"Invalid section_type. Must be one of: {valid_types}", "found": False}
        
        try:
            # Escape keywords for AppleScript
            escaped_keywords = keywords.replace('"', '\\"').replace('\\', '\\\\')
            
            # Use AppleScript to find and select the section
            applescript = f'''
            tell application "Microsoft Word"
                if (count of documents) > 0 then
                    set targetDoc to active document
                    set searchKeywords to "{escaped_keywords}"
                    set searchType to "{section_type}"
                    
                    -- Search in the document
                    set findResult to false
                    set foundText to ""
                    set foundType to ""
                    
                    -- For now, implement a simple text search
                    try
                        set searchRange to text object of targetDoc
                        tell searchRange
                            clear formatting of find object
                            set content of find object to searchKeywords
                            set match case of find object to false
                            if execute find find object then
                                select searchRange
                                set findResult to true
                                set foundText to content of searchRange
                                set foundType to "paragraph"
                            end if
                        end tell
                    end try
                    
                    if findResult then
                        return "FOUND:" & foundType & ":" & foundText
                    else
                        return "NOT_FOUND"
                    end if
                else
                    return "ERROR: No document is open"
                end if
            end tell
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', applescript,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8').strip()
                logger.error(f"AppleScript error: {error_msg}")
                return {"error": f"Error finding section: {error_msg}", "found": False}
            
            result = stdout.decode('utf-8').strip()
            
            if result.startswith("ERROR:"):
                return {"error": result, "found": False}
            elif result.startswith("FOUND:"):
                # Parse the result: FOUND:type:text
                parts = result.split(":", 2)
                found_type = parts[1] if len(parts) > 1 else "unknown"
                found_text = parts[2] if len(parts) > 2 else ""
                
                return {
                    "found": True,
                    "section_text": found_text,
                    "section_type": found_type,
                    "instance_id": target_instance_id
                }
            elif result == "NOT_FOUND":
                return {
                    "found": False,
                    "section_text": "",
                    "section_type": "",
                    "instance_id": target_instance_id
                }
            else:
                return {
                    "found": False,
                    "section_text": "",
                    "section_type": "",
                    "instance_id": target_instance_id
                }
        
        except Exception as e:
            logger.error(f"Error finding section on macOS: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}", "found": False}
    
    async def select_next_section(self, section_type: str = "any", instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Select the next section in the document after the current selection."""
        logger.info(f"Selecting next section of type: {section_type}")
        
        target_instance_id = self.get_target_instance_id(instance_id)
        if not target_instance_id:
            return {"error": "No Word instances found", "found": False}
        
        valid_types = ["heading", "paragraph", "bookmark", "any"]
        if section_type not in valid_types:
            return {"error": f"Invalid section_type. Must be one of: {valid_types}", "found": False}
        
        try:
            # Reset state if document has changed
            await self._reset_state_if_document_changed()
            
            # Get total paragraph count first
            count_script = '''
            tell application "Microsoft Word"
                if (count of documents) > 0 then
                    tell active document
                        return count of paragraphs
                    end tell
                else
                    return 0
                end if
            end tell
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', count_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                return {"error": "Could not get paragraph count", "found": False}
            
            try:
                total_paragraphs = int(stdout.decode('utf-8').strip())
            except ValueError:
                return {"error": "Invalid paragraph count", "found": False}
            
            logger.info(f"Document has {total_paragraphs} paragraphs, processed: {len(self._processed_paragraphs)}")
            
            # Now check each paragraph individually
            for para_index in range(1, total_paragraphs + 1):
                if para_index in self._processed_paragraphs:
                    continue
                
                # Get content of this specific paragraph
                content_script = f'''
                tell application "Microsoft Word"
                    if (count of documents) > 0 then
                        tell active document
                            try
                                set targetPara to paragraph {para_index}
                                set paraContent to content of text object of targetPara
                                if paraContent is missing value then
                                    return "MISSING"
                                else
                                    return paraContent
                                end if
                            on error
                                return "ERROR"
                            end try
                        end tell
                    else
                        return "NO_DOC"
                    end if
                end tell
                '''
                
                process = await asyncio.create_subprocess_exec(
                    'osascript', '-e', content_script,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    continue
                
                content = stdout.decode('utf-8').strip()
                
                if content in ["MISSING", "ERROR", "NO_DOC"] or len(content) <= 10:
                    continue
                
                # Check if this paragraph is English and untranslated
                is_english = self._is_english_content(content)
                is_translated = self._is_translated_content(content)
                
                if is_english and not is_translated:
                    # Mark as processed and select this paragraph
                    self._processed_paragraphs.add(para_index)
                    
                    # Select the paragraph in Word
                    success = await self._select_paragraph_by_index(para_index)
                    if success:
                        logger.info(f"Selected paragraph {para_index}: '{content[:50]}...'. Total processed: {len(self._processed_paragraphs)}")
                        return {
                            "found": True,
                            "section_text": content,
                            "section_type": "paragraph",
                            "instance_id": target_instance_id
                        }
            
            # No more untranslated paragraphs found
            return {
                "found": False,
                "reason": f"No more untranslated English paragraphs found. Processed: {len(self._processed_paragraphs)}/{total_paragraphs}",
                "instance_id": target_instance_id
            }
        
        except Exception as e:
            logger.error(f"Error selecting next section on macOS: {str(e)}")
            return {"error": f"Error executing tool: {str(e)}", "found": False}
    
    def _is_english_content(self, content: str) -> bool:
        """Check if content appears to be primarily English."""
        english_words = ["the ", "and ", "of ", "to ", "in ", "for ", "with ", "by ", "at ", "on ", "from ", "up ", "about ", "into ", "through ", "during ", "before ", "after ", "above ", "below ", "between "]
        content_lower = content.lower()
        
        english_count = sum(1 for word in english_words if word in content_lower)
        return english_count >= 2  # Must have at least 2 common English words
    
    def _is_translated_content(self, content: str) -> bool:
        """Check if content appears to be translated (contains Chinese or translation markers)."""
        # Check for explicit markers
        if "[中文翻译]" in content or "[TRANSLATED]" in content:
            return True
        
        # Check for common Chinese characters/words
        chinese_indicators = ["我们", "的", "在", "与", "为", "通过", "技术", "数据", "项目", "和", "是", "有", "可以", "将", "这", "那", "等"]
        
        for indicator in chinese_indicators:
            if indicator in content:
                return True
        
        return False
    
    async def _select_paragraph_by_index(self, para_index: int) -> bool:
        """Select a specific paragraph by its index."""
        try:
            applescript = f'''
            tell application "Microsoft Word"
                if (count of documents) > 0 then
                    tell active document
                        try
                            set targetPara to paragraph {para_index}
                            select text object of targetPara
                            return "SUCCESS"
                        on error errMsg
                            return "ERROR:" & errMsg
                        end try
                    end tell
                else
                    return "ERROR: No document is open"
                end if
            end tell
            '''
            
            process = await asyncio.create_subprocess_exec(
                'osascript', '-e', applescript,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                result = stdout.decode('utf-8').strip()
                return result == "SUCCESS"
            else:
                logger.error(f"Error selecting paragraph {para_index}: {stderr.decode('utf-8').strip()}")
                return False
                
        except Exception as e:
            logger.error(f"Exception selecting paragraph {para_index}: {str(e)}")
            return False 