"""
Base database module for Ollama integration.

This module provides the base classes and common functionality for database adapters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union, Protocol
from datetime import datetime
from pydantic import BaseModel

from ..config import Config
from ..exceptions import DataSourceError

T = TypeVar('T', bound=BaseModel)
V = TypeVar('V', bound=Union[str, int, float, bool, List, Dict])

class QueryBuilder(Protocol):
    """Protocol for building database queries."""
    
    def build_filter(self, field: str, operator: str, value: Any) -> Dict[str, Any]:
        """Build a filter condition."""
        ...
    
    def build_sort(self, field: str, direction: str = "asc") -> Dict[str, Any]:
        """Build a sort condition."""
        ...
    
    def build_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        """Build pagination parameters."""
        ...

class BaseDatabaseAdapter(Generic[T], ABC):
    """Abstract base class for database adapters."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the database adapter.
        
        Args:
            config: Configuration instance. If None, creates a new one.
        """
        self.config = config or Config()
        self._query_builder: Optional[QueryBuilder] = None
    
    @property
    def query_builder(self) -> QueryBuilder:
        """Get the query builder instance."""
        if not self._query_builder:
            raise DataSourceError("Query builder not initialized")
        return self._query_builder
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to the database."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the database."""
        pass
    
    @abstractmethod
    async def create_tables(self) -> None:
        """Create necessary database tables."""
        pass
    
    @abstractmethod
    async def save_record(self, collection: str, data: Dict[str, Any]) -> str:
        """Save a record to the database.
        
        Args:
            collection: Collection/table name
            data: Record data
            
        Returns:
            Record ID
        """
        pass
    
    @abstractmethod
    async def get_record(self, collection: str, record_id: str) -> Dict[str, Any]:
        """Get a record from the database.
        
        Args:
            collection: Collection/table name
            record_id: Record ID
            
        Returns:
            Record data
        """
        pass
    
    @abstractmethod
    async def search_records(
        self,
        collection: str,
        query: Dict[str, Any],
        sort: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for records in the database.
        
        Args:
            collection: Collection/table name
            query: Search query
            sort: Sort parameters
            page: Page number
            page_size: Items per page
            
        Returns:
            List of matching records
        """
        pass
    
    @abstractmethod
    async def update_record(
        self,
        collection: str,
        record_id: str,
        data: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Update a record in the database.
        
        Args:
            collection: Collection/table name
            record_id: Record ID
            data: Updated data
            upsert: Create if not exists
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record from the database.
        
        Args:
            collection: Collection/table name
            record_id: Record ID
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def bulk_save_records(self, collection: str, records: List[Dict[str, Any]]) -> List[str]:
        """Save multiple records to the database.
        
        Args:
            collection: Collection/table name
            records: List of records
            
        Returns:
            List of record IDs
        """
        pass
    
    @abstractmethod
    async def bulk_update_records(
        self,
        collection: str,
        updates: List[Dict[str, Any]]
    ) -> int:
        """Update multiple records in the database.
        
        Args:
            collection: Collection/table name
            updates: List of updates
            
        Returns:
            Number of updated records
        """
        pass
    
    @abstractmethod
    async def bulk_delete_records(self, collection: str, record_ids: List[str]) -> int:
        """Delete multiple records from the database.
        
        Args:
            collection: Collection/table name
            record_ids: List of record IDs
            
        Returns:
            Number of deleted records
        """
        pass

class VectorDatabaseAdapter(BaseDatabaseAdapter[T]):
    """Abstract base class for vector database adapters."""
    
    @abstractmethod
    async def save_vector(
        self,
        collection: str,
        text: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a vector to the database.
        
        Args:
            collection: Collection/table name
            text: Associated text
            vector: Vector embedding
            metadata: Additional metadata
            
        Returns:
            Vector ID
        """
        pass
    
    @abstractmethod
    async def search_vectors(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors.
        
        Args:
            collection: Collection/table name
            query_vector: Query vector
            limit: Maximum number of results
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar vectors
        """
        pass
    
    @abstractmethod
    async def bulk_save_vectors(
        self,
        collection: str,
        vectors: List[Dict[str, Any]]
    ) -> List[str]:
        """Save multiple vectors to the database.
        
        Args:
            collection: Collection/table name
            vectors: List of vectors with text and embedding
            
        Returns:
            List of vector IDs
        """
        pass
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot_product / (norm_a * norm_b)

class DocumentDatabaseAdapter(BaseDatabaseAdapter[T]):
    """Abstract base class for document database adapters."""
    
    @abstractmethod
    async def save_document(
        self,
        collection: str,
        document: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a document to the database.
        
        Args:
            collection: Collection/table name
            document: Document data
            metadata: Additional metadata
            
        Returns:
            Document ID
        """
        pass
    
    @abstractmethod
    async def search_documents(
        self,
        collection: str,
        query: Dict[str, Any],
        sort: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for documents.
        
        Args:
            collection: Collection/table name
            query: Search query
            sort: Sort parameters
            page: Page number
            page_size: Items per page
            
        Returns:
            List of matching documents
        """
        pass
    
    @abstractmethod
    async def bulk_save_documents(
        self,
        collection: str,
        documents: List[Dict[str, Any]]
    ) -> List[str]:
        """Save multiple documents to the database.
        
        Args:
            collection: Collection/table name
            documents: List of documents
            
        Returns:
            List of document IDs
        """
        pass 