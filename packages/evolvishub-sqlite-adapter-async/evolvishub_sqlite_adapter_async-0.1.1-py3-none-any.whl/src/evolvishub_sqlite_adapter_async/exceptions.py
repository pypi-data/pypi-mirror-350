"""
Custom exceptions for the SQLite adapter.
"""

class SQLiteError(Exception):
    """Base exception for all SQLite adapter errors."""
    pass


class ConnectionError(SQLiteError):
    """Raised when there are issues with database connections."""
    pass


class QueryError(SQLiteError):
    """Raised when there are issues with query execution."""
    pass


class PoolError(SQLiteError):
    """Raised when there are issues with the connection pool."""
    pass


class TransactionError(SQLiteError):
    """Raised when there are issues with transactions."""
    pass


class ConfigurationError(SQLiteError):
    """Raised when there are issues with the configuration."""
    pass 