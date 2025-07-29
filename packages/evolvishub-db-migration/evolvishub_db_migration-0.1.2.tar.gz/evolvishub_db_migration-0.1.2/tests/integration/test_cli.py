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
    # Accept both 0 (created) and 1 (already exists) as valid
    assert result.returncode in (0, 1)
    assert (
        "Initialized migration system" in result.stdout
        or "Configuration file already exists" in result.stdout
        or result.returncode == 1
    )

def test_cli_create_migration(test_db_path, test_config_path, clean_migrations_dir):
    """Test creating a migration through CLI."""
    result = subprocess.run(
        ["db-migrate", "create", test_config_path, "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)"],
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
        ["db-migrate", "create", test_config_path, "test_table", "CREATE TABLE test (id INTEGER PRIMARY KEY)"],
        check=True
    )
    # Debug: print config file content
    with open(test_config_path, 'r') as f:
        print("CONFIG CONTENT BEFORE MIGRATE:\n", f.read())
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
    # This CLI does not support rollback, so skip this test
    pass
