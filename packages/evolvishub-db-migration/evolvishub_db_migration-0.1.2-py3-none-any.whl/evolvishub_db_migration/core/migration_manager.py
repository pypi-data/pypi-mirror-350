from typing import List, Optional
from pathlib import Path
from datetime import datetime

from ..config.config import ConfigManager
from ..models.migration import Migration
from ..databases.base import DatabaseDriver
from ..drivers.driver_factory import DriverFactory
from ..utils.logging_config import get_logger

logger = get_logger(__name__)

class MigrationManager:
    def __init__(self, config_path):
        config_path = Path(config_path)
        self.config_manager = ConfigManager(str(config_path))
        self.db_driver: Optional[DatabaseDriver] = None
        logger.info(f"Initialized MigrationManager with config: {config_path}")

    def get_database_driver(self) -> DatabaseDriver:
        """Get the appropriate database driver based on configuration"""
        if not self.db_driver:
            db_config = self.config_manager.get_database_config()
            if not db_config or 'database_type' not in db_config:
                logger.error("Database type not specified in configuration")
                raise ValueError("Database type not specified in configuration")
            self.db_driver = DriverFactory.get_driver(db_config)
            logger.info(f"Initialized database driver: {db_config['database_type']}")
        return self.db_driver

    def load_migrations(self) -> List[Migration]:
        """Load all migration files from the migrations directory"""
        migrations_dir = Path(self.config_manager.get_migration_directory())
        if not migrations_dir.exists():
            logger.warning(f"Migrations directory does not exist: {migrations_dir}")
            return []

        migrations = []
        for file in sorted(migrations_dir.glob("*.sql")):
            with open(file, "r") as f:
                sql = f.read()
            name = file.stem
            version = name.split("_")[0]
            migrations.append(Migration(name=name, version=version, sql=sql))
            logger.debug(f"Loaded migration: {name} (version: {version})")
        
        logger.info(f"Loaded {len(migrations)} migrations from {migrations_dir}")
        return migrations

    def apply_migrations(self, verbose: bool = False) -> None:
        """Apply all pending migrations"""
        db_driver = None
        try:
            db_driver = self.get_database_driver()
            db_driver.connect()
            
            migrations = self.load_migrations()
            for migration in migrations:
                if verbose:
                    logger.info(f"Applying migration: {migration.name}")
                    logger.debug(f"SQL: {migration.sql}")
                
                db_driver.execute_migration(migration.sql)
                db_driver.record_migration(migration.name)
                
                if verbose:
                    logger.info(f"Successfully applied migration: {migration.name}")
        finally:
            if db_driver and hasattr(db_driver, 'close'):
                db_driver.close()
                logger.debug("Database connection closed")

    def create_migration(self, name, sql):
        """Create a new migration file with the given name and SQL."""
        if not sql.strip():
            logger.error("Attempted to create migration with empty SQL")
            raise ValueError("SQL cannot be empty.")
        
        # Create migrations directory if it doesn't exist
        migrations_dir = Path(self.config_manager.get_migration_directory())
        migrations_dir.mkdir(exist_ok=True)
        
        # Get existing migrations to determine next version number
        existing_migrations = list(migrations_dir.glob("*.sql"))
        next_version = len(existing_migrations) + 1
        version = f"{next_version:03d}"  # Format as 001, 002, etc.
        
        # Check for duplicate migration names
        for file in migrations_dir.glob("*.sql"):
            if file.stem.endswith(f"_{name}"):
                logger.error(f"Migration with name '{name}' already exists")
                raise ValueError(f"Migration with name '{name}' already exists.")
        
        # Generate migration filename
        filename = f"{version}_{name}.sql"
        file_path = migrations_dir / filename
        
        # Write SQL to file
        with open(file_path, 'w') as f:
            f.write(sql)
        
        logger.info(f"Created migration: {filename}")
        # Return a Migration object with the name without .sql extension
        return Migration(name=file_path.stem, version=version, sql=sql)

    def get_migration_status(self) -> list:
        """Get the status of all migrations."""
        db_driver = None
        try:
            db_driver = self.get_database_driver()
            db_driver.connect()
            
            # Get all migrations
            migrations = self.load_migrations()
            # Get applied migrations
            applied_migrations = db_driver.get_applied_migrations()
            
            # Create status list
            status = []
            for migration in migrations:
                status.append({
                    'name': migration.name,
                    'version': migration.version,
                    'applied': migration.version in applied_migrations
                })
            return status
        finally:
            if db_driver and hasattr(db_driver, 'close'):
                db_driver.close()
                logger.debug("Database connection closed") 