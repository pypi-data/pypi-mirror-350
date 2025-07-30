import pytest
from evolvishub_ollama_adapter.constants import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    DEFAULT_TOP_K,
    DEFAULT_REPEAT_PENALTY,
    DEFAULT_NUM_CTX,
    DEFAULT_NUM_THREAD,
    DEFAULT_TEXT_CHUNK_SIZE,
    DEFAULT_TEXT_CHUNK_OVERLAP,
    DEFAULT_IMAGE_MAX_SIZE,
    DEFAULT_IMAGE_QUALITY,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_MAX_SIZE,
    DEFAULT_LOG_BACKUP_COUNT,
    SUPPORTED_MODELS,
    SUPPORTED_IMAGE_FORMATS,
    SUPPORTED_TEXT_FORMATS,
    SUPPORTED_CODE_FORMATS,
    SUPPORTED_BINARY_FORMATS,
    SUPPORTED_ROLES,
    SUPPORTED_OPTIONS
)

def test_default_values():
    """Test default values."""
    # API defaults
    assert DEFAULT_BASE_URL == "http://localhost:11434"
    assert DEFAULT_TIMEOUT == 60
    assert DEFAULT_MAX_RETRIES == 3
    assert DEFAULT_MODEL == "llama2"
    
    # Model defaults
    assert DEFAULT_TEMPERATURE == 0.7
    assert DEFAULT_TOP_P == 0.9
    assert DEFAULT_TOP_K == 40
    assert DEFAULT_REPEAT_PENALTY == 1.1
    assert DEFAULT_NUM_CTX == 2048
    assert DEFAULT_NUM_THREAD == 4
    
    # Data source defaults
    assert DEFAULT_TEXT_CHUNK_SIZE == 1000
    assert DEFAULT_TEXT_CHUNK_OVERLAP == 200
    assert DEFAULT_IMAGE_MAX_SIZE == 1024
    assert DEFAULT_IMAGE_QUALITY == 85
    
    # Logging defaults
    assert DEFAULT_LOG_LEVEL == "INFO"
    assert DEFAULT_LOG_FORMAT == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert DEFAULT_LOG_FILE == "ollama.log"
    assert DEFAULT_LOG_MAX_SIZE == 10485760
    assert DEFAULT_LOG_BACKUP_COUNT == 5

def test_supported_models():
    """Test supported models."""
    assert isinstance(SUPPORTED_MODELS, list)
    assert len(SUPPORTED_MODELS) > 0
    assert "llama2" in SUPPORTED_MODELS
    assert "mistral" in SUPPORTED_MODELS
    assert "codellama" in SUPPORTED_MODELS
    assert "vicuna" in SUPPORTED_MODELS

def test_supported_formats():
    """Test supported file formats."""
    # Image formats
    assert isinstance(SUPPORTED_IMAGE_FORMATS, list)
    assert len(SUPPORTED_IMAGE_FORMATS) > 0
    assert "png" in SUPPORTED_IMAGE_FORMATS
    assert "jpg" in SUPPORTED_IMAGE_FORMATS
    assert "jpeg" in SUPPORTED_IMAGE_FORMATS
    
    # Text formats
    assert isinstance(SUPPORTED_TEXT_FORMATS, list)
    assert len(SUPPORTED_TEXT_FORMATS) > 0
    assert "txt" in SUPPORTED_TEXT_FORMATS
    assert "md" in SUPPORTED_TEXT_FORMATS
    assert "rst" in SUPPORTED_TEXT_FORMATS
    
    # Code formats
    assert isinstance(SUPPORTED_CODE_FORMATS, list)
    assert len(SUPPORTED_CODE_FORMATS) > 0
    assert "py" in SUPPORTED_CODE_FORMATS
    assert "js" in SUPPORTED_CODE_FORMATS
    assert "java" in SUPPORTED_CODE_FORMATS
    assert "cpp" in SUPPORTED_CODE_FORMATS
    
    # Binary formats
    assert isinstance(SUPPORTED_BINARY_FORMATS, list)
    assert len(SUPPORTED_BINARY_FORMATS) > 0
    assert "pdf" in SUPPORTED_BINARY_FORMATS
    assert "jpg" in SUPPORTED_BINARY_FORMATS
    assert "png" in SUPPORTED_BINARY_FORMATS

