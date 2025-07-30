import pytest
import numpy as np
from PIL import Image
import io
import base64
from evolvishub_ollama_adapter.utils import (
    encode_image,
    encode_image_async,
    decode_image,
    resize_image,
    cosine_similarity,
    format_prompt,
    parse_model_options,
    format_chat_history,
    parse_model_name
)
from evolvishub_ollama_adapter.exceptions import ValidationError

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img = Image.new('RGB', (100, 100), color='red')
    return img

@pytest.fixture
def sample_image_bytes(sample_image):
    """Convert sample image to bytes."""
    img_byte_arr = io.BytesIO()
    sample_image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def test_encode_image():
    """Test image encoding."""
    # Create a test image
    image = Image.new('RGB', (100, 100), color='red')
    
    # Test with PIL Image
    encoded = encode_image(image)
    assert encoded.startswith('data:image/png;base64,')
    
    # Test with None
    with pytest.raises(ValueError):
        encode_image(None)
    
    # Test with invalid image mode
    image = Image.new('CMYK', (100, 100))
    with pytest.raises(ValueError):
        encode_image(image)

@pytest.mark.asyncio
async def test_encode_image_async():
    """Test async image encoding."""
    # Create a test image
    image = Image.new('RGB', (100, 100), color='red')
    
    # Test with PIL Image
    encoded = await encode_image_async(image)
    assert encoded.startswith('data:image/png;base64,')
    
    # Test with None
    with pytest.raises(ValueError):
        await encode_image_async(None)
    
    # Test with invalid image mode
    image = Image.new('CMYK', (100, 100))
    with pytest.raises(ValueError):
        await encode_image_async(image)

def test_decode_image():
    """Test image decoding."""
    # Create a test image
    image = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Test with base64 string
    decoded = decode_image(encoded)
    assert isinstance(decoded, Image.Image)
    assert decoded.size == (100, 100)
    
    # Test with data URL
    data_url = f'data:image/png;base64,{encoded}'
    decoded = decode_image(data_url)
    assert isinstance(decoded, Image.Image)
    assert decoded.size == (100, 100)
    
    # Test with None
    with pytest.raises(ValueError):
        decode_image(None)
    
    # Test with invalid data
    with pytest.raises(IOError):
        decode_image('invalid')

def test_resize_image():
    """Test image resizing."""
    # Create a test image
    image = Image.new('RGB', (2000, 1000), color='red')
    
    # Test resizing
    resized = resize_image(image, max_size=1000)
    assert isinstance(resized, Image.Image)
    assert max(resized.size) == 1000
    
    # Test with None
    with pytest.raises(ValueError):
        resize_image(None)
    
    # Test with invalid max_size
    with pytest.raises(ValueError):
        resize_image(image, max_size=0)

def test_cosine_similarity():
    """Test cosine similarity calculation."""
    # Test with valid vectors
    a = [1, 2, 3]
    b = [4, 5, 6]
    similarity = cosine_similarity(a, b)
    assert isinstance(similarity, float)
    assert 0 <= similarity <= 1
    
    # Test with None
    with pytest.raises(ValueError):
        cosine_similarity(None, b)
    
    # Test with different lengths
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1, 2, 3])
    
    # Test with non-numeric values
    with pytest.raises(ValueError):
        cosine_similarity([1, '2'], [1, 2])

def test_format_prompt():
    """Test prompt formatting."""
    # Test with valid template and values
    template = "Hello, {name}!"
    values = {"name": "World"}
    formatted = format_prompt(template, values)
    assert formatted == "Hello, World!"
    
    # Test with None template
    with pytest.raises(ValueError):
        format_prompt(None, values)
    
    # Test with invalid template type
    with pytest.raises(ValueError):
        format_prompt(123, values)
    
    # Test with invalid values type
    with pytest.raises(ValueError):
        format_prompt(template, "invalid")
    
    # Test with missing variable
    with pytest.raises(KeyError):
        format_prompt(template, {})

