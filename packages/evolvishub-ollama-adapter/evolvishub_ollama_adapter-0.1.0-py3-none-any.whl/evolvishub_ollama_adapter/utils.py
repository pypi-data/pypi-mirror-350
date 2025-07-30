"""
Utility functions for Ollama integration.
"""

import base64
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

import aiofiles
from PIL import Image
import numpy as np
import io

def encode_image(image_path: Union[str, Path, Image.Image]) -> str:
    """Encode an image file to base64.
    
    Args:
        image_path: Path to the image file or PIL Image object
        
    Returns:
        Base64-encoded image string with data URL prefix
        
    Raises:
        ValueError: If image_path is None or invalid
        IOError: If image file cannot be read
    """
    if image_path is None:
        raise ValueError("Image path cannot be None")

    if isinstance(image_path, Image.Image):
        if not image_path.mode in ('RGB', 'RGBA', 'L'):
            raise ValueError(f"Unsupported image mode: {image_path.mode}")
        buffer = io.BytesIO()
        image_path.save(buffer, format=image_path.format or 'PNG')
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except IOError as e:
        raise IOError(f"Failed to read image file: {str(e)}")

async def encode_image_async(image_path: Union[str, Path, Image.Image]) -> str:
    """Asynchronously encode an image file to base64.
    
    Args:
        image_path: Path to the image file or PIL Image object
        
    Returns:
        Base64-encoded image string with data URL prefix
        
    Raises:
        ValueError: If image_path is None or invalid
        IOError: If image file cannot be read
    """
    if image_path is None:
        raise ValueError("Image path cannot be None")

    if isinstance(image_path, Image.Image):
        if not image_path.mode in ('RGB', 'RGBA', 'L'):
            raise ValueError(f"Unsupported image mode: {image_path.mode}")
        buffer = io.BytesIO()
        image_path.save(buffer, format=image_path.format or 'PNG')
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    try:
        async with aiofiles.open(image_path, "rb") as f:
            content = await f.read()
            encoded = base64.b64encode(content).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except IOError as e:
        raise IOError(f"Failed to read image file: {str(e)}")

def decode_image(image_data: str) -> Image.Image:
    """Decode a base64-encoded image.
    
    Args:
        image_data: Base64-encoded image string or data URL
        
    Returns:
        Decoded PIL Image
        
    Raises:
        ValueError: If image_data is None or invalid
        IOError: If image data cannot be decoded
    """
    if image_data is None:
        raise ValueError("Image data cannot be None")

    if not isinstance(image_data, str):
        raise ValueError("Image data must be a string")

    if image_data.startswith('data:'):
        # Remove data URL prefix
        image_data = image_data.split(',', 1)[1]

    try:
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        if not image.mode in ('RGB', 'RGBA', 'L'):
            image = image.convert('RGB')
        return image
    except Exception as e:
        raise IOError(f"Failed to decode image: {str(e)}")

def resize_image(image: Union[str, Path, Image.Image], max_size: int = 1024) -> Image.Image:
    """Resize an image while maintaining aspect ratio.
    
    Args:
        image: Path to the image file or PIL Image object
        max_size: Maximum dimension size
        
    Returns:
        Resized PIL Image
        
    Raises:
        ValueError: If image is None or max_size is invalid
        IOError: If image file cannot be read
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(max_size, int) or max_size <= 0:
        raise ValueError("max_size must be a positive integer")

    try:
        if isinstance(image, (str, Path)):
            image = Image.open(image)
        
        if not image.mode in ('RGB', 'RGBA', 'L'):
            image = image.convert('RGB')
        
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        return image
    except Exception as e:
        raise IOError(f"Failed to resize image: {str(e)}")

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score
        
    Raises:
        ValueError: If vectors are None or have different lengths
    """
    if a is None or b is None:
        raise ValueError("Vectors cannot be None")
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    if not all(isinstance(x, (int, float)) for x in a + b):
        raise ValueError("Vectors must contain only numbers")

    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return np.dot(a, b) / (a_norm * b_norm)

def format_prompt(template: str, values: Dict[str, Any]) -> str:
    """Format a prompt template with variables.
    
    Args:
        template: Prompt template string
        values: Dictionary of template variables
        
    Returns:
        Formatted prompt string
        
    Raises:
        ValueError: If template is None or values is invalid
        KeyError: If template contains variables not in values
    """
    if template is None:
        raise ValueError("Template cannot be None")
    if not isinstance(template, str):
        raise ValueError("Template must be a string")
    if not isinstance(values, dict):
        raise ValueError("Values must be a dictionary")

    try:
        return template.format(**values)
    except KeyError as e:
        raise KeyError(f"Missing template variable: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to format prompt: {str(e)}")

