"""
Database adapters for Ollama integration.

This package provides database adapters for storing and retrieving Ollama-related data,
including model information, generation history, and embeddings.
"""

from .base import (
    BaseDatabaseAdapter,
    VectorDatabaseAdapter,
    DocumentDatabaseAdapter,
    QueryBuilder
)
from .sqlite import SQLiteAdapter, SQLiteQueryBuilder
from .postgresql import PostgreSQLAdapter, PostgreSQLQueryBuilder
from .mongodb import MongoDBAdapter, MongoDBQueryBuilder

__all__ = [
    # Base classes
    'BaseDatabaseAdapter',
    'VectorDatabaseAdapter',
    'DocumentDatabaseAdapter',
    'QueryBuilder',
    
    # SQLite implementation
    'SQLiteAdapter',
    'SQLiteQueryBuilder',
    
    # PostgreSQL implementation
    'PostgreSQLAdapter',
    'PostgreSQLQueryBuilder',
    
    # MongoDB implementation
    'MongoDBAdapter',
    'MongoDBQueryBuilder'
] 