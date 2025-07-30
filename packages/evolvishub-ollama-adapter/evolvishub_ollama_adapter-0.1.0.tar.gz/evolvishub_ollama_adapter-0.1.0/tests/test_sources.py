"""
Tests for the data sources module.
"""

import json
from pathlib import Path

import pytest
import yaml

from evolvishub_ollama_adapter.sources import (
    DataSource,
    DictDataSource,
    FileDataSource,
    MemoryDataSource,
)
from evolvishub_ollama_adapter.exceptions import DataSourceError

pytestmark = pytest.mark.asyncio

# Test data
TEST_DATA = {
    "text": "Hello, World!",
    "number": 42,
    "list": [1, 2, 3],
    "dict": {"key": "value"}
}

async def test_abstract_data_source():
    """Test that DataSource cannot be instantiated."""
    with pytest.raises(TypeError):
        DataSource()

async def test_memory_data_source_initialization():
    """Test MemoryDataSource initialization."""
    source = MemoryDataSource()
    assert isinstance(source, MemoryDataSource)
    assert source.source == {}

async def test_memory_data_source_with_initial_data():
    """Test MemoryDataSource with initial data."""
    source = MemoryDataSource(initial_data=TEST_DATA)
    assert source.source == TEST_DATA

async def test_memory_data_source_load_save(memory_source):
    """Test MemoryDataSource load and save operations."""
    # Save data
    await memory_source.save_data(TEST_DATA)
    assert memory_source.source == TEST_DATA

    # Load data
    loaded_data = await memory_source.load_data()
    assert loaded_data == TEST_DATA

async def test_dict_data_source_initialization():
    """Test DictDataSource initialization."""
    source = DictDataSource(source={}, model_class=dict)
    assert isinstance(source, DictDataSource)
    assert source.source == {}
    assert source.model_class == dict

async def test_dict_data_source_operations():
    """Test DictDataSource operations."""
    source = DictDataSource(source={}, model_class=dict)
    test_data = {"key": "value"}
    
    # Save data
    await source.save_data(test_data)
    assert source.source == test_data
    
    # Get data
    data = await source.get_data()
    assert data == test_data

async def test_file_data_source_initialization(tmp_path):
    """Test FileDataSource initialization."""
    test_file = tmp_path / "test.json"
    source = FileDataSource(str(test_file), format="json")
    assert isinstance(source, FileDataSource)
    assert source.file_path == str(test_file)
    assert source.format == "json"

async def test_file_data_source_invalid_format(tmp_path):
    """Test FileDataSource with invalid format."""
    test_file = tmp_path / "test.txt"
    with pytest.raises(DataSourceError):
        FileDataSource(str(test_file), format="invalid")

async def test_file_data_source_json_operations(tmp_path):
    """Test FileDataSource JSON operations."""
    test_file = tmp_path / "test.json"
    source = FileDataSource(str(test_file), format="json")
    
    # Save data
    test_data = {"key": "value"}
    await source.save_data(test_data)
    assert Path(source.file_path).exists()
    
    # Get data
    data = await source.get_data()
    assert data == test_data

async def test_file_data_source_yaml_operations(tmp_path):
    """Test FileDataSource YAML operations."""
    test_file = tmp_path / "test.yaml"
    source = FileDataSource(str(test_file), format="yaml")
    
    # Save data
    test_data = {"key": "value"}
    await source.save_data(test_data)
    assert Path(source.file_path).exists()
    
    # Get data
    data = await source.get_data()
    assert data == test_data

async def test_file_data_source_text_operations(tmp_path):
    """Test FileDataSource text operations."""
    test_file = tmp_path / "test.txt"
    source = FileDataSource(str(test_file), format="text")
    
    # Save data
    test_data = "Hello, world!"
    await source.save_data(test_data)
    assert Path(source.file_path).exists()
    
    # Get data
    data = await source.get_data()
    assert data == test_data

async def test_file_data_source_nonexistent_file(tmp_path):
    """Test FileDataSource with nonexistent file."""
    test_file = tmp_path / "nonexistent.json"
    source = FileDataSource(str(test_file), format="json")
    
    # Try to get data from nonexistent file
    with pytest.raises(DataSourceError):
        await source.get_data()

    # Saving should create the file
    await source.save_data(TEST_DATA)
    assert Path(source.file_path).exists()
    loaded_data = await source.load_data()
    assert loaded_data == TEST_DATA 