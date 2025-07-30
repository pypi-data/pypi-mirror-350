"""
Text-based data sources for Ollama integration.

This module provides implementations for text, markdown, and code data sources.
"""

import json
from typing import Any, Dict, List, Optional, Union, TextIO, Iterator
from pathlib import Path
import markdown
import aiofiles

from .base import TextDataSource
from ..config import Config
from ..exceptions import DataSourceError

class PlainTextDataSource(TextDataSource):
    """Plain text data source implementation."""
    
    async def get_data(self) -> List[str]:
        """Get text chunks from source.
        
        Returns:
            List of text chunks
        """
        content = await self._load_content()
        return list(self._chunk_text(content))
    
    async def save_data(self, data: List[str]) -> bool:
        """Save text chunks to source.
        
        Args:
            data: List of text chunks
            
        Returns:
            True if save was successful
        """
        try:
            content = "\n".join(data)
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    await f.write(content)
            else:
                self.source.write(content)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save text: {str(e)}")

class MarkdownDataSource(TextDataSource):
    """Markdown data source implementation."""
    
    def __init__(
        self,
        source: Union[str, Path, TextIO],
        extract_code: bool = True,
        chunk_size: int = 1000,
        overlap: int = 100,
        config: Optional[Config] = None
    ):
        """Initialize the markdown data source.
        
        Args:
            source: Markdown source (file path or text stream)
            extract_code: Whether to extract code blocks
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
            config: Configuration instance
        """
        super().__init__(source, chunk_size, overlap, config)
        self.extract_code = extract_code
    
    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from markdown."""
        blocks = []
        in_code_block = False
        current_block = []
        
        for line in text.splitlines():
            if line.startswith("```"):
                if in_code_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
                in_code_block = not in_code_block
            elif in_code_block:
                current_block.append(line)
        
        return blocks
    
    async def get_data(self) -> List[str]:
        """Get markdown content from source.
        
        Returns:
            List of markdown sections or code blocks
        """
        content = await self._load_content()
        if self.extract_code:
            return self._extract_code_blocks(content)
        return list(self._chunk_text(content))
    
    async def save_data(self, data: List[str]) -> bool:
        """Save markdown content to source.
        
        Args:
            data: List of markdown sections
            
        Returns:
            True if save was successful
        """
        try:
            content = "\n\n".join(data)
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    await f.write(content)
            else:
                self.source.write(content)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save markdown: {str(e)}")

class CodeDataSource(TextDataSource):
    """Code file data source implementation."""
    
    def __init__(
        self,
        source: Union[str, Path, TextIO],
        language: Optional[str] = None,
        chunk_size: int = 1000,
        overlap: int = 100,
        config: Optional[Config] = None
    ):
        """Initialize the code data source.
        
        Args:
            source: Code source (file path or text stream)
            language: Programming language
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
            config: Configuration instance
        """
        super().__init__(source, chunk_size, overlap, config)
        self.language = language or self._detect_language()
    
    def _detect_language(self) -> str:
        """Detect programming language from file extension."""
        if isinstance(self.source, (str, Path)):
            ext = Path(self.source).suffix.lower()
            # Map common extensions to languages
            ext_map = {
                ".py": "python",
                ".js": "javascript",
                ".ts": "typescript",
                ".java": "java",
                ".cpp": "cpp",
                ".c": "c",
                ".go": "go",
                ".rs": "rust",
                ".rb": "ruby",
                ".php": "php",
                ".swift": "swift",
                ".kt": "kotlin",
                ".scala": "scala",
                ".hs": "haskell",
                ".lua": "lua",
                ".sh": "shell",
                ".sql": "sql",
            }
            return ext_map.get(ext, "text")
        return "text"
    
    async def get_data(self) -> List[str]:
        """Get code content from source.
        
        Returns:
            List of code blocks
        """
        try:
            content = await self._load_content()
            # Format code for Ollama
            return [f"```{self.language}\n{content}\n```"]
        except Exception as e:
            raise DataSourceError(f"Failed to read code: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save code content to source.
        
        Args:
            data: List of code blocks
            
        Returns:
            True if save was successful
        """
        try:
            if not data:
                return False
                
            # Extract code from Ollama format
            code = data[0]
            if code.startswith("```") and code.endswith("```"):
                code = code[code.find("\n") + 1:code.rfind("\n")]
            
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    await f.write(code)
            else:
                self.source.write(code)
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save code: {str(e)}") 