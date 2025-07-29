"""
Custom exceptions for Evolvishub SQLite Adapter.
"""

class SQLiteAdapterError(Exception):
    """Base exception for all SQLite adapter errors."""
    pass


class ConnectionError(SQLiteAdapterError):
    """Raised when there is an error connecting to the database."""
    pass


class QueryError(SQLiteAdapterError):
    """Raised when there is an error executing a query."""
    pass


class TransactionError(SQLiteAdapterError):
    """Raised when there is an error in a transaction."""
    pass


class ConfigurationError(SQLiteAdapterError):
    """Raised when there is an error in the configuration."""
    pass


class PoolError(SQLiteAdapterError):
    """Raised when there is an error with the connection pool."""
    pass


class MigrationError(SQLiteAdapterError):
    """Raised when there is an error during database migration."""
    pass 