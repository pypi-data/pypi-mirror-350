"""
Ollama-specific utility functions.
"""

import base64
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

import aiofiles
from PIL import Image
import numpy as np

def encode_image(image_path: Union[str, Path]) -> str:
    """Encode an image file to base64.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64-encoded image string
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

async def encode_image_async(image_path: Union[str, Path]) -> str:
    """Asynchronously encode an image file to base64.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64-encoded image string
    """
    async with aiofiles.open(image_path, "rb") as f:
        content = await f.read()
        return base64.b64encode(content).decode("utf-8")

def decode_image(image_data: str) -> bytes:
    """Decode a base64-encoded image.
    
    Args:
        image_data: Base64-encoded image string
        
    Returns:
        Decoded image bytes
    """
    return base64.b64decode(image_data)

def resize_image(image_path: Union[str, Path], max_size: int = 1024) -> Image.Image:
    """Resize an image while maintaining aspect ratio.
    
    Args:
        image_path: Path to the image file
        max_size: Maximum dimension size
        
    Returns:
        Resized PIL Image
    """
    image = Image.open(image_path)
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    return image

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score
    """
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return np.dot(a, b) / (a_norm * b_norm)

def format_prompt(template: str, **kwargs: Any) -> str:
    """Format a prompt template with variables.
    
    Args:
        template: Prompt template string
        **kwargs: Template variables
        
    Returns:
        Formatted prompt string
    """
    return template.format(**kwargs)

def parse_model_options(options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse and validate model options.
    
    Args:
        options: Raw model options
        
    Returns:
        Validated model options
    """
    if not options:
        return {}
    
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
    """
    formatted = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")
    return "\n".join(formatted)

def parse_model_name(name: str) -> Dict[str, str]:
    """Parse a model name into its components.
    
    Args:
        name: Model name (e.g., "llama2:7b")
        
    Returns:
        Dictionary with model components
    """
    parts = name.split(":")
    return {
        "name": parts[0],
        "version": parts[1] if len(parts) > 1 else None,
        "variant": parts[2] if len(parts) > 2 else None
    } 