import requests
from typing import Dict, Any, Optional
from ..constants import DEFAULT_BASE_URL, DEFAULT_NUM_CTX

def generate_text(
    prompt: str,
    model: str,
    base_url: str = DEFAULT_BASE_URL,
    num_ctx: int = DEFAULT_NUM_CTX,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate text using Ollama model.
    
    Args:
        prompt (str): The input prompt for text generation
        model (str): The name of the model to use
        base_url (str): The base URL for the Ollama API
        num_ctx (int): The context window size
        **kwargs: Additional parameters to pass to the model
        
    Returns:
        Dict[str, Any]: The generated text response
    """
    url = f"{base_url}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "num_ctx": num_ctx,
        **kwargs
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json() 