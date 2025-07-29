import pytest
from pathlib import Path
from evolvishub_db_migration.migration_file import MigrationFile

def test_migration_file_creation(clean_migrations_dir):
    """Test creating a migration file."""
    migration = MigrationFile(
        version=1,
        name="test_migration",
        up_sql="CREATE TABLE test (id INTEGER PRIMARY KEY)",
        down_sql="DROP TABLE IF EXISTS test"
    )
    
    file_path = clean_migrations_dir / "1_test_migration.sql"
    migration.save(file_path)
    
    assert file_path.exists()
    
    # Verify file contents
    with open(file_path, 'r') as f:
        content = f.read()
        assert "-- Migration: 1_test_migration" in content
        assert "-- Up SQL:" in content
        assert "CREATE TABLE test (id INTEGER PRIMARY KEY)" in content
        assert "-- Down SQL:" in content
        assert "DROP TABLE IF EXISTS test" in content

def test_migration_file_load(clean_migrations_dir):
    """Test loading a migration file."""
    # Create a test migration file
    file_path = clean_migrations_dir / "1_test_migration.sql"
    with open(file_path, 'w') as f:
        f.write("""
-- Migration: 1_test_migration
-- Up SQL:
CREATE TABLE test (id INTEGER PRIMARY KEY)
-- Down SQL:
DROP TABLE IF EXISTS test
""")
    
    # Load the migration file
    migration = MigrationFile.load(file_path)
    
    assert migration.version == 1
    assert migration.name == "test_migration"
    assert migration.up_sql == "CREATE TABLE test (id INTEGER PRIMARY KEY)"
    assert migration.down_sql == "DROP TABLE IF EXISTS test"

def test_migration_file_invalid_format(clean_migrations_dir):
    """Test loading migration file with invalid format."""
    # Create invalid migration file
    file_path = clean_migrations_dir / "1_test_migration.sql"
    with open(file_path, 'w') as f:
        f.write("""
-- Invalid format
CREATE TABLE test (id INTEGER PRIMARY KEY)
""")
    
    with pytest.raises(ValueError):
        MigrationFile.load(file_path)

def test_migration_file_version_parsing(clean_migrations_dir):
    """Test parsing migration version from filename."""
    # Test valid versions
    valid_versions = [
        ("1_test_migration.sql", 1),
        ("123_test_migration.sql", 123),
        ("001_test_migration.sql", 1)
    ]
    
    for filename, expected_version in valid_versions:
        file_path = clean_migrations_dir / filename
        migration = MigrationFile(
            version=expected_version,
            name="test_migration",
            up_sql="CREATE TABLE test (id INTEGER PRIMARY KEY)",
            down_sql="DROP TABLE IF EXISTS test"
        )
        migration.save(file_path)
        loaded_migration = MigrationFile.load(file_path)
        assert loaded_migration.version == expected_version
    
    # Test invalid versions
    invalid_versions = [
        "test_migration.sql",
        "a1_test_migration.sql",
        "1.0_test_migration.sql",
        "_test_migration.sql"
    ]
    
    for filename in invalid_versions:
        file_path = clean_migrations_dir / filename
        with pytest.raises(ValueError):
            MigrationFile(
                version=1,
                name="test_migration",
                up_sql="CREATE TABLE test (id INTEGER PRIMARY KEY)",
                down_sql="DROP TABLE IF EXISTS test"
            ).save(file_path)
