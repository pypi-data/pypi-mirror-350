"""
Model data sources for Ollama integration.

This module provides implementations for dictionary and stream data sources.
"""

from typing import Any, Dict, List, Optional, Union, AsyncIterator, Tuple
from pydantic import BaseModel
import json
import asyncio

from .base import ModelDataSource
from ..config import Config
from ..exceptions import DataSourceError

class DictDataSource(ModelDataSource):
    """Dictionary-based data source."""
    
    def __init__(self, source: Dict[str, Any], model_class: type = dict):
        """Initialize dictionary data source.
        
        Args:
            source: Source dictionary
            model_class: Class to use for model data
            
        Raises:
            DataSourceError: If source is invalid
        """
        if not isinstance(source, dict):
            raise DataSourceError("Source must be a dictionary")
        if model_class is not None and not isinstance(model_class, type):
            raise DataSourceError("Model class must be a type")
        self.source = source
        self.model_class = model_class if model_class is not None else dict
        
    async def get_data(self) -> Dict[str, Any]:
        """Get data from dictionary.
        
        Returns:
            Dictionary data
            
        Raises:
            DataSourceError: If data cannot be retrieved
        """
        try:
            return dict(self.source)
        except Exception as e:
            raise DataSourceError(f"Failed to get data: {str(e)}")
            
    async def save_data(self, data: Dict[str, Any]) -> None:
        """Save data to dictionary.
        
        Args:
            data: Data to save
            
        Raises:
            DataSourceError: If data cannot be saved
        """
        try:
            if not isinstance(data, dict):
                raise DataSourceError("Data must be a dictionary")
            self.source.clear()
            self.source.update(data)
        except Exception as e:
            raise DataSourceError(f"Failed to save data: {str(e)}")
            
    async def append(self, key: str, value: Any) -> None:
        """Append value to dictionary.
        
        Args:
            key: Dictionary key
            value: Value to append
            
        Raises:
            DataSourceError: If value cannot be appended
        """
        try:
            if not isinstance(key, str):
                raise DataSourceError("Key must be a string")
            self.source[key] = value
        except Exception as e:
            raise DataSourceError(f"Failed to append value: {str(e)}")
            
    async def extend(self, data: Dict[str, Any]) -> None:
        """Extend dictionary with data.
        
        Args:
            data: Data to extend with
            
        Raises:
            DataSourceError: If data cannot be extended
        """
        try:
            if not isinstance(data, dict):
                raise DataSourceError("Data must be a dictionary")
            self.source.update(data)
        except Exception as e:
            raise DataSourceError(f"Failed to extend data: {str(e)}")
            
    async def clear(self) -> None:
        """Clear dictionary.
        
        Raises:
            DataSourceError: If dictionary cannot be cleared
        """
        try:
            self.source.clear()
        except Exception as e:
            raise DataSourceError(f"Failed to clear data: {str(e)}")
            
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from dictionary.
        
        Args:
            key: Dictionary key
            default: Default value if key not found
            
        Returns:
            Value for key or default
            
        Raises:
            DataSourceError: If value cannot be retrieved
        """
        try:
            if not isinstance(key, str):
                raise DataSourceError("Key must be a string")
            return self.source.get(key, default)
        except Exception as e:
            raise DataSourceError(f"Failed to get value: {str(e)}")
            
    async def set(self, key: str, value: Any) -> None:
        """Set value in dictionary.
        
        Args:
            key: Dictionary key
            value: Value to set
            
        Raises:
            DataSourceError: If value cannot be set
        """
        try:
            if not isinstance(key, str):
                raise DataSourceError("Key must be a string")
            self.source[key] = value
        except Exception as e:
            raise DataSourceError(f"Failed to set value: {str(e)}")
            
    async def delete(self, key: str) -> None:
        """Delete value from dictionary.
        
        Args:
            key: Dictionary key
            
        Raises:
            DataSourceError: If value cannot be deleted
        """
        try:
            if not isinstance(key, str):
                raise DataSourceError("Key must be a string")
            if key not in self.source:
                raise DataSourceError(f"Key not found: {key}")
            del self.source[key]
        except Exception as e:
            raise DataSourceError(f"Failed to delete value: {str(e)}")
            
    async def has_key(self, key: str) -> bool:
        """Check if key exists in dictionary.
        
        Args:
            key: Dictionary key
            
        Returns:
            True if key exists, False otherwise
            
        Raises:
            DataSourceError: If key cannot be checked
        """
        try:
            if not isinstance(key, str):
                raise DataSourceError("Key must be a string")
            return key in self.source
        except Exception as e:
            raise DataSourceError(f"Failed to check key: {str(e)}")
            
    async def keys(self) -> List[str]:
        """Get dictionary keys.
        
        Returns:
            List of keys
            
        Raises:
            DataSourceError: If keys cannot be retrieved
        """
        try:
            return list(self.source.keys())
        except Exception as e:
            raise DataSourceError(f"Failed to get keys: {str(e)}")
            
    async def values(self) -> List[Any]:
        """Get dictionary values.
        
        Returns:
            List of values
            
        Raises:
            DataSourceError: If values cannot be retrieved
        """
        try:
            return list(self.source.values())
        except Exception as e:
            raise DataSourceError(f"Failed to get values: {str(e)}")
            
    async def items(self) -> List[Tuple[str, Any]]:
        """Get dictionary items.
        
        Returns:
            List of (key, value) pairs
            
        Raises:
            DataSourceError: If items cannot be retrieved
        """
        try:
            return list(self.source.items())
        except Exception as e:
            raise DataSourceError(f"Failed to get items: {str(e)}")
            
    async def size(self) -> int:
        """Get dictionary size.
        
        Returns:
            Number of items
            
        Raises:
            DataSourceError: If size cannot be retrieved
        """
        try:
            return len(self.source)
        except Exception as e:
            raise DataSourceError(f"Failed to get size: {str(e)}")
            
    async def is_empty(self) -> bool:
        """Check if dictionary is empty.
        
        Returns:
            True if empty, False otherwise
            
        Raises:
            DataSourceError: If emptiness cannot be checked
        """
        try:
            return len(self.source) == 0
        except Exception as e:
            raise DataSourceError(f"Failed to check emptiness: {str(e)}")

class StreamDataSource(ModelDataSource):
    """Stream data source implementation."""
    
    def __init__(
        self,
        source: AsyncIterator[Union[Dict[str, Any], BaseModel]],
        model_class: type[BaseModel],
        buffer_size: int = 100,
        config: Optional[Config] = None
    ):
        """Initialize the stream data source.
        
        Args:
            source: Async iterator of dictionaries or models
            model_class: Pydantic model class for validation
            buffer_size: Number of items to buffer
            config: Configuration instance
        """
        super().__init__(source, model_class, config)
        self.buffer_size = buffer_size
        self._buffer: List[BaseModel] = []
        self._iterator: Optional[AsyncIterator[BaseModel]] = None
    
    async def _get_next_batch(self) -> List[BaseModel]:
        """Get next batch of models from stream."""
        if self._iterator is None:
            self._iterator = self._iterate_models()
        
        batch = []
        try:
            for _ in range(self.buffer_size):
                model = await anext(self._iterator)
                batch.append(model)
        except StopAsyncIteration:
            pass
        
        return batch
    
    async def _iterate_models(self) -> AsyncIterator[BaseModel]:
        """Iterate over models from source."""
        async for item in self.source:
            try:
                if isinstance(item, BaseModel):
                    yield item
                else:
                    yield self.model_class(**item)
            except Exception as e:
                raise DataSourceError(f"Failed to process stream item: {str(e)}")
    
    async def get_data(self) -> List[str]:
        """Get model data from stream.
        
        Returns:
            List of JSON-serialized models
        """
        try:
            if not self._buffer:
                self._buffer = await self._get_next_batch()
            
            if not self._buffer:
                return []
            
            # Get one item from buffer
            model = self._buffer.pop(0)
            return [model.model_dump_json()]
        except Exception as e:
            raise DataSourceError(f"Failed to get stream data: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save model data to stream.
        
        Args:
            data: List of JSON-serialized models
            
        Returns:
            True if save was successful
            
        Raises:
            DataSourceError: Stream writing is not supported
        """
        raise DataSourceError("Stream writing is not supported") 