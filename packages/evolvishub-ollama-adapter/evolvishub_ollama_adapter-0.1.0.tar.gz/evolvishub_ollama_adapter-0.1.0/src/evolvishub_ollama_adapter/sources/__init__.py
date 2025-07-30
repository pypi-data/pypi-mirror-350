"""
Data sources for Ollama integration.

This package provides implementations for various data sources:
- Text sources (plain text, markdown, code)
- Binary sources (PDF, images)
- Model sources (dictionary, stream)
- Ollama sources (responses, embeddings, chat)
"""

from .base import (
    DataSource,
    TextDataSource,
    BinaryDataSource,
    ModelDataSource,
    FileDataSource
)

from .text import (
    PlainTextDataSource,
    MarkdownDataSource,
    CodeDataSource
)

from .binary import (
    PDFDataSource,
    ImageDataSource
)

from .model import (
    DictDataSource,
    StreamDataSource
)

from .ollama import (
    OllamaResponse,
    OllamaEmbedding,
    OllamaChatMessage,
    OllamaChatHistory,
    OllamaResponseSource,
    OllamaEmbeddingSource,
    OllamaChatSource
)

from .memory import MemoryDataSource

__all__ = [
    # Base classes
    "DataSource",
    "TextDataSource",
    "BinaryDataSource",
    "ModelDataSource",
    
    # Text sources
    "PlainTextDataSource",
    "MarkdownDataSource",
    "CodeDataSource",
    
    # Binary sources
    "PDFDataSource",
    "ImageDataSource",
    
    # Model sources
    "DictDataSource",
    "StreamDataSource",
    
    # Ollama sources
    "OllamaResponse",
    "OllamaEmbedding",
    "OllamaChatMessage",
    "OllamaChatHistory",
    "OllamaResponseSource",
    "OllamaEmbeddingSource",
    "OllamaChatSource",
    
    # File source
    "FileDataSource",
    "MemoryDataSource"
] 