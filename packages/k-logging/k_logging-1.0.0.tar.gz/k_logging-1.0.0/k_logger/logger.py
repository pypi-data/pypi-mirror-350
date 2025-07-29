"""
Korean-friendly logger implementation using loguru
"""

import sys
from datetime import datetime
from loguru import logger
import pytz


def setup_korean_logger(level="INFO", show_file_info=True):
    """
    Setup Korean-friendly logger with abbreviated levels and Korean timezone
    
    Args:
        level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        show_file_info (bool): Whether to show file path and line number
        
    Returns:
        loguru.Logger: Configured logger instance
    """
    # Remove default handler
    logger.remove()
    
    # Set up Korean timezone
    kst = pytz.timezone('Asia/Seoul')
    
    # Custom time format function for Korean time
    def korean_time_format(record):
        utc_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        korean_time = utc_time.astimezone(kst)
        record["extra"]["korean_time"] = korean_time.strftime("%m-%d %H:%M:%S")
        return record["extra"]["korean_time"]
    
    # Custom level abbreviation function
    def level_abbreviation(record):
        level_map = {
            "DEBUG": "D",
            "INFO": "I", 
            "WARNING": "W",
            "ERROR": "E",
            "CRITICAL": "C"
        }
        record["extra"]["level_short"] = level_map.get(record["level"].name, record["level"].name[0])
        return record["extra"]["level_short"]
    
    # Create format string based on show_file_info option
    if show_file_info:
        format_string = "<level>{extra[level_short]}</level> <green>{extra[korean_time]}</green> | <cyan>{file.path}:{line}</cyan> - <level>{message}</level>"
    else:
        format_string = "<level>{extra[level_short]}</level> <green>{extra[korean_time]}</green> - <level>{message}</level>"
    
    # Add handler with Korean time and abbreviated levels
    logger.add(
        sys.stderr, 
        format=format_string,
        level=level,
        filter=lambda record: record.update({
            "extra": {
                "korean_time": korean_time_format(record),
                "level_short": level_abbreviation(record)
            }
        }) or True
    )
    
    return logger


def get_logger():
    """
    Get the current logger instance
    
    Returns:
        loguru.Logger: Current logger instance
    """
    return logger


# Default setup for convenience
_default_logger_setup = False

def auto_setup():
    """Automatically setup logger on first import"""
    global _default_logger_setup
    if not _default_logger_setup:
        setup_korean_logger()
        _default_logger_setup = True

# Auto-setup on import (can be disabled by calling logger.remove() after import)
auto_setup() 