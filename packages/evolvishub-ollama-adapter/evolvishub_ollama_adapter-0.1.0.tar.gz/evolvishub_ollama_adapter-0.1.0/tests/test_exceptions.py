import pytest
from evolvishub_ollama_adapter.exceptions import (
    OllamaError,
    OllamaConnectionError,
    OllamaTimeoutError,
    OllamaModelError,
    OllamaValidationError,
    OllamaConfigError
)

def test_ollama_error():
    """Test base OllamaError."""
    # Test with message
    error = OllamaError("Test error")
    assert str(error) == "Test error"
    
    # Test with message and cause
    cause = Exception("Original error")
    error = OllamaError("Test error", cause)
    assert str(error) == "Test error"
    assert error.__cause__ == cause

def test_ollama_connection_error():
    """Test OllamaConnectionError."""
    # Test with message
    error = OllamaConnectionError("Connection failed")
    assert str(error) == "Connection failed"
    assert isinstance(error, OllamaError)
    
    # Test with message and cause
    cause = Exception("Network error")
    error = OllamaConnectionError("Connection failed", cause)
    assert str(error) == "Connection failed"
    assert error.__cause__ == cause

def test_ollama_timeout_error():
    """Test OllamaTimeoutError."""
    # Test with message
    error = OllamaTimeoutError("Request timed out")
    assert str(error) == "Request timed out"
    assert isinstance(error, OllamaError)
    
    # Test with message and cause
    cause = Exception("Timeout error")
    error = OllamaTimeoutError("Request timed out", cause)
    assert str(error) == "Request timed out"
    assert error.__cause__ == cause

def test_ollama_model_error():
    """Test OllamaModelError."""
    # Test with message
    error = OllamaModelError("Model not found")
    assert str(error) == "Model not found"
    assert isinstance(error, OllamaError)
    
    # Test with message and cause
    cause = Exception("Model error")
    error = OllamaModelError("Model not found", cause)
    assert str(error) == "Model not found"
    assert error.__cause__ == cause

def test_ollama_validation_error():
    """Test OllamaValidationError."""
    # Test with message
    error = OllamaValidationError("Invalid input")
    assert str(error) == "Invalid input"
    assert isinstance(error, OllamaError)
    
    # Test with message and cause
    cause = Exception("Validation error")
    error = OllamaValidationError("Invalid input", cause)
    assert str(error) == "Invalid input"
    assert error.__cause__ == cause

def test_ollama_config_error():
    """Test OllamaConfigError."""
    # Test with message
    error = OllamaConfigError("Invalid configuration")
    assert str(error) == "Invalid configuration"
    assert isinstance(error, OllamaError)
    
    # Test with message and cause
    cause = Exception("Config error")
    error = OllamaConfigError("Invalid configuration", cause)
    assert str(error) == "Invalid configuration"
    assert error.__cause__ == cause

def test_error_inheritance():
    """Test error inheritance hierarchy."""
    # Test base error
    base_error = OllamaError("Base error")
    assert isinstance(base_error, Exception)
    
    # Test connection error
    conn_error = OllamaConnectionError("Connection error")
    assert isinstance(conn_error, OllamaError)
    
    # Test timeout error
    timeout_error = OllamaTimeoutError("Timeout error")
    assert isinstance(timeout_error, OllamaError)
    
    # Test model error
    model_error = OllamaModelError("Model error")
    assert isinstance(model_error, OllamaError)
    
    # Test validation error
    validation_error = OllamaValidationError("Validation error")
    assert isinstance(validation_error, OllamaError)
    
    # Test config error
    config_error = OllamaConfigError("Config error")
    assert isinstance(config_error, OllamaError)

def test_error_with_details():
    """Test errors with additional details."""
    # Test with details
    error = OllamaError("Test error", details={"code": 500, "reason": "Internal error"})
    assert str(error) == "Test error"
    assert error.details == {"code": 500, "reason": "Internal error"}
    
    # Test with details and cause
    cause = Exception("Original error")
    error = OllamaError("Test error", cause=cause, details={"code": 500})
    assert str(error) == "Test error"
    assert error.__cause__ == cause
    assert error.details == {"code": 500}

def test_error_equality():
    """Test error equality."""
    # Test same error
    error1 = OllamaError("Test error")
    error2 = OllamaError("Test error")
    assert error1 == error2
    
    # Test different messages
    error1 = OllamaError("Error 1")
    error2 = OllamaError("Error 2")
    assert error1 != error2
    
    # Test different types
    error1 = OllamaError("Test error")
    error2 = OllamaConnectionError("Test error")
    assert error1 != error2
    
    # Test with details
    error1 = OllamaError("Test error", details={"code": 500})
    error2 = OllamaError("Test error", details={"code": 500})
    assert error1 == error2
    
    # Test with different details
    error1 = OllamaError("Test error", details={"code": 500})
    error2 = OllamaError("Test error", details={"code": 400})
    assert error1 != error2 