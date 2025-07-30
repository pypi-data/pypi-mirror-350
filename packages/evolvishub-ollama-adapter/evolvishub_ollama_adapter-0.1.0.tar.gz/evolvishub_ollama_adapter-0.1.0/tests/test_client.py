"""
Integration tests for the client module.
"""

import json
import pytest
import pytest_asyncio
from typing import AsyncGenerator

from evolvishub_ollama_adapter.client import OllamaClient
from evolvishub_ollama_adapter.ollama.models import GenerateRequest, GenerateResponse, ModelList
from evolvishub_ollama_adapter.exceptions import OllamaError, ValidationError
from evolvishub_ollama_adapter.config import Config

@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initialization."""
    client = OllamaClient()
    assert client.host == "localhost"
    assert client.port == 11434
    assert client.timeout == 30
    assert client.base_url == "http://localhost:11434"

    client = OllamaClient(host="custom", port=1234, timeout=60)
    assert client.host == "custom"
    assert client.port == 1234
    assert client.timeout == 60
    assert client.base_url == "http://custom:1234"

@pytest.mark.asyncio
async def test_generate(async_ollama_client):
    """Test text generation."""
    response = await async_ollama_client.agenerate("Hello, world!")
    assert isinstance(response, dict)
    assert "response" in response

@pytest.mark.asyncio
async def test_generate_stream(async_ollama_client):
    """Test streaming text generation."""
    responses = []
    async for response in await async_ollama_client.agenerate(
        prompt="What is the capital of France?",
        model="llama2",
        stream=True
    ):
        responses.append(response)
    
    assert len(responses) > 0
    assert all(isinstance(r, dict) for r in responses)
    assert all("response" in r for r in responses)
    assert responses[-1].get("done", False)

@pytest.mark.asyncio
async def test_list_models(async_ollama_client):
    """Test listing models."""
    response = await async_ollama_client.alist_models()
    assert isinstance(response, dict)
    assert "models" in response

@pytest.mark.asyncio
async def test_health_check(async_ollama_client):
    """Test health check."""
    is_healthy = await async_ollama_client.health_check()
    assert is_healthy is True

@pytest.mark.asyncio
async def test_invalid_model(async_ollama_client):
    """Test generation with invalid model."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="")

@pytest.mark.asyncio
async def test_invalid_prompt(async_ollama_client):
    """Test generation with invalid prompt."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("", model="llama2")

@pytest.mark.asyncio
async def test_invalid_options(async_ollama_client):
    """Test generation with invalid options."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", options="invalid")

@pytest.mark.asyncio
async def test_invalid_stream(async_ollama_client):
    """Test generation with invalid stream parameter."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", stream="invalid")

@pytest.mark.asyncio
async def test_invalid_context(async_ollama_client):
    """Test generation with invalid context."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", context="invalid")

@pytest.mark.asyncio
async def test_invalid_system(async_ollama_client):
    """Test generation with invalid system prompt."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", system=123)

@pytest.mark.asyncio
async def test_invalid_template(async_ollama_client):
    """Test generation with invalid template."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", template=123)

@pytest.mark.asyncio
async def test_invalid_model_name(async_ollama_client):
    """Test generation with invalid model name."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model=123)

@pytest.mark.asyncio
async def test_invalid_prompt_type(async_ollama_client):
    """Test generation with invalid prompt type."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate(123, model="llama2")

@pytest.mark.asyncio
async def test_invalid_options_type(async_ollama_client):
    """Test generation with invalid options type."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", options=123)

@pytest.mark.asyncio
async def test_invalid_stream_type(async_ollama_client):
    """Test generation with invalid stream type."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", stream=123)

@pytest.mark.asyncio
async def test_invalid_context_type(async_ollama_client):
    """Test generation with invalid context type."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", context=123)

@pytest.mark.asyncio
async def test_invalid_system_type(async_ollama_client):
    """Test generation with invalid system type."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", system=123)

@pytest.mark.asyncio
async def test_invalid_template_type(async_ollama_client):
    """Test generation with invalid template type."""
    with pytest.raises(ValidationError):
        await async_ollama_client.agenerate("test", model="llama2", template=123)

@pytest.mark.asyncio
async def test_generate_with_context(async_ollama_client):
    """Test text generation with context."""
    context = {
        "system_prompt": "You are a helpful AI assistant.",
        "examples": [
            {"prompt": "What is Python?", "response": "Python is a programming language."}
        ]
    }
    response = await async_ollama_client.agenerate(
        prompt="What is Python?",
        context=context,
        max_tokens=50
    )
    assert isinstance(response, dict)
    assert "response" in response

@pytest.mark.asyncio
async def test_generate_with_parameters(async_ollama_client):
    """Test text generation with custom parameters."""
    response = await async_ollama_client.agenerate(
        prompt="What is Python?",
        max_tokens=50,
        temperature=0.7,
        top_p=0.9
    )
    assert isinstance(response, dict)
    assert "response" in response 