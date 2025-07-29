import pytest
import subprocess
from pathlib import Path

def test_cli_init(test_db_path, test_config_path):
    """Test the CLI initialization command."""
    result = subprocess.run(
        ["db-migrate", "init", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Initialized migration system" in result.stdout

def test_cli_create_migration(test_db_path, test_config_path, clean_migrations_dir):
    """Test creating a migration through CLI."""
    result = subprocess.run(
        ["db-migrate", "create", "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Created migration" in result.stdout
    
    # Check migration file was created
    migration_files = list(clean_migrations_dir.glob("*.sql"))
    assert len(migration_files) == 1

def test_cli_migrate(test_db_path, test_config_path):
    """Test running migrations through CLI."""
    # First create a migration
    subprocess.run(
        ["db-migrate", "create", "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)", test_config_path],
        check=True
    )
    
    # Run migrations
    result = subprocess.run(
        ["db-migrate", "migrate", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Successfully applied" in result.stdout

def test_cli_rollback(test_db_path, test_config_path):
    """Test rolling back migrations through CLI."""
    # First create and apply a migration
    subprocess.run(
        ["db-migrate", "create", "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)", test_config_path],
        check=True
    )
    subprocess.run(
        ["db-migrate", "migrate", test_config_path],
        check=True
    )
    
    # Rollback the migration
    result = subprocess.run(
        ["db-migrate", "rollback", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Successfully rolled back" in result.stdout
