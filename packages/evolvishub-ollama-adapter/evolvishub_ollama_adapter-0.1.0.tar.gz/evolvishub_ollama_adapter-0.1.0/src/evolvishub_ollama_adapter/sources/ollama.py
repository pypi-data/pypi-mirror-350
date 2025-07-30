"""
Ollama-specific data sources for integration.

This module provides specialized data sources for handling Ollama model outputs,
embeddings, and chat history.
"""

from typing import Any, Dict, List, Optional, Union, AsyncIterator
from pathlib import Path
import json
import aiofiles
from pydantic import BaseModel, Field

from .base import ModelDataSource
from ..config import Config
from ..exceptions import DataSourceError

class OllamaResponse(BaseModel):
    """Model for Ollama API responses."""
    model: str
    created_at: str
    response: str
    done: bool = True
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_duration: Optional[int] = None
    eval_count: Optional[int] = None

class OllamaEmbedding(BaseModel):
    """Model for Ollama embeddings."""
    embedding: List[float]
    text: str

class OllamaChatMessage(BaseModel):
    """Model for Ollama chat messages."""
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str
    images: Optional[List[str]] = None  # Base64 encoded images

class OllamaChatHistory(BaseModel):
    """Model for Ollama chat history."""
    messages: List[OllamaChatMessage]
    model: str
    system_prompt: Optional[str] = None

