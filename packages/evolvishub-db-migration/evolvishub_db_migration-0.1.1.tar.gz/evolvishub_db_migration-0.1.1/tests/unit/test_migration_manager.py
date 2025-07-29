import unittest
from unittest.mock import Mock, patch

from src.evolvishub_db_migration.core import MigrationManager


class TestMigrationManager(unittest.TestCase):
    def setUp(self):
        self.config_manager = Mock()
        self.manager = MigrationManager()
        self.manager.config_manager = self.config_manager

    @patch('src.evolvishub_db_migration.core.DatabaseDriver')
    def test_get_database_driver(self, mock_driver):
        """Test getting database driver"""
        self.config_manager.get_database_config.return_value = {
            'database_type': 'sqlite',
            'connection_string': 'sqlite:///test.db'
        }
        
        driver = self.manager._get_database_driver()
        self.assertIsNotNone(driver)

    def test_load_migrations(self):
        """Test loading migrations"""
        self.config_manager.get_migration_directory.return_value = 'tests/fixtures/migrations'
        
        migrations = self.manager.load_migrations()
        self.assertGreater(len(migrations), 0)
        
        for migration in migrations:
            self.assertTrue(hasattr(migration, 'name'))
            self.assertTrue(hasattr(migration, 'version'))
            self.assertTrue(hasattr(migration, 'sql'))

    @patch('src.evolvishub_db_migration.core.DatabaseDriver')
    def test_apply_migrations(self, mock_driver):
        """Test applying migrations"""
        self.config_manager.get_database_config.return_value = {
            'database_type': 'sqlite',
            'connection_string': 'sqlite:///test.db'
        }
        
        mock_driver.get_applied_migrations.return_value = []
        
        self.manager.apply_migrations()
        mock_driver.execute_migration.assert_called()

if __name__ == '__main__':
    unittest.main()
