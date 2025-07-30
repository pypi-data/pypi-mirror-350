"""Utility functions for image processing."""

import base64
from io import BytesIO
from typing import Union, Tuple, Optional, List, Dict, Any
from pathlib import Path
import io

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np

from .constants import MAX_IMAGE_SIZE, SUPPORTED_IMAGE_FORMATS
from .exceptions import ValidationError
from .file_utils import validate_file_path, is_image_file, ensure_directory

def validate_image_size(image_path: Union[str, Path]) -> None:
    """Validate that an image file is not too large.
    
    Args:
        image_path: Path to the image file
        
    Raises:
        ValidationError: If image file is too large
    """
    size = Path(image_path).stat().st_size
    if size > MAX_IMAGE_SIZE:
        raise ValidationError(f"Image file is too large: {size} bytes (max: {MAX_IMAGE_SIZE} bytes)")

def load_image(image_path: Union[str, Path]) -> Image.Image:
    """Load an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL Image object
        
    Raises:
        ValidationError: If image file is invalid or cannot be loaded
    """
    path = validate_file_path(image_path)
    if not is_image_file(path):
        raise ValidationError(f"File is not a supported image file: {image_path}")
    validate_image_size(path)
    try:
        return Image.open(path)
    except Exception as e:
        raise ValidationError(f"Failed to load image: {e}")

def save_image(image: Image.Image, file_path: Union[str, Path], format: Optional[str] = None) -> None:
    """Save an image to a file.
    
    Args:
        image: PIL Image object
        file_path: Path to save the image
        format: Image format (PNG, JPEG, etc.)
        
    Raises:
        ValidationError: If image cannot be saved
    """
    try:
        path = Path(file_path)
        ensure_directory(path.parent)
        
        if format is None:
            format = path.suffix[1:].upper() or "PNG"
        
        image.save(path, format=format)
    except Exception as e:
        raise ValidationError(f"Failed to save image: {e}")

