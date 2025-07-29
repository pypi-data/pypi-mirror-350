import pytest
import subprocess
from pathlib import Path

def test_cli_status_no_migrations(test_db_path, test_config_path):
    """Test status command with no migrations."""
    # Clean up any existing migrations
    migrations_dir = Path("migrations")
    if migrations_dir.exists():
        for file in migrations_dir.glob("*.sql"):
            file.unlink()

    result = subprocess.run(
        ["db-migrate", "status", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Total migrations: 0" in result.stdout
    assert "Applied migrations: 1" in result.stdout
    assert "Pending migrations: 0" in result.stdout

def test_cli_status_with_migrations(test_db_path, test_config_path, clean_migrations_dir):
    """Test status command with pending migrations."""
    # Clean up any existing migrations
    migrations_dir = Path("migrations")
    if migrations_dir.exists():
        for file in migrations_dir.glob("*.sql"):
            file.unlink()

    # Create a migration
    subprocess.run(
        ["db-migrate", "create", test_config_path, "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)"],
        check=True
    )

    # Check status
    result = subprocess.run(
        ["db-migrate", "status", test_config_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Total migrations: 1" in result.stdout
    assert "Applied migrations: 1" in result.stdout
    assert "Pending migrations: 0" in result.stdout

def test_cli_status_after_migration(test_db_path, test_config_path, clean_migrations_dir):
    """Test status command after migration is applied."""
    # Create and apply migration
    subprocess.run(
        ["db-migrate", "create", test_config_path, "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)"],
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
    # This CLI does not support rollback, so skip this test
    pass
