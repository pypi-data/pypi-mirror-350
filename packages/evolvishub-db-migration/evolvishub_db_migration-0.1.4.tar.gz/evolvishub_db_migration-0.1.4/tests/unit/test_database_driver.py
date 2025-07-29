import pytest
from evolvishub_db_migration.databases.sqlite import SQLiteDriver
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def test_database_driver_init():
    """Test database driver initialization."""
    driver = SQLiteDriver('sqlite:///:memory:')
    assert driver is not None

def test_database_driver_execute_sql():
    """Test executing SQL statements."""
    driver = SQLiteDriver('sqlite:///:memory:')
    driver.connect()
    # Test successful execution
    sql = "CREATE TABLE test (id INTEGER PRIMARY KEY)"
    driver.execute_migration(sql)
    # No exception means success
    # Test error handling
    invalid_sql = "INVALID SQL"
    with pytest.raises(Exception):
        driver.execute_migration(invalid_sql)

def test_database_driver_get_applied_migrations():
    """Test getting applied migrations."""
    driver = SQLiteDriver('sqlite:///:memory:')
    driver.connect()
    # Create test table
    driver.execute_migration(
        """
        CREATE TABLE IF NOT EXISTS applied_migrations (
            name TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Test empty migrations
    migrations = driver.get_applied_migrations()
    assert isinstance(migrations, list)

def test_database_driver_mark_migration_applied():
    """Test marking migration as applied."""
    driver = SQLiteDriver('sqlite:///:memory:')
    driver.connect()
    # Create test table
    driver.execute_migration(
        """
        CREATE TABLE IF NOT EXISTS applied_migrations (
            name TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Test marking migration
    driver.record_migration('test_migration')
    # Verify migration was marked
    migrations = driver.get_applied_migrations()
    assert 'test_migration' in migrations
