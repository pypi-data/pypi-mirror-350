# EvolvisHub DB Migration

A robust database migration tool developed by [Evolvis AI](https://evolvis.ai) for managing database schema changes efficiently and reliably.

## About Evolvis AI

[Evolvis AI](https://evolvis.ai) is a leading provider of AI-powered solutions, helping businesses transform their operations through innovative technology. Our mission is to make artificial intelligence accessible to companies of all sizes, enabling them to compete effectively in today's data-driven environment.

## Author

**Alban Maxhuni, PhD**  
Email: [a.maxhuni@evolvis.ai](mailto:a.maxhuni@evolvis.ai)  
Senior Software Engineer at Evolvis AI

## Features

- Support for multiple database types (SQLite, PostgreSQL, MySQL)
- Version-controlled migrations
- Rollback capability
- Migration status tracking
- Command-line interface
- Configuration management
- Logging and error handling

## Installation

```bash
pip install evolvishub-db-migration
```

## Usage

### Initialize a new migration project

```bash
db-migrate init config.yaml
```

### Create a new migration

```bash
db-migrate create config.yaml my_migration "CREATE TABLE my_table (id INTEGER PRIMARY KEY)"
```

### Apply migrations

```bash
db-migrate migrate config.yaml
```

### Check migration status

```bash
db-migrate status config.yaml
```

Example output:
```
Total migrations: 1
Applied migrations: 1
Pending migrations: 0
✓ 001_my_migration (version: 001)
All migrations applied
```

## Configuration

The configuration file (`config.yaml`) should have the following structure:

```yaml
database:
  type: sqlite
  connection_string: sqlite:///database.db

migrations:
  directory: migrations
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/evolvis-ai/evolvishub-db-migration.git
cd evolvishub-db-migration
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact [a.maxhuni@evolvis.ai](mailto:a.maxhuni@evolvis.ai) or visit [Evolvis AI](https://evolvis.ai).

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the Evolvis AI team for their support and guidance