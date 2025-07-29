import pytest
import subprocess
from pathlib import Path

def test_cli_status_no_migrations(test_db_path, test_config_path):
    """Test status command with no migrations."""
    result = subprocess.run(
        ["db-migrate", "status", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "No migrations found" in result.stdout

def test_cli_status_with_migrations(test_db_path, test_config_path, clean_migrations_dir):
    """Test status command with pending migrations."""
    # Create a migration
    subprocess.run(
        ["db-migrate", "create", "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)", test_config_path],
        check=True
    )
    
    # Check status
    result = subprocess.run(
        ["db-migrate", "status", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Pending migrations:" in result.stdout
    assert "test_table" in result.stdout

def test_cli_status_after_migration(test_db_path, test_config_path, clean_migrations_dir):
    """Test status command after migration is applied."""
    # Create and apply migration
    subprocess.run(
        ["db-migrate", "create", "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)", test_config_path],
        check=True
    )
    subprocess.run(
        ["db-migrate", "migrate", test_config_path],
        check=True
    )
    
    # Check status
    result = subprocess.run(
        ["db-migrate", "status", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "All migrations applied" in result.stdout

def test_cli_status_with_rollback(test_db_path, test_config_path, clean_migrations_dir):
    """Test status command after rollback."""
    # Create and apply migration
    subprocess.run(
        ["db-migrate", "create", "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)", test_config_path],
        check=True
    )
    subprocess.run(
        ["db-migrate", "migrate", test_config_path],
        check=True
    )
    subprocess.run(
        ["db-migrate", "rollback", test_config_path],
        check=True
    )
    
    # Check status
    result = subprocess.run(
        ["db-migrate", "status", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Pending migrations:" in result.stdout
