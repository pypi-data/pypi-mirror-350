import pytest
import os
from pathlib import Path
import tempfile
from contextlib import contextmanager

@pytest.fixture(scope="session")
def test_db_path():
    """Fixture to create a temporary SQLite database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        yield str(db_path)

@pytest.fixture(scope="session")
def test_config_path():
    """Fixture to create a temporary configuration file."""
    with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w', delete=False) as f:
        config_content = """
database:
  connection_string: sqlite:///test.db
  migrations_path: migrations
"""
        f.write(config_content)
        f.flush()
    yield f.name
    os.unlink(f.name)

@pytest.fixture(scope="function")
def clean_migrations_dir():
    """Fixture to ensure migrations directory is clean before each test."""
    migrations_dir = Path("migrations")
    if migrations_dir.exists():
        for file in migrations_dir.glob("*.sql"):
            file.unlink()
    else:
        migrations_dir.mkdir()
    yield migrations_dir
    for file in migrations_dir.glob("*.sql"):
        file.unlink()
