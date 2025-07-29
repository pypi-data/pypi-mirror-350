"""
Main SQLite adapter implementation.

This module provides an asynchronous SQLite adapter with connection pooling,
transaction management, and comprehensive error handling. It is designed to be
thread-safe and efficient for high-concurrency applications.

Example:
    ```python
    async def main():
        # Initialize adapter with config file
        adapter = SQLiteAdapter("config.ini")
        await adapter.connect()
        
        # Execute a query
        result = await adapter.execute("SELECT * FROM users")
        print(result)
        
        # Use transactions
        async with adapter.transaction() as tx:
            await tx.execute("INSERT INTO users (name) VALUES (?)", ["John"])
    ```
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncGenerator, Callable, List, Optional, TypeVar, Union, cast

import aiosqlite

from .config_manager import ConfigManager, DatabaseConfig
from .exceptions import (
    ConnectionError,
    PoolError,
    QueryError,
    TransactionError,
)
from .logging import log_error, log_query, log_result
from .types import Parameters, Result, Row, TransactionContext

logger = logging.getLogger(__name__)

T = TypeVar("T")
AsyncFunc = Callable[..., Any]


def with_connection(func: AsyncFunc) -> AsyncFunc:
    """Decorator to handle connection acquisition and release.
    
    This decorator manages the lifecycle of database connections, ensuring they
    are properly acquired from the pool and released back after use.
    
    Args:
        func: The async function to wrap.
        
    Returns:
        Wrapped function that handles connection management.
        
    Raises:
        ConnectionError: If the adapter is closed when attempting to use it.
    """
    @wraps(func)
    async def wrapper(self: "SQLiteAdapter", *args: Any, **kwargs: Any) -> Any:
        if self._closed:
            raise ConnectionError("Adapter is closed")
        
        conn = None
        try:
            conn = await self._pool.get()
            return await func(self, conn, *args, **kwargs)
        finally:
            if conn is not None and not self._closed:
                await self._pool.put(conn)
    
    return cast(AsyncFunc, wrapper)


class SQLiteAdapter:
    """Async SQLite adapter with connection pooling.
    
    This class provides a high-level interface for working with SQLite databases
    asynchronously. It includes features such as:
    
    - Connection pooling for efficient resource management
    - Transaction management with context managers
    - Comprehensive error handling
    - Configurable SQLite settings
    - Type-safe query execution
    
    Attributes:
        config (DatabaseConfig): The current database configuration.
        _pool (asyncio.Queue): Connection pool queue.
        _pool_size (int): Current number of connections in the pool.
        _closed (bool): Whether the adapter is closed.
    """
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize the SQLite adapter.
        
        Args:
            config: Database configuration. If not provided, will be loaded from
                   environment variables or config file.
        """
        self.config_manager = ConfigManager()
        self.config = config or self.config_manager.load_config()
        self._pool: asyncio.Queue[aiosqlite.Connection] = asyncio.Queue()
        self._pool_size = 0
        self._closed = False
        self._initialized = False
    
    @property
    def pool_size(self) -> int:
        """Get the current pool size."""
        return self._pool_size
    
    async def connect(self) -> None:
        """Connect to the database and initialize the connection pool."""
        if self._initialized:
            return

        try:
            # Create connection pool
            self._pool = asyncio.Queue(maxsize=self.config.pool_size)
            
            # Initialize pool with connections
            for _ in range(self.config.pool_size):
                conn = await aiosqlite.connect(
                    self.config.database,
                    timeout=self.config.timeout,
                    check_same_thread=self.config.check_same_thread,
                )
                await self._configure_connection(conn)
                await self._pool.put(conn)

            # Set pool size and mark as initialized
            self._pool_size = self.config.pool_size
            self._initialized = True
            logger.info(f"Initialized connection pool with {self._pool_size} connections")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
    
    async def _create_connection(self) -> Any:
        """Create a new database connection.
        
        Returns:
            SQLite connection
            
        Raises:
            ConnectionError: If connection fails
        """
        try:
            return await aiosqlite.connect(
                self.config.database,
                timeout=self.config.timeout,
                check_same_thread=self.config.check_same_thread,
            )
        except Exception as e:
            raise ConnectionError(f"Failed to create connection: {e}")
    
    async def _configure_connection(self, conn: aiosqlite.Connection) -> None:
        """Configure SQLite connection with settings.
        
        Args:
            conn: The SQLite connection to configure.
        """
        try:
            await conn.execute(f"PRAGMA journal_mode = {self.config.journal_mode}")
            await conn.execute(f"PRAGMA synchronous = {self.config.synchronous}")
            await conn.execute(f"PRAGMA foreign_keys = {'ON' if self.config.foreign_keys else 'OFF'}")
            await conn.execute(f"PRAGMA cache_size = {self.config.cache_size}")
            await conn.execute(f"PRAGMA temp_store = {self.config.temp_store}")
            await conn.execute(f"PRAGMA page_size = {self.config.page_size}")
            await conn.commit()  # Ensure settings are applied
        except Exception as e:
            raise ConnectionError(f"Failed to configure connection: {e}")
    
    async def close(self) -> None:
        """Close all connections in the pool.
        
        This method should be called when the adapter is no longer needed to
        properly clean up resources.
        """
        if self._closed:
            return
        
        self._closed = True
        while not self._pool.empty():
            conn = await self._pool.get()
            await conn.close()
        
        self._pool_size = 0
        logger.info("Closed all connections")
    
    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        """Acquire a connection from the pool.
        
        This is a low-level method that provides direct access to a database
        connection. It's recommended to use higher-level methods like execute()
        or transaction() instead.
        
        Yields:
            A SQLite connection from the pool.
            
        Example:
            ```python
            async with adapter.acquire() as conn:
                await conn.execute("SELECT 1")
            ```
        """
        if self._closed:
            raise ConnectionError("Adapter is closed")
        
        conn = None
        try:
            conn = await self._pool.get()
            yield conn
        finally:
            if conn is not None and not self._closed:
                await self._pool.put(conn)
    
    @with_connection
    async def execute(
        self,
        conn: aiosqlite.Connection,
        query: str,
        parameters: Parameters = None,
    ) -> Result:
        """Execute a query and return the result.
        
        Args:
            conn: Database connection (provided by decorator).
            query: SQL query to execute.
            parameters: Query parameters (optional).
            
        Returns:
            A dictionary containing:
                - rows: List of result rows as dictionaries
                - rowcount: Number of affected rows
                - lastrowid: ID of the last inserted row
                
        Raises:
            QueryError: If query execution fails.
        """
        try:
            log_query(query, parameters)
            cursor = await conn.execute(query, parameters or ())
            
            # Check if this is a DDL statement (CREATE, ALTER, DROP)
            is_ddl = query.strip().upper().startswith(('CREATE', 'ALTER', 'DROP'))
            
            # For DDL statements, commit immediately and ensure all connections see the change
            if is_ddl:
                await conn.commit()
                # Close and reopen all connections to ensure they see the schema change
                old_pool = self._pool
                self._pool = asyncio.Queue(maxsize=self.config.pool_size)
                
                # Close old connections
                while not old_pool.empty():
                    old_conn = await old_pool.get()
                    await old_conn.close()
                
                # Create new connections
                for _ in range(self.config.pool_size):
                    new_conn = await aiosqlite.connect(
                        self.config.database,
                        timeout=self.config.timeout,
                        check_same_thread=self.config.check_same_thread,
                    )
                    await self._configure_connection(new_conn)
                    await self._pool.put(new_conn)
            
            rows = await cursor.fetchall()
            result = {
                "rows": [dict(zip([col[0] for col in cursor.description], row)) for row in rows] if cursor.description else [],
                "rowcount": cursor.rowcount,
                "lastrowid": cursor.lastrowid,
            }
            log_result(result)
            return result
        except Exception as e:
            log_error(e, query, parameters)
            raise QueryError(f"Query execution failed: {e}")
    
    @with_connection
    async def fetch_one(
        self,
        conn: aiosqlite.Connection,
        query: str,
        parameters: Parameters = None,
    ) -> Optional[Row]:
        """Fetch a single row from the database.
        
        Args:
            conn: Database connection (provided by decorator).
            query: SQL query to execute.
            parameters: Query parameters (optional).
            
        Returns:
            A single row as a dictionary, or None if no rows are found.
            
        Raises:
            QueryError: If query execution fails.
            
        Example:
            ```python
            user = await adapter.fetch_one(
                "SELECT * FROM users WHERE id = ?",
                [1]
            )
            if user:
                print(user["name"])
            ```
        """
        try:
            log_query(query, parameters)
            cursor = await conn.execute(query, parameters or ())
            row = await cursor.fetchone()
            if row:
                result = dict(zip([col[0] for col in cursor.description], row))
                log_result(result)
                return result
            return None
        except Exception as e:
            log_error(e, query, parameters)
            raise QueryError(f"Query execution failed: {e}")
    
    @with_connection
    async def fetch_all(
        self,
        conn: aiosqlite.Connection,
        query: str,
        parameters: Parameters = None,
    ) -> List[Row]:
        """Fetch all rows from the database.
        
        Args:
            conn: Database connection (provided by decorator).
            query: SQL query to execute.
            parameters: Query parameters (optional).
            
        Returns:
            List of rows as dictionaries.
            
        Raises:
            QueryError: If query execution fails.
            
        Example:
            ```python
            users = await adapter.fetch_all(
                "SELECT * FROM users WHERE age > ?",
                [18]
            )
            for user in users:
                print(user["name"])
            ```
        """
        try:
            log_query(query, parameters)
            cursor = await conn.execute(query, parameters or ())
            rows = await cursor.fetchall()
            result = [dict(zip([col[0] for col in cursor.description], row)) for row in rows]
            log_result(result)
            return result
        except Exception as e:
            log_error(e, query, parameters)
            raise QueryError(f"Query execution failed: {e}")
    
    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[TransactionContext, None]:
        """Get a transaction context.

        Returns:
            A transaction context that can be used as an async context manager.

        Example:
            ```python
            async with adapter.transaction() as tx:
                await tx.execute("INSERT INTO users (name) VALUES (?)", ["John"])
            ```
        """
        if not self._initialized:
            raise ConnectionError("Adapter not initialized")

        async with self.acquire() as conn:
            async with TransactionContext(conn) as transaction_conn:
                yield transaction_conn
    
    async def execute_many(
        self,
        query: str,
        parameters_list: List[Parameters],
    ) -> Result:
        """Execute a query multiple times with different parameters.
        
        This method is useful for batch operations like bulk inserts or updates.
        
        Args:
            query: SQL query to execute.
            parameters_list: List of parameter sets to execute the query with.
            
        Returns:
            A dictionary containing:
                - rows: List of result rows as dictionaries
                - rowcount: Total number of affected rows
                - lastrowid: ID of the last inserted row
                
        Raises:
            QueryError: If query execution fails.
            
        Example:
            ```python
            users = [
                ["John", "john@example.com"],
                ["Jane", "jane@example.com"]
            ]
            result = await adapter.execute_many(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                users
            )
            print(f"Inserted {result['rowcount']} users")
            ```
        """
        try:
            log_query(query, parameters_list)
            async with self.acquire() as conn:
                cursor = await conn.executemany(query, parameters_list)
                rows = await cursor.fetchall()
                result = {
                    "rows": [dict(zip([col[0] for col in cursor.description], row)) for row in rows],
                    "rowcount": cursor.rowcount,
                    "lastrowid": cursor.lastrowid,
                }
                log_result(result)
                return result
        except Exception as e:
            log_error(e, query, parameters_list)
            raise QueryError(f"Batch execution failed: {e}")
    
    async def execute_script(self, script: str) -> None:
        """Execute a SQL script.

        Args:
            script: SQL script to execute.

        Raises:
            QueryError: If script execution fails.

        Example:
            ```python
            await adapter.execute_script('''
                CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
                CREATE TABLE profiles (user_id INTEGER, bio TEXT);
            ''')
            ```
        """
        try:
            log_query(script)
            async with self.acquire() as conn:
                await conn.executescript(script)
                await conn.commit()
                # Update all connections in the pool to see the schema change
                for _ in range(self._pool_size):
                    async with self.acquire() as update_conn:
                        await update_conn.execute("PRAGMA schema_version")
                        await update_conn.commit()
        except Exception as e:
            log_error(e, script)
            raise QueryError(f"Script execution failed: {e}")

    @property
    def initialized(self):
        return self._initialized

    @property
    def closed(self):
        return self._closed

    @property
    def pool(self):
        return self._pool


