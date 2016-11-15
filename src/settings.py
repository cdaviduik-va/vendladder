"""
settings.py Documentation
"""
import os

STATIC_VERSION_NUMBER = 1

IS_DEV_APPSERVER = 'development' in os.environ.get('SERVER_SOFTWARE', '').lower()
