"""File utility functions."""

import os
import mimetypes
from pathlib import Path
from typing import List, Optional, Union
import shutil
import tempfile

from .constants import (
    SUPPORTED_TEXT_FORMATS,
    SUPPORTED_IMAGE_FORMATS,
    SUPPORTED_DOCUMENT_FORMATS,
    SUPPORTED_SPREADSHEET_FORMATS,
    SUPPORTED_PRESENTATION_FORMATS,
    SUPPORTED_ARCHIVE_FORMATS
)
from .exceptions import ValidationError

def is_supported_format(file_path: Union[str, Path], formats: Optional[List[str]] = None) -> bool:
    """Check if a file has a supported format.
    
    Args:
        file_path: Path to the file
        formats: Optional list of supported formats. If None, checks against all supported formats.
        
    Returns:
        True if the file format is supported, False otherwise
    """
    if formats is None:
        formats = (
            SUPPORTED_TEXT_FORMATS +
            SUPPORTED_IMAGE_FORMATS +
            SUPPORTED_DOCUMENT_FORMATS +
            SUPPORTED_SPREADSHEET_FORMATS +
            SUPPORTED_PRESENTATION_FORMATS +
            SUPPORTED_ARCHIVE_FORMATS
        )
    
    file_path = Path(file_path)
    return file_path.suffix.lower() in formats

def is_text_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is a text file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a text file, False otherwise
    """
    return is_supported_format(file_path, SUPPORTED_TEXT_FORMATS)

def is_image_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is an image file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is an image file, False otherwise
    """
    return is_supported_format(file_path, SUPPORTED_IMAGE_FORMATS)

def is_document_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is a document file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a document file, False otherwise
    """
    return is_supported_format(file_path, SUPPORTED_DOCUMENT_FORMATS)

def is_spreadsheet_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is a spreadsheet file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a spreadsheet file, False otherwise
    """
    return is_supported_format(file_path, SUPPORTED_SPREADSHEET_FORMATS)

def is_presentation_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is a presentation file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a presentation file, False otherwise
    """
    return is_supported_format(file_path, SUPPORTED_PRESENTATION_FORMATS)

def is_archive_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is an archive file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is an archive file, False otherwise
    """
    return is_supported_format(file_path, SUPPORTED_ARCHIVE_FORMATS)

def is_binary_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is a supported binary file (document, spreadsheet, or presentation)."""
    return (
        is_document_file(file_path)
        or is_spreadsheet_file(file_path)
        or is_presentation_file(file_path)
    )

def validate_file_path(file_path: Union[str, Path]) -> Path:
    """Validate a file path.
    
    Args:
        file_path: Path to validate
        
    Returns:
        Validated Path object
        
    Raises:
        ValidationError: If the path is invalid
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise ValidationError(f"File does not exist: {path}")
        if not path.is_file():
            raise ValidationError(f"Path is not a file: {path}")
        return path
    except Exception as e:
        raise ValidationError(f"Invalid file path: {str(e)}")

def ensure_directory(directory: Union[str, Path]) -> Path:
    """Ensure a directory exists.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for the directory
        
    Raises:
        ValidationError: If the directory cannot be created
    """
    try:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        raise ValidationError(f"Failed to create directory: {str(e)}")

def get_file_extension(file_path: Union[str, Path]) -> str:
    """Get a file's extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension (including the dot)
    """
    return Path(file_path).suffix.lower()

def get_mime_type(file_path: Union[str, Path]) -> str:
    """Get a file's MIME type.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MIME type string
    """
    return mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

def get_file_mime_type(file_path: Union[str, Path]) -> str:
    """Get the MIME type of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MIME type string
    """
    return get_mime_type(file_path)

def read_file_content(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Read the content of a text file and return as a string.
    
    Args:
        file_path: Path to the file
        encoding: File encoding (default: utf-8)
        
    Returns:
        File content as a string
        
    Raises:
        ValidationError: If the file cannot be read
    """
    path = validate_file_path(file_path)
    if not is_text_file(path):
        raise ValidationError(f"File is not a supported text file: {file_path}")
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise ValidationError(f"Failed to read file: {e}")

def read_binary_file(file_path: Union[str, Path]) -> bytes:
    """Read the content of a binary file and return as bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File content as bytes
        
    Raises:
        ValidationError: If the file cannot be read
    """
    path = validate_file_path(file_path)
    if not (is_binary_file(path) or is_image_file(path) or is_archive_file(path)):
        raise ValidationError(f"File is not a supported binary file: {file_path}")
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        raise ValidationError(f"Failed to read binary file: {e}")

def get_file_size(file_path: Union[str, Path]) -> int:
    """Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Size of the file in bytes
        
    Raises:
        ValidationError: If the file does not exist or cannot be accessed
    """
    path = validate_file_path(file_path)
    try:
        return path.stat().st_size
    except Exception as e:
        raise ValidationError(f"Failed to get file size: {e}")

def write_file_content(file_path: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
    """Write content to a text file.
    
    Args:
        file_path: Path to the file
        content: String content to write
        encoding: File encoding (default: utf-8)
        
    Raises:
        ValidationError: If the file cannot be written
    """
    try:
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise ValidationError(f"Failed to write file: {e}")

def copy_file(src: Union[str, Path], dst: Union[str, Path], overwrite: bool = False) -> None:
    """Copy a file from src to dst.
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite the destination file if it exists
        
    Raises:
        ValidationError: If the file cannot be copied
    """
    src_path = validate_file_path(src)
    dst_path = Path(dst)
    if dst_path.exists() and not overwrite:
        raise ValidationError(f"Destination file already exists: {dst}")
    try:
        shutil.copy2(src_path, dst_path)
    except Exception as e:
        raise ValidationError(f"Failed to copy file: {e}")

def move_file(src: Union[str, Path], dst: Union[str, Path], overwrite: bool = False) -> None:
    """Move a file from src to dst.
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite the destination file if it exists
        
    Raises:
        ValidationError: If the file cannot be moved
    """
    src_path = validate_file_path(src)
    dst_path = Path(dst)
    if dst_path.exists() and not overwrite:
        raise ValidationError(f"Destination file already exists: {dst}")
    try:
        shutil.move(str(src_path), str(dst_path))
    except Exception as e:
        raise ValidationError(f"Failed to move file: {e}")

def delete_file(file_path: Union[str, Path]) -> None:
    """Delete a file at the given path.
    
    Args:
        file_path: Path to the file
        
    Raises:
        ValidationError: If the file cannot be deleted
    """
    path = validate_file_path(file_path)
    try:
        path.unlink()
    except Exception as e:
        raise ValidationError(f"Failed to delete file: {e}")

def list_directory(directory: Union[str, Path]) -> list:
    """List files and directories in a given directory path.
    
    Args:
        directory: Directory path
        
    Returns:
        List of file and directory names
        
    Raises:
        ValidationError: If the directory cannot be listed
    """
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        raise ValidationError(f"Directory does not exist: {directory}")
    try:
        return [item.name for item in path.iterdir()]
    except Exception as e:
        raise ValidationError(f"Failed to list directory: {e}")

def create_temp_file(suffix="", prefix="tmp", dir=None):
    """Create a temporary file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return path

def get_file_hash(file_path):
    """Stub: Return a dummy file hash."""
    return "dummyhash" 