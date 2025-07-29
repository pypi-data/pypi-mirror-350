"""
Synchronous SQLite adapter implementation.
"""

import logging
import sqlite3
from contextlib import contextmanager
from queue import Queue
from typing import Any, Dict, List, Optional, Union, Set
import os

from ..config import DatabaseConfig
from ..utils.exceptions import (
    ConnectionError,
    QueryError,
    TransactionError,
    PoolError,
)


class SyncSQLiteAdapter:
    """
    Synchronous SQLite adapter with connection pooling and transaction support.
    
    Attributes:
        config (DatabaseConfig): Database configuration
        _pool (Queue): Connection pool
        _logger (logging.Logger): Logger instance
        _transaction_connections (Set[sqlite3.Connection]): Set of connections in transaction
    """
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize the sync SQLite adapter.
        
        Args:
            config (DatabaseConfig): Database configuration
        """
        if not config.database:
            raise ValueError("Database path must be provided.")
        self.config = config
        self._pool: Optional[Queue] = None
        self._logger = self._setup_logger()
        self._transaction_connections: Set[sqlite3.Connection] = set()
        self._current_transaction_conn: Optional[sqlite3.Connection] = None
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with the configured settings."""
        logger = logging.getLogger("evolvishub_sqlite_adapter")
        logger.setLevel(self.config.log_level.upper())
        
        if self.config.log_file:
            handler = logging.FileHandler(self.config.log_file)
        else:
            handler = logging.StreamHandler()
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def connect(self) -> None:
        """Initialize the connection pool."""
        try:
            self._pool = Queue(maxsize=self.config.pool_size)
            for _ in range(self.config.pool_size):
                conn = sqlite3.connect(
                    self.config.database,
                    check_same_thread=self.config.check_same_thread,
                )
                conn.execute(f"PRAGMA journal_mode = {self.config.journal_mode}")
                conn.execute(f"PRAGMA synchronous = {self.config.synchronous}")
                conn.execute(f"PRAGMA foreign_keys = {'ON' if self.config.foreign_keys else 'OFF'}")
                conn.execute(f"PRAGMA cache_size = {self.config.cache_size}")
                conn.execute(f"PRAGMA temp_store = {self.config.temp_store}")
                conn.execute(f"PRAGMA page_size = {self.config.page_size}")
                self._pool.put(conn)
            
            self._logger.info(f"Initialized connection pool with {self.config.pool_size} connections")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize connection pool: {str(e)}")
    
    def close(self) -> None:
        """Close all connections in the pool."""
        if not self._pool:
            return
        
        while not self._pool.empty():
            conn = self._pool.get()
            conn.close()
        
        self._logger.info("Closed all database connections")
        self._pool = None
        self._transaction_connections.clear()
        self._current_transaction_conn = None
    
    @contextmanager
    def _get_connection(self):
        """Get a connection from the pool."""
        if not self._pool:
            raise PoolError("Connection pool not initialized")
        
        # If we're in a transaction, use the same connection
        if self._current_transaction_conn is not None:
            yield self._current_transaction_conn
            return
        
        conn = self._pool.get()
        try:
            yield conn
        finally:
            if conn not in self._transaction_connections:
                self._pool.put(conn)
    
    def execute(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> None:
        """
        Execute a query without returning results.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
        """
        if not query:
            raise ValueError("Query cannot be empty")

        try:
            with self._get_connection() as conn:
                conn.execute(query, params or ())
                if conn not in self._transaction_connections:
                    conn.commit()
        except sqlite3.Error as e:
            raise QueryError(str(e))
        except Exception as e:
            if self._current_transaction_conn is not None:
                raise TransactionError(str(e))
            raise
    
    def fetch_one(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row from the database.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
            
        Returns:
            Optional[Dict[str, Any]]: Row as dictionary or None if no results
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(query, params or ())
                row = cursor.fetchone()
                if row:
                    return dict(zip([col[0] for col in cursor.description], row))
                return None
        except Exception as e:
            raise QueryError(f"Failed to fetch one: {str(e)}")
    
    def fetch_all(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch all rows from the database.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
            
        Returns:
            List[Dict[str, Any]]: List of rows as dictionaries
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(query, params or ())
                rows = cursor.fetchall()
                return [
                    dict(zip([col[0] for col in cursor.description], row))
                    for row in rows
                ]
        except Exception as e:
            raise QueryError(f"Failed to fetch all: {str(e)}")
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        if self._current_transaction_conn is not None:
            raise TransactionError("Nested transactions are not supported")
        
        with self._get_connection() as conn:
            try:
                self._current_transaction_conn = conn
                conn.execute("BEGIN")
                self._transaction_connections.add(conn)
                yield conn  # Yield the connection object
                conn.commit()
            except Exception as e:
                conn.rollback()
                if isinstance(e, TransactionError):
                    raise
                raise TransactionError(str(e))
            finally:
                self._current_transaction_conn = None
                self._transaction_connections.remove(conn)

    def create_table(self, query: str):
        if not query:
            raise ValueError("Query must be provided.")
        self.execute(query)

    def create_table_from_file(self, file_path: str):
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(f"SQL file not found: {file_path}")
        with open(file_path, "r") as f:
            sql = f.read()
        self.create_table(sql)

    def execute_query(self, query: str, params=None):
        if not query:
            raise ValueError("Query must be provided.")
        self.execute(query, params)

    def table_exists(self, table_name: str) -> bool:
        if not table_name:
            raise ValueError("Table name must be provided.")
        result = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return result is not None

    def get_table_schema(self, table_name: str):
        if not table_name:
            raise ValueError("Table name must be provided.")
        query = f"PRAGMA table_info({table_name})"
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            columns = cursor.fetchall()
            # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
            return [
                {"cid": col[0], "name": col[1], "type": col[2], "notnull": col[3], "dflt_value": col[4], "pk": col[5]}
                for col in columns
            ]

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
