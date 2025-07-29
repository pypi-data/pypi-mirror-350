from abc import ABC, abstractmethod
from typing import List, Optional

class DatabaseDriver(ABC):
    @abstractmethod
    def connect(self):
        """Connect to the database"""
        pass

    @abstractmethod
    def execute_migration(self, migration_sql: str, rollback_sql: Optional[str] = None):
        """Execute a migration with transaction support"""
        pass

    @abstractmethod
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migrations"""
        pass

    @abstractmethod
    def record_migration(self, migration_name: str, rollback_sql: Optional[str] = None):
        """Record a migration as applied"""
        pass

    @abstractmethod
    def rollback_migration(self, migration_name: str):
        """Rollback a specific migration"""
        pass

    @abstractmethod
    def close(self):
        """Close the database connection"""
        pass
