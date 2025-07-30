"""
Ollama-specific implementations for the adapter.
"""

from .models import (
    GenerateRequest, GenerateResponse,
    EmbeddingRequest, EmbeddingResponse,
    ChatRequest, ChatResponse,
    ModelInfo, ModelList
)
from .utils import (
    encode_image, encode_image_async, decode_image,
    resize_image, cosine_similarity, format_prompt,
    parse_model_options, format_chat_history, parse_model_name
)

__all__ = [
    "GenerateRequest", "GenerateResponse",
    "EmbeddingRequest", "EmbeddingResponse",
    "ChatRequest", "ChatResponse",
    "ModelInfo", "ModelList",
    "encode_image", "encode_image_async", "decode_image",
    "resize_image", "cosine_similarity", "format_prompt",
    "parse_model_options", "format_chat_history", "parse_model_name"
] 