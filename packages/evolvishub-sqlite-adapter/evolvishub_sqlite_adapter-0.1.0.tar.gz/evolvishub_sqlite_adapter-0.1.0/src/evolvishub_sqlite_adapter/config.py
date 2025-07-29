"""
Database configuration module for Evolvishub SQLite Adapter.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """
    Configuration for SQLite database connection.
    
    Attributes:
        database (str): Path to the SQLite database file
        pool_size (int): Maximum number of connections in the pool
        journal_mode (str): SQLite journal mode (WAL, DELETE, TRUNCATE, PERSIST, MEMORY, OFF)
        synchronous (str): SQLite synchronous mode (OFF, NORMAL, FULL, EXTRA)
        foreign_keys (bool): Enable foreign key constraints
        check_same_thread (bool): Check if the connection is used in the same thread
        cache_size (int): SQLite cache size in pages
        temp_store (str): SQLite temporary storage mode (DEFAULT, FILE, MEMORY)
        page_size (int): SQLite page size in bytes
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (Optional[str]): Path to log file, if None logs to console
    """
    
    database: str
    pool_size: int = 5
    journal_mode: str = "WAL"
    synchronous: str = "NORMAL"
    foreign_keys: bool = True
    check_same_thread: bool = False
    cache_size: int = 2000
    temp_store: str = "MEMORY"
    page_size: int = 4096
    log_level: str = "INFO"
    log_file: Optional[str] = None

    def __post_init__(self):
        """Validate configuration values after initialization."""
        if self.pool_size < 1:
            raise ValueError("pool_size must be at least 1")
        
        if self.cache_size < 0:
            raise ValueError("cache_size must be non-negative")
        
        if self.page_size not in [512, 1024, 2048, 4096, 8192, 16384, 32768]:
            raise ValueError("page_size must be a power of 2 between 512 and 32768")
        
        valid_journal_modes = ["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
        if self.journal_mode.upper() not in valid_journal_modes:
            raise ValueError(f"journal_mode must be one of {valid_journal_modes}")
        
        valid_sync_modes = ["OFF", "NORMAL", "FULL", "EXTRA"]
        if self.synchronous.upper() not in valid_sync_modes:
            raise ValueError(f"synchronous must be one of {valid_sync_modes}")
        
        valid_temp_stores = ["DEFAULT", "FILE", "MEMORY"]
        if self.temp_store.upper() not in valid_temp_stores:
            raise ValueError(f"temp_store must be one of {valid_temp_stores}")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"log_level must be one of {valid_log_levels}") 