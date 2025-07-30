"""
SQLite database adapter for Ollama integration.

This module provides the SQLite implementation of the database adapter.
"""

import json
from typing import Any, Dict, List, Optional
import aiosqlite
from datetime import datetime

from .base import VectorDatabaseAdapter, QueryBuilder
from ..config import Config
from ..exceptions import DataSourceError

class SQLiteQueryBuilder(QueryBuilder):
    """SQLite query builder implementation."""
    
    def build_filter(self, field: str, operator: str, value: Any) -> Dict[str, Any]:
        """Build a filter condition for SQLite."""
        operators = {
            "eq": "=",
            "ne": "!=",
            "gt": ">",
            "gte": ">=",
            "lt": "<",
            "lte": "<=",
            "like": "LIKE",
            "in": "IN"
        }
        
        if operator not in operators:
            raise ValueError(f"Unsupported operator: {operator}")
        
        return {
            "field": field,
            "operator": operators[operator],
            "value": value
        }
    
    def build_sort(self, field: str, direction: str = "asc") -> Dict[str, Any]:
        """Build a sort condition for SQLite."""
        if direction not in ["asc", "desc"]:
            raise ValueError(f"Invalid sort direction: {direction}")
        
        return {
            "field": field,
            "direction": direction.upper()
        }
    
    def build_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        """Build pagination parameters for SQLite."""
        if page < 1 or page_size < 1:
            raise ValueError("Page and page size must be positive")
        
        return {
            "offset": (page - 1) * page_size,
            "limit": page_size
        }

