"""
Tests for the models module.
"""

import pytest
from pydantic import ValidationError

from evolvishub_ollama_adapter.ollama.models import (
    GenerateRequest,
    GenerateResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ChatRequest,
    ChatResponse,
    ChatMessage,
    ModelInfo,
    ModelList,
)


def test_generate_request():
    """Test GenerateRequest model."""
    # Valid request
    request = GenerateRequest(
        model="llama2",
        prompt="Hello, world!",
        options={
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    assert request.model == "llama2"
    assert request.prompt == "Hello, world!"
    assert request.options["temperature"] == 0.7
    assert request.options["top_p"] == 0.9
    
    # Invalid model
    with pytest.raises(ValidationError):
        GenerateRequest(
            model="",  # Empty model name
            prompt="Hello, world!"
        )
    
    # Invalid prompt
    with pytest.raises(ValidationError):
        GenerateRequest(
            model="llama2",
            prompt=""  # Empty prompt
        )
    
    # Invalid options
    with pytest.raises(ValidationError):
        GenerateRequest(
            model="llama2",
            prompt="Hello, world!",
            options={"invalid": "option"}
        )


def test_generate_response():
    """Test GenerateResponse model."""
    # Valid response
    response = GenerateResponse(
        model="llama2",
        created_at="2024-01-01T00:00:00Z",
        response="Hello, world!",
        done=True
    )
    assert response.model == "llama2"
    assert response.response == "Hello, world!"
    assert response.done is True
    
    # Invalid model
    with pytest.raises(ValidationError):
        GenerateResponse(
            model="",  # Empty model name
            response="Hello, world!",
            done=True
        )
    
    # Invalid response
    with pytest.raises(ValidationError):
        GenerateResponse(
            model="llama2",
            response=None,  # None response
            done=True
        )


def test_embedding_request():
    """Test EmbeddingRequest model."""
    # Valid request
    request = EmbeddingRequest(
        model="llama2",
        prompt="Hello, world!"
    )
    assert request.model == "llama2"
    assert request.prompt == "Hello, world!"
    
    # Invalid model
    with pytest.raises(ValidationError):
        EmbeddingRequest(
            model="",  # Empty model name
            prompt="Hello, world!"
        )
    
    # Invalid prompt
    with pytest.raises(ValidationError):
        EmbeddingRequest(
            model="llama2",
            prompt=""  # Empty prompt
        )


def test_embedding_response():
    """Test EmbeddingResponse model."""
    # Valid response
    response = EmbeddingResponse(
        embedding=[0.1, 0.2, 0.3]
    )
    assert response.embedding == [0.1, 0.2, 0.3]
    
    # Invalid embedding
    with pytest.raises(ValidationError):
        EmbeddingResponse(
            embedding=[]  # Empty embedding
        )


def test_chat_message():
    """Test ChatMessage model."""
    # Valid message
    message = ChatMessage(
        role="user",
        content="Hello, world!"
    )
    assert message.role == "user"
    assert message.content == "Hello, world!"
    
    # Invalid role
    with pytest.raises(ValidationError):
        ChatMessage(
            role="invalid",  # Invalid role
            content="Hello, world!"
        )
    
    # Invalid content
    with pytest.raises(ValidationError):
        ChatMessage(
            role="user",
            content=""  # Empty content
        )


def test_chat_request():
    """Test ChatRequest model."""
    # Valid request
    request = ChatRequest(
        model="llama2",
        messages=[
            ChatMessage(role="user", content="Hi!"),
            ChatMessage(role="assistant", content="Hello!")
        ]
    )
    assert request.model == "llama2"
    assert len(request.messages) == 2
    assert request.messages[0].role == "user"
    assert request.messages[1].role == "assistant"
    
    # Invalid model
    with pytest.raises(ValidationError):
        ChatRequest(
            model="",  # Empty model name
            messages=[ChatMessage(role="user", content="Hi!")]
        )
    
    # Invalid messages
    with pytest.raises(ValidationError):
        ChatRequest(
            model="llama2",
            messages=[]  # Empty messages
        )


def test_chat_response():
    """Test ChatResponse model."""
    # Valid response
    message = ChatMessage(role="assistant", content="Hello!")
    response = ChatResponse(
        model="llama2",
        created_at="2024-01-01T00:00:00Z",
        message=message,
        done=True
    )
    assert response.model == "llama2"
    assert response.message.content == "Hello!"
    assert response.done is True
    
    # Invalid model
    with pytest.raises(ValidationError):
        ChatResponse(
            model="",  # Empty model name
            message=ChatMessage(role="assistant", content="Hello!"),
            done=True
        )
    
    # Invalid message
    with pytest.raises(ValidationError):
        ChatResponse(
            model="llama2",
            message=None,  # None message
            done=True
        )


def test_model_info():
    """Test ModelInfo model."""
    # Valid info
    info = ModelInfo(
        name="llama2",
        modified_at="2024-01-01T00:00:00Z",
        size=7000000000,
        digest="sha256:123",
        details={
            "format": "gguf",
            "family": "llama",
            "parameter_size": "7B"
        }
    )
    assert info.name == "llama2"
    assert info.modified_at == "2024-01-01T00:00:00Z"
    assert info.size == 7000000000
    assert info.digest == "sha256:123"
    assert info.details["format"] == "gguf"
    
    # Invalid name
    with pytest.raises(ValidationError):
        ModelInfo(
            name="",  # Empty name
            modified_at="2024-01-01T00:00:00Z",
            size=7000000000,
            digest="sha256:123",
            details={}
        )
    
    # Invalid size
    with pytest.raises(ValidationError):
        ModelInfo(
            name="llama2",
            modified_at="2024-01-01T00:00:00Z",
            size=-1,  # Negative size
            digest="sha256:123",
            details={}
        )


def test_model_list():
    """Test ModelList model."""
    # Valid list
    model_list = ModelList(
        models=[
            ModelInfo(
                name="llama2",
                modified_at="2024-01-01T00:00:00Z",
                size=7000000000,
                digest="sha256:123",
                details={}
            )
        ]
    )
    assert len(model_list.models) == 1
    assert model_list.models[0].name == "llama2"
    
    # Empty list
    model_list = ModelList(models=[])
    assert len(model_list.models) == 0
    
    # Invalid models
    with pytest.raises(ValidationError):
        ModelList(models=None)  # None models 