"""
PostgreSQL database adapter for Ollama integration.

This module provides the PostgreSQL implementation of the database adapter.
"""

import json
from typing import Any, Dict, List, Optional
import asyncpg
from datetime import datetime

from .base import VectorDatabaseAdapter, QueryBuilder
from ..config import Config
from ..exceptions import DataSourceError

class PostgreSQLQueryBuilder(QueryBuilder):
    """PostgreSQL query builder implementation."""
    
    def build_filter(self, field: str, operator: str, value: Any) -> Dict[str, Any]:
        """Build a filter condition for PostgreSQL."""
        operators = {
            "eq": "=",
            "ne": "!=",
            "gt": ">",
            "gte": ">=",
            "lt": "<",
            "lte": "<=",
            "like": "ILIKE",
            "in": "IN",
            "contains": "@>",
            "contained": "<@",
            "overlaps": "&&"
        }
        
        if operator not in operators:
            raise ValueError(f"Unsupported operator: {operator}")
        
        return {
            "field": field,
            "operator": operators[operator],
            "value": value
        }
    
    def build_sort(self, field: str, direction: str = "asc") -> Dict[str, Any]:
        """Build a sort condition for PostgreSQL."""
        if direction not in ["asc", "desc"]:
            raise ValueError(f"Invalid sort direction: {direction}")
        
        return {
            "field": field,
            "direction": direction.upper()
        }
    
    def build_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        """Build pagination parameters for PostgreSQL."""
        if page < 1 or page_size < 1:
            raise ValueError("Page and page size must be positive")
        
        return {
            "offset": (page - 1) * page_size,
            "limit": page_size
        }

