import pytest
import os
import tempfile
import shutil
from pathlib import Path
from evolvishub_ollama_adapter.file_utils import (
    ensure_directory,
    get_file_extension,
    is_supported_format,
    get_file_size,
    get_file_mime_type,
    read_file_content,
    write_file_content,
    copy_file,
    move_file,
    delete_file,
    list_directory,
    create_temp_file,
    get_file_hash
)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    # Create text file
    text_file = os.path.join(temp_dir, "test.txt")
    with open(text_file, "w") as f:
        f.write("Hello, World!")
    
    # Create binary file
    binary_file = os.path.join(temp_dir, "test.bin")
    with open(binary_file, "wb") as f:
        f.write(b"Binary content")
    
    # Create image file
    image_file = os.path.join(temp_dir, "test.png")
    with open(image_file, "wb") as f:
        f.write(b"PNG image content")
    
    return {
        "text": text_file,
        "binary": binary_file,
        "image": image_file
    }

def test_ensure_directory(temp_dir):
    """Test directory creation and existence check."""
    # Test creating new directory
    new_dir = os.path.join(temp_dir, "new_dir")
    ensure_directory(new_dir)
    assert os.path.exists(new_dir)
    assert os.path.isdir(new_dir)
    
    # Test existing directory
    ensure_directory(new_dir)  # Should not raise error
    assert os.path.exists(new_dir)
    
    # Test with nested path
    nested_dir = os.path.join(temp_dir, "nested", "deep", "path")
    ensure_directory(nested_dir)
    assert os.path.exists(nested_dir)
    assert os.path.isdir(nested_dir)

def test_get_file_extension(sample_files):
    """Test file extension extraction."""
    assert get_file_extension(sample_files["text"]) == "txt"
    assert get_file_extension(sample_files["binary"]) == "bin"
    assert get_file_extension(sample_files["image"]) == "png"
    
    # Test with no extension
    no_ext = os.path.join(os.path.dirname(sample_files["text"]), "noext")
    assert get_file_extension(no_ext) == ""

def test_is_supported_format(sample_files):
    """Test format support checking."""
    assert is_supported_format(sample_files["text"], ["txt", "md"])
    assert is_supported_format(sample_files["image"], ["png", "jpg"])
    assert not is_supported_format(sample_files["binary"], ["txt", "md"])
    
    # Test with no extension
    no_ext = os.path.join(os.path.dirname(sample_files["text"]), "noext")
    assert not is_supported_format(no_ext, ["txt", "md"])

def test_get_file_size(sample_files):
    """Test file size retrieval."""
    assert get_file_size(sample_files["text"]) == 13  # "Hello, World!"
    assert get_file_size(sample_files["binary"]) == 14  # "Binary content"
    assert get_file_size(sample_files["image"]) == 17  # "PNG image content"
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        get_file_size("nonexistent.txt")

def test_get_file_mime_type(sample_files):
    """Test MIME type detection."""
    assert get_file_mime_type(sample_files["text"]) == "text/plain"
    assert get_file_mime_type(sample_files["image"]) == "image/png"
    assert get_file_mime_type(sample_files["binary"]) == "application/octet-stream"
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        get_file_mime_type("nonexistent.txt")

def test_read_file_content(sample_files):
    """Test file content reading."""
    # Test text file
    content = read_file_content(sample_files["text"])
    assert content == "Hello, World!"
    
    # Test binary file
    content = read_file_content(sample_files["binary"], binary=True)
    assert content == b"Binary content"
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        read_file_content("nonexistent.txt")

def test_write_file_content(temp_dir):
    """Test file content writing."""
    # Test text file
    text_file = os.path.join(temp_dir, "write_test.txt")
    write_file_content(text_file, "Test content")
    assert os.path.exists(text_file)
    with open(text_file, "r") as f:
        assert f.read() == "Test content"
    
    # Test binary file
    binary_file = os.path.join(temp_dir, "write_test.bin")
    write_file_content(binary_file, b"Binary content", binary=True)
    assert os.path.exists(binary_file)
    with open(binary_file, "rb") as f:
        assert f.read() == b"Binary content"

def test_copy_file(sample_files, temp_dir):
    """Test file copying."""
    # Test text file copy
    dest = os.path.join(temp_dir, "copy.txt")
    copy_file(sample_files["text"], dest)
    assert os.path.exists(dest)
    with open(dest, "r") as f:
        assert f.read() == "Hello, World!"
    
    # Test binary file copy
    dest = os.path.join(temp_dir, "copy.bin")
    copy_file(sample_files["binary"], dest)
    assert os.path.exists(dest)
    with open(dest, "rb") as f:
        assert f.read() == b"Binary content"
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        copy_file("nonexistent.txt", dest)

def test_move_file(sample_files, temp_dir):
    """Test file moving."""
    # Test text file move
    dest = os.path.join(temp_dir, "move.txt")
    move_file(sample_files["text"], dest)
    assert os.path.exists(dest)
    assert not os.path.exists(sample_files["text"])
    with open(dest, "r") as f:
        assert f.read() == "Hello, World!"
    
    # Test binary file move
    dest = os.path.join(temp_dir, "move.bin")
    move_file(sample_files["binary"], dest)
    assert os.path.exists(dest)
    assert not os.path.exists(sample_files["binary"])
    with open(dest, "rb") as f:
        assert f.read() == b"Binary content"
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        move_file("nonexistent.txt", dest)

def test_delete_file(sample_files):
    """Test file deletion."""
    # Test text file deletion
    delete_file(sample_files["text"])
    assert not os.path.exists(sample_files["text"])
    
    # Test binary file deletion
    delete_file(sample_files["binary"])
    assert not os.path.exists(sample_files["binary"])
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        delete_file("nonexistent.txt")

def test_list_directory(temp_dir, sample_files):
    """Test directory listing."""
    # Create subdirectory
    subdir = os.path.join(temp_dir, "subdir")
    os.makedirs(subdir)
    
    # List directory
    files = list_directory(temp_dir)
    assert len(files) == 4  # 3 files + 1 subdirectory
    assert "test.txt" in files
    assert "test.bin" in files
    assert "test.png" in files
    assert "subdir" in files
    
    # List with pattern
    files = list_directory(temp_dir, pattern="*.txt")
    assert len(files) == 1
    assert "test.txt" in files

def test_create_temp_file(temp_dir):
    """Test temporary file creation."""
    # Create temporary file
    temp_file = create_temp_file(temp_dir, suffix=".txt")
    assert os.path.exists(temp_file)
    assert temp_file.endswith(".txt")
    
    # Create temporary file with content
    content = "Test content"
    temp_file = create_temp_file(temp_dir, content=content, suffix=".txt")
    assert os.path.exists(temp_file)
    with open(temp_file, "r") as f:
        assert f.read() == content

def test_get_file_hash(sample_files):
    """Test file hash calculation."""
    # Test text file hash
    text_hash = get_file_hash(sample_files["text"])
    assert len(text_hash) == 64  # SHA-256 hash length
    
    # Test binary file hash
    binary_hash = get_file_hash(sample_files["binary"])
    assert len(binary_hash) == 64
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        get_file_hash("nonexistent.txt") 