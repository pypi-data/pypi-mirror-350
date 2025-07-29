"""
Factory module for creating platform-specific Word backend instances.
"""

import sys
import logging
from typing import Type
from .base import WordBackend
from .windows import WindowsWordBackend
from .macos import MacOSWordBackend

logger = logging.getLogger(__name__)


def get_word_backend() -> WordBackend:
    """
    Factory function that returns the appropriate Word backend for the current platform.
    
    Returns:
        WordBackend: Platform-specific Word backend instance
        
    Raises:
        NotImplementedError: If the current platform is not supported
    """
    platform = sys.platform.lower()
    
    if platform == 'win32':
        logger.info("Creating Windows Word backend")
        return WindowsWordBackend()
    elif platform == 'darwin':
        logger.info("Creating macOS Word backend")
        return MacOSWordBackend()
    else:
        raise NotImplementedError(f"Platform '{platform}' is not supported. Only Windows (win32) and macOS (darwin) are supported.")


def get_backend_class() -> Type[WordBackend]:
    """
    Returns the appropriate Word backend class for the current platform.
    
    Returns:
        Type[WordBackend]: Platform-specific Word backend class
        
    Raises:
        NotImplementedError: If the current platform is not supported
    """
    platform = sys.platform.lower()
    
    if platform == 'win32':
        return WindowsWordBackend
    elif platform == 'darwin':
        return MacOSWordBackend
    else:
        raise NotImplementedError(f"Platform '{platform}' is not supported. Only Windows (win32) and macOS (darwin) are supported.")


def is_platform_supported() -> bool:
    """
    Check if the current platform is supported.
    
    Returns:
        bool: True if the platform is supported, False otherwise
    """
    platform = sys.platform.lower()
    return platform in ['win32', 'darwin']


def get_platform_name() -> str:
    """
    Get a human-readable name for the current platform.
    
    Returns:
        str: Platform name
    """
    platform = sys.platform.lower()
    
    if platform == 'win32':
        return "Windows"
    elif platform == 'darwin':
        return "macOS"
    else:
        return f"Unsupported ({platform})" 