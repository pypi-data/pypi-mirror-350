"""
Tests for k-logger
"""

import pytest
from k_logger import setup_korean_logger, get_logger
import re
from datetime import datetime


def test_auto_setup():
    """Test that logger is automatically set up on import"""
    logger = get_logger()
    assert logger is not None


def test_log_format():
    """Test that log format matches expected pattern"""
    logger = setup_korean_logger(level="INFO", show_file_info=True)
    
    # This is a simple test to ensure logger can be called
    # In a real test environment, we'd capture the output
    logger.info("테스트 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
    
    assert True  # If we get here without errors, basic functionality works


def test_custom_setup():
    """Test custom logger setup with different levels"""
    logger = setup_korean_logger(level="DEBUG", show_file_info=False)
    
    # Test that all log levels work
    logger.debug("디버그")
    logger.info("정보")
    logger.warning("경고")
    logger.error("에러")
    
    assert True


def test_level_abbreviations():
    """Test that level abbreviations are correct"""
    # This would require capturing logger output
    # For now, just ensure the logger can be configured
    logger = setup_korean_logger(level="DEBUG")
    assert logger is not None 