"""Tests for the logging module."""

import logging
import os
import pytest
from pathlib import Path
import tempfile

from evolvishub_ollama_adapter.logging import (
    setup_logging,
    get_logger,
    configure_logging
)
from evolvishub_ollama_adapter.exceptions import ConfigurationError

@pytest.fixture
def temp_log_dir():
    """Create a temporary directory for log files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

def test_setup_logging(temp_log_dir):
    """Test basic logging setup."""
    log_file = os.path.join(temp_log_dir, "test.log")
    setup_logging(level="DEBUG", format="%(levelname)s - %(message)s", file=log_file)
    logger = get_logger("test")
    logger.debug("Debug message")
    assert os.path.exists(log_file)

def test_logging_levels(temp_log_dir):
    """Test different logging levels."""
    log_file = os.path.join(temp_log_dir, "test.log")
    setup_logging(level="INFO", format="%(levelname)s - %(message)s", file=log_file)
    logger = get_logger("test")
    logger.info("Info message")
    assert os.path.exists(log_file)

def test_logging_format(temp_log_dir):
    """Test custom logging format."""
    log_file = os.path.join(temp_log_dir, "test.log")
    setup_logging(level="INFO", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", file=log_file)
    logger = get_logger("test")
    logger.info("Info message")
    assert os.path.exists(log_file)

def test_log_rotation(temp_log_dir):
    """Test log file rotation."""
    log_file = os.path.join(temp_log_dir, "test.log")
    setup_logging(level="INFO", format="%(levelname)s - %(message)s", file=log_file, max_size=100, backup_count=2)
    logger = get_logger("test")
    for _ in range(100):
        logger.info("Log message")
    assert os.path.exists(log_file)

def test_multiple_loggers(temp_log_dir):
    """Test multiple loggers."""
    log_file = os.path.join(temp_log_dir, "test.log")
    setup_logging(level="INFO", format="%(name)s - %(levelname)s - %(message)s", file=log_file)
    logger1 = get_logger("logger1")
    logger2 = get_logger("logger2")
    logger1.info("Logger1 message")
    logger2.info("Logger2 message")
    assert os.path.exists(log_file)

def test_configure_logging(temp_log_dir):
    """Test configure_logging function."""
    # Create config
    config = {
        "level": "DEBUG",
        "format": "%(levelname)s - %(message)s",
        "file": os.path.join(temp_log_dir, "test.log"),
        "max_size": 10485760,
        "backup_count": 5
    }
    
    # Configure logging
    configure_logging(config)
    
    # Get logger
    logger = get_logger("test")
    
    # Test logging
    logger.debug("Debug message")
    logger.info("Info message")
    
    # Verify log file
    assert os.path.exists(config["file"])
    with open(config["file"], "r") as f:
        content = f.read()
        assert "Debug message" in content
        assert "Info message" in content

def test_invalid_log_level(temp_log_dir):
    """Test invalid log level."""
    log_file = os.path.join(temp_log_dir, "test.log")
    with pytest.raises(ConfigurationError):
        setup_logging(level="INVALID", format="%(levelname)s - %(message)s", file=log_file)

def test_invalid_log_format(temp_log_dir):
    """Test invalid log format."""
    log_file = os.path.join(temp_log_dir, "test.log")
    with pytest.raises(Exception):
        setup_logging(level="INFO", format="%(invalid)s - %(message)s", file=log_file)

def test_invalid_log_file(temp_log_dir):
    """Test invalid log file."""
    with pytest.raises(Exception):
        setup_logging(level="INFO", format="%(levelname)s - %(message)s", file="/invalid/path/test.log")

def test_logger_reuse():
    """Test logger reuse."""
    setup_logging(level="INFO")
    logger1 = get_logger("logger1")
    logger2 = get_logger("logger2")
    assert logger1 is not None
    assert logger2 is not None

def test_logger_hierarchy():
    """Test logger hierarchy."""
    setup_logging(level="INFO")
    parent_logger = get_logger("parent")
    child_logger = get_logger("parent.child")
    assert parent_logger is not None
    assert child_logger is not None 