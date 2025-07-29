"""
Logging utility functions for Taskinity.

This module contains utilities for setting up and configuring logging.
"""
import logging
import os
import sys
from typing import Optional, Union, Dict, Any

def setup_logger(
    name: str = "taskinity", 
    level: Union[int, str] = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    propagate: bool = False
) -> logging.Logger:
    """
    Set up and configure a logger.
    
    Args:
        name: Name of the logger.
        level: Logging level (e.g., logging.INFO, logging.DEBUG).
        log_file: Path to log file. If None, logs only to console.
        log_format: Custom log format. If None, uses a default format.
        propagate: Whether to propagate logs to parent loggers.
        
    Returns:
        Configured logger instance.
    """
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Set level
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    logger.setLevel(level)
    
    # Set propagation
    logger.propagate = propagate
    
    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Set default format if not provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is provided
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
