"""
Test configuration and fixtures.
"""

import os
import pytest
import pytest_asyncio
import aiohttp
import requests
import time
from typing import AsyncGenerator, Generator
from aiohttp import ClientSession

from evolvishub_ollama_adapter.client import OllamaClient
from evolvishub_ollama_adapter.ollama.models import GenerateRequest, GenerateResponse
from evolvishub_ollama_adapter.config import Config

def wait_for_ollama(max_retries=30, retry_interval=1):
    """Wait for Ollama to be ready."""
    for _ in range(max_retries):
        try:
            response = requests.get("http://localhost:11434/api/health")
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(retry_interval)
    return False

@pytest.fixture(scope="session", autouse=True)
def setup_ollama():
    """Set up Ollama for testing."""
    if not wait_for_ollama():
        pytest.skip("Ollama is not available")
    yield

@pytest.fixture
def ollama_client() -> Generator[OllamaClient, None, None]:
    """Create an Ollama client for testing."""
    client = OllamaClient(base_url="http://localhost:11434")
    yield client
    client.close()

@pytest_asyncio.fixture
async def async_ollama_client() -> AsyncGenerator[OllamaClient, None]:
    """Create an async Ollama client for testing."""
    client = OllamaClient(base_url="http://localhost:11434")
    yield client
    await client.aclose()

@pytest.fixture
def generate_request() -> GenerateRequest:
    """Create a sample generate request for testing."""
    return GenerateRequest(
        model="llama2",
        prompt="What is the capital of France?",
        stream=False,
    )

@pytest_asyncio.fixture
async def async_client_session() -> AsyncGenerator[ClientSession, None]:
    """Create an async client session for testing."""
    async with ClientSession() as session:
        yield session

@pytest.fixture
def config() -> Config:
    """Create a test configuration."""
    return Config(
        host="localhost",
        port=11434,
        timeout=30,
        model="llama2"
    ) 