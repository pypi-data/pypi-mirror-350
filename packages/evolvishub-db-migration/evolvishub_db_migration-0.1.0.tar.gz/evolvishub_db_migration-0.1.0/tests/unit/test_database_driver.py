import pytest
from unittest.mock import Mock
from src.evolvishub_db_migration.database import DatabaseDriver
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def test_database_driver_init():
    """Test database driver initialization."""
    config = {
        'database_type': 'sqlite',
        'connection_string': 'sqlite:///:memory:'
    }
    driver = DatabaseDriver(config)
    assert driver.engine is not None
    assert driver.connection is not None

def test_database_driver_execute_sql():
    """Test executing SQL statements."""
    config = {
        'database_type': 'sqlite',
        'connection_string': 'sqlite:///:memory:'
    }
    driver = DatabaseDriver(config)
    
    # Test successful execution
    sql = "CREATE TABLE test (id INTEGER PRIMARY KEY)"
    result = driver.execute_sql(sql)
    assert result is True
    
    # Test error handling
    invalid_sql = "INVALID SQL"
    with pytest.raises(SQLAlchemyError):
        driver.execute_sql(invalid_sql)

def test_database_driver_get_applied_migrations():
    """Test getting applied migrations."""
    config = {
        'database_type': 'sqlite',
        'connection_string': 'sqlite:///:memory:'
    }
    driver = DatabaseDriver(config)
    
    # Create test table
    driver.execute_sql("""
        CREATE TABLE IF NOT EXISTS migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Test empty migrations
    migrations = driver.get_applied_migrations()
    assert len(migrations) == 0
    
    # Add test migration
    driver.execute_sql("""
        INSERT INTO migrations (version, name)
        VALUES (1, 'test_migration')
    """)
    
    # Test with migrations
    migrations = driver.get_applied_migrations()
    assert len(migrations) == 1
    assert migrations[0]['version'] == 1
    assert migrations[0]['name'] == 'test_migration'

def test_database_driver_mark_migration_applied():
    """Test marking migration as applied."""
    config = {
        'database_type': 'sqlite',
        'connection_string': 'sqlite:///:memory:'
    }
    driver = DatabaseDriver(config)
    
    # Create test table
    driver.execute_sql("""
        CREATE TABLE IF NOT EXISTS migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Test marking migration
    driver.mark_migration_applied(1, 'test_migration')
    
    # Verify migration was marked
    migrations = driver.get_applied_migrations()
    assert len(migrations) == 1
    assert migrations[0]['version'] == 1
    assert migrations[0]['name'] == 'test_migration'
