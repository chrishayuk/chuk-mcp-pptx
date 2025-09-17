"""
Presentation Manager for PowerPoint MCP Server

Manages PowerPoint presentations with support for virtual filesystem integration.
Each presentation can be auto-saved to VFS for persistence and multi-server access.
"""
import base64
import io
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from pptx import Presentation

logger = logging.getLogger(__name__)


class PresentationManager:
    """
    Manages PowerPoint presentations with optional VFS integration.
    
    This manager can work in two modes:
    1. In-memory mode: Presentations stored in memory (default)
    2. VFS mode: Presentations auto-saved to virtual filesystem
    """
    
    def __init__(self, use_vfs: bool = False, vfs_base_path: str = "vfs://presentations"):
        """
        Initialize the presentation manager.
        
        Args:
            use_vfs: Whether to use virtual filesystem for persistence
            vfs_base_path: Base path in VFS for storing presentations
        """
        self.use_vfs = use_vfs
        self.vfs_base_path = vfs_base_path
        self._presentations: Dict[str, Presentation] = {}
        self._current_presentation: Optional[str] = None
        self._vfs_client = None  # Will be initialized if VFS is enabled
        
        if use_vfs:
            self._init_vfs()
    
    def _init_vfs(self):
        """Initialize VFS client connection."""
        # This would connect to the VFS MCP server
        # For now, we'll keep it as a placeholder
        logger.info(f"VFS mode enabled with base path: {self.vfs_base_path}")
    
    def _get_vfs_path(self, name: str) -> str:
        """Get the VFS path for a presentation."""
        return f"{self.vfs_base_path}/{name}.pptx"
    
    def _save_to_vfs(self, name: str, prs: Presentation) -> bool:
        """
        Save presentation to VFS.
        
        Args:
            name: Presentation name
            prs: Presentation object
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_vfs:
            return True
            
        try:
            # Convert presentation to base64
            buffer = io.BytesIO()
            prs.save(buffer)
            buffer.seek(0)
            data = base64.b64encode(buffer.read()).decode('utf-8')
            
            # In a real implementation, this would call the VFS MCP server
            # For example: vfs_write(path=self._get_vfs_path(name), content=data)
            logger.info(f"Would save to VFS: {self._get_vfs_path(name)}")
            return True
        except Exception as e:
            logger.error(f"Failed to save to VFS: {e}")
            return False
    
    def _load_from_vfs(self, name: str) -> Optional[Presentation]:
        """
        Load presentation from VFS.
        
        Args:
            name: Presentation name
            
        Returns:
            Presentation object or None if not found
        """
        if not self.use_vfs:
            return None
            
        try:
            # In a real implementation, this would call the VFS MCP server
            # For example: data = vfs_read(path=self._get_vfs_path(name))
            logger.info(f"Would load from VFS: {self._get_vfs_path(name)}")
            return None
        except Exception as e:
            logger.error(f"Failed to load from VFS: {e}")
            return None
    
    def create(self, name: str) -> str:
        """Create a new presentation."""
        prs = Presentation()
        self._presentations[name] = prs
        self._current_presentation = name
        
        # Auto-save to VFS if enabled
        self._save_to_vfs(name, prs)
        
        return f"Created presentation '{name}'"
    
    def get(self, name: Optional[str] = None) -> Optional[Presentation]:
        """
        Get a presentation by name.
        
        Args:
            name: Presentation name (uses current if not specified)
            
        Returns:
            Presentation object or None if not found
        """
        pres_name = name or self._current_presentation
        if not pres_name:
            return None
            
        # Check memory first
        if pres_name in self._presentations:
            return self._presentations[pres_name]
        
        # Try loading from VFS if enabled
        if self.use_vfs:
            prs = self._load_from_vfs(pres_name)
            if prs:
                self._presentations[pres_name] = prs
                return prs
        
        return None
    
    def save(self, name: Optional[str] = None) -> bool:
        """
        Save presentation to VFS (if enabled).
        
        Args:
            name: Presentation name (uses current if not specified)
            
        Returns:
            True if successful, False otherwise
        """
        pres_name = name or self._current_presentation
        if not pres_name or pres_name not in self._presentations:
            return False
            
        return self._save_to_vfs(pres_name, self._presentations[pres_name])
    
    def update(self, name: Optional[str] = None) -> bool:
        """
        Update presentation in VFS after modifications.
        
        This should be called after any modification to ensure VFS persistence.
        
        Args:
            name: Presentation name (uses current if not specified)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_vfs:
            return True
            
        pres_name = name or self._current_presentation
        if not pres_name or pres_name not in self._presentations:
            return False
            
        return self._save_to_vfs(pres_name, self._presentations[pres_name])
    
    def delete(self, name: str) -> bool:
        """
        Delete a presentation from memory and VFS.
        
        Args:
            name: Presentation name
            
        Returns:
            True if successful, False otherwise
        """
        if name not in self._presentations:
            return False
            
        del self._presentations[name]
        
        # Update current if we deleted it
        if self._current_presentation == name:
            self._current_presentation = next(iter(self._presentations), None) if self._presentations else None
        
        # Delete from VFS if enabled
        if self.use_vfs:
            # In a real implementation: vfs_delete(path=self._get_vfs_path(name))
            logger.info(f"Would delete from VFS: {self._get_vfs_path(name)}")
        
        return True
    
    def list_presentations(self) -> Dict[str, int]:
        """
        List all presentations with slide counts.
        
        Returns:
            Dictionary mapping presentation names to slide counts
        """
        result = {}
        
        # List from memory
        for name, prs in self._presentations.items():
            result[name] = len(prs.slides)
        
        # In VFS mode, we could also list from VFS directory
        if self.use_vfs:
            # In a real implementation: vfs_list(path=self.vfs_base_path)
            pass
        
        return result
    
    def set_current(self, name: str) -> bool:
        """
        Set the current presentation.
        
        Args:
            name: Presentation name
            
        Returns:
            True if successful, False if presentation not found
        """
        if name not in self._presentations:
            # Try loading from VFS
            if self.use_vfs:
                prs = self._load_from_vfs(name)
                if prs:
                    self._presentations[name] = prs
                else:
                    return False
            else:
                return False
        
        self._current_presentation = name
        return True
    
    def get_current_name(self) -> Optional[str]:
        """Get the name of the current presentation."""
        return self._current_presentation
    
    def export_base64(self, name: Optional[str] = None) -> Optional[str]:
        """
        Export presentation as base64.
        
        Args:
            name: Presentation name (uses current if not specified)
            
        Returns:
            Base64-encoded presentation data or None
        """
        prs = self.get(name)
        if not prs:
            return None
            
        try:
            buffer = io.BytesIO()
            prs.save(buffer)
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to export as base64: {e}")
            return None
    
    def import_base64(self, data: str, name: str) -> bool:
        """
        Import presentation from base64.
        
        Args:
            data: Base64-encoded presentation data
            name: Name for the imported presentation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            buffer = io.BytesIO(base64.b64decode(data))
            prs = Presentation(buffer)
            self._presentations[name] = prs
            self._current_presentation = name
            
            # Auto-save to VFS if enabled
            self._save_to_vfs(name, prs)
            
            return True
        except Exception as e:
            logger.error(f"Failed to import from base64: {e}")
            return False
    
    def clear_all(self):
        """Clear all presentations from memory."""
        self._presentations.clear()
        self._current_presentation = None
        
        # Note: This doesn't delete from VFS, only clears memory
        # VFS presentations can still be loaded on demand