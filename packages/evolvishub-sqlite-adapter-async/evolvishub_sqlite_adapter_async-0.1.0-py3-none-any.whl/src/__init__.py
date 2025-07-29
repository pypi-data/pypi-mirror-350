"""
Evolvishub SQLite Adapter - A professional async SQLite adapter library.
"""

from evolvishub_sqlite_adapter_async.adapter import SQLiteAdapter
from evolvishub_sqlite_adapter_async.config_manager import ConfigManager, DatabaseConfig
from evolvishub_sqlite_adapter_async.exceptions import (
    SQLiteError,
    ConnectionError,
    PoolError,
    QueryError,
    TransactionError,
    ConfigurationError,
)
from evolvishub_sqlite_adapter_async.logging import (
    log_query,
    log_result,
    log_error,
    sanitize_query,
    sanitize_parameters,
    sanitize_row,
    sanitize_result,
)
from evolvishub_sqlite_adapter_async.types import Row, Result, Parameters, TransactionContext

__version__ = "0.1.0"

__all__ = [
    # Main classes
    "SQLiteAdapter",
    "ConfigManager",
    "DatabaseConfig",
    
    # Exceptions
    "SQLiteError",
    "ConnectionError",
    "PoolError",
    "QueryError",
    "TransactionError",
    "ConfigurationError",
    
    # Types
    "Row",
    "Result",
    "Parameters",
    "TransactionContext",
    
    # Logging utilities
    "log_query",
    "log_result",
    "log_error",
    "sanitize_query",
    "sanitize_parameters",
    "sanitize_row",
    "sanitize_result",
]