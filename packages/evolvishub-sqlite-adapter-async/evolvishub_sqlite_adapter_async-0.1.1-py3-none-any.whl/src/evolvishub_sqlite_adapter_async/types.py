"""
Type definitions for the SQLite adapter.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

import aiosqlite

from .exceptions import ConfigurationError, QueryError, TransactionError
from .type_defs import Parameters, Result, Row

@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration.
    
    Attributes:
        database: Path to the SQLite database file.
        pool_size: Number of connections in the pool.
        timeout: Connection timeout in seconds.
        journal_mode: SQLite journal mode (WAL, DELETE, etc.).
        synchronous: SQLite synchronous mode (OFF, NORMAL, FULL, EXTRA).
        foreign_keys: Whether to enable foreign key constraints.
        check_same_thread: Whether to check if connection is used in same thread.
        cache_size: SQLite cache size in pages (negative for KB).
        temp_store: Where to store temporary tables and indices.
        page_size: SQLite page size in bytes.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file, if any.
    """
    database: str
    pool_size: int
    timeout: float
    journal_mode: str
    synchronous: str
    foreign_keys: bool
    check_same_thread: bool
    cache_size: int
    temp_store: str
    page_size: int
    log_level: str
    log_file: str

    def __post_init__(self):
        """Validate configuration after initialization."""
        self.validate()

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "DatabaseConfig":
        """Create configuration from dictionary.
        
        Args:
            config_dict: Dictionary containing configuration values.
            
        Returns:
            A new DatabaseConfig instance.
            
        Example:
            ```python
            config = DatabaseConfig.from_dict({
                "database": "test.db",
                "pool_size": 5,
                "timeout": 30.0,
                "journal_mode": "WAL",
                "synchronous": "NORMAL",
                "foreign_keys": True,
                "check_same_thread": False,
                "cache_size": -2000,
                "temp_store": "MEMORY",
                "page_size": 4096,
                "log_level": "INFO",
                "log_file": "sqlite.log"
            })
            ```
        """
        return cls(
            database=str(config_dict["database"]),
            pool_size=int(config_dict["pool_size"]),
            timeout=float(config_dict["timeout"]),
            journal_mode=str(config_dict["journal_mode"]),
            synchronous=str(config_dict["synchronous"]),
            foreign_keys=bool(config_dict["foreign_keys"]),
            check_same_thread=bool(config_dict["check_same_thread"]),
            cache_size=int(config_dict["cache_size"]),
            temp_store=str(config_dict["temp_store"]),
            page_size=int(config_dict["page_size"]),
            log_level=str(config_dict["log_level"]),
            log_file=str(config_dict["log_file"]) if config_dict.get("log_file") else "",
        )

    def validate(self) -> None:
        """Validate configuration values.
        
        Checks that all configuration values are within acceptable ranges and
        have valid values.
        
        Raises:
            ConfigurationError: If any configuration value is invalid.
            
        Example:
            ```python
            try:
                config.validate()
            except ConfigurationError as e:
                print(f"Invalid configuration: {e}")
            ```
        """
        if not self.database:
            raise ConfigurationError("Database path is required")
            
        if self.pool_size < 1:
            raise ConfigurationError("pool_size must be at least 1")
        
        if self.timeout <= 0:
            raise ConfigurationError("timeout must be positive")
        
        valid_journal_modes = {"WAL", "DELETE", "TRUNCATE", "PERSIST", "MEMORY", "OFF"}
        if self.journal_mode.upper() not in valid_journal_modes:
            raise ConfigurationError(f"journal_mode must be one of {valid_journal_modes}")
        
        valid_sync_modes = {"OFF", "NORMAL", "FULL", "EXTRA"}
        if self.synchronous.upper() not in valid_sync_modes:
            raise ConfigurationError(f"synchronous must be one of {valid_sync_modes}")
        
        valid_temp_stores = {"DEFAULT", "FILE", "MEMORY"}
        if self.temp_store.upper() not in valid_temp_stores:
            raise ConfigurationError(f"temp_store must be one of {valid_temp_stores}")
        
        if self.page_size not in {512, 1024, 2048, 4096, 8192, 16384, 32768}:
            raise ConfigurationError("page_size must be a power of 2 between 512 and 32768")
            
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level.upper() not in valid_log_levels:
            raise ConfigurationError(f"log_level must be one of {valid_log_levels}")

class TransactionContext:
    """Transaction context manager for SQLite operations."""

    def __init__(self, connection: aiosqlite.Connection):
        """Initialize transaction context.
        
        Args:
            connection: SQLite connection to use for transaction.
        """
        self.connection = connection
        self._in_transaction = False

    async def __aenter__(self) -> 'TransactionContext':
        """Start transaction."""
        await self.connection.execute("BEGIN")
        self._in_transaction = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """End transaction."""
        if not self._in_transaction:
            return

        try:
            if exc_type is None:
                await self.connection.execute("COMMIT")
            else:
                await self.connection.execute("ROLLBACK")
        finally:
            self._in_transaction = False

    async def execute(
        self,
        query: str,
        parameters: Optional[Parameters] = None
    ) -> Result:
        """Execute a query within transaction.
        
        Args:
            query: SQL query to execute
            parameters: Optional query parameters
            
        Returns:
            QueryResult containing rows, row count, and last row ID
            
        Raises:
            QueryError: If query execution fails
            TransactionError: If no active transaction
        """
        if not self._in_transaction:
            raise TransactionError("No active transaction")
            
        try:
            cursor = await self.connection.execute(query, parameters or ())
            rows = await cursor.fetchall()
            
            result: Result = {
                'rows': [dict(zip([col[0] for col in cursor.description], row)) for row in rows] if cursor.description else [],
                'rowcount': cursor.rowcount,
                'lastrowid': cursor.lastrowid
            }
            
            # Commit after each operation to ensure changes are persisted
            await self.connection.commit()
            
            return result
                
        except Exception as e:
            raise QueryError(f"Transaction query execution failed: {e}")
    
    async def fetch_one(self, query: str, parameters: Parameters = None) -> Optional[Row]:
        """Fetch a single row within the transaction.
        
        Args:
            query: SQL query to execute.
            parameters: Query parameters (optional).
            
        Returns:
            A single row as a dictionary, or None if no rows are found.
        """
        cursor = await self.connection.execute(query, parameters or ())
        row = await cursor.fetchone()
        return dict(zip([col[0] for col in cursor.description], row)) if row and cursor.description else None
    
    async def fetch_all(self, query: str, parameters: Parameters = None) -> List[Row]:
        """Fetch all rows within the transaction.
        
        Args:
            query: SQL query to execute.
            parameters: Query parameters (optional).
            
        Returns:
            List of rows as dictionaries.
        """
        cursor = await self.connection.execute(query, parameters or ())
        rows = await cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows] if cursor.description else [] 