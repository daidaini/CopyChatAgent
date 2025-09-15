#!/usr/bin/env python3
"""
Simple test script to verify logging functionality
"""
import sys
import os
sys.path.append('backend')

from logger import Logger
import time

def test_logging():
    print("Testing logging functionality...")

    # Test logger creation
    logger = Logger('test', 'logs')

    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Test with some data
    test_data = {
        'user_id': 123,
        'action': 'test_action',
        'timestamp': time.time()
    }
    logger.info(f"Test data: {test_data}")

    print("Logging test completed. Check the logs directory for output.")

if __name__ == '__main__':
    test_logging()