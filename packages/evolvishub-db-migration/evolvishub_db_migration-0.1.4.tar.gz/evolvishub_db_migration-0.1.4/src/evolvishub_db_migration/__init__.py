"""Database Migration Tool - A flexible database migration tool supporting multiple databases"""

__version__ = '0.1.0'

from .core import MigrationManager
from .models.migration import Migration
from .config.config import ConfigManager
from .databases import base

__all__ = [
    'MigrationManager',
    'Migration',
    'ConfigManager'
]
