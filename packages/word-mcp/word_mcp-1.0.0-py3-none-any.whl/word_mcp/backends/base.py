"""
Abstract base class for Word backend implementations.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class WordInstance:
    """Represents a Word instance/document."""
    
    def __init__(self, instance_id: str, document_title: str, is_active: bool = False):
        self.instance_id = instance_id
        self.document_title = document_title
        self.is_active = is_active
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "document_title": self.document_title,
            "is_active": self.is_active
        }


class WordBackend(ABC):
    """Abstract base class for Word backend implementations."""
    
    def __init__(self):
        self.instances: List[WordInstance] = []
    
    @abstractmethod
    async def detect_instances(self) -> List[WordInstance]:
        """Detect and return all running Word instances."""
        pass
    
    @abstractmethod
    async def get_selection_text(self, instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Get the currently selected text from the specified Word instance."""
        pass
    
    @abstractmethod
    async def replace_selection_text(self, text: str, instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Replace the currently selected text in the specified Word instance."""
        pass
    
    @abstractmethod
    async def find_and_select_section(self, keywords: str, section_type: str = "any", instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Find and select a section in the document that contains the specified keywords."""
        pass
    
    @abstractmethod
    async def select_next_section(self, section_type: str = "any", instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Select the next section in the document after the current selection."""
        pass
    
    def get_target_instance_id(self, instance_id: Optional[str] = None) -> Optional[str]:
        """Get the target instance ID, defaulting to the active instance if not specified."""
        if instance_id:
            return instance_id
        
        # Find the active instance
        for instance in self.instances:
            if instance.is_active:
                return instance.instance_id
        
        # If no active instance, return the first one
        if self.instances:
            return self.instances[0].instance_id
        
        return None
    
    async def list_instances(self) -> Dict[str, Any]:
        """List all available Word instances."""
        await self.detect_instances()
        return {
            "instances": [instance.to_dict() for instance in self.instances]
        } 