class PostgreSQLAdapter(VectorDatabaseAdapter):
    """PostgreSQL database adapter."""
    
    def __init__(self, dsn: str, config: Optional[Config] = None):
        """Initialize PostgreSQL adapter.
        
        Args:
            dsn: PostgreSQL connection string
            config: Configuration instance
        """
        super().__init__(config)
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
        self._query_builder = PostgreSQLQueryBuilder()
    
    async def connect(self) -> None:
        """Connect to PostgreSQL database."""
        self.pool = await asyncpg.create_pool(self.dsn)
        await self.create_tables()
    
    async def disconnect(self) -> None:
        """Disconnect from PostgreSQL database."""
        if self.pool:
            await self.pool.close()
    
    async def create_tables(self) -> None:
        """Create necessary PostgreSQL tables."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        async with self.pool.acquire() as conn:
            # Enable vector extension
            await conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
            
            # Create collections table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS collections (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create records table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    collection_id TEXT NOT NULL REFERENCES collections(id),
                    data JSONB NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create vectors table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS vectors (
                    id TEXT PRIMARY KEY,
                    collection_id TEXT NOT NULL REFERENCES collections(id),
                    text TEXT NOT NULL,
                    vector vector NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_records_collection_id ON records(collection_id);
                CREATE INDEX IF NOT EXISTS idx_vectors_collection_id ON vectors(collection_id);
                CREATE INDEX IF NOT EXISTS idx_records_created_at ON records(created_at);
                CREATE INDEX IF NOT EXISTS idx_vectors_created_at ON vectors(created_at);
            """)
    
    async def _ensure_collection(self, collection: str) -> str:
        """Ensure a collection exists and return its ID."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM collections WHERE name = $1",
                collection
            )
            if row:
                return row['id']
            
            collection_id = f"col_{datetime.now().timestamp()}"
            await conn.execute(
                "INSERT INTO collections (id, name) VALUES ($1, $2)",
                collection_id, collection
            )
            return collection_id
    
    async def save_record(self, collection: str, data: Dict[str, Any]) -> str:
        """Save a record to PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        record_id = f"rec_{datetime.now().timestamp()}"
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO records (id, collection_id, data) VALUES ($1, $2, $3)",
                record_id, collection_id, json.dumps(data)
            )
        
        return record_id
    
    async def get_record(self, collection: str, record_id: str) -> Dict[str, Any]:
        """Get a record from PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT r.id, r.data, r.metadata, r.created_at
                FROM records r
                JOIN collections c ON r.collection_id = c.id
                WHERE c.name = $1 AND r.id = $2
                """,
                collection, record_id
            )
            
            if not row:
                raise DataSourceError(f"Record not found: {record_id}")
            
            return {
                "id": row['id'],
                "data": row['data'],
                "metadata": row['metadata'],
                "created_at": row['created_at']
            }
    
    async def search_records(
        self,
        collection: str,
        query: Dict[str, Any],
        sort: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for records in PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        # Build query conditions
        conditions = []
        params = []
        param_index = 1
        
        for field, value in query.items():
            if isinstance(value, dict):
                for op, val in value.items():
                    filter_cond = self.query_builder.build_filter(field, op, val)
                    conditions.append(f"data->>'{filter_cond['field']}' {filter_cond['operator']} ${param_index}")
                    params.append(filter_cond['value'])
                    param_index += 1
            else:
                conditions.append(f"data->>'{field}' = ${param_index}")
                params.append(value)
                param_index += 1
        
        # Build sort conditions
        sort_clause = ""
        if sort:
            sort_conditions = []
            for field, direction in sort.items():
                sort_cond = self.query_builder.build_sort(field, direction)
                sort_conditions.append(f"data->>'{sort_cond['field']}' {sort_cond['direction']}")
            sort_clause = f"ORDER BY {', '.join(sort_conditions)}"
        
        # Build pagination
        pagination = self.query_builder.build_pagination(page, page_size)
        
        # Execute query
        query = f"""
            SELECT r.id, r.data, r.metadata, r.created_at
            FROM records r
            JOIN collections c ON r.collection_id = c.id
            WHERE c.name = ${param_index} {' AND ' + ' AND '.join(conditions) if conditions else ''}
            {sort_clause}
            LIMIT ${param_index + 1} OFFSET ${param_index + 2}
        """
        
        params.extend([collection, pagination['limit'], pagination['offset']])
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            
            return [{
                "id": row['id'],
                "data": row['data'],
                "metadata": row['metadata'],
                "created_at": row['created_at']
            } for row in rows]
    
    async def update_record(
        self,
        collection: str,
        record_id: str,
        data: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Update a record in PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.pool.acquire() as conn:
            if upsert:
                await conn.execute(
                    """
                    INSERT INTO records (id, collection_id, data)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data
                    """,
                    record_id, collection_id, json.dumps(data)
                )
            else:
                await conn.execute(
                    """
                    UPDATE records
                    SET data = $1
                    WHERE collection_id = $2 AND id = $3
                    """,
                    json.dumps(data), collection_id, record_id
                )
        
        return True
    
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record from PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM records WHERE collection_id = $1 AND id = $2",
                collection_id, record_id
            )
        
        return True
    
    async def bulk_save_records(self, collection: str, records: List[Dict[str, Any]]) -> List[str]:
        """Save multiple records to PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        record_ids = []
        
        async with self.pool.acquire() as conn:
            for record in records:
                record_id = f"rec_{datetime.now().timestamp()}"
                record_ids.append(record_id)
                
                await conn.execute(
                    "INSERT INTO records (id, collection_id, data) VALUES ($1, $2, $3)",
                    record_id, collection_id, json.dumps(record)
                )
        
        return record_ids
    
    async def bulk_update_records(
        self,
        collection: str,
        updates: List[Dict[str, Any]]
    ) -> int:
        """Update multiple records in PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        updated = 0
        
        async with self.pool.acquire() as conn:
            for update in updates:
                record_id = update.get('id')
                if not record_id:
                    continue
                
                await conn.execute(
                    """
                    UPDATE records
                    SET data = $1
                    WHERE collection_id = $2 AND id = $3
                    """,
                    json.dumps(update.get('data', {})), collection_id, record_id
                )
                updated += 1
        
        return updated
    
    async def bulk_delete_records(self, collection: str, record_ids: List[str]) -> int:
        """Delete multiple records from PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM records WHERE collection_id = $1 AND id = ANY($2)",
                collection_id, record_ids
            )
        
        return len(record_ids)
    
    async def save_vector(
        self,
        collection: str,
        text: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a vector to PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        vector_id = f"vec_{datetime.now().timestamp()}"
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO vectors (id, collection_id, text, vector, metadata) VALUES ($1, $2, $3, $4, $5)",
                vector_id, collection_id, text, vector, json.dumps(metadata) if metadata else None
            )
        
        return vector_id
    
    async def search_vectors(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, text, vector, metadata, created_at,
                       1 - (vector <=> $1) as similarity
                FROM vectors
                WHERE collection_id = $2
                AND 1 - (vector <=> $1) >= $3
                ORDER BY vector <=> $1
                LIMIT $4
                """,
                query_vector, collection_id, min_similarity, limit
            )
            
            return [{
                "id": row['id'],
                "text": row['text'],
                "similarity": row['similarity'],
                "metadata": row['metadata'],
                "created_at": row['created_at']
            } for row in rows]
    
    async def bulk_save_vectors(
        self,
        collection: str,
        vectors: List[Dict[str, Any]]
    ) -> List[str]:
        """Save multiple vectors to PostgreSQL."""
        if not self.pool:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        vector_ids = []
        
        async with self.pool.acquire() as conn:
            for vector_data in vectors:
                vector_id = f"vec_{datetime.now().timestamp()}"
                vector_ids.append(vector_id)
                
                text = vector_data.get('text', '')
                vector = vector_data.get('vector', [])
                metadata = vector_data.get('metadata')
                
                await conn.execute(
                    "INSERT INTO vectors (id, collection_id, text, vector, metadata) VALUES ($1, $2, $3, $4, $5)",
                    vector_id, collection_id, text, vector, json.dumps(metadata) if metadata else None
                )
        
        return vector_ids 