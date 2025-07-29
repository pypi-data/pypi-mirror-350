from typing import Dict, Any
import yaml
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file: str = 'migration.ini'):
        self.config_path = Path(config_file)
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            if config is None:
                config = {
                    'database': {
                        'type': 'sqlite',
                        'connection_string': 'sqlite:///./database.db'
                    },
                    'migrations': {
                        'directory': './migrations'
                    }
                }
        else:
            config = {
                'database': {
                    'type': 'sqlite',
                    'connection_string': 'sqlite:///./database.db'
                },
                'migrations': {
                    'directory': './migrations'
                }
            }
            self.save_config(config)
        return config

    @staticmethod
    def validate_database_type(db_type: str) -> bool:
        """Validate if the database type is supported"""
        supported_databases = ['sqlite', 'postgresql', 'mysql', 'mssql']
        return db_type.lower() in supported_databases

    def _validate_database_config(self, config: Dict[str, Any]) -> None:
        """Validate database configuration"""
        db_type = config.get('database', {}).get('type', 'sqlite').lower()
        if not self.validate_database_type(db_type):
            raise ValueError(f"Unsupported database type: {db_type}. Supported types are: sqlite, postgresql, mysql, mssql")

    def get_database_config(self) -> Dict[str, Any]:
        config = self.config.get('database', {}) if self.config else {}
        self._validate_database_config({'database': config})
        return {
            'database_type': config.get('type', 'sqlite'),
            'connection_string': config.get('connection_string', 'sqlite:///./database.db')
        }

    def get_migration_directory(self) -> Path:
        """Get the directory where migrations are stored"""
        return Path(self.config.get('migrations', {}).get('directory', './migrations'))

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
