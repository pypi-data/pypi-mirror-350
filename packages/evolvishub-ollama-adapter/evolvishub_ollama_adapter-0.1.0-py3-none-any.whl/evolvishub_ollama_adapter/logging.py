"""
Logging configuration for the Ollama adapter.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional, Dict, Any

from .config import Config
from .exceptions import ConfigurationError

def setup_logging(config: Optional[Dict[str, Any]] = None, level=None, format=None, file=None, max_size=None, backup_count=None) -> None:
    """Set up logging configuration.
    
    Args:
        config: Configuration dictionary with logging settings.
            If None, uses default configuration.
        level: Logging level (overrides config)
        format: Logging format (overrides config)
        file: Log file path (overrides config)
        max_size: Max log file size (overrides config)
        backup_count: Log file backup count (overrides config)
        
    Raises:
        ConfigurationError: If logging setup fails
    """
    try:
        # Get logging configuration
        log_level = (level or (config.get("level") if config else "INFO")).upper()
        log_format = (format or (config.get("format") if config else "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        log_file = (file or (config.get("file") if config else "logs/ollama.log"))
        max_bytes = (max_size or (config.get("max_size") if config else 10485760))  # 10MB
        backup_count = (backup_count or (config.get("backup_count") if config else 5))
        
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level not in valid_levels:
            raise ValueError(f"Invalid logging level: {log_level}")
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level))
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(console_handler)
        
    except Exception as e:
        raise ConfigurationError(f"Failed to set up logging: {str(e)}")

# Alias for setup_logging
configure_logging = setup_logging

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

def set_log_level(level: str) -> None:
    """Set logging level.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Raises:
        ValueError: If level is invalid
    """
    if not isinstance(level, str):
        raise ValueError("Level must be a string")
    if level.upper() not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid logging level: {level}")
        
    logging.getLogger().setLevel(getattr(logging, level.upper()))
    
def set_log_format(format: str) -> None:
    """Set logging format.
    
    Args:
        format: Logging format string
        
    Raises:
        ValueError: If format is invalid
    """
    if not isinstance(format, str):
        raise ValueError("Format must be a string")
        
    formatter = logging.Formatter(format)
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)
        
def set_log_file(file: str) -> None:
    """Set log file.
    
    Args:
        file: Path to log file
        
    Raises:
        ValueError: If file path is invalid
    """
    if not isinstance(file, str):
        raise ValueError("File must be a string")
        
    # Create logs directory if it doesn't exist
    log_path = Path(file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing file handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            root_logger.removeHandler(handler)
            
    # Add new file handler
    file_handler = logging.FileHandler(file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    root_logger.addHandler(file_handler) 