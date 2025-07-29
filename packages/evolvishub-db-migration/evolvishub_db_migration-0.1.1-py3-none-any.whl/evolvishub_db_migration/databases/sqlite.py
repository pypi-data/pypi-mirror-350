from .base import DatabaseDriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

class SQLiteDriver(DatabaseDriver):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = None
        self.Session = None

    def connect(self):
        self.engine = create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)
        # Create migrations table if it doesn't exist
        self._create_migrations_table()

    def _create_migrations_table(self):
        session = self.Session()
        try:
            session.execute("""
                CREATE TABLE IF NOT EXISTS applied_migrations (
                    name TEXT PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def execute_migration(self, migration_sql: str):
        session = self.Session()
        try:
            session.execute(migration_sql)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_applied_migrations(self) -> List[str]:
        session = self.Session()
        try:
            result = session.execute("SELECT name FROM applied_migrations ORDER BY applied_at")
            return [row[0] for row in result]
        finally:
            session.close()

    def record_migration(self, migration_name: str):
        session = self.Session()
        try:
            session.execute(
                "INSERT INTO applied_migrations (name) VALUES (:name)",
                {'name': migration_name}
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
