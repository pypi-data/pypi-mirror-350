from typing import List, Dict, Optional, Any
import os
from pathlib import Path
from .models.migration import Migration
from .config.config import ConfigManager
from .databases.base import DatabaseDriver
from .databases.postgresql import PostgreSQLDriver
from .databases.sqlite import SQLiteDriver
from .databases.mysql import MySQLDriver
from .databases.mssql import MSQLServerDriver

class MigrationManager:
    def __init__(self, config_file: str = 'migration.ini'):
        self.config_manager = ConfigManager(config_file)
        self.db_driver: DatabaseDriver = self._get_database_driver()
        self.config = self.config_manager.get_database_config()

    def _get_database_driver(self) -> DatabaseDriver:
        config = self.config_manager.get_database_config()
        db_type = config['database_type'].lower()
        connection_string = config['connection_string']

        if db_type == 'postgresql':
            return PostgreSQLDriver(connection_string)
        elif db_type == 'sqlite':
            return SQLiteDriver(connection_string)
        elif db_type == 'mysql':
            return MySQLDriver(connection_string)
        elif db_type == 'mssql':
            return MSQLServerDriver(connection_string)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def load_migrations(self) -> List[Migration]:
        migrations_dir = Path(self.config_manager.get_migration_directory())
        migrations = []
        
        # Load migrations from migrations directory
        if migrations_dir.exists():
            for file in migrations_dir.glob('*.sql'):
                with open(file, 'r') as f:
                    sql = f.read()
                migration = Migration(
                    name=file.stem,
                    version=file.stem.split('_')[0],
                    sql=sql
                )
                migrations.append(migration)

        # Load migrations from migration.ini
        if self.config_manager.config.has_section('MIGRATIONS'):
            for name, sql in self.config_manager.config.items('MIGRATIONS'):
                migration = Migration(
                    name=name,
                    version=name.split('_')[0],
                    sql=sql
                )
                migrations.append(migration)

        # Sort migrations by version
        migrations.sort(key=lambda x: x.version)
        return migrations

    def get_migration_status(self) -> Dict[str, Any]:
        """Get the current migration status"""
        migrations = self.load_migrations()
        applied_migrations = self.db_driver.get_applied_migrations()
        
        pending_migrations = [m for m in migrations if m.name not in applied_migrations]
        
        return {
            'total': len(migrations),
            'applied': len(applied_migrations),
            'pending': len(pending_migrations),
            'pending_migrations': pending_migrations
        }

    def apply_migrations(self, verbose: bool = False):
        """Apply pending migrations with transaction support"""
        migrations = self.load_migrations()
        applied_migrations = self.db_driver.get_applied_migrations()
        
        if verbose:
            print(f"Connecting to database: {self.config['database_type']}")
            print(f"Migration directory: {self.config_manager.get_migration_directory()}")
        
        try:
            self.db_driver.connect()
            
            for migration in migrations:
                if migration.name not in applied_migrations:
                    if verbose:
                        print(f"\nApplying migration: {migration.name}")
                        print(f"SQL: {migration.sql}")
                    
                    try:
                        self.db_driver.execute_migration(migration.sql)
                        self.db_driver.record_migration(migration.name)
                        if verbose:
                            print(f"Successfully applied migration: {migration.name}")
                        else:
                            print(f"✓ {migration.name}")
                    except Exception as e:
                        if verbose:
                            print(f"Error applying migration {migration.name}: {str(e)}")
                        raise
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            raise
        finally:
            if hasattr(self.db_driver, 'close'):
                self.db_driver.close()
