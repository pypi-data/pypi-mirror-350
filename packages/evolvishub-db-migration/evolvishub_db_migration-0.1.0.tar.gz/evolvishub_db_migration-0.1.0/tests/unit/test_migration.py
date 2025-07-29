import pytest
from evolvishub_db_migration.migration import MigrationManager
from evolvishub_db_migration.config import Config

def test_migration_creation(test_db_path, clean_migrations_dir):
    """Test creating a new migration."""
    manager = MigrationManager(test_db_path)
    
    # Create a new migration
    migration = manager.create_migration("test_migration", "CREATE TABLE test (id INTEGER PRIMARY KEY)")
    assert migration.version > 0
    assert migration.name == "test_migration"
    assert migration.up_sql == "CREATE TABLE test (id INTEGER PRIMARY KEY)"
    assert migration.down_sql == "DROP TABLE IF EXISTS test"
    
    # Check that migration file was created
    migration_file = clean_migrations_dir / f"{migration.version}_test_migration.sql"
    assert migration_file.exists()

def test_invalid_sql(test_db_path):
    """Test handling of invalid SQL."""
    manager = MigrationManager(test_db_path)
    
    with pytest.raises(ValueError):
        manager.create_migration("invalid", "INVALID SQL")

def test_duplicate_migration(test_db_path, clean_migrations_dir):
    """Test creating duplicate migrations."""
    manager = MigrationManager(test_db_path)
    
    # Create first migration
    migration1 = manager.create_migration("test", "CREATE TABLE test (id INTEGER PRIMARY KEY)")
    
    # Try to create another migration with same name
    with pytest.raises(ValueError):
        manager.create_migration("test", "CREATE TABLE test2 (id INTEGER PRIMARY KEY)")
