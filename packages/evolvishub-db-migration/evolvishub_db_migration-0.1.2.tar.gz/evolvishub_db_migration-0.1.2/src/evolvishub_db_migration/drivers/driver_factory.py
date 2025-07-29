from ..databases.sqlite import SQLiteDriver
from ..databases.base import DatabaseDriver

class DriverFactory:
    @staticmethod
    def get_driver(db_config) -> DatabaseDriver:
        """Get the appropriate database driver based on configuration."""
        if db_config.get('database_type') == 'sqlite':
            return SQLiteDriver(db_config['connection_string'])
        else:
            raise ValueError(f"Unsupported database type: {db_config.get('database_type')}") 