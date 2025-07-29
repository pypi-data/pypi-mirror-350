from abc import ABC, abstractmethod
from typing import List, Optional

class DatabaseDriver(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_migration(self, migration_sql: str):
        pass

    @abstractmethod
    def get_applied_migrations(self) -> List[str]:
        pass

    @abstractmethod
    def record_migration(self, migration_name: str):
        pass
