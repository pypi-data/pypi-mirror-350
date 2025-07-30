"""Memory-based data source implementation."""

from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from .base import DataSource
from ..config import Config
from ..exceptions import DataSourceError

class MemoryDataSource(DataSource):
    """In-memory data source implementation."""
    
    def __init__(self, initial_data: Optional[dict] = None, config: Optional[dict] = None):
        """Initialize the memory data source.
        
        Args:
            initial_data: Optional initial data
            config: Configuration instance
        """
        super().__init__(initial_data or {}, config)
    
    async def get_data(self) -> dict:
        """Get data from memory.
        
        Returns:
            Data stored in memory
        """
        return self.source
    
    async def save_data(self, data: dict) -> bool:
        """Save data to memory.
        
        Args:
            data: Data to save
            
        Returns:
            True if save was successful
        """
        try:
            self.source.clear()
            self.source.update(data)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save data to memory: {str(e)}")
    
    def append(self, text: str) -> None:
        """Append text to memory.
        
        Args:
            text: Text to append
            
        Raises:
            DataSourceError: If text cannot be appended
        """
        try:
            self.source.append(text)
        except Exception as e:
            raise DataSourceError(f"Failed to append text to memory: {str(e)}")
    
    def extend(self, texts: List[str]) -> None:
        """Extend memory with multiple texts.
        
        Args:
            texts: List of texts to append
            
        Raises:
            DataSourceError: If texts cannot be appended
        """
        try:
            self.source.extend(texts)
        except Exception as e:
            raise DataSourceError(f"Failed to extend memory with texts: {str(e)}")
    
    def clear(self) -> None:
        """Clear memory.
        
        Raises:
            DataSourceError: If memory cannot be cleared
        """
        try:
            self.source.clear()
        except Exception as e:
            raise DataSourceError(f"Failed to clear memory: {str(e)}")
    
    def __len__(self) -> int:
        """Get the number of items in memory.
        
        Returns:
            Number of items
        """
        return len(self.source)
    
    def __getitem__(self, index: int) -> str:
        """Get an item from memory.
        
        Args:
            index: Item index
            
        Returns:
            Item from memory
            
        Raises:
            DataSourceError: If index is invalid
        """
        try:
            return self.source[index]
        except Exception as e:
            raise DataSourceError(f"Failed to get item from memory: {str(e)}")
    
    def __iter__(self) -> List[str]:
        """Iterate over items in memory.
        
        Returns:
            Iterator over items
        """
        return iter(self.source) 