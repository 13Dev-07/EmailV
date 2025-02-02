"""
Logger Module
Provides logging functionality.
"""

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """
    Sets up and returns a logger.

    Args:
        name (str): The name of the logger.
        level (str): Logging level.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # File Handler with rotation
    file_handler = RotatingFileHandler('logs/main.log', maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Adding Handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger