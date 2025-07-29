from typing import Dict, Any
import configparser
import os

class ConfigManager:
    def __init__(self, config_file: str = 'migration.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            # Set default configuration
            self.config['DEFAULT'] = {
                'database_type': 'sqlite',
                'connection_string': 'sqlite:///./database.db',
                'migration_directory': './migrations'
            }

    @staticmethod
    def validate_database_type(db_type: str) -> bool:
        """Validate if the database type is supported"""
        supported_databases = ['sqlite', 'postgresql', 'mysql', 'mssql']
        return db_type.lower() in supported_databases

    def get_database_config(self) -> Dict[str, Any]:
        config = dict(self.config['DEFAULT'])
        db_type = config.get('database_type', 'sqlite').lower()
        
        if not self.validate_database_type(db_type):
            raise ValueError(f"Unsupported database type: {db_type}. Supported types are: sqlite, postgresql, mysql, mssql")
            
        return config

    def get_migration_directory(self) -> str:
        """Get the directory where migrations are stored"""
        return self.config['DEFAULT'].get('migration_directory', './migrations')

    def get_database_config(self) -> Dict[str, Any]:
        return dict(self.config['DEFAULT'])