class OllamaResponseSource(ModelDataSource):
    """Data source for Ollama model responses."""
    
    def __init__(
        self,
        source: Union[str, Path, Dict[str, Any], List[Dict[str, Any]]],
        config: Optional[Config] = None
    ):
        """Initialize the Ollama response source.
        
        Args:
            source: Response source (file path or response data)
            config: Configuration instance
        """
        super().__init__(OllamaResponse, config)
        self.source = source
        self._data: Optional[List[OllamaResponse]] = None
    
    async def _load_responses(self) -> List[OllamaResponse]:
        """Load responses from source."""
        if self._data is not None:
            return self._data
            
        try:
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="r", encoding="utf-8") as f:
                    content = await f.read()
                    data = json.loads(content)
            else:
                data = self.source
            
            if isinstance(data, dict):
                self._data = [self.model_class(**data)]
            else:
                self._data = [self.model_class(**item) for item in data]
            return self._data
        except Exception as e:
            raise DataSourceError(f"Failed to load responses: {str(e)}")
    
    async def get_data(self) -> List[str]:
        """Get response data from source.
        
        Returns:
            List of JSON-serialized responses
        """
        try:
            responses = await self._load_responses()
            return [response.model_dump_json() for response in responses]
        except Exception as e:
            raise DataSourceError(f"Failed to get response data: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save response data to source.
        
        Args:
            data: List of JSON-serialized responses
            
        Returns:
            True if save was successful
        """
        try:
            responses = []
            for item in data:
                response_data = json.loads(item)
                responses.append(self.model_class(**response_data))
            
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    if len(responses) == 1:
                        await f.write(responses[0].model_dump_json())
                    else:
                        await f.write(json.dumps([r.model_dump() for r in responses]))
            else:
                if isinstance(self.source, dict):
                    self.source.clear()
                    self.source.update(responses[0].model_dump())
                else:
                    self.source.clear()
                    self.source.extend([r.model_dump() for r in responses])
            
            self._data = responses
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save response data: {str(e)}")

class OllamaEmbeddingSource(ModelDataSource):
    """Data source for Ollama embeddings."""
    
    def __init__(
        self,
        source: Union[str, Path, Dict[str, Any], List[Dict[str, Any]]],
        config: Optional[Config] = None
    ):
        """Initialize the Ollama embedding source.
        
        Args:
            source: Embedding source (file path or embedding data)
            config: Configuration instance
        """
        super().__init__(OllamaEmbedding, config)
        self.source = source
        self._data: Optional[List[OllamaEmbedding]] = None
    
    async def _load_embeddings(self) -> List[OllamaEmbedding]:
        """Load embeddings from source."""
        if self._data is not None:
            return self._data
            
        try:
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="r", encoding="utf-8") as f:
                    content = await f.read()
                    data = json.loads(content)
            else:
                data = self.source
            
            if isinstance(data, dict):
                self._data = [self.model_class(**data)]
            else:
                self._data = [self.model_class(**item) for item in data]
            return self._data
        except Exception as e:
            raise DataSourceError(f"Failed to load embeddings: {str(e)}")
    
    async def get_data(self) -> List[str]:
        """Get embedding data from source.
        
        Returns:
            List of JSON-serialized embeddings
        """
        try:
            embeddings = await self._load_embeddings()
            return [embedding.model_dump_json() for embedding in embeddings]
        except Exception as e:
            raise DataSourceError(f"Failed to get embedding data: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save embedding data to source.
        
        Args:
            data: List of JSON-serialized embeddings
            
        Returns:
            True if save was successful
        """
        try:
            embeddings = []
            for item in data:
                embedding_data = json.loads(item)
                embeddings.append(self.model_class(**embedding_data))
            
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    if len(embeddings) == 1:
                        await f.write(embeddings[0].model_dump_json())
                    else:
                        await f.write(json.dumps([e.model_dump() for e in embeddings]))
            else:
                if isinstance(self.source, dict):
                    self.source.clear()
                    self.source.update(embeddings[0].model_dump())
                else:
                    self.source.clear()
                    self.source.extend([e.model_dump() for e in embeddings])
            
            self._data = embeddings
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save embedding data: {str(e)}")

class OllamaChatSource(ModelDataSource):
    """Data source for Ollama chat history."""
    
    def __init__(
        self,
        source: Union[str, Path, Dict[str, Any]],
        config: Optional[Config] = None
    ):
        """Initialize the Ollama chat source.
        
        Args:
            source: Chat source (file path or chat data)
            config: Configuration instance
        """
        super().__init__(OllamaChatHistory, config)
        self.source = source
        self._data: Optional[OllamaChatHistory] = None
    
    async def _load_chat(self) -> OllamaChatHistory:
        """Load chat history from source."""
        if self._data is not None:
            return self._data
            
        try:
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="r", encoding="utf-8") as f:
                    content = await f.read()
                    data = json.loads(content)
            else:
                data = self.source
            
            self._data = self.model_class(**data)
            return self._data
        except Exception as e:
            raise DataSourceError(f"Failed to load chat history: {str(e)}")
    
    async def get_data(self) -> List[str]:
        """Get chat history from source.
        
        Returns:
            List containing JSON-serialized chat history
        """
        try:
            chat = await self._load_chat()
            return [chat.model_dump_json()]
        except Exception as e:
            raise DataSourceError(f"Failed to get chat history: {str(e)}")
    
    async def save_data(self, data: List[str]) -> bool:
        """Save chat history to source.
        
        Args:
            data: List containing JSON-serialized chat history
            
        Returns:
            True if save was successful
        """
        try:
            if not data:
                return False
            
            chat_data = json.loads(data[0])
            chat = self.model_class(**chat_data)
            
            if isinstance(self.source, (str, Path)):
                async with aiofiles.open(self.source, mode="w", encoding="utf-8") as f:
                    await f.write(chat.model_dump_json())
            else:
                self.source.clear()
                self.source.update(chat.model_dump())
            
            self._data = chat
            return True
        except Exception as e:
            raise DataSourceError(f"Failed to save chat history: {str(e)}")
    
    async def add_message(self, role: str, content: str, images: Optional[List[str]] = None) -> bool:
        """Add a message to the chat history.
        
        Args:
            role: Message role (system, user, or assistant)
            content: Message content
            images: Optional list of base64-encoded images
            
        Returns:
            True if message was added successfully
        """
        try:
            chat = await self._load_chat()
            message = OllamaChatMessage(role=role, content=content, images=images)
            chat.messages.append(message)
            return await self.save_data([chat.model_dump_json()])
        except Exception as e:
            raise DataSourceError(f"Failed to add message: {str(e)}")
    
    async def clear_history(self) -> bool:
        """Clear the chat history.
        
        Returns:
            True if history was cleared successfully
        """
        try:
            chat = await self._load_chat()
            chat.messages.clear()
            return await self.save_data([chat.model_dump_json()])
        except Exception as e:
            raise DataSourceError(f"Failed to clear history: {str(e)}") 