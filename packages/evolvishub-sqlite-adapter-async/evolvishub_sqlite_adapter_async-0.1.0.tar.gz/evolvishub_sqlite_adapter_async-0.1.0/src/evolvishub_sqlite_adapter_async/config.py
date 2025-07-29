"""
Configuration module for the SQLite adapter.
"""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class SQLiteConfig:
    """
    Configuration for SQLite adapter.
    
    Attributes:
        database: Path to the SQLite database file
        pool_size: Maximum number of connections in the pool
        timeout: Connection timeout in seconds
        journal_mode: SQLite journal mode (WAL, DELETE, TRUNCATE, PERSIST, MEMORY, OFF)
        synchronous: SQLite synchronous mode (OFF, NORMAL, FULL, EXTRA)
        foreign_keys: Enable foreign key constraints
        check_same_thread: Check if the connection is used in the same thread
    """
    
    database: str | Path
    pool_size: int = 5
    timeout: float = 30.0
    journal_mode: str = "WAL"
    synchronous: str = "NORMAL"
    foreign_keys: bool = True
    check_same_thread: bool = False
    
    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.pool_size < 1:
            raise ValueError("pool_size must be at least 1")
        
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        valid_journal_modes = {"WAL", "DELETE", "TRUNCATE", "PERSIST", "MEMORY", "OFF"}
        if self.journal_mode.upper() not in valid_journal_modes:
            raise ValueError(f"journal_mode must be one of {valid_journal_modes}")
        
        valid_sync_modes = {"OFF", "NORMAL", "FULL", "EXTRA"}
        if self.synchronous.upper() not in valid_sync_modes:
            raise ValueError(f"synchronous must be one of {valid_sync_modes}")
        
        # Convert string path to Path object
        if isinstance(self.database, str):
            self.database = Path(self.database) 