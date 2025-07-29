"""
Evolvishub SQLite Adapter - A modern SQLite adapter for Python applications.
"""

from .async_adapter.adapter import AsyncSQLiteAdapter
from .sync_adapter.adapter import SyncSQLiteAdapter
from .config import DatabaseConfig
from .utils.exceptions import (
    ConnectionError,
    QueryError,
    TransactionError,
    PoolError,
)

# For backward compatibility
SQLiteAdapter = SyncSQLiteAdapter

__version__ = "0.1.0"

__all__ = [
    "AsyncSQLiteAdapter",
    "SyncSQLiteAdapter",
    "SQLiteAdapter",
    "DatabaseConfig",
    "ConnectionError",
    "QueryError",
    "TransactionError",
    "PoolError",
]