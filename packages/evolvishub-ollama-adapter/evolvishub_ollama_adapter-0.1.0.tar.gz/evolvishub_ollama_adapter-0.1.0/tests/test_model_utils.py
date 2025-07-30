"""Tests for model utilities."""

import os
import json
import pytest
from pathlib import Path

from evolvishub_ollama_adapter.model_utils import (
    load_model,
    save_model,
    get_model_info,
    get_model_architecture,
    get_model_config,
    get_model_weights,
    set_model_weights,
    get_model_device,
    set_model_device,
    get_model_dtype,
    set_model_dtype,
    get_model_mode,
    set_model_mode,
    get_model_metrics,
    get_model_loss,
    get_model_accuracy,
)

@pytest.fixture
def sample_model():
    """Create a sample model for testing."""
    return {
        "name": "test_model",
        "version": "1.0.0",
        "architecture": "transformer",
        "parameters": {
            "num_layers": 12,
            "hidden_size": 768,
            "num_heads": 12,
            "vocab_size": 50000,
        },
        "description": "Test model",
        "author": "Test Author",
        "license": "MIT",
        "created_at": "2024-01-01",
        "updated_at": "2024-01-01",
        "weights": {
            "layer1": {"weight": 1.0},
            "layer2": {"weight": 2.0},
        },
        "device": "cpu",
        "dtype": "float32",
        "mode": "eval",
        "metrics": {
            "loss": 0.1,
            "accuracy": 0.95,
        },
    }

@pytest.fixture
def temp_model_file(tmp_path):
    """Create a temporary model file for testing."""
    model_path = tmp_path / "test_model.json"
    return str(model_path)

def test_load_model(temp_model_file, sample_model):
    """Test loading a model from file."""
    # Save model first
    save_model(sample_model, temp_model_file)
    
    # Load model
    loaded_model = load_model(temp_model_file)
    assert loaded_model == sample_model
    
    # Test invalid path
    with pytest.raises(ValueError):
        load_model("nonexistent_model.json")
        
    # Test invalid input
    with pytest.raises(ValueError):
        load_model("")

def test_save_model(temp_model_file, sample_model):
    """Test saving a model to file."""
    # Save model
    save_model(sample_model, temp_model_file)
    
    # Verify file exists and content
    assert os.path.exists(temp_model_file)
    with open(temp_model_file, "r") as f:
        saved_model = json.load(f)
    assert saved_model == sample_model
    
    # Test invalid model
    with pytest.raises(ValueError):
        save_model({}, temp_model_file)
        
    # Test invalid path
    with pytest.raises(ValueError):
        save_model(sample_model, "")

def test_get_model_info(sample_model):
    """Test getting model information."""
    info = get_model_info(sample_model)
    assert info["name"] == sample_model["name"]
    assert info["version"] == sample_model["version"]
    assert info["architecture"] == sample_model["architecture"]
    assert info["parameters"] == sample_model["parameters"]
    assert info["description"] == sample_model["description"]
    assert info["author"] == sample_model["author"]
    assert info["license"] == sample_model["license"]
    assert info["created_at"] == sample_model["created_at"]
    assert info["updated_at"] == sample_model["updated_at"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_info({})

def test_get_model_architecture(sample_model):
    """Test getting model architecture."""
    architecture = get_model_architecture(sample_model)
    assert architecture == sample_model["architecture"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_architecture({})

def test_get_model_config(sample_model):
    """Test getting model configuration."""
    config = get_model_config(sample_model)
    assert config == sample_model["parameters"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_config({})

def test_get_model_weights(sample_model):
    """Test getting model weights."""
    weights = get_model_weights(sample_model)
    assert weights == sample_model["weights"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_weights({})

def test_set_model_weights(sample_model):
    """Test setting model weights."""
    new_weights = {"layer3": {"weight": 3.0}}
    set_model_weights(sample_model, new_weights)
    assert sample_model["weights"] == new_weights
    
    # Test invalid model
    with pytest.raises(ValueError):
        set_model_weights({}, new_weights)
        
    # Test invalid weights
    with pytest.raises(ValueError):
        set_model_weights(sample_model, "invalid")

def test_get_model_device(sample_model):
    """Test getting model device."""
    device = get_model_device(sample_model)
    assert device == sample_model["device"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_device({})

def test_set_model_device(sample_model):
    """Test setting model device."""
    new_device = "cuda"
    set_model_device(sample_model, new_device)
    assert sample_model["device"] == new_device
    
    # Test invalid model
    with pytest.raises(ValueError):
        set_model_device({}, new_device)
        
    # Test invalid device
    with pytest.raises(ValueError):
        set_model_device(sample_model, "")

def test_get_model_dtype(sample_model):
    """Test getting model data type."""
    dtype = get_model_dtype(sample_model)
    assert dtype == sample_model["dtype"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_dtype({})

def test_set_model_dtype(sample_model):
    """Test setting model data type."""
    new_dtype = "float16"
    set_model_dtype(sample_model, new_dtype)
    assert sample_model["dtype"] == new_dtype
    
    # Test invalid model
    with pytest.raises(ValueError):
        set_model_dtype({}, new_dtype)
        
    # Test invalid dtype
    with pytest.raises(ValueError):
        set_model_dtype(sample_model, "")

def test_get_model_mode(sample_model):
    """Test getting model mode."""
    mode = get_model_mode(sample_model)
    assert mode == sample_model["mode"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_mode({})

def test_set_model_mode(sample_model):
    """Test setting model mode."""
    new_mode = "train"
    set_model_mode(sample_model, new_mode)
    assert sample_model["mode"] == new_mode
    
    # Test invalid model
    with pytest.raises(ValueError):
        set_model_mode({}, new_mode)
        
    # Test invalid mode
    with pytest.raises(ValueError):
        set_model_mode(sample_model, "")

def test_get_model_metrics(sample_model):
    """Test getting model metrics."""
    metrics = get_model_metrics(sample_model)
    assert metrics == sample_model["metrics"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_metrics({})

def test_get_model_loss(sample_model):
    """Test getting model loss."""
    loss = get_model_loss(sample_model)
    assert loss == sample_model["metrics"]["loss"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_loss({})

def test_get_model_accuracy(sample_model):
    """Test getting model accuracy."""
    accuracy = get_model_accuracy(sample_model)
    assert accuracy == sample_model["metrics"]["accuracy"]
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_accuracy({}) 