"""
Custom exceptions for the Ollama adapter.
"""

class OllamaError(Exception):
    """Base exception for Ollama adapter errors."""
    pass

class DataSourceError(OllamaError):
    """Exception raised for data source errors."""
    pass

class ConfigurationError(OllamaError):
    """Exception raised for configuration errors."""
    pass

# Alias for ConfigurationError
OllamaConfigError = ConfigurationError

class ValidationError(OllamaError):
    """Exception raised for validation errors."""
    pass

# Alias for ValidationError
OllamaValidationError = ValidationError

class APIError(OllamaError):
    """Exception raised for API errors."""
    pass

class ModelError(OllamaError):
    """Exception raised for model-related errors."""
    pass

class OllamaConnectionError(OllamaError):
    """Raised when there is an error connecting to the Ollama server."""
    pass

class OllamaTimeoutError(OllamaError):
    """Raised when a request to the Ollama server times out."""
    pass

class OllamaModelError(OllamaError):
    """Raised when there is an error with the model configuration or response."""
    pass

class DataSourceFormatError(DataSourceError):
    """Raised when there is an error with the data format."""
    pass

class DataSourceIOError(DataSourceError):
    """Raised when there is an error reading from or writing to a data source."""
    pass

class DataSourceValidationError(DataSourceError):
    """Raised when data validation fails."""
    pass

class DatabaseError(OllamaError):
    """Exception raised for database-related errors."""
    pass

class CacheError(OllamaError):
    """Exception raised for cache-related errors."""
    pass

class FileError(OllamaError):
    """Exception raised for file-related errors."""
    pass

class ImageError(OllamaError):
    """Exception raised for image-related errors."""
    pass

class TextError(OllamaError):
    """Exception raised for text-related errors."""
    pass 