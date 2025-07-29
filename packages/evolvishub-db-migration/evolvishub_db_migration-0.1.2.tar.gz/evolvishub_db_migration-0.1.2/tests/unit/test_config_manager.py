import pytest
from pathlib import Path
from evolvishub_db_migration.config.config import ConfigManager
import yaml

def test_config_manager_init():
    """Test ConfigManager initialization."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)
    assert config_manager.config_path == config_path

def test_load_config():
    """Test loading configuration."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)

    # Test loading valid config
    config = config_manager.load_config()
    assert 'database' in config
    assert 'migrations' in config
    assert config['database']['type'] == 'sqlite'
    assert config['database']['connection_string'] == 'sqlite:///test.db'
    assert config['migrations']['directory'] in ('migrations', './migrations')

def test_get_database_config():
    """Test getting database configuration."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)

    db_config = config_manager.get_database_config()
    assert 'database_type' in db_config
    assert 'connection_string' in db_config
    assert db_config['database_type'] == 'sqlite'
    assert db_config['connection_string'] == 'sqlite:///test.db'

    # Test invalid database type
    invalid_config = {
        'database': {
            'type': 'invalid',
            'connection_string': 'invalid://connection'
        },
        'migrations': {
            'directory': 'migrations'
        }
    }
    config_manager.config = invalid_config
    with pytest.raises(ValueError):
        config_manager.get_database_config()

def test_get_migration_directory():
    """Test getting migration directory."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)

    migrations_dir = config_manager.get_migration_directory()
    assert migrations_dir == Path('migrations')

def test_validate_config():
    """Test configuration validation."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)

    # Test valid database type
    assert config_manager.validate_database_type('sqlite')
    assert config_manager.validate_database_type('postgresql')
    assert config_manager.validate_database_type('mysql')
    assert config_manager.validate_database_type('mssql')

    # Test invalid database type
    assert not config_manager.validate_database_type('invalid')

def test_save_config():
    """Test saving configuration."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)

    # Test saving valid config
    new_config = {
        'database': {
            'type': 'sqlite',
            'connection_string': 'sqlite:///test.db'
        },
        'migrations': {
            'directory': 'migrations'
        }
    }
    config_manager.save_config(new_config)

    # Verify config was saved
    with open(config_path, 'r') as f:
        saved_config = yaml.safe_load(f)
    assert saved_config == new_config