class Transaction:
    """Asynchronous transaction context manager."""
    
    def __init__(self, adapter: SQLiteAdapter):
        """Initialize transaction with adapter.
        
        Args:
            adapter: SQLite adapter instance
        """
        self.adapter = adapter
        self.conn: Optional[aiosqlite.Connection] = None
        
    async def __aenter__(self) -> 'Transaction':
        """Start transaction."""
        self.conn = await self.adapter._get_connection()
        await self.conn.execute("BEGIN")
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """End transaction."""
        if not self.conn:
            return
            
        try:
            if exc_type is None:
                await self.conn.execute("COMMIT")
            else:
                await self.conn.execute("ROLLBACK")
                raise TransactionError(f"Transaction failed: {exc_val}")
                
        finally:
            self.adapter._release_connection(self.conn)
            self.conn = None
            
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
        if not self.conn:
            raise TransactionError("No active transaction")
            
        try:
            log_query(query, parameters)
            
            async with self.conn.cursor() as cursor:
                await cursor.execute(query, parameters or {})
                rows = await cursor.fetchall()
                
                result: Result = {
                    'rows': [dict(zip([col[0] for col in cursor.description], row)) for row in rows],
                    'row_count': cursor.rowcount,
                    'last_row_id': cursor.lastrowid
                }
                
                log_result(result)
                return result
                
        except Exception as e:
            log_error(e)
            raise QueryError(f"Transaction query execution failed: {e}")

    async def _get_connection(self) -> aiosqlite.Connection:
        """Get a connection from the pool."""
        if self.adapter.closed:
            raise ConnectionError("Adapter is closed")
            
        if not self.adapter.initialized:
            await self.adapter.connect()
            
        try:
            return await self.adapter.pool.get()
        except asyncio.QueueEmpty:
            raise PoolError("No connections available in pool")
            
    def _release_connection(self, conn: aiosqlite.Connection) -> None:
        """Release a connection back to the pool."""
        if not self.adapter.closed and conn:
            self.adapter.pool.put_nowait(conn)
            
    @property
    def is_closed(self) -> bool:
        """Check if the adapter is closed."""
        return self.adapter.closed
        
    @property
    def pool_size(self) -> int:
        """Get the current pool size."""
        return self.adapter.pool_size 