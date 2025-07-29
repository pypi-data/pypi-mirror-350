"""
Logging utilities for the Evolvishub SQLite Adapter.
"""

import logging

def setup_logger(log_level, log_file=None):
    """
    Set up the logger with the configured settings.
    
    Args:
        log_level (str): Logging level (e.g., "INFO", "DEBUG").
        log_file (str, optional): Path to the log file.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("evolvishub_sqlite_adapter")
    logger.setLevel(log_level.upper())
    
    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger 