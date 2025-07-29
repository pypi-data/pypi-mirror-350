"""
Configuration manager for SQLite adapter.

This module provides a functional configuration management system for the SQLite
adapter. It supports loading configuration from files, validating settings, and
providing default values when needed.

Example:
    ```python
    # Load from file
    config_manager = ConfigManager("config.ini")
    config = config_manager.load_config()
    
    # Use defaults
    config_manager = ConfigManager()
    config = config_manager.load_config()
    ```
"""

import configparser
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from .exceptions import ConfigurationError
from .types import DatabaseConfig

logger = logging.getLogger(__name__)

class ConfigManager:
    """Configuration manager for SQLite adapter."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self._config: Optional[DatabaseConfig] = None
        
    def load_config(self) -> DatabaseConfig:
        """Load configuration from file or environment.
        
        Returns:
            Database configuration
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        if self._config:
            return self._config
            
        if self.config_file:
            self._config = self._load_from_file()
        else:
            self._config = self._load_from_env()
            
        self._validate_config(self._config)
        return self._config
        
    def _load_from_file(self) -> DatabaseConfig:
        """Load configuration from file.
        
        Returns:
            Database configuration
            
        Raises:
            ConfigurationError: If configuration file is invalid
        """
        if not os.path.exists(self.config_file):
            raise ConfigurationError(f"Configuration file not found: {self.config_file}")
            
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        if "sqlite" not in config:
            raise ConfigurationError("Missing [sqlite] section in configuration file")
            
        sqlite_config = config["sqlite"]
        config_dict = {
            "database": sqlite_config.get("database"),
            "pool_size": sqlite_config.getint("pool_size", 5),
            "timeout": sqlite_config.getfloat("timeout", 30.0),
            "journal_mode": sqlite_config.get("journal_mode", "WAL"),
            "synchronous": sqlite_config.get("synchronous", "NORMAL"),
            "foreign_keys": sqlite_config.getboolean("foreign_keys", True),
            "check_same_thread": sqlite_config.getboolean("check_same_thread", False),
            "cache_size": sqlite_config.getint("cache_size", -2000),
            "temp_store": sqlite_config.get("temp_store", "MEMORY"),
            "page_size": sqlite_config.getint("page_size", 4096),
            "log_level": sqlite_config.get("log_level", "INFO"),
            "log_file": sqlite_config.get("log_file", "")
        }
        
        return DatabaseConfig.from_dict(config_dict)
        
    def _load_from_env(self) -> DatabaseConfig:
        """Load configuration from environment variables.
        
        Returns:
            Database configuration
            
        Raises:
            ConfigurationError: If required environment variables are missing
        """
        if "SQLITE_DATABASE" not in os.environ:
            raise ConfigurationError("SQLITE_DATABASE environment variable is required")
            
        config_dict = {
            "database": os.environ["SQLITE_DATABASE"],
            "pool_size": int(os.environ.get("SQLITE_POOL_SIZE", "5")),
            "timeout": float(os.environ.get("SQLITE_TIMEOUT", "30.0")),
            "journal_mode": os.environ.get("SQLITE_JOURNAL_MODE", "WAL"),
            "synchronous": os.environ.get("SQLITE_SYNCHRONOUS", "NORMAL"),
            "foreign_keys": os.environ.get("SQLITE_FOREIGN_KEYS", "ON").upper() == "ON",
            "check_same_thread": os.environ.get("SQLITE_CHECK_SAME_THREAD", "OFF").upper() == "ON",
            "cache_size": int(os.environ.get("SQLITE_CACHE_SIZE", "-2000")),
            "temp_store": os.environ.get("SQLITE_TEMP_STORE", "MEMORY"),
            "page_size": int(os.environ.get("SQLITE_PAGE_SIZE", "4096")),
            "log_level": os.environ.get("SQLITE_LOG_LEVEL", "INFO"),
            "log_file": os.environ.get("SQLITE_LOG_FILE", "")
        }
        
        return DatabaseConfig.from_dict(config_dict)
        
    def _validate_config(self, config: DatabaseConfig) -> None:
        """Validate configuration values.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        config.validate()
        
    def setup_logging(self) -> None:
        """Set up logging based on configuration."""
        if not self._config:
            self.load_config()
            
        logging.basicConfig(
            level=self._config.log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename=self._config.log_file if self._config.log_file else None
        )