def test_supported_roles():
    """Test supported chat roles."""
    assert isinstance(SUPPORTED_ROLES, list)
    assert len(SUPPORTED_ROLES) > 0
    assert "user" in SUPPORTED_ROLES
    assert "assistant" in SUPPORTED_ROLES
    assert "system" in SUPPORTED_ROLES

def test_supported_options():
    """Test supported model options."""
    assert isinstance(SUPPORTED_OPTIONS, list)
    assert len(SUPPORTED_OPTIONS) > 0
    assert "temperature" in SUPPORTED_OPTIONS
    assert "top_p" in SUPPORTED_OPTIONS
    assert "top_k" in SUPPORTED_OPTIONS
    assert "repeat_penalty" in SUPPORTED_OPTIONS
    assert "num_ctx" in SUPPORTED_OPTIONS
    assert "num_thread" in SUPPORTED_OPTIONS

def test_format_consistency():
    """Test format consistency."""
    # Check for duplicates
    all_formats = (
        SUPPORTED_IMAGE_FORMATS +
        SUPPORTED_TEXT_FORMATS +
        SUPPORTED_CODE_FORMATS +
        SUPPORTED_BINARY_FORMATS
    )
    assert len(all_formats) == len(set(all_formats))
    
    # Check for lowercase
    for format_list in [
        SUPPORTED_IMAGE_FORMATS,
        SUPPORTED_TEXT_FORMATS,
        SUPPORTED_CODE_FORMATS,
        SUPPORTED_BINARY_FORMATS
    ]:
        assert all(f.islower() for f in format_list)

def test_role_consistency():
    """Test role consistency."""
    # Check for duplicates
    assert len(SUPPORTED_ROLES) == len(set(SUPPORTED_ROLES))
    
    # Check for lowercase
    assert all(r.islower() for r in SUPPORTED_ROLES)

def test_option_consistency():
    """Test option consistency."""
    # Check for duplicates
    assert len(SUPPORTED_OPTIONS) == len(set(SUPPORTED_OPTIONS))
    
    # Check for lowercase
    assert all(o.islower() for o in SUPPORTED_OPTIONS)

def test_model_consistency():
    """Test model consistency."""
    # Check for duplicates
    assert len(SUPPORTED_MODELS) == len(set(SUPPORTED_MODELS))
    
    # Check for lowercase
    assert all(m.islower() for m in SUPPORTED_MODELS)

def test_default_value_types():
    """Test default value types."""
    # Numeric defaults
    assert isinstance(DEFAULT_TIMEOUT, int)
    assert isinstance(DEFAULT_MAX_RETRIES, int)
    assert isinstance(DEFAULT_TEMPERATURE, float)
    assert isinstance(DEFAULT_TOP_P, float)
    assert isinstance(DEFAULT_TOP_K, int)
    assert isinstance(DEFAULT_REPEAT_PENALTY, float)
    assert isinstance(DEFAULT_NUM_CTX, int)
    assert isinstance(DEFAULT_NUM_THREAD, int)
    assert isinstance(DEFAULT_TEXT_CHUNK_SIZE, int)
    assert isinstance(DEFAULT_TEXT_CHUNK_OVERLAP, int)
    assert isinstance(DEFAULT_IMAGE_MAX_SIZE, int)
    assert isinstance(DEFAULT_IMAGE_QUALITY, int)
    assert isinstance(DEFAULT_LOG_MAX_SIZE, int)
    assert isinstance(DEFAULT_LOG_BACKUP_COUNT, int)
    
    # String defaults
    assert isinstance(DEFAULT_BASE_URL, str)
    assert isinstance(DEFAULT_MODEL, str)
    assert isinstance(DEFAULT_LOG_LEVEL, str)
    assert isinstance(DEFAULT_LOG_FORMAT, str)
    assert isinstance(DEFAULT_LOG_FILE, str) 