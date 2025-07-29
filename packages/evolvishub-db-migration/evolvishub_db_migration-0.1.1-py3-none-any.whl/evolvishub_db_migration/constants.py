"""Constants for the database migration tool"""

# Database types
SUPPORTED_DATABASES = ['sqlite', 'postgresql', 'mysql', 'mssql']

# Migration file patterns
MIGRATION_FILE_PATTERN = r'^v\d+_[a-zA-Z0-9_]+\.sql$'

# Default values
DEFAULT_DATABASE_TYPE = 'sqlite'
DEFAULT_CONNECTION_STRING = 'sqlite:///./database.db'
DEFAULT_MIGRATION_DIRECTORY = './migrations'

# Error messages
ERROR_INVALID_MIGRATION_NAME = "Invalid migration name format: {name}"
ERROR_INVALID_VERSION = "Invalid version format: {version}"
ERROR_UNSUPPORTED_DATABASE = "Unsupported database type: {db_type}"
ERROR_MISSING_CONFIG = "Missing required configuration: {key}"
ERROR_EMPTY_VALUE = "{key} cannot be empty"

# SQL Templates
CREATE_MIGRATIONS_TABLE_SQL = {
    'sqlite': """
        CREATE TABLE IF NOT EXISTS applied_migrations (
            name TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rollback_sql TEXT
        )
    """,
    'postgresql': """
        CREATE TABLE IF NOT EXISTS applied_migrations (
            name TEXT PRIMARY KEY,
            applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            rollback_sql TEXT
        )
    """,
    'mysql': """
        CREATE TABLE IF NOT EXISTS applied_migrations (
            name VARCHAR(255) PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rollback_sql TEXT
        )
    """,
    'mssql': """
        IF NOT EXISTS (
            SELECT * FROM sys.objects 
            WHERE object_id = OBJECT_ID(N'[dbo].[applied_migrations]') 
            AND type in (N'U')
        )
        BEGIN
            CREATE TABLE [dbo].[applied_migrations] (
                [name] NVARCHAR(255) PRIMARY KEY,
                [applied_at] DATETIME DEFAULT GETDATE(),
                [rollback_sql] NVARCHAR(MAX)
            )
        END
    """
}
