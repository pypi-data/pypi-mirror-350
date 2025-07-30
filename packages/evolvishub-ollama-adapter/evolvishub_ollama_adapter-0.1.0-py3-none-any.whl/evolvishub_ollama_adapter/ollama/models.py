"""
Ollama-specific data models.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from typing import TextIO, BinaryIO, Iterator
import aiofiles
from datetime import datetime

class GenerateRequest(BaseModel):
    """Generate request model."""
    
    model: str = Field(..., min_length=1)
    prompt: str = Field(..., min_length=1)
    system: Optional[str] = Field(None, description="System prompt")
    template: Optional[str] = Field(None, description="Prompt template")
    context: Optional[List[int]] = Field(None, description="Context window")
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)
    stream: Optional[bool] = Field(False, description="Stream response")

    @field_validator("model")
    def validate_model(cls, v: str) -> str:
        """Validate model name."""
        if not v:
            raise ValueError("Model name cannot be empty")
        return v
        
    @field_validator("prompt")
    def validate_prompt(cls, v: str) -> str:
        """Validate prompt."""
        if not v:
            raise ValueError("Prompt cannot be empty")
        return v
        
    @field_validator("options")
    def validate_options(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Validate options."""
        if v is not None and not isinstance(v, dict):
            raise ValueError("Options must be a dictionary")
        return v

class GenerateResponse(BaseModel):
    """Generate response model."""
    
    model: str = Field(..., min_length=1)
    created_at: datetime
    response: str = Field(..., min_length=1)
    done: bool = True
    context: Optional[List[int]] = Field(None, description="Context window")
    total_duration: Optional[int] = Field(None, description="Total duration in nanoseconds")
    load_duration: Optional[int] = Field(None, description="Model load duration in nanoseconds")
    prompt_eval_count: Optional[int] = Field(None, description="Number of prompt tokens evaluated")
    prompt_eval_duration: Optional[int] = Field(None, description="Prompt evaluation duration in nanoseconds")
    eval_count: Optional[int] = Field(None, description="Number of tokens generated")
    eval_duration: Optional[int] = Field(None, description="Generation duration in nanoseconds")

class EmbeddingRequest(BaseModel):
    """Embedding request model."""
    
    model: str = Field(..., min_length=1)
    prompt: str = Field(..., min_length=1)
    options: Optional[Dict[str, Any]] = Field(None, description="Model options")

    @field_validator("model")
    def validate_model(cls, v: str) -> str:
        """Validate model name."""
        if not v:
            raise ValueError("Model name cannot be empty")
        return v
        
    @field_validator("prompt")
    def validate_prompt(cls, v: str) -> str:
        """Validate prompt."""
        if not v:
            raise ValueError("Prompt cannot be empty")
        return v

class EmbeddingResponse(BaseModel):
    """Embedding response model."""
    
    embedding: List[float] = Field(..., min_items=1)

    @field_validator("embedding")
    def validate_embedding(cls, v: List[float]) -> List[float]:
        """Validate embedding."""
        if not v:
            raise ValueError("Embedding cannot be empty")
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("Embedding must contain only numbers")
        return v

class ChatMessage(BaseModel):
    """Chat message model."""
    
    role: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    images: Optional[List[str]] = Field(None, description="Base64-encoded images")

    @field_validator("role")
    def validate_role(cls, v: str) -> str:
        """Validate role."""
        if not v:
            raise ValueError("Role cannot be empty")
        if v not in ("user", "assistant", "system"):
            raise ValueError("Role must be one of: user, assistant, system")
        return v
        
    @field_validator("content")
    def validate_content(cls, v: str) -> str:
        """Validate content."""
        if not v:
            raise ValueError("Content cannot be empty")
        return v

class ChatRequest(BaseModel):
    """Chat request model."""
    
    model: str = Field(..., min_length=1)
    messages: List[ChatMessage] = Field(..., min_items=1)
    stream: Optional[bool] = Field(False, description="Stream response")
    options: Optional[Dict[str, Any]] = Field(None, description="Model options")

    @field_validator("model")
    def validate_model(cls, v: str) -> str:
        """Validate model name."""
        if not v:
            raise ValueError("Model name cannot be empty")
        return v
        
    @field_validator("messages")
    def validate_messages(cls, v: List[ChatMessage]) -> List[ChatMessage]:
        """Validate messages."""
        if not v:
            raise ValueError("Messages cannot be empty")
        return v

class ChatResponse(BaseModel):
    """Chat response model."""
    
    model: str = Field(..., min_length=1)
    created_at: datetime
    message: ChatMessage
    done: bool = True
    total_duration: Optional[int] = Field(None, description="Total duration in nanoseconds")
    load_duration: Optional[int] = Field(None, description="Model load duration in nanoseconds")
    prompt_eval_count: Optional[int] = Field(None, description="Number of prompt tokens evaluated")
    prompt_eval_duration: Optional[int] = Field(None, description="Prompt evaluation duration in nanoseconds")
    eval_count: Optional[int] = Field(None, description="Number of tokens generated")
    eval_duration: Optional[int] = Field(None, description="Generation duration in nanoseconds")

class ModelInfo(BaseModel):
    """Model info model."""
    
    name: str = Field(..., min_length=1)
    modified_at: str = Field(..., description="Last modification timestamp")
    size: int = Field(..., gt=0)
    digest: str = Field(..., min_length=1)
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate name."""
        if not v:
            raise ValueError("Name cannot be empty")
        return v
        
    @field_validator("size")
    def validate_size(cls, v: int) -> int:
        """Validate size."""
        if v <= 0:
            raise ValueError("Size must be positive")
        return v
        
    @field_validator("digest")
    def validate_digest(cls, v: str) -> str:
        """Validate digest."""
        if not v:
            raise ValueError("Digest cannot be empty")
        return v

class ModelList(BaseModel):
    """Model list model."""
    
    models: List[ModelInfo] = Field(default_factory=list) 