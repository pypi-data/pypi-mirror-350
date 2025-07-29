import pytest
from pathlib import Path
from evolvishub_db_migration.core import MigrationManager

def test_migration_creation(test_db_path, clean_migrations_dir):
    """Test creating a new migration."""
    manager = MigrationManager(test_db_path)
    
    # Create a new migration
    migration = manager.create_migration("test_migration", "CREATE TABLE test (id INTEGER PRIMARY KEY)")
    assert int(migration.version) > 0
    assert migration.name.startswith(f"{int(migration.version):03d}_")
    assert "test_migration" in migration.name
    assert migration.sql == "CREATE TABLE test (id INTEGER PRIMARY KEY)"
    
    # Verify migration file was created
    migration_files = list(clean_migrations_dir.glob("*.sql"))
    assert len(migration_files) == 1
    assert migration_files[0].stem == migration.name

def test_invalid_sql(test_db_path):
    """Test handling of invalid SQL."""
    manager = MigrationManager(test_db_path)
    
    with pytest.raises(ValueError):
        manager.create_migration("test_migration", "   ")

    with pytest.raises(ValueError):
        manager.create_migration("test_migration", "")

def test_duplicate_migration(test_db_path, clean_migrations_dir):
    """Test creating duplicate migrations."""
    manager = MigrationManager(test_db_path)
    
    # Create first migration
    migration1 = manager.create_migration("test", "CREATE TABLE test (id INTEGER PRIMARY KEY)")
    
    # Try to create another migration with same name
    with pytest.raises(ValueError):
        manager.create_migration("test", "CREATE TABLE test2 (id INTEGER PRIMARY KEY)")