def test_parse_model_options():
    """Test model options parsing."""
    # Test with valid options
    options = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "mirostat": 0,
        "mirostat_eta": 0.1,
        "mirostat_tau": 5.0,
        "num_ctx": 2048,
        "num_gpu": 1,
        "num_thread": 4,
        "repeat_last_n": 64,
        "seed": 42,
        "stop": ["\n", "Human:"],
        "tfs_z": 1.0,
        "num_predict": 128,
        "typical_p": 0.9,
    }
    parsed = parse_model_options(options)
    assert isinstance(parsed, dict)
    assert all(key in parsed for key in options)
    
    # Test with None
    assert parse_model_options(None) == {}
    
    # Test with invalid options type
    with pytest.raises(ValueError):
        parse_model_options("invalid")
    
    # Test with invalid option value
    with pytest.raises(ValueError):
        parse_model_options({"temperature": "invalid"})

def test_format_chat_history():
    """Test chat history formatting."""
    # Test messages
    messages = [
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "How are you?"}
    ]
    
    # Format history
    history = format_chat_history(messages)
    
    # Verify result
    assert history == "User: Hi!\nAssistant: Hello!\nUser: How are you?"

def test_parse_model_name():
    """Test model name parsing."""
    # Test cases
    test_cases = [
        ("llama2", ("llama2", None)),
        ("llama2:7b", ("llama2", "7b")),
        ("mistral:7b-instruct", ("mistral", "7b-instruct")),
        ("codellama:13b-python", ("codellama", "13b-python"))
    ]
    
    # Test each case
    for input_name, expected in test_cases:
        name, version = parse_model_name(input_name)
        assert (name, version) == expected

def test_encode_image_invalid_input():
    """Test image encoding with invalid input."""
    # Test with None
    with pytest.raises((ValueError, OSError)):
        encode_image(None)
    # Test with invalid type
    with pytest.raises((ValueError, OSError)):
        encode_image("not an image")

def test_decode_image_invalid_input():
    """Test image decoding with invalid input."""
    # Test with None
    with pytest.raises((ValueError, OSError)):
        decode_image(None)
    # Test with invalid format
    with pytest.raises((ValueError, OSError)):
        decode_image("not a data URL")
    # Test with invalid base64
    with pytest.raises((ValueError, OSError)):
        decode_image("data:image/png;base64,invalid")

def test_resize_image_invalid_input():
    """Test image resizing with invalid input."""
    # Test with None
    with pytest.raises(ValueError):
        resize_image(None)
    
    # Test with invalid size
    with pytest.raises(ValueError):
        resize_image(Image.new('RGB', (100, 100)), max_size=0)

def test_cosine_similarity_invalid_input():
    """Test cosine similarity with invalid input."""
    # Test with None
    with pytest.raises(ValueError):
        cosine_similarity(None, np.array([1, 0, 0]))
    
    # Test with different dimensions
    with pytest.raises(ValueError):
        cosine_similarity(np.array([1, 0]), np.array([1, 0, 0]))

def test_format_prompt_invalid_input():
    """Test prompt formatting with invalid input."""
    # Test with None
    with pytest.raises(ValueError):
        format_prompt(None, {})
    
    # Test with missing value
    with pytest.raises(KeyError):
        format_prompt("Hello, {name}!", {})

def test_parse_model_options_invalid_input():
    """Test model options parsing with invalid input."""
    # Test with None
    with pytest.raises((ValueError, TypeError, ValidationError)):
        parse_model_options(None)
    # Test with invalid option
    with pytest.raises((ValueError, TypeError, ValidationError)):
        parse_model_options({"invalid": "option"})

def test_format_chat_history_invalid_input():
    """Test chat history formatting with invalid input."""
    # Test with None
    with pytest.raises((ValueError, KeyError, TypeError, ValidationError)):
        format_chat_history(None)
    # Test with invalid message
    with pytest.raises((KeyError, ValueError, TypeError, ValidationError)):
        format_chat_history([{"invalid": "message"}])

def test_parse_model_name_invalid_input():
    """Test model name parsing with invalid input."""
    # Test with None
    with pytest.raises(ValueError):
        parse_model_name(None)
    
    # Test with empty string
    with pytest.raises(ValueError):
        parse_model_name("") 