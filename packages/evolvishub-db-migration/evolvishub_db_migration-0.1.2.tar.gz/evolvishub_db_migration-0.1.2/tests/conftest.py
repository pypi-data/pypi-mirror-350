import pytest
import os
from pathlib import Path
import tempfile
from contextlib import contextmanager
import shutil

@pytest.fixture
def test_db_path():
    """Create a temporary database file."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    yield db_path
    Path(db_path).unlink()

@pytest.fixture
def test_config_path(test_db_path):
    """Create a temporary config file with the correct database path."""
    with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
        config_path = f.name
        config_content = f"""
database:
  type: sqlite
  connection_string: sqlite:///{test_db_path}
migrations:
  directory: migrations
"""
        f.write(config_content.encode())
    yield config_path
    Path(config_path).unlink()

@pytest.fixture
def clean_migrations_dir():
    """Create a clean migrations directory."""
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
    migrations_dir.mkdir()
    yield migrations_dir
    shutil.rmtree(migrations_dir)
