"""
Timezone utilities for Python 3.9+ compatibility.

This module provides timezone-aware datetime functions that work
across different Python versions, including Python 3.13.
"""
from datetime import datetime, timezone


def utc_now():
    """
    Get current UTC datetime, compatible with Python 3.9+.
    
    This replaces the deprecated datetime.utcnow() method.
    
    Returns:
        datetime: Current UTC datetime with timezone info.
    """
    return datetime.now(timezone.utc)


def utc_timestamp():
    """
    Get current UTC timestamp.
    
    Returns:
        float: Current UTC timestamp.
    """
    return utc_now().timestamp()
