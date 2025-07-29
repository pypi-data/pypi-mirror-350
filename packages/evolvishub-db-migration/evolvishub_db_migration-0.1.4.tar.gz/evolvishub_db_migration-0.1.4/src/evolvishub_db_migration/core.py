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
import sqlparse
import re

def extract_version(name: str) -> int:
    # Handles '001_test', 'v1_test', etc.
    m = re.match(r'(?:v)?(\d+)', name)
    if m:
        return int(m.group(1))
    return 0

class MigrationManager:
    
    def __init__(self, config_file: str = 'migration.ini'):
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.get_database_config()
        self.db_driver = self._get_database_driver()
        if self.db_driver:
            self.db_driver.connect()

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

    def __del__(self):
        """Clean up database connection when the manager is destroyed."""
        if hasattr(self, 'db_driver') and self.db_driver and hasattr(self.db_driver, 'close'):
            self.db_driver.close()

    def create_migration(self, name: str, sql: str) -> Migration:
        """Create a new migration file"""
        # Validate SQL
        parsed = sqlparse.parse(sql)
        if not parsed or not any(str(stmt).strip() for stmt in parsed):
            raise ValueError("Invalid SQL")

        # Get migrations directory
        migrations_dir = self.config_manager.get_migration_directory()
        migrations_dir.mkdir(parents=True, exist_ok=True)

        # Get next version number
        existing_migrations = self.load_migrations()
        next_version = 1
        if existing_migrations:
            last_version = max(extract_version(m.name) for m in existing_migrations)
            next_version = last_version + 1

        # Check for duplicate migration name
        for m in existing_migrations:
            if m.name.endswith(f"_{name}"):
                raise ValueError(f"Migration with name '{name}' already exists.")

        # Create migration file
        migration_name = f"{next_version:03d}_{name}"
        migration_file = migrations_dir / f"{migration_name}.sql"
        
        # Check for duplicate migration file
        if migration_file.exists():
            raise ValueError(f"Migration file already exists: {migration_file}")

        # Write migration file
        with open(migration_file, 'w') as f:
            f.write(sql)

        return Migration(
            name=migration_name,
            version=f"{next_version:03d}",
            sql=sql
        )

    def load_migrations(self) -> List[Migration]:
        migrations_dir = Path(self.config_manager.get_migration_directory())
        migrations = []
        
        # Load migrations from migrations directory
        if migrations_dir.exists():
            for file in migrations_dir.glob('*.sql'):
                with open(file, 'r') as f:
                    sql = f.read()
                version = extract_version(file.stem)
                migration = Migration(
                    name=file.stem,
                    version=f"{version:03d}",
                    sql=sql
                )
                migrations.append(migration)

        # Sort migrations by version
        migrations.sort(key=lambda x: extract_version(x.name))
        return migrations

    def get_migration_status(self) -> Dict[str, Any]:
        """Get the current migration status"""
        migrations = self.load_migrations()
        applied_migrations = self.db_driver.get_applied_migrations() if self.db_driver else []
        
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
        applied_migrations = self.db_driver.get_applied_migrations() if self.db_driver else []
        
        if verbose:
            print(f"Connecting to database: {self.config['database_type']}")
            print(f"Migration directory: {self.config_manager.get_migration_directory()}")
        
        if not self.db_driver:
            raise RuntimeError("Database driver is not initialized.")
        
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
