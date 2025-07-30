"""
Base data source module for Ollama integration.

This module provides the base classes and common functionality for data sources.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union, Protocol, Type
from datetime import datetime
from pydantic import BaseModel
from pathlib import Path
from typing import TextIO, BinaryIO, Iterator
import aiofiles
import json
import yaml
import os

from ..config import Config
from ..exceptions import DataSourceError

T = TypeVar('T')
V = TypeVar('V', bound=Union[str, int, float, bool, List, Dict])

class DataSource(ABC):
    """Base class for data sources."""

    def __init__(self, source: Optional[Any] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize data source.

        Args:
            source: Data source object
            config: Configuration dictionary
        """
        self.source = source
        self.config = config or {}

    @abstractmethod
    async def get_data(self) -> Any:
        """Get data from source.

        Returns:
            Data from source

        Raises:
            DataSourceError: If data cannot be retrieved
        """
        pass

    @abstractmethod
    async def save_data(self, data: Any) -> bool:
        """Save data to source.

        Args:
            data: Data to save

        Returns:
            True if data was saved successfully

        Raises:
            DataSourceError: If data cannot be saved
        """
        pass

class TextDataSource(DataSource):
    """Text data source."""

    def __init__(self, source: Optional[Union[str, Path]] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize text data source.

        Args:
            source: Path to text file
            config: Configuration dictionary
        """
        super().__init__(source, config)
        self.chunk_size = self.config.get("chunk_size", 1000)
        self.overlap = self.config.get("overlap", 100)

    async def get_data(self) -> List[str]:
        """Get text data from source.

        Returns:
            List of text chunks

        Raises:
            DataSourceError: If data cannot be retrieved
        """
        if not self.source:
            raise DataSourceError("No source specified")

        try:
            with open(self.source, "r", encoding="utf-8") as f:
                text = f.read()
            return self._chunk_text(text)
        except Exception as e:
            raise DataSourceError(f"Failed to read text file: {str(e)}")

    async def save_data(self, data: Union[str, List[str]]) -> bool:
        """Save text data to source.

        Args:
            data: Text data to save

        Returns:
            True if data was saved successfully

        Raises:
            DataSourceError: If data cannot be saved
        """
        if not self.source:
            raise DataSourceError("No source specified")

        try:
            if isinstance(data, list):
                data = "\n".join(data)
            with open(self.source, "w", encoding="utf-8") as f:
                f.write(data)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to write text file: {str(e)}")

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            if end < text_len:
                # Try to find a good break point
                break_point = text.rfind(" ", start + self.chunk_size - self.overlap, end)
                if break_point > start:
                    end = break_point + 1
            chunks.append(text[start:end])
            start = end - self.overlap

        return chunks

class BinaryDataSource(DataSource):
    """Binary data source."""

    def __init__(self, source: Optional[Union[str, Path]] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize binary data source.

        Args:
            source: Path to binary file
            config: Configuration dictionary
        """
        super().__init__(source, config)

    async def get_data(self) -> bytes:
        """Get binary data from source.

        Returns:
            Binary data

        Raises:
            DataSourceError: If data cannot be retrieved
        """
        if not self.source:
            raise DataSourceError("No source specified")

        try:
            with open(self.source, "rb") as f:
                return f.read()
        except Exception as e:
            raise DataSourceError(f"Failed to read binary file: {str(e)}")

    async def save_data(self, data: bytes) -> bool:
        """Save binary data to source.

        Args:
            data: Binary data to save

        Returns:
            True if data was saved successfully

        Raises:
            DataSourceError: If data cannot be saved
        """
        if not self.source:
            raise DataSourceError("No source specified")

        try:
            with open(self.source, "wb") as f:
                f.write(data)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to write binary file: {str(e)}")

class ModelDataSource(DataSource):
    """Model data source."""

    def __init__(self, source: Optional[Dict[str, Any]] = None, model_class: Optional[Type] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize model data source.

        Args:
            source: Model data dictionary
            model_class: Model class
            config: Configuration dictionary
        """
        super().__init__(source, config)
        self.model_class = model_class

    async def get_data(self) -> Any:
        """Get model data from source.

        Returns:
            Model instance

        Raises:
            DataSourceError: If data cannot be retrieved
        """
        if not self.source:
            raise DataSourceError("No source specified")

        if not self.model_class:
            raise DataSourceError("No model class specified")

        try:
            return self.model_class(**self.source)
        except Exception as e:
            raise DataSourceError(f"Failed to create model instance: {str(e)}")

    async def save_data(self, data: Any) -> bool:
        """Save model data to source.

        Args:
            data: Model instance to save

        Returns:
            True if data was saved successfully

        Raises:
            DataSourceError: If data cannot be saved
        """
        if not self.source:
            raise DataSourceError("No source specified")

        try:
            self.source.clear()
            self.source.update(data.dict())
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save model data: {str(e)}")

class FileDataSource(DataSource):
    """File-based data source."""
    
    def __init__(self, file_path: str, format: str = "text", **kwargs):
        """Initialize file data source.
        
        Args:
            file_path: Path to the file
            format: File format (text, json, yaml, binary)
            kwargs: Accept extra keyword arguments for compatibility
        Raises:
            DataSourceError: If file_path is invalid
        """
        if not isinstance(file_path, str) or not file_path:
            raise DataSourceError("File path must be a non-empty string")
        if not isinstance(format, str) or not format:
            raise DataSourceError("Format must be a non-empty string")
        if format not in ["text", "json", "yaml", "binary"]:
            raise DataSourceError(f"Unsupported format: {format}")
        self.file_path = file_path
        self.format = format
        # Accept and ignore extra kwargs for compatibility
        
    async def get_data(self) -> Any:
        """Get data from file.
        
        Returns:
            File contents based on format
            
        Raises:
            DataSourceError: If file cannot be read
        """
        try:
            if not os.path.exists(self.file_path):
                raise DataSourceError(f"File does not exist: {self.file_path}")
                
            if self.format == "text":
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return f.read()
            elif self.format == "json":
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            elif self.format == "yaml":
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            elif self.format == "binary":
                with open(self.file_path, "rb") as f:
                    return f.read()
        except Exception as e:
            raise DataSourceError(f"Failed to read file: {str(e)}")
            
    async def save_data(self, data: Any) -> None:
        """Save data to file.
        
        Args:
            data: Data to save
            
        Raises:
            DataSourceError: If data cannot be saved
        """
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            if self.format == "text":
                if not isinstance(data, str):
                    raise DataSourceError("Data must be a string for text format")
                with open(self.file_path, "w", encoding="utf-8") as f:
                    f.write(data)
            elif self.format == "json":
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            elif self.format == "yaml":
                with open(self.file_path, "w", encoding="utf-8") as f:
                    yaml.dump(data, f)
            elif self.format == "binary":
                if not isinstance(data, bytes):
                    raise DataSourceError("Data must be bytes for binary format")
                with open(self.file_path, "wb") as f:
                    f.write(data)
        except Exception as e:
            raise DataSourceError(f"Failed to save file: {str(e)}")

    load_data = get_data  # Alias for test compatibility

class MemoryDataSource(DataSource):
    """Memory data source."""

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize memory data source.

        Args:
            initial_data: Initial data dictionary
            config: Configuration dictionary
        """
        super().__init__(initial_data or {}, config)

    async def get_data(self) -> Dict[str, Any]:
        """Get data from memory.

        Returns:
            Data dictionary

        Raises:
            DataSourceError: If data cannot be retrieved
        """
        return self.source

    async def save_data(self, data: Dict[str, Any]) -> bool:
        """Save data to memory.

        Args:
            data: Data dictionary to save

        Returns:
            True if data was saved successfully

        Raises:
            DataSourceError: If data cannot be saved
        """
        try:
            self.source.clear()
            self.source.update(data)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save data to memory: {str(e)}")

class DictDataSource(DataSource):
    """Dictionary data source."""

    def __init__(self, source: Optional[Dict[str, Any]] = None, model_class: Optional[Type] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize dictionary data source.

        Args:
            source: Data dictionary
            model_class: Model class for data conversion
            config: Configuration dictionary
        """
        super().__init__(source or {}, config)
        self.model_class = model_class

    async def get_data(self) -> Any:
        """Get data from dictionary.

        Returns:
            Data or model instance

        Raises:
            DataSourceError: If data cannot be retrieved
        """
        if self.model_class:
            try:
                return self.model_class(**self.source)
            except Exception as e:
                raise DataSourceError(f"Failed to create model instance: {str(e)}")
        return self.source

    async def save_data(self, data: Any) -> bool:
        """Save data to dictionary.

        Args:
            data: Data or model instance to save

        Returns:
            True if data was saved successfully

        Raises:
            DataSourceError: If data cannot be saved
        """
        try:
            if self.model_class and isinstance(data, self.model_class):
                self.source.clear()
                self.source.update(data.dict())
            else:
                self.source.clear()
                self.source.update(data)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save data to dictionary: {str(e)}") 