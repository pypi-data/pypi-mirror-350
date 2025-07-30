"""
Binary data sources for Ollama integration.

This module provides implementations for PDF and image data sources.
"""

import base64
from typing import Any, Dict, List, Optional, Union, BinaryIO
from pathlib import Path
import aiofiles
import PyPDF2
from PIL import Image
import io

from .base import BinaryDataSource
from ..config import Config
from ..exceptions import DataSourceError

class PDFDataSource(BinaryDataSource):
    """PDF data source implementation."""
    
    def __init__(
        self,
        source: Union[str, Path, BinaryIO],
        extract_images: bool = True,
        config: Optional[Config] = None
    ):
        """Initialize the PDF data source.
        
        Args:
            source: PDF source (file path or binary stream)
            extract_images: Whether to extract images
            config: Configuration instance
        """
        super().__init__(source, config)
        self.extract_images = extract_images
        self._pdf: Optional[PyPDF2.PdfReader] = None
    
    async def _load_pdf(self) -> PyPDF2.PdfReader:
        """Load PDF from source."""
        if self._pdf is not None:
            return self._pdf
            
        content = await self._load_content()
        self._pdf = PyPDF2.PdfReader(io.BytesIO(content))
        return self._pdf
    
    def _extract_images(self, pdf: PyPDF2.PdfReader) -> List[str]:
        """Extract images from PDF."""
        images = []
        for page in pdf.pages:
            if "/XObject" in page["/Resources"]:
                x_objects = page["/Resources"]["/XObject"]
                for obj in x_objects:
                    if x_objects[obj]["/Subtype"] == "/Image":
                        try:
                            image = x_objects[obj]
                            data = image.get_data()
                            if image["/ColorSpace"] == "/DeviceRGB":
                                mode = "RGB"
                            else:
                                mode = "P"
                            
                            img = Image.frombytes(mode, (image["/Width"], image["/Height"]), data)
                            buffer = io.BytesIO()
                            img.save(buffer, format="PNG")
                            images.append(base64.b64encode(buffer.getvalue()).decode())
                        except Exception:
                            continue
        return images
    
    async def get_data(self) -> List[str]:
        """Get PDF content from source.
        
        Returns:
            List of PDF pages and optionally images
        """
        try:
            pdf = await self._load_pdf()
            pages = []
            
            # Extract text from pages
            for page in pdf.pages:
                text = page.extract_text()
                if text.strip():
                    pages.append(text)
            
            # Extract images if requested
            if self.extract_images:
                images = self._extract_images(pdf)
                pages.extend(images)
            
            return pages
        except Exception as e:
            raise DataSourceError(f"Failed to read PDF: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save text content to PDF.
        
        Args:
            data: List of text pages
            
        Returns:
            True if save was successful
            
        Raises:
            DataSourceError: PDF writing is not supported
        """
        raise DataSourceError("PDF writing is not supported")

class ImageDataSource(BinaryDataSource):
    """Image data source implementation."""
    
    def __init__(
        self,
        source: Union[str, Path, BinaryIO],
        format: str = "PNG",
        max_size: Optional[tuple[int, int]] = None,
        config: Optional[Config] = None
    ):
        """Initialize the image data source.
        
        Args:
            source: Image source (file path or binary stream)
            format: Output image format
            max_size: Maximum image size (width, height)
            config: Configuration instance
        """
        super().__init__(source, config)
        self.format = format.upper()
        self.max_size = max_size
        self._image: Optional[Image.Image] = None
    
    async def _load_image(self) -> Image.Image:
        """Load image from source."""
        if self._image is not None:
            return self._image
            
        content = await self._load_content()
        self._image = Image.open(io.BytesIO(content))
        
        # Resize if needed
        if self.max_size:
            self._image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
        
        return self._image
    
    async def get_data(self) -> List[str]:
        """Get image data from source.
        
        Returns:
            List containing base64-encoded image
        """
        try:
            image = await self._load_image()
            buffer = io.BytesIO()
            image.save(buffer, format=self.format)
            return [base64.b64encode(buffer.getvalue()).decode()]
        except Exception as e:
            raise DataSourceError(f"Failed to read image: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save image data to source.
        
        Args:
            data: List containing base64-encoded image
            
        Returns:
            True if save was successful
        """
        try:
            if not data:
                return False
            
            # Decode base64 image
            image_data = base64.b64decode(data[0])
            image = Image.open(io.BytesIO(image_data))
            
            # Save image
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="wb") as f:
                    buffer = io.BytesIO()
                    image.save(buffer, format=self.format)
                    await f.write(buffer.getvalue())
            else:
                buffer = io.BytesIO()
                image.save(buffer, format=self.format)
                self.source.write(buffer.getvalue())
            
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save image: {str(e)}") 