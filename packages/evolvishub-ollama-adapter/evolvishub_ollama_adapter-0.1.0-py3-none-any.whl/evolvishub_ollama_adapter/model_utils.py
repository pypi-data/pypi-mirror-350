"""
Model utilities for Ollama integration.
"""

from typing import Dict, Any, Optional, List, Union
import json
from pathlib import Path
import os

from .constants import (
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    DEFAULT_TOP_K,
    DEFAULT_REPEAT_PENALTY,
    DEFAULT_MAX_TOKENS,
)
from .exceptions import ValidationError
from .file_utils import ensure_directory

def load_model(model_path: str, *args, **kwargs) -> Dict[str, Any]:
    """Load model configuration from file.
    
    Args:
        model_path: Path to model configuration file
        
    Returns:
        Model configuration dictionary
        
    Raises:
        ValueError: If model_path is invalid
        IOError: If model file cannot be read
    """
    if not isinstance(model_path, str) or not model_path:
        raise ValueError("Model path must be a non-empty string")
    if not os.path.exists(model_path):
        raise ValueError(f"Model file does not exist: {model_path}")
        
    try:
        with open(model_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Failed to read model file: {str(e)}")
        
def save_model(model: Dict[str, Any], model_path: str, *args, **kwargs) -> None:
    """Save model configuration to file.
    
    Args:
        model: Model configuration dictionary
        model_path: Path to save model configuration
        
    Raises:
        ValueError: If model or model_path is invalid
        IOError: If model file cannot be written
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
    if not isinstance(model_path, str) or not model_path:
        raise ValueError("Model path must be a non-empty string")
        
    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, "w") as f:
            json.dump(model, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to write model file: {str(e)}")
        
def get_model_info(model: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
    """Get model information.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model information dictionary
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return {
        "name": model.get("name", ""),
        "version": model.get("version", ""),
        "architecture": model.get("architecture", ""),
        "parameters": model.get("parameters", {}),
        "description": model.get("description", ""),
        "author": model.get("author", ""),
        "license": model.get("license", ""),
        "created_at": model.get("created_at", ""),
        "updated_at": model.get("updated_at", "")
    }
    
def get_model_architecture(model: Dict[str, Any], *args, **kwargs) -> str:
    """Get model architecture.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model architecture string
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("architecture", "")
    
def get_model_config(model: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
    """Get model configuration.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model configuration dictionary
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("parameters", {})
    
def get_model_weights(model: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
    """Get model weights.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model weights dictionary
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("weights", {})
    
def set_model_weights(model: Dict[str, Any], weights: Dict[str, Any], *args, **kwargs) -> None:
    """Set model weights.
    
    Args:
        model: Model configuration dictionary
        weights: Model weights dictionary
        
    Raises:
        ValueError: If model or weights is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
    if not isinstance(weights, dict):
        raise ValueError("Weights must be a dictionary")
        
    model["weights"] = weights
    
def get_model_device(model: Dict[str, Any], *args, **kwargs) -> str:
    """Get model device.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model device string
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("device", "cpu")
    
def set_model_device(model: Dict[str, Any], device: str, *args, **kwargs) -> None:
    """Set model device.
    
    Args:
        model: Model configuration dictionary
        device: Model device string
        
    Raises:
        ValueError: If model or device is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
    if not isinstance(device, str) or not device:
        raise ValueError("Device must be a non-empty string")
        
    model["device"] = device
    
def get_model_dtype(model: Dict[str, Any], *args, **kwargs) -> str:
    """Get model data type.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model data type string
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("dtype", "float32")
    
def set_model_dtype(model: Dict[str, Any], dtype: str, *args, **kwargs) -> None:
    """Set model data type.
    
    Args:
        model: Model configuration dictionary
        dtype: Model data type string
        
    Raises:
        ValueError: If model or dtype is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
    if not isinstance(dtype, str) or not dtype:
        raise ValueError("Data type must be a non-empty string")
        
    model["dtype"] = dtype
    
def get_model_mode(model: Dict[str, Any], *args, **kwargs) -> str:
    """Get model mode.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model mode string
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("mode", "eval")
    
def set_model_mode(model: Dict[str, Any], mode: str, *args, **kwargs) -> None:
    """Set model mode.
    
    Args:
        model: Model configuration dictionary
        mode: Model mode string
        
    Raises:
        ValueError: If model or mode is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
    if not isinstance(mode, str) or not mode:
        raise ValueError("Mode must be a non-empty string")
        
    model["mode"] = mode
    
def get_model_metrics(model: Dict[str, Any], *args, **kwargs) -> Dict[str, float]:
    """Get model metrics.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model metrics dictionary
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("metrics", {})
    
def get_model_loss(model: Dict[str, Any], *args, **kwargs) -> float:
    """Get model loss.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model loss value
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("metrics", {}).get("loss", 0.0)
    
def get_model_accuracy(model: Dict[str, Any], *args, **kwargs) -> float:
    """Get model accuracy.
    
    Args:
        model: Model configuration dictionary
        
    Returns:
        Model accuracy value
        
    Raises:
        ValueError: If model is invalid
    """
    if not isinstance(model, dict) or not model:
        raise ValueError("Model must be a non-empty dictionary")
        
    return model.get("metrics", {}).get("accuracy", 0.0)

def validate_model_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Validate model parameters.
    
    Args:
        params: Model parameters to validate
        
    Returns:
        Validated parameters with defaults applied
        
    Raises:
        ValidationError: If parameters are invalid
    """
    validated = {
        "model": params.get("model", DEFAULT_MODEL),
        "temperature": float(params.get("temperature", DEFAULT_TEMPERATURE)),
        "top_p": float(params.get("top_p", DEFAULT_TOP_P)),
        "top_k": int(params.get("top_k", DEFAULT_TOP_K)),
        "repeat_penalty": float(params.get("repeat_penalty", DEFAULT_REPEAT_PENALTY)),
        "max_tokens": int(params.get("max_tokens", DEFAULT_MAX_TOKENS)),
    }
    
    # Validate temperature
    if not 0 <= validated["temperature"] <= 1:
        raise ValidationError("Temperature must be between 0 and 1")
    
    # Validate top_p
    if not 0 <= validated["top_p"] <= 1:
        raise ValidationError("Top P must be between 0 and 1")
    
    # Validate top_k
    if validated["top_k"] < 1:
        raise ValidationError("Top K must be greater than 0")
    
    # Validate repeat_penalty
    if validated["repeat_penalty"] < 0:
        raise ValidationError("Repeat penalty must be non-negative")
    
    # Validate max_tokens
    if validated["max_tokens"] < 1:
        raise ValidationError("Max tokens must be greater than 0")
    
    return validated

def format_prompt(prompt: str, system_prompt: Optional[str] = None) -> str:
    """Format a prompt with optional system prompt.
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        
    Returns:
        Formatted prompt string
    """
    if system_prompt:
        return f"{system_prompt}\n\n{prompt}"
    return prompt

def format_chat_messages(messages: List[Dict[str, str]]) -> str:
    """Format chat messages into a single string.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        Formatted chat string
        
    Raises:
        ValidationError: If messages are invalid
    """
    if not messages:
        raise ValidationError("No messages provided")
    
    formatted = []
    for msg in messages:
        if not isinstance(msg, dict):
            raise ValidationError("Message must be a dictionary")
        if "role" not in msg or "content" not in msg:
            raise ValidationError("Message must have 'role' and 'content' keys")
        if not isinstance(msg["role"], str) or not isinstance(msg["content"], str):
            raise ValidationError("Message role and content must be strings")
        
        role = msg["role"].lower()
        if role not in ["system", "user", "assistant"]:
            raise ValidationError("Invalid message role")
        
        formatted.append(f"{role.capitalize()}: {msg['content']}")
    
    return "\n\n".join(formatted)

def save_model_config(config: Dict[str, Any], path: Union[str, Path]) -> None:
    """Save model configuration to a file.
    
    Args:
        config: Model configuration dictionary
        path: Path to save configuration
        
    Raises:
        ValidationError: If configuration is invalid or cannot be saved
    """
    try:
        with open(path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        raise ValidationError(f"Failed to save model configuration: {e}")

def load_model_config(path: Union[str, Path]) -> Dict[str, Any]:
    """Load model configuration from a file.
    
    Args:
        path: Path to configuration file
        
    Returns:
        Model configuration dictionary
        
    Raises:
        ValidationError: If configuration file is invalid or cannot be loaded
    """
    try:
        with open(path, "r") as f:
            config = json.load(f)
        return validate_model_params(config)
    except Exception as e:
        raise ValidationError(f"Failed to load model configuration: {e}")

def get_model_size(model_path: str, *args, **kwargs) -> int:
    if not isinstance(model_path, str) or not model_path:
        raise ValueError("Model path must be a non-empty string")
    if not os.path.exists(model_path):
        raise ValueError(f"Model file does not exist: {model_path}")
    try:
        return os.path.getsize(model_path)
    except Exception as e:
        raise ValueError(f"Failed to get model size: {str(e)}")

def get_model_parameters(model_config: dict) -> dict:
    """Get the parameters dictionary from a model configuration.
    
    Args:
        model_config: Model configuration dictionary
        
    Returns:
        Parameters dictionary
        
    Raises:
        ValidationError: If the parameters are missing or invalid
    """
    if not isinstance(model_config, dict):
        raise ValidationError("Model configuration must be a dictionary.")
    params = model_config.get("parameters")
    if not isinstance(params, dict):
        raise ValidationError("Model 'parameters' must be a dictionary.")
    return params

def get_model_layers(model_config: dict) -> int:
    """Get the number of layers from a model configuration if present.
    
    Args:
        model_config: Model configuration dictionary
        
    Returns:
        Number of layers (int), or 0 if not specified
    """
    if not isinstance(model_config, dict):
        raise ValidationError("Model configuration must be a dictionary.")
    params = model_config.get("parameters", {})
    return int(params.get("num_layers", 0))

def validate_model(model_config: dict) -> bool:
    """Validate a model configuration dictionary.
    
    Args:
        model_config: Model configuration dictionary
        
    Returns:
        True if the model configuration is valid
        
    Raises:
        ValidationError: If the model configuration is invalid
    """
    if not isinstance(model_config, dict):
        raise ValidationError("Model configuration must be a dictionary.")
    required_keys = ["name", "parameters"]
    for key in required_keys:
        if key not in model_config:
            raise ValidationError(f"Missing required key in model configuration: {key}")
    if not isinstance(model_config["parameters"], dict):
        raise ValidationError("Model 'parameters' must be a dictionary.")
    return True 