"""File-based data source implementation."""

from typing import Any, Dict, List, Optional, Union, TextIO, Iterator
from pathlib import Path
import aiofiles

from .base import DataSource
from ..config import Config
from ..exceptions import DataSourceError
from ..file_utils import (
    is_text_file,
    is_image_file,
    is_binary_file,
    read_file_content,
    read_binary_file
)

class FileDataSource(DataSource):
    """Generic file data source implementation."""
    
    def __init__(
        self,
        source: Union[str, Path],
        chunk_size: int = 1000,
        overlap: int = 100,
        config: Optional[Config] = None
    ):
        """Initialize the file data source.
        
        Args:
            source: File path
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
            config: Configuration instance
        """
        super().__init__(source, chunk_size, overlap, config)
        if not isinstance(source, (str, Path)):
            raise DataSourceError("FileDataSource requires a file path")
    
    async def get_data(self) -> List[str]:
        """Get content from file.
        
        Returns:
            List of content chunks
            
        Raises:
            DataSourceError: If file cannot be read
        """
        try:
            if is_text_file(self.source):
                content = read_file_content(self.source)
                return list(self._chunk_text(content))
            elif is_image_file(self.source):
                # For images, return the file path as a single chunk
                return [str(self.source)]
            elif is_binary_file(self.source):
                # For binary files, read as bytes and convert to base64
                content = read_binary_file(self.source)
                return [content.decode("utf-8")]
            else:
                raise DataSourceError(f"Unsupported file type: {self.source}")
        except Exception as e:
            raise DataSourceError(f"Failed to read file: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save content to file.
        
        Args:
            data: List of content chunks
            
        Returns:
            True if save was successful
            
        Raises:
            DataSourceError: If file cannot be written
        """
        try:
            if is_text_file(self.source):
                content = "\n".join(data)
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    await f.write(content)
            elif is_image_file(self.source):
                # For images, we don't support writing back
                raise DataSourceError("Writing to image files is not supported")
            elif is_binary_file(self.source):
                # For binary files, write raw bytes
                content = data[0].encode("utf-8")
                async with aiofiles.open(self.source, mode="wb") as f:
                    await f.write(content)
            else:
                raise DataSourceError(f"Unsupported file type: {self.source}")
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to write file: {str(e)}")
    
    def _chunk_text(self, text: str) -> Iterator[str]:
        """Split text into chunks.
        
        Args:
            text: Text to split
            
        Yields:
            Text chunks
        """
        if not text:
            return
        
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            if end < text_len:
                # Try to find a good breaking point
                break_point = text.rfind(" ", start, end)
                if break_point > start:
                    end = break_point
            
            yield text[start:end].strip()
            start = end - self.overlap if end < text_len else end 