"""
Evolvishub Ollama Adapter - A Python library for interacting with Ollama.
"""

from .config import Config
from .exceptions import (
    OllamaError,
    DataSourceError,
    ConfigurationError,
    ValidationError,
    APIError,
    ModelError,
)
from .ollama.models import (
    GenerateRequest,
    GenerateResponse,
    ModelInfo,
    ModelList,
)
from .sources import (
    DataSource,
    DictDataSource,
    StreamDataSource,
    ModelDataSource,
    TextDataSource,
    PlainTextDataSource,
    MarkdownDataSource,
    PDFDataSource,
    ImageDataSource,
    CodeDataSource,
)
from .logging import setup_logging, get_logger
from .client import OllamaClient

__version__ = "0.1.0"

__all__ = [
    "OllamaClient",
    "Config",
    "OllamaError",
    "DataSourceError",
    "ConfigurationError",
    "ValidationError",
    "APIError",
    "ModelError",
    "GenerateRequest",
    "GenerateResponse",
    "ModelInfo",
    "ModelList",
    "DataSource",
    "DictDataSource",
    "StreamDataSource",
    "ModelDataSource",
    "TextDataSource",
    "PlainTextDataSource",
    "MarkdownDataSource",
    "PDFDataSource",
    "ImageDataSource",
    "CodeDataSource",
    "setup_logging",
    "get_logger",
] 