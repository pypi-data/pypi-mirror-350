import argparse
from .core import MigrationManager

def main():
    parser = argparse.ArgumentParser(description='Database Migration Tool')
    parser.add_argument('--config', default='migration.ini', help='Path to configuration file')
    parser.add_argument('--list', action='store_true', help='List all available migrations')
    parser.add_argument('--apply', action='store_true', help='Apply pending migrations')
    parser.add_argument('--status', action='store_true', help='Show migration status')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    try:
        manager = MigrationManager(args.config)
        
        if args.list:
            migrations = manager.load_migrations()
            print("Available migrations:")
            for migration in migrations:
                print(f"- {migration.name} (v{migration.version})")
        elif args.apply:
            manager.apply_migrations(verbose=args.verbose)
            print("Migrations applied successfully")
        elif args.status:
            status = manager.get_migration_status()
            print("Migration Status:")
            print(f"Total migrations: {status['total']}")
            print(f"Applied migrations: {status['applied']}")
            print(f"Pending migrations: {status['pending']}")
            if status['pending'] > 0:
                print("\nPending migrations:")
                for migration in status['pending_migrations']:
                    print(f"- {migration.name} (v{migration.version})")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