def resize_image(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    """Resize an image while maintaining aspect ratio.
    
    Args:
        image: PIL Image object
        max_size: Maximum width and height
        
    Returns:
        Resized PIL Image object
    """
    width, height = image.size
    max_width, max_height = max_size
    
    # Calculate new dimensions
    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    return image

def convert_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert an image to base64 string.
    
    Args:
        image: PIL Image object
        format: Image format (PNG, JPEG, etc.)
        
    Returns:
        Base64 encoded image string
    """
    buffer = BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def image_to_base64(image_path: Union[str, Path], max_size: Optional[Tuple[int, int]] = None) -> str:
    """Convert an image file to base64 string.
    
    Args:
        image_path: Path to the image file
        max_size: Optional maximum width and height
        
    Returns:
        Base64 encoded image string
        
    Raises:
        ValidationError: If image file is invalid or cannot be processed
    """
    image = load_image(image_path)
    if max_size:
        image = resize_image(image, max_size)
    return convert_to_base64(image)

def base64_to_image(base64_string: str) -> Image.Image:
    """Convert a base64 string to PIL Image.
    
    Args:
        base64_string: Base64 encoded image string
        
    Returns:
        PIL Image object
        
    Raises:
        ValidationError: If base64 string is invalid or cannot be decoded
    """
    try:
        image_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(image_data))
    except Exception as e:
        raise ValidationError(f"Failed to decode base64 image: {e}")

def image_to_numpy(image: Image.Image) -> np.ndarray:
    """Convert a PIL Image to numpy array.
    
    Args:
        image: PIL Image object
        
    Returns:
        Numpy array representation of the image
    """
    return np.array(image)

def numpy_to_image(array: np.ndarray) -> Image.Image:
    """Convert a numpy array to PIL Image.
    
    Args:
        array: Numpy array representation of the image
        
    Returns:
        PIL Image object
        
    Raises:
        ValidationError: If array is invalid or cannot be converted
    """
    try:
        return Image.fromarray(array)
    except Exception as e:
        raise ValidationError(f"Failed to convert numpy array to image: {e}")

def convert_image_format(
    image: Union[str, Path, Image.Image, bytes],
    format: str = "PNG",
    quality: int = 95
) -> bytes:
    """Convert an image to a different format.
    
    Args:
        image: Image to convert (file path, PIL Image, or bytes)
        format: Target format (e.g., 'PNG', 'JPEG')
        quality: Quality for lossy formats (1-100)
        
    Returns:
        Image data in the new format as bytes
        
    Raises:
        ValidationError: If the image cannot be converted
    """
    try:
        # Convert input to PIL Image if needed
        if isinstance(image, (str, Path)):
            image = Image.open(image)
        elif isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))
        elif not isinstance(image, Image.Image):
            raise ValidationError("Invalid image input type")
        
        # Convert to RGB if needed
        if format.upper() == "JPEG" and image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format=format, quality=quality)
        return buffer.getvalue()
        
    except Exception as e:
        raise ValidationError(f"Failed to convert image format: {str(e)}")

def get_image_info(image_path: Union[str, Path]) -> dict:
    """Get basic information about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with image info: format, size, mode, etc.
        
    Raises:
        ValidationError: If the image cannot be opened or is invalid
    """
    try:
        with Image.open(image_path) as img:
            return {
                "format": img.format,
                "size": img.size,
                "mode": img.mode,
                "info": img.info,
            }
    except Exception as e:
        raise ValidationError(f"Failed to get image info: {e}")

def create_image_from_array(array: 'np.ndarray', mode: str = 'RGB') -> Image.Image:
    """Create a PIL Image from a numpy array.
    
    Args:
        array: Numpy array representing the image
        mode: Color mode (default: 'RGB')
        
    Returns:
        PIL Image object
        
    Raises:
        ValidationError: If the image cannot be created
    """
    try:
        return Image.fromarray(array, mode)
    except Exception as e:
        raise ValidationError(f"Failed to create image from array: {e}")

def apply_image_filter(image: Image.Image, filter_name: str) -> Image.Image:
    """Apply a named filter to a PIL Image.
    
    Args:
        image: PIL Image object
        filter_name: Name of the filter (e.g., 'BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', etc.)
        
    Returns:
        Filtered PIL Image object
        
    Raises:
        ValidationError: If the filter is not supported or cannot be applied
    """
    try:
        filter_map = {
            'BLUR': ImageFilter.BLUR,
            'CONTOUR': ImageFilter.CONTOUR,
            'DETAIL': ImageFilter.DETAIL,
            'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
            'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
            'EMBOSS': ImageFilter.EMBOSS,
            'FIND_EDGES': ImageFilter.FIND_EDGES,
            'SHARPEN': ImageFilter.SHARPEN,
            'SMOOTH': ImageFilter.SMOOTH,
            'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
        }
        if filter_name.upper() not in filter_map:
            raise ValidationError(f"Unsupported filter: {filter_name}")
        return image.filter(filter_map[filter_name.upper()])
    except Exception as e:
        raise ValidationError(f"Failed to apply image filter: {e}")

def encode_image(image: Image.Image, format: str = "PNG") -> str:
    """Encode a PIL Image as a base64 string.
    
    Args:
        image: PIL Image object
        format: Image format (default: 'PNG')
        
    Returns:
        Base64-encoded string of the image
        
    Raises:
        ValidationError: If the image cannot be encoded
    """
    try:
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return encoded
    except Exception as e:
        raise ValidationError(f"Failed to encode image: {e}")

def decode_image(encoded_str: str) -> Image.Image:
    """Decode a base64 string into a PIL Image.
    
    Args:
        encoded_str: Base64-encoded string of the image
        
    Returns:
        PIL Image object
        
    Raises:
        ValidationError: If the image cannot be decoded
    """
    try:
        image_data = base64.b64decode(encoded_str)
        buffer = io.BytesIO(image_data)
        return Image.open(buffer)
    except Exception as e:
        raise ValidationError(f"Failed to decode image: {e}")

def validate_image(image_path: Union[str, Path], max_size: int = None) -> bool:
    """Check if a file is a valid image and optionally check its size.
    
    Args:
        image_path: Path to the image file
        max_size: Maximum allowed file size in bytes (optional)
        
    Returns:
        True if the file is a valid image and meets size requirements
        
    Raises:
        ValidationError: If the file is not a valid image or exceeds max_size
    """
    path = Path(image_path)
    try:
        with Image.open(path) as img:
            img.verify()
        if max_size is not None and path.stat().st_size > max_size:
            raise ValidationError(f"Image file exceeds maximum size: {max_size} bytes")
        return True
    except Exception as e:
        raise ValidationError(f"Invalid image file: {e}")

def get_image_dominant_color(image: Image.Image) -> tuple:
    """Get the dominant color of a PIL Image as an RGB tuple.
    
    Args:
        image: PIL Image object
        
    Returns:
        Dominant color as an (R, G, B) tuple
    """
    image = image.convert('RGB')
    small_image = image.resize((50, 50))
    result = small_image.getcolors(50 * 50)
    dominant_color = max(result, key=lambda item: item[0])[1]
    return dominant_color

def get_image_average_color(image):
    """Stub: Return a dummy average color."""
    return (0, 0, 0)

def get_image_histogram(image: Image.Image) -> Dict[str, List[int]]:
    """Get image histogram.
    
    Args:
        image: PIL Image
        
    Returns:
        Dictionary with histogram data for each channel
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    # Convert to RGB if needed
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')
        
    # Get histogram for each channel
    if image.mode == 'RGB':
        r, g, b = image.split()
        return {
            'red': r.histogram(),
            'green': g.histogram(),
            'blue': b.histogram()
        }
    else:
        return {'gray': image.histogram()}

def get_image_edges(image: Image.Image) -> Image.Image:
    """Get image edges.
    
    Args:
        image: PIL Image
        
    Returns:
        Image with edges highlighted
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    # Convert to grayscale if needed
    if image.mode != 'L':
        image = image.convert('L')
        
    # Apply edge detection
    return image.filter(ImageFilter.FIND_EDGES)

def get_image_blur(image: Image.Image) -> Image.Image:
    """Apply blur to image.
    
    Args:
        image: PIL Image
        
    Returns:
        Blurred image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    return image.filter(ImageFilter.BLUR)

def get_image_sharpen(image: Image.Image) -> Image.Image:
    """Apply sharpening to image.
    
    Args:
        image: PIL Image
        
    Returns:
        Sharpened image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    return image.filter(ImageFilter.SHARPEN)

def get_image_grayscale(image: Image.Image) -> Image.Image:
    """Convert image to grayscale.
    
    Args:
        image: PIL Image
        
    Returns:
        Grayscale image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    return image.convert('L')

def get_image_sepia(image: Image.Image) -> Image.Image:
    """Apply sepia filter to image.
    
    Args:
        image: PIL Image
        
    Returns:
        Sepia-toned image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    # Create sepia matrix (12 values for RGB conversion)
    sepia_matrix = (
        0.393, 0.769, 0.189, 0,
        0.349, 0.686, 0.168, 0,
        0.272, 0.534, 0.131, 0
    )
    
    # Apply sepia filter
    return image.convert('RGB', matrix=sepia_matrix)

def get_image_negative(image: Image.Image) -> Image.Image:
    """Invert image colors.
    
    Args:
        image: PIL Image
        
    Returns:
        Inverted image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    return ImageOps.invert(image)

def get_image_rotate(image: Image.Image, angle: float) -> Image.Image:
    """Rotate image.
    
    Args:
        image: PIL Image
        angle: Rotation angle in degrees
        
    Returns:
        Rotated image
        
    Raises:
        ValueError: If image or angle is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
    if not isinstance(angle, (int, float)):
        raise ValueError("Angle must be a number")
        
    return image.rotate(angle, expand=True)

def get_image_flip(image: Image.Image) -> Image.Image:
    """Flip image horizontally.
    
    Args:
        image: PIL Image
        
    Returns:
        Flipped image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def get_image_crop(image: Image.Image, left: int, top: int, right: int, bottom: int) -> Image.Image:
    """Crop image.
    
    Args:
        image: PIL Image
        left: Left coordinate
        top: Top coordinate
        right: Right coordinate
        bottom: Bottom coordinate
        
    Returns:
        Cropped image
        
    Raises:
        ValueError: If image or coordinates are invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
    if not all(isinstance(x, int) for x in (left, top, right, bottom)):
        raise ValueError("Coordinates must be integers")
    if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
        raise ValueError("Invalid crop coordinates")
        
    return image.crop((left, top, right, bottom))

def get_image_paste(image, paste_image, position):
    """Paste an image onto another image at a specified position."""
    image.paste(paste_image, position)
    return image

def get_image_alpha_composite(image1, image2):
    """Alpha composite two images together."""
    from PIL import Image
    return Image.alpha_composite(image1.convert('RGBA'), image2.convert('RGBA'))

def get_image_watermark(image: Image.Image, watermark: Image.Image) -> Image.Image:
    """Add watermark to image.
    
    Args:
        image: PIL Image
        watermark: Watermark image
        
    Returns:
        Watermarked image
        
    Raises:
        ValueError: If image or watermark is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
    if not isinstance(watermark, Image.Image):
        raise ValueError("Watermark must be a PIL Image")
        
    # Convert to RGBA if needed
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
        
    # Create new image
    result = Image.new('RGBA', image.size, (0, 0, 0, 0))
    result.paste(image, (0, 0))
    
    # Calculate watermark position
    wm_width, wm_height = watermark.size
    img_width, img_height = image.size
    x = (img_width - wm_width) // 2
    y = (img_height - wm_height) // 2
    
    # Paste watermark
    result.paste(watermark, (x, y), watermark)
    return result

def get_image_border(image: Image.Image, width: int, color: str = 'black') -> Image.Image:
    """Add border to image.
    
    Args:
        image: PIL Image
        width: Border width in pixels
        color: Border color
        
    Returns:
        Image with border
        
    Raises:
        ValueError: If image, width, or color is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
    if not isinstance(width, int) or width < 0:
        raise ValueError("Width must be a non-negative integer")
    if not isinstance(color, str):
        raise ValueError("Color must be a string")
        
    return ImageOps.expand(image, border=width, fill=color)

def get_image_padding(image: Image.Image, padding: int) -> Image.Image:
    """Add padding to image.
    
    Args:
        image: PIL Image
        padding: Padding width in pixels
        
    Returns:
        Image with padding
        
    Raises:
        ValueError: If image or padding is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
    if not isinstance(padding, int) or padding < 0:
        raise ValueError("Padding must be a non-negative integer")
        
    return ImageOps.expand(image, border=padding, fill='white')

def get_image_mirror(image: Image.Image) -> Image.Image:
    """Create mirror image.
    
    Args:
        image: PIL Image
        
    Returns:
        Mirrored image
        
    Raises:
        ValueError: If image is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
        
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def get_image_transpose(image: Image.Image, method: str) -> Image.Image:
    """Transpose image.
    
    Args:
        image: PIL Image
        method: Transpose method ('FLIP_LEFT_RIGHT', 'FLIP_TOP_BOTTOM', 'ROTATE_90', 'ROTATE_180', 'ROTATE_270')
        
    Returns:
        Transposed image
        
    Raises:
        ValueError: If image or method is invalid
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image")
    if not isinstance(method, str):
        raise ValueError("Method must be a string")
        
    methods = {
        'FLIP_LEFT_RIGHT': Image.FLIP_LEFT_RIGHT,
        'FLIP_TOP_BOTTOM': Image.FLIP_TOP_BOTTOM,
        'ROTATE_90': Image.ROTATE_90,
        'ROTATE_180': Image.ROTATE_180,
        'ROTATE_270': Image.ROTATE_270
    }
    
    if method not in methods:
        raise ValueError(f"Invalid transpose method: {method}")
        
    return image.transpose(methods[method])

def get_image_thumbnail(image, size=(128, 128)):
    """Create a thumbnail of an image."""
    image.thumbnail(size)
    return image 