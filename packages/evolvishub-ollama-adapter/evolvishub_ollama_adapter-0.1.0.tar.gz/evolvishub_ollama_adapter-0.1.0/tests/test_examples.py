"""Tests for example usage files."""

import asyncio
import pytest
from pathlib import Path

from evolvishub_ollama_adapter import OllamaClient
from evolvishub_ollama_adapter.sources import (
    FileDataSource,
    MemoryDataSource,
    DictDataSource
)

pytestmark = pytest.mark.asyncio

async def test_basic_usage(ollama_client, tmp_path):
    """Test the basic usage example."""
    # Create test data file
    data_file = tmp_path / "context.json"
    data_file.write_text('{"test": "data"}')
    
    # Initialize components
    data_source = FileDataSource(str(data_file), format="json")
    
    # Test data loading
    context = await data_source.load_data()
    assert context == {"test": "data"}
    
    # Test text generation
    response = await ollama_client.generate(
        prompt="What is Python?",
        context=context,
        max_tokens=50
    )
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Test data saving
    await data_source.save_data({"response": response})
    saved_data = await data_source.load_data()
    assert saved_data["response"] == response

async def test_advanced_usage(ollama_client, tmp_path):
    """Test the advanced usage example."""
    # Create test data file
    data_file = tmp_path / "advanced_context.json"
    data_file.write_text('{"test": "data"}')
    
    # Initialize components
    memory_source = MemoryDataSource()
    dict_source = DictDataSource()
    file_source = FileDataSource(str(data_file), format="json")
    
    # Test loading from file
    file_data = await file_source.load_data()
    assert file_data == {"test": "data"}
    
    # Test storing in memory
    await memory_source.save_data(file_data)
    memory_data = await memory_source.load_data()
    assert memory_data == file_data
    
    # Test dictionary operations
    await dict_source.save_data({
        "file_data": file_data,
        "status": "loaded"
    })
    dict_data = await dict_source.load_data()
    assert dict_data["file_data"] == file_data
    assert dict_data["status"] == "loaded"
    
    # Test text generation with context
    response = await ollama_client.generate(
        prompt="What is Python?",
        context=file_data,
        max_tokens=50,
        temperature=0.7
    )
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Test saving response to all sources
    await memory_source.save_data({"response": response})
    await dict_source.set("last_response", response)
    await file_source.save_data({
        "prompt": "What is Python?",
        "response": response,
        "context": file_data
    })
    
    # Verify saved data
    memory_response = (await memory_source.load_data())["response"]
    dict_response = await dict_source.get("last_response")
    file_data = await file_source.load_data()
    
    assert memory_response == response
    assert dict_response == response
    assert file_data["response"] == response
    
    # Test cleanup
    await memory_source.clear()
    await dict_source.clear()
    
    assert await memory_source.load_data() == {}
    assert await dict_source.load_data() == {} 