class SQLiteAdapter(VectorDatabaseAdapter):
    """SQLite database adapter."""
    
    def __init__(self, db_path: str, config: Optional[Config] = None):
        """Initialize SQLite adapter.
        
        Args:
            db_path: Path to SQLite database file
            config: Configuration instance
        """
        super().__init__(config)
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None
        self._query_builder = SQLiteQueryBuilder()
    
    async def connect(self) -> None:
        """Connect to SQLite database."""
        self.conn = await aiosqlite.connect(self.db_path)
        await self.create_tables()
    
    async def disconnect(self) -> None:
        """Disconnect from SQLite database."""
        if self.conn:
            await self.conn.close()
    
    async def create_tables(self) -> None:
        """Create necessary SQLite tables."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        # Create collections table
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create records table
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY,
                collection_id TEXT NOT NULL,
                data TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (collection_id) REFERENCES collections (id)
            )
        """)
        
        # Create vectors table
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id TEXT PRIMARY KEY,
                collection_id TEXT NOT NULL,
                text TEXT NOT NULL,
                vector BLOB NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (collection_id) REFERENCES collections (id)
            )
        """)
        
        await self.conn.commit()
    
    async def _ensure_collection(self, collection: str) -> str:
        """Ensure a collection exists and return its ID."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        async with self.conn.execute(
            "SELECT id FROM collections WHERE name = ?",
            (collection,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
        
        collection_id = f"col_{datetime.now().timestamp()}"
        await self.conn.execute(
            "INSERT INTO collections (id, name) VALUES (?, ?)",
            (collection_id, collection)
        )
        await self.conn.commit()
        return collection_id
    
    async def save_record(self, collection: str, data: Dict[str, Any]) -> str:
        """Save a record to SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        record_id = f"rec_{datetime.now().timestamp()}"
        data_json = json.dumps(data)
        
        await self.conn.execute(
            "INSERT INTO records (id, collection_id, data) VALUES (?, ?, ?)",
            (record_id, collection_id, data_json)
        )
        await self.conn.commit()
        
        return record_id
    
    async def get_record(self, collection: str, record_id: str) -> Dict[str, Any]:
        """Get a record from SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.conn.execute(
            """
            SELECT r.id, r.data, r.metadata, r.created_at
            FROM records r
            JOIN collections c ON r.collection_id = c.id
            WHERE c.name = ? AND r.id = ?
            """,
            (collection, record_id)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise DataSourceError(f"Record not found: {record_id}")
            
            return {
                "id": row[0],
                "data": json.loads(row[1]),
                "metadata": json.loads(row[2]) if row[2] else None,
                "created_at": row[3]
            }
    
    async def search_records(
        self,
        collection: str,
        query: Dict[str, Any],
        sort: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for records in SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        # Build query conditions
        conditions = []
        params = []
        
        for field, value in query.items():
            if isinstance(value, dict):
                for op, val in value.items():
                    filter_cond = self.query_builder.build_filter(field, op, val)
                    conditions.append(f"json_extract(data, '$.{filter_cond['field']}') {filter_cond['operator']} ?")
                    params.append(filter_cond['value'])
            else:
                conditions.append(f"json_extract(data, '$.{field}') = ?")
                params.append(value)
        
        # Build sort conditions
        sort_clause = ""
        if sort:
            sort_conditions = []
            for field, direction in sort.items():
                sort_cond = self.query_builder.build_sort(field, direction)
                sort_conditions.append(f"json_extract(data, '$.{sort_cond['field']}') {sort_cond['direction']}")
            sort_clause = f"ORDER BY {', '.join(sort_conditions)}"
        
        # Build pagination
        pagination = self.query_builder.build_pagination(page, page_size)
        
        # Execute query
        query = f"""
            SELECT r.id, r.data, r.metadata, r.created_at
            FROM records r
            JOIN collections c ON r.collection_id = c.id
            WHERE c.name = ? {' AND ' + ' AND '.join(conditions) if conditions else ''}
            {sort_clause}
            LIMIT ? OFFSET ?
        """
        
        params = [collection] + params + [pagination['limit'], pagination['offset']]
        
        async with self.conn.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            
            return [{
                "id": row[0],
                "data": json.loads(row[1]),
                "metadata": json.loads(row[2]) if row[2] else None,
                "created_at": row[3]
            } for row in rows]
    
    async def update_record(
        self,
        collection: str,
        record_id: str,
        data: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Update a record in SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        data_json = json.dumps(data)
        
        if upsert:
            await self.conn.execute(
                """
                INSERT INTO records (id, collection_id, data)
                VALUES (?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET data = excluded.data
                """,
                (record_id, collection_id, data_json)
            )
        else:
            await self.conn.execute(
                """
                UPDATE records
                SET data = ?
                WHERE collection_id = ? AND id = ?
                """,
                (data_json, collection_id, record_id)
            )
        
        await self.conn.commit()
        return True
    
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record from SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        await self.conn.execute(
            "DELETE FROM records WHERE collection_id = ? AND id = ?",
            (collection_id, record_id)
        )
        await self.conn.commit()
        
        return True
    
    async def bulk_save_records(self, collection: str, records: List[Dict[str, Any]]) -> List[str]:
        """Save multiple records to SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        record_ids = []
        
        for record in records:
            record_id = f"rec_{datetime.now().timestamp()}"
            record_ids.append(record_id)
            data_json = json.dumps(record)
            
            await self.conn.execute(
                "INSERT INTO records (id, collection_id, data) VALUES (?, ?, ?)",
                (record_id, collection_id, data_json)
            )
        
        await self.conn.commit()
        return record_ids
    
    async def bulk_update_records(
        self,
        collection: str,
        updates: List[Dict[str, Any]]
    ) -> int:
        """Update multiple records in SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        updated = 0
        
        for update in updates:
            record_id = update.get('id')
            if not record_id:
                continue
            
            data_json = json.dumps(update.get('data', {}))
            
            await self.conn.execute(
                """
                UPDATE records
                SET data = ?
                WHERE collection_id = ? AND id = ?
                """,
                (data_json, collection_id, record_id)
            )
            updated += 1
        
        await self.conn.commit()
        return updated
    
    async def bulk_delete_records(self, collection: str, record_ids: List[str]) -> int:
        """Delete multiple records from SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        placeholders = ','.join(['?' for _ in record_ids])
        await self.conn.execute(
            f"DELETE FROM records WHERE collection_id = ? AND id IN ({placeholders})",
            [collection_id] + record_ids
        )
        await self.conn.commit()
        
        return len(record_ids)
    
    async def save_vector(
        self,
        collection: str,
        text: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a vector to SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        vector_id = f"vec_{datetime.now().timestamp()}"
        metadata_json = json.dumps(metadata) if metadata else None
        vector_bytes = json.dumps(vector).encode()
        
        await self.conn.execute(
            "INSERT INTO vectors (id, collection_id, text, vector, metadata) VALUES (?, ?, ?, ?, ?)",
            (vector_id, collection_id, text, vector_bytes, metadata_json)
        )
        await self.conn.commit()
        
        return vector_id
    
    async def search_vectors(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        async with self.conn.execute(
            "SELECT id, text, vector, metadata, created_at FROM vectors WHERE collection_id = ?",
            (collection_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            
            results = []
            for row in rows:
                stored_vector = json.loads(row[2].decode())
                similarity = self._cosine_similarity(query_vector, stored_vector)
                
                if similarity >= min_similarity:
                    results.append({
                        "id": row[0],
                        "text": row[1],
                        "similarity": similarity,
                        "metadata": json.loads(row[3]) if row[3] else None,
                        "created_at": row[4]
                    })
            
            # Sort by similarity and limit results
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
    
    async def bulk_save_vectors(
        self,
        collection: str,
        vectors: List[Dict[str, Any]]
    ) -> List[str]:
        """Save multiple vectors to SQLite."""
        if not self.conn:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        vector_ids = []
        
        for vector_data in vectors:
            vector_id = f"vec_{datetime.now().timestamp()}"
            vector_ids.append(vector_id)
            
            text = vector_data.get('text', '')
            vector = vector_data.get('vector', [])
            metadata = vector_data.get('metadata')
            
            metadata_json = json.dumps(metadata) if metadata else None
            vector_bytes = json.dumps(vector).encode()
            
            await self.conn.execute(
                "INSERT INTO vectors (id, collection_id, text, vector, metadata) VALUES (?, ?, ?, ?, ?)",
                (vector_id, collection_id, text, vector_bytes, metadata_json)
            )
        
        await self.conn.commit()
        return vector_ids 