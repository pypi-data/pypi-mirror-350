"""
Unit tests for configuration management.
"""

import os
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile

from evolvishub_ollama_adapter.config import Config

@pytest.fixture
def temp_ini_file():
    """Create a temporary INI config file."""
    with NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
        f.write("""
[Ollama]
base_url = http://test:11434
timeout = 30
max_retries = 2
default_model = test-model

[Models]
test-model = 7b

[ModelOptions]
temperature = 0.8
top_p = 0.95
        """)
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def temp_yaml_file():
    """Create a temporary YAML config file."""
    with NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""
ollama:
  base_url: http://test:11434
  timeout: 30
  max_retries: 2
  default_model: test-model

models:
  test-model: 7b

model_options:
  temperature: 0.8
  top_p: 0.95
        """)
    yield f.name
    os.unlink(f.name)

def test_default_config():
    """Test default configuration creation."""
    config = Config()
    assert config.get("Ollama", "base_url") == "http://localhost:11434"
    assert config.getint("Ollama", "timeout") == 60
    assert config.getint("Ollama", "max_retries") == 3

def test_ini_config(temp_ini_file):
    """Test INI configuration loading."""
    config = Config(temp_ini_file, config_type="ini")
    assert config.get("Ollama", "base_url") == "http://test:11434"
    assert config.getint("Ollama", "timeout") == 30
    assert config.getint("Ollama", "max_retries") == 2
    assert config.get("Models", "test-model") == "7b"

@pytest.mark.skipif(not Config.YAML_AVAILABLE, reason="PyYAML not installed")
def test_yaml_config(temp_yaml_file):
    """Test YAML configuration loading."""
    config = Config(temp_yaml_file, config_type="yaml")
    assert config.get("ollama", "base_url") == "http://test:11434"
    assert config.getint("ollama", "timeout") == 30
    assert config.getint("ollama", "max_retries") == 2
    assert config.get("models", "test-model") == "7b"

def test_config_getters():
    """Test configuration getter methods."""
    config = Config()
    
    # Test integer getter
    assert isinstance(config.getint("Ollama", "timeout"), int)
    assert config.getint("Ollama", "nonexistent", 42) == 42
    
    # Test float getter
    assert isinstance(config.getfloat("ModelOptions", "temperature"), float)
    assert config.getfloat("ModelOptions", "nonexistent", 0.5) == 0.5
    
    # Test boolean getter
    assert isinstance(config.getboolean("DataSources", "markdown_extract_code"), bool)
    assert config.getboolean("DataSources", "nonexistent", True) is True
    
    # Test list getter
    patterns = config.getlist("FileSources", "text_patterns")
    assert isinstance(patterns, list)
    assert all(isinstance(p, str) for p in patterns)

def test_config_setters():
    """Test configuration setter methods."""
    config = Config()
    
    # Test setting values
    config.set("Test", "string", "value")
    config.set("Test", "int", 42)
    config.set("Test", "float", 3.14)
    config.set("Test", "bool", True)
    
    assert config.get("Test", "string") == "value"
    assert config.getint("Test", "int") == 42
    assert config.getfloat("Test", "float") == 3.14
    assert config.getboolean("Test", "bool") is True

def test_model_options():
    """Test model options retrieval."""
    config = Config()
    options = config.get_model_options()
    
    assert isinstance(options, dict)
    assert "temperature" in options
    assert "top_p" in options
    assert "top_k" in options
    assert isinstance(options["temperature"], float)
    assert isinstance(options["top_k"], int)

def test_file_patterns():
    """Test file patterns retrieval."""
    config = Config()
    patterns = config.get_file_patterns()
    
    assert isinstance(patterns, dict)
    assert "text" in patterns
    assert "code" in patterns
    assert "binary" in patterns
    assert all(isinstance(p, list) for p in patterns.values())

def test_storage_paths():
    """Test storage paths retrieval."""
    config = Config()
    paths = config.get_storage_paths()
    
    assert isinstance(paths, dict)
    assert "temp" in paths
    assert "cache" in paths
    assert "output" in paths
    assert all(isinstance(p, Path) for p in paths.values())

def test_config_save(temp_ini_file):
    """Test configuration saving."""
    config = Config(temp_ini_file, config_type="ini")
    config.set("Test", "new_value", "test")
    
    # Save to new file
    new_file = temp_ini_file + ".new"
    config.save(new_file)
    
    # Load from new file
    new_config = Config(new_file, config_type="ini")
    assert new_config.get("Test", "new_value") == "test"
    
    os.unlink(new_file)

def test_environment_override(monkeypatch):
    """Test environment variable configuration override."""
    monkeypatch.setenv("OLLAMA_CONFIG", "test_config.ini")
    config = Config()
    assert config.config_path == "test_config.ini" 