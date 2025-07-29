from .base import DatabaseDriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

class PostgreSQLDriver(DatabaseDriver):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = None
        self.Session = None
        self.session = None

    def connect(self):
        """Connect to the database and create migrations table if needed"""
        self.engine = create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_migrations_table()

    def _create_migrations_table(self):
        """Create migrations tracking table if it doesn't exist"""
        session = self.Session()
        try:
            session.execute("""
                CREATE TABLE IF NOT EXISTS applied_migrations (
                    name TEXT PRIMARY KEY,
                    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    rollback_sql TEXT
                )
            """)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def execute_migration(self, migration_sql: str, rollback_sql: Optional[str] = None):
        """Execute a migration with transaction support"""
        session = self.Session()
        try:
            # Start transaction
            session.begin()
            
            # Execute migration
            session.execute(migration_sql)
            
            # Record migration with rollback SQL
            session.execute(
                """
                INSERT INTO applied_migrations (name, applied_at, rollback_sql)
                VALUES (:name, CURRENT_TIMESTAMP, :rollback_sql)
                """,
                {'name': self.current_migration_name, 'rollback_sql': rollback_sql}
            )
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migrations"""
        session = self.Session()
        try:
            result = session.execute("SELECT name FROM applied_migrations ORDER BY applied_at")
            return [row[0] for row in result]
        finally:
            session.close()

    def record_migration(self, migration_name: str, rollback_sql: Optional[str] = None):
        """Record a migration as applied"""
        self.current_migration_name = migration_name
        session = self.Session()
        try:
            session.execute(
                """
                INSERT INTO applied_migrations (name, applied_at, rollback_sql)
                VALUES (:name, CURRENT_TIMESTAMP, :rollback_sql)
                """,
                {'name': migration_name, 'rollback_sql': rollback_sql}
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def rollback_migration(self, migration_name: str):
        """Rollback a specific migration"""
        session = self.Session()
        try:
            # Get rollback SQL
            result = session.execute(
                "SELECT rollback_sql FROM applied_migrations WHERE name = :name",
                {'name': migration_name}
            )
            rollback_sql = result.fetchone()[0]
            
            if rollback_sql:
                # Execute rollback
                session.execute(rollback_sql)
                
                # Delete migration record
                session.execute(
                    "DELETE FROM applied_migrations WHERE name = :name",
                    {'name': migration_name}
                )
                session.commit()
            else:
                raise ValueError(f"No rollback SQL found for migration: {migration_name}")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def close(self):
        """Close the database connection"""
        if self.engine:
            self.engine.dispose()
