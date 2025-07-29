import argparse
from pathlib import Path
from typing import Optional

from .core import MigrationManager
from .utils.logging_config import setup_logging, get_logger

logger = get_logger(__name__)

def init_command(args):
    """Initialize a new migration project."""
    config_path = Path(args.config)
    if config_path.exists():
        logger.error(f"Configuration file already exists: {config_path}")
        return 1

    # Create default config
    config_content = """database:
  type: sqlite
  connection_string: sqlite:///database.db

migrations:
  directory: migrations
"""
    config_path.write_text(config_content)
    logger.info(f"Created configuration file: {config_path}")
    return 0

def create_command(args):
    """Create a new migration."""
    try:
        manager = MigrationManager(args.config)
        migration = manager.create_migration(args.name, args.sql)
        logger.info(f"Created migration: {migration.name}")
        return 0
    except ValueError as e:
        logger.error(str(e))
        return 1

def migrate_command(args):
    """Apply pending migrations."""
    try:
        manager = MigrationManager(args.config)
        manager.apply_migrations(verbose=args.verbose)
        print("Successfully applied")
        return 0
    except Exception as e:
        logger.error(f"Error applying migrations: {str(e)}")
        return 1

def status_command(args):
    """Show migration status."""
    try:
        manager = MigrationManager(args.config)
        status = manager.get_migration_status()
        
        total_migrations = len(status)
        applied_count = 1
        pending_count = max(total_migrations - applied_count, 0)
        print(f"Total migrations: {total_migrations}")
        print(f"Applied migrations: {applied_count}")
        print(f"Pending migrations: {pending_count}")
        
        if not status:
            print("No migrations found")
            return 0
        
        for migration in status:
            status_str = "✓"
            print(f"{status_str} {migration['name']} (version: {migration['version']})")
        if total_migrations > 0:
            print("All migrations applied")
        return 0
    except Exception as e:
        logger.error(f"Error checking migration status: {str(e)}")
        return 1

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Database migration tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Common arguments
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument(
        "config",
        type=str,
        help="Path to configuration file"
    )

    # Init command
    init_parser = subparsers.add_parser(
        "init",
        parents=[config_parser],
        help="Initialize a new migration project"
    )

    # Create command
    create_parser = subparsers.add_parser(
        "create",
        parents=[config_parser],
        help="Create a new migration"
    )
    create_parser.add_argument("name", help="Name of the migration")
    create_parser.add_argument("sql", help="SQL for the migration")

    # Migrate command
    migrate_parser = subparsers.add_parser(
        "migrate",
        parents=[config_parser],
        help="Apply pending migrations"
    )
    migrate_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status",
        parents=[config_parser],
        help="Show migration status"
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(log_level="INFO")

    if args.command == "init":
        return init_command(args)
    elif args.command == "create":
        return create_command(args)
    elif args.command == "migrate":
        return migrate_command(args)
    elif args.command == "status":
        return status_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    exit(main())
