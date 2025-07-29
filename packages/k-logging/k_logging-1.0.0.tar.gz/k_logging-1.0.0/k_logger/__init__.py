"""
K-Logger: Korean-friendly logging utility
A simple and clean logger with Korean timezone and abbreviated log levels.
"""

from .logger import setup_korean_logger, get_logger

__version__ = "1.0.0"
__author__ = "june-oh"
__email__ = "ohjs@sogang.ac.kr"

__all__ = ["setup_korean_logger", "get_logger"] 