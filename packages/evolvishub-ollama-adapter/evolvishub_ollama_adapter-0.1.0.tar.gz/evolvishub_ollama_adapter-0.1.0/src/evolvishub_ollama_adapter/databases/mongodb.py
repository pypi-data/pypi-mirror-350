"""
MongoDB database adapter for Ollama integration.

This module provides the MongoDB implementation of the database adapter.
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId

from .base import DocumentDatabaseAdapter, QueryBuilder
from ..config import Config
from ..exceptions import DataSourceError

class MongoDBQueryBuilder(QueryBuilder):
    """MongoDB query builder implementation."""
    
    def build_filter(self, field: str, operator: str, value: Any) -> Dict[str, Any]:
        """Build a filter condition for MongoDB."""
        operators = {
            "eq": "$eq",
            "ne": "$ne",
            "gt": "$gt",
            "gte": "$gte",
            "lt": "$lt",
            "lte": "$lte",
            "like": "$regex",
            "in": "$in",
            "nin": "$nin",
            "exists": "$exists",
            "type": "$type"
        }
        
        if operator not in operators:
            raise ValueError(f"Unsupported operator: {operator}")
        
        if operator == "like":
            return {field: {"$regex": value, "$options": "i"}}
        
        return {field: {operators[operator]: value}}
    
    def build_sort(self, field: str, direction: str = "asc") -> Dict[str, Any]:
        """Build a sort condition for MongoDB."""
        if direction not in ["asc", "desc"]:
            raise ValueError(f"Invalid sort direction: {direction}")
        
        return {field: 1 if direction == "asc" else -1}
    
    def build_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        """Build pagination parameters for MongoDB."""
        if page < 1 or page_size < 1:
            raise ValueError("Page and page size must be positive")
        
        return {
            "skip": (page - 1) * page_size,
            "limit": page_size
        }

class MongoDBAdapter(DocumentDatabaseAdapter):
    """MongoDB database adapter."""
    
    def __init__(self, connection_string: str, database_name: str, config: Optional[Config] = None):
        """Initialize MongoDB adapter.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
            config: Configuration instance
        """
        super().__init__(config)
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self._query_builder = MongoDBQueryBuilder()
    
    async def connect(self) -> None:
        """Connect to MongoDB database."""
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        await self.create_indexes()
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB database."""
        if self.client:
            self.client.close()
    
    async def create_indexes(self) -> None:
        """Create necessary MongoDB indexes."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        # Create indexes for records collection
        await self.db.records.create_index("collection_id")
        await self.db.records.create_index("created_at")
        await self.db.records.create_index([("data", "text")])
        
        # Create indexes for vectors collection
        await self.db.vectors.create_index("collection_id")
        await self.db.vectors.create_index("created_at")
        await self.db.vectors.create_index([("vector", "2dsphere")])
    
    async def _ensure_collection(self, collection: str) -> str:
        """Ensure a collection exists and return its ID."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_doc = await self.db.collections.find_one({"name": collection})
        if collection_doc:
            return str(collection_doc["_id"])
        
        result = await self.db.collections.insert_one({
            "name": collection,
            "created_at": datetime.utcnow()
        })
        return str(result.inserted_id)
    
    async def save_record(self, collection: str, data: Dict[str, Any]) -> str:
        """Save a record to MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        record_id = str(ObjectId())
        
        await self.db.records.insert_one({
            "_id": ObjectId(record_id),
            "collection_id": collection_id,
            "data": data,
            "created_at": datetime.utcnow()
        })
        
        return record_id
    
    async def get_record(self, collection: str, record_id: str) -> Dict[str, Any]:
        """Get a record from MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        record = await self.db.records.find_one({
            "collection_id": collection_id,
            "_id": ObjectId(record_id)
        })
        
        if not record:
            raise DataSourceError(f"Record not found: {record_id}")
        
        return {
            "id": str(record["_id"]),
            "data": record["data"],
            "metadata": record.get("metadata"),
            "created_at": record["created_at"]
        }
    
    async def search_records(
        self,
        collection: str,
        query: Dict[str, Any],
        sort: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for records in MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        # Build MongoDB query
        mongo_query = {"collection_id": collection_id}
        
        for field, value in query.items():
            if isinstance(value, dict):
                for op, val in value.items():
                    filter_cond = self.query_builder.build_filter(f"data." + field, op, val)
                    mongo_query.update(filter_cond)
            else:
                mongo_query[f"data.{field}"] = value
        
        # Build sort conditions
        sort_dict = {}
        if sort:
            for field, direction in sort.items():
                sort_cond = self.query_builder.build_sort(f"data." + field, direction)
                sort_dict.update(sort_cond)
        
        # Build pagination
        pagination = self.query_builder.build_pagination(page, page_size)
        
        # Execute query
        cursor = self.db.records.find(mongo_query)
        
        if sort_dict:
            cursor = cursor.sort(list(sort_dict.items()))
        
        cursor = cursor.skip(pagination["skip"]).limit(pagination["limit"])
        
        records = await cursor.to_list(length=pagination["limit"])
        
        return [{
            "id": str(record["_id"]),
            "data": record["data"],
            "metadata": record.get("metadata"),
            "created_at": record["created_at"]
        } for record in records]
    
    async def update_record(
        self,
        collection: str,
        record_id: str,
        data: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Update a record in MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        result = await self.db.records.update_one(
            {
                "collection_id": collection_id,
                "_id": ObjectId(record_id)
            },
            {
                "$set": {
                    "data": data,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=upsert
        )
        
        return result.modified_count > 0 or (upsert and result.upserted_id is not None)
    
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record from MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        result = await self.db.records.delete_one({
            "collection_id": collection_id,
            "_id": ObjectId(record_id)
        })
        
        return result.deleted_count > 0
    
    async def bulk_save_records(self, collection: str, records: List[Dict[str, Any]]) -> List[str]:
        """Save multiple records to MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        record_ids = []
        
        for record in records:
            record_id = ObjectId()
            record_ids.append(str(record_id))
            
            await self.db.records.insert_one({
                "_id": record_id,
                "collection_id": collection_id,
                "data": record,
                "created_at": datetime.utcnow()
            })
        
        return record_ids
    
    async def bulk_update_records(
        self,
        collection: str,
        updates: List[Dict[str, Any]]
    ) -> int:
        """Update multiple records in MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        updated = 0
        
        for update in updates:
            record_id = update.get('id')
            if not record_id:
                continue
            
            result = await self.db.records.update_one(
                {
                    "collection_id": collection_id,
                    "_id": ObjectId(record_id)
                },
                {
                    "$set": {
                        "data": update.get('data', {}),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                updated += 1
        
        return updated
    
    async def bulk_delete_records(self, collection: str, record_ids: List[str]) -> int:
        """Delete multiple records from MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        result = await self.db.records.delete_many({
            "collection_id": collection_id,
            "_id": {"$in": [ObjectId(rid) for rid in record_ids]}
        })
        
        return result.deleted_count
    
    async def save_document(
        self,
        collection: str,
        document: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a document to MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        document_id = str(ObjectId())
        
        await self.db.documents.insert_one({
            "_id": ObjectId(document_id),
            "collection_id": collection_id,
            "content": document,
            "metadata": metadata,
            "created_at": datetime.utcnow()
        })
        
        return document_id
    
    async def search_documents(
        self,
        collection: str,
        query: Dict[str, Any],
        sort: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for documents in MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        # Build MongoDB query
        mongo_query = {"collection_id": collection_id}
        
        for field, value in query.items():
            if isinstance(value, dict):
                for op, val in value.items():
                    filter_cond = self.query_builder.build_filter(f"content." + field, op, val)
                    mongo_query.update(filter_cond)
            else:
                mongo_query[f"content.{field}"] = value
        
        # Build sort conditions
        sort_dict = {}
        if sort:
            for field, direction in sort.items():
                sort_cond = self.query_builder.build_sort(f"content." + field, direction)
                sort_dict.update(sort_cond)
        
        # Build pagination
        pagination = self.query_builder.build_pagination(page, page_size)
        
        # Execute query
        cursor = self.db.documents.find(mongo_query)
        
        if sort_dict:
            cursor = cursor.sort(list(sort_dict.items()))
        
        cursor = cursor.skip(pagination["skip"]).limit(pagination["limit"])
        
        documents = await cursor.to_list(length=pagination["limit"])
        
        return [{
            "id": str(doc["_id"]),
            "content": doc["content"],
            "metadata": doc.get("metadata"),
            "created_at": doc["created_at"]
        } for doc in documents]
    
    async def save_vector(
        self,
        collection: str,
        text: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a vector to MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        vector_id = str(ObjectId())
        
        await self.db.vectors.insert_one({
            "_id": ObjectId(vector_id),
            "collection_id": collection_id,
            "text": text,
            "vector": vector,
            "metadata": metadata,
            "created_at": datetime.utcnow()
        })
        
        return vector_id
    
    async def search_vectors(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        
        # Use MongoDB's $geoNear for vector similarity search
        pipeline = [
            {
                "$match": {
                    "collection_id": collection_id
                }
            },
            {
                "$geoNear": {
                    "near": query_vector,
                    "distanceField": "similarity",
                    "spherical": True,
                    "maxDistance": 1 - min_similarity,
                    "limit": limit
                }
            }
        ]
        
        cursor = self.db.vectors.aggregate(pipeline)
        vectors = await cursor.to_list(length=limit)
        
        return [{
            "id": str(vec["_id"]),
            "text": vec["text"],
            "similarity": 1 - vec["similarity"],
            "metadata": vec.get("metadata"),
            "created_at": vec["created_at"]
        } for vec in vectors]
    
    async def bulk_save_vectors(
        self,
        collection: str,
        vectors: List[Dict[str, Any]]
    ) -> List[str]:
        """Save multiple vectors to MongoDB."""
        if not self.db:
            raise DataSourceError("Not connected to database")
        
        collection_id = await self._ensure_collection(collection)
        vector_ids = []
        
        for vector_data in vectors:
            vector_id = ObjectId()
            vector_ids.append(str(vector_id))
            
            text = vector_data.get('text', '')
            vector = vector_data.get('vector', [])
            metadata = vector_data.get('metadata')
            
            await self.db.vectors.insert_one({
                "_id": vector_id,
                "collection_id": collection_id,
                "text": text,
                "vector": vector,
                "metadata": metadata,
                "created_at": datetime.utcnow()
            })
        
        return vector_ids 