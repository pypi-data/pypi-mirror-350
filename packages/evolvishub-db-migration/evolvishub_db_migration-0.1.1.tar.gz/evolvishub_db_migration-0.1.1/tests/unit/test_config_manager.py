import pytest
from src.evolvishub_db_migration.config import ConfigManager
from pathlib import Path
import yaml

def test_config_manager_init():
    """Test configuration manager initialization."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)
    assert config_manager.config_path == config_path
    assert config_manager.config is not None

def test_load_config():
    """Test loading configuration."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)
    
    # Test loading valid config
    config = config_manager.load_config()
    assert 'database' in config
    assert 'connection_string' in config['database']
    
    # Test loading invalid config
    invalid_path = Path("nonexistent.yaml")
    with pytest.raises(FileNotFoundError):
        ConfigManager(invalid_path).load_config()

def test_get_database_config():
    """Test getting database configuration."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)
    
    db_config = config_manager.get_database_config()
    assert 'database_type' in db_config
    assert 'connection_string' in db_config
    
    # Test invalid database type
    invalid_config = {
        'database': {
            'type': 'invalid',
            'connection_string': 'invalid://connection'
        }
    }
    with pytest.raises(ValueError):
        config_manager._validate_database_config(invalid_config)

def test_get_migration_directory():
    """Test getting migration directory."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)
    
    migrations_dir = config_manager.get_migration_directory()
    assert isinstance(migrations_dir, Path)
    assert migrations_dir.exists()

def test_validate_config():
    """Test configuration validation."""
    config_path = Path("tests/fixtures/test_config.yaml")
    config_manager = ConfigManager(config_path)
    
    # Test valid config
    valid_config = {
        'database': {
            'type': 'sqlite',
            'connection_string': 'sqlite:///test.db'
        },
        'migrations': {
            'directory': 'migrations'
        }
    }
    config_manager._validate_config(valid_config)
    
    # Test invalid config
    invalid_config = {
        'database': {
            'type': 'invalid',
            'connection_string': 'invalid://connection'
        }
    }
    with pytest.raises(ValueError):
        config_manager._validate_config(invalid_config)

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
    
    # Clean up
    with open(config_path, 'w') as f:
        f.write("""
database:
  connection_string: sqlite:///test.db
  migrations_path: migrations
""")