def parse_model_options(options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse and validate model options.
    
    Args:
        options: Raw model options
        
    Returns:
        Validated model options
        
    Raises:
        ValueError: If options contain invalid values
    """
    if options is None:
        raise ValidationError("Options cannot be None")
    if not isinstance(options, dict):
        raise ValidationError("Options must be a dictionary")
    
    valid_options = {
        "temperature": float,
        "top_p": float,
        "top_k": int,
        "repeat_penalty": float,
        "presence_penalty": float,
        "frequency_penalty": float,
        "mirostat": int,
        "mirostat_eta": float,
        "mirostat_tau": float,
        "num_ctx": int,
        "num_gpu": int,
        "num_thread": int,
        "repeat_last_n": int,
        "seed": int,
        "stop": Union[str, List[str]],
        "tfs_z": float,
        "num_predict": int,
        "typical_p": float,
    }
    
    parsed_options = {}
    for key, value in options.items():
        if key in valid_options:
            expected_type = valid_options[key]
            if isinstance(expected_type, type):
                try:
                    parsed_options[key] = expected_type(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid value for option {key}: {value}")
            else:
                parsed_options[key] = value
    
    return parsed_options

def format_chat_history(messages: List[Dict[str, Any]]) -> str:
    """Format chat history as a string.
    
    Args:
        messages: List of chat messages
        
    Returns:
        Formatted chat history string
        
    Raises:
        ValueError: If messages is None or invalid
    """
    if messages is None:
        raise ValidationError("Messages cannot be None")
    if not isinstance(messages, list):
        raise ValidationError("Messages must be a list")
    for msg in messages:
        if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
            raise ValidationError("Each message must be a dict with 'role' and 'content'")

    formatted = []
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        if not isinstance(role, str) or not isinstance(content, str):
            raise ValueError("Message role and content must be strings")
        formatted.append(f"{role}: {content}")
    return "\n".join(formatted)

def parse_model_name(name: str) -> tuple[str, Optional[str]]:
    """Parse a model name into its components.
    
    Args:
        name: Model name (e.g., "llama2:7b")
        
    Returns:
        Tuple of (model_name, version)
        
    Raises:
        ValueError: If name is None or invalid
    """
    if name is None:
        raise ValueError("Model name cannot be None")
    if not isinstance(name, str):
        raise ValueError("Model name must be a string")
    if not name:
        raise ValueError("Model name cannot be empty")

    parts = name.split(":")
    return parts[0], parts[1] if len(parts) > 1 else None 
"""
Utility functions for Ollama integration.
"""

import base64
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

import aiofiles
from PIL import Image
import numpy as np
import io

def encode_image(image_path: Union[str, Path, Image.Image]) -> str:
    """Encode an image file to base64.
    
    Args:
        image_path: Path to the image file or PIL Image object
        
    Returns:
        Base64-encoded image string with data URL prefix
        
    Raises:
        ValueError: If image_path is None or invalid
        IOError: If image file cannot be read
    """
    if image_path is None:
        raise ValueError("Image path cannot be None")

    if isinstance(image_path, Image.Image):
        if not image_path.mode in ('RGB', 'RGBA', 'L'):
            raise ValueError(f"Unsupported image mode: {image_path.mode}")
        buffer = io.BytesIO()
        image_path.save(buffer, format=image_path.format or 'PNG')
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except IOError as e:
        raise IOError(f"Failed to read image file: {str(e)}")

async def encode_image_async(image_path: Union[str, Path, Image.Image]) -> str:
    """Asynchronously encode an image file to base64.
    
    Args:
        image_path: Path to the image file or PIL Image object
        
    Returns:
        Base64-encoded image string with data URL prefix
        
    Raises:
        ValueError: If image_path is None or invalid
        IOError: If image file cannot be read
    """
    if image_path is None:
        raise ValueError("Image path cannot be None")

    if isinstance(image_path, Image.Image):
        if not image_path.mode in ('RGB', 'RGBA', 'L'):
            raise ValueError(f"Unsupported image mode: {image_path.mode}")
        buffer = io.BytesIO()
        image_path.save(buffer, format=image_path.format or 'PNG')
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    try:
        async with aiofiles.open(image_path, "rb") as f:
            content = await f.read()
            encoded = base64.b64encode(content).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except IOError as e:
        raise IOError(f"Failed to read image file: {str(e)}")

def decode_image(image_data: str) -> Image.Image:
    """Decode a base64-encoded image.
    
    Args:
        image_data: Base64-encoded image string or data URL
        
    Returns:
        Decoded PIL Image
        
    Raises:
        ValueError: If image_data is None or invalid
        IOError: If image data cannot be decoded
    """
    if image_data is None:
        raise ValueError("Image data cannot be None")

    if not isinstance(image_data, str):
        raise ValueError("Image data must be a string")

    if image_data.startswith('data:'):
        # Remove data URL prefix
        image_data = image_data.split(',', 1)[1]

    try:
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        if not image.mode in ('RGB', 'RGBA', 'L'):
            image = image.convert('RGB')
        return image
    except Exception as e:
        raise IOError(f"Failed to decode image: {str(e)}")

def resize_image(image: Union[str, Path, Image.Image], max_size: int = 1024) -> Image.Image:
    """Resize an image while maintaining aspect ratio.
    
    Args:
        image: Path to the image file or PIL Image object
        max_size: Maximum dimension size
        
    Returns:
        Resized PIL Image
        
    Raises:
        ValueError: If image is None or max_size is invalid
        IOError: If image file cannot be read
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not isinstance(max_size, int) or max_size <= 0:
        raise ValueError("max_size must be a positive integer")

    try:
        if isinstance(image, (str, Path)):
            image = Image.open(image)
        
        if not image.mode in ('RGB', 'RGBA', 'L'):
            image = image.convert('RGB')
        
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        return image
    except Exception as e:
        raise IOError(f"Failed to resize image: {str(e)}")

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score
        
    Raises:
        ValueError: If vectors are None or have different lengths
    """
    if a is None or b is None:
        raise ValueError("Vectors cannot be None")
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    if not all(isinstance(x, (int, float)) for x in a + b):
        raise ValueError("Vectors must contain only numbers")

    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return np.dot(a, b) / (a_norm * b_norm)

def format_prompt(template: str, values: Dict[str, Any]) -> str:
    """Format a prompt template with variables.
    
    Args:
        template: Prompt template string
        values: Dictionary of template variables
        
    Returns:
        Formatted prompt string
        
    Raises:
        ValueError: If template is None or values is invalid
        KeyError: If template contains variables not in values
    """
    if template is None:
        raise ValueError("Template cannot be None")
    if not isinstance(template, str):
        raise ValueError("Template must be a string")
    if not isinstance(values, dict):
        raise ValueError("Values must be a dictionary")

    try:
        return template.format(**values)
    except KeyError as e:
        raise KeyError(f"Missing template variable: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to format prompt: {str(e)}")

def parse_model_options(options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse and validate model options.
    
    Args:
        options: Raw model options
        
    Returns:
        Validated model options
        
    Raises:
        ValueError: If options contain invalid values
    """
    if not options:
        return {}
    
    if not isinstance(options, dict):
        raise ValueError("Options must be a dictionary")
    
    valid_options = {
        "temperature": float,
        "top_p": float,
        "top_k": int,
        "repeat_penalty": float,
        "presence_penalty": float,
        "frequency_penalty": float,
        "mirostat": int,
        "mirostat_eta": float,
        "mirostat_tau": float,
        "num_ctx": int,
        "num_gpu": int,
        "num_thread": int,
        "repeat_last_n": int,
        "seed": int,
        "stop": Union[str, List[str]],
        "tfs_z": float,
        "num_predict": int,
        "typical_p": float,
    }
    
    parsed_options = {}
    for key, value in options.items():
        if key in valid_options:
            expected_type = valid_options[key]
            if isinstance(expected_type, type):
                try:
                    parsed_options[key] = expected_type(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid value for option {key}: {value}")
            else:
                parsed_options[key] = value
    
    return parsed_options

def format_chat_history(messages: List[Dict[str, Any]]) -> str:
    """Format chat history as a string.
    
    Args:
        messages: List of chat messages
        
    Returns:
        Formatted chat history string
        
    Raises:
        ValueError: If messages is None or invalid
    """
    if messages is None:
        raise ValueError("Messages cannot be None")
    if not isinstance(messages, list):
        raise ValueError("Messages must be a list")
    if not all(isinstance(msg, dict) for msg in messages):
        raise ValueError("All messages must be dictionaries")

    formatted = []
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        if not isinstance(role, str) or not isinstance(content, str):
            raise ValueError("Message role and content must be strings")
        formatted.append(f"{role}: {content}")
    return "\n".join(formatted)

def parse_model_name(name: str) -> tuple[str, Optional[str]]:
    """Parse a model name into its components.
    
    Args:
        name: Model name (e.g., "llama2:7b")
        
    Returns:
        Tuple of (model_name, version)
        
    Raises:
        ValueError: If name is None or invalid
    """
    if name is None:
        raise ValueError("Model name cannot be None")
    if not isinstance(name, str):
        raise ValueError("Model name must be a string")
    if not name:
        raise ValueError("Model name cannot be empty")

    parts = name.split(":")
    return parts[0], parts[1] if len(parts) > 1 else None 