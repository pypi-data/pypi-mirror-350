"""
Pointr Cloud Commons - A Python package for interacting with Pointr Cloud APIs.

This package provides a set of tools for interacting with various Pointr Cloud APIs,
including services for managing sites, buildings, levels, and SDK configurations.
"""

import logging

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import main classes for easy access
from pointr_cloud_common.api.v9.v9_api_service import V9ApiService
from pointr_cloud_common.api.v9.base_service import V9ApiError

# Version information
__version__ = '0.1.0'
