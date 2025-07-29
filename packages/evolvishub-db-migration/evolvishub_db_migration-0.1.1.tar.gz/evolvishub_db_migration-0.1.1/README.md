# evolvishub-db-migration

## Evolvis AI Database Migration Tool

[![PyPI version](https://badge.fury.io/py/evolvishub-db-migration.svg)](https://badge.fury.io/py/evolvishub-db-migration)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://readthedocs.org/projects/evolvishub-db-migration/badge/?version=latest)](https://evolvishub-db-migration.readthedocs.io)
[![Build Status](https://github.com/evolvisai/evolvishub-db-migration/workflows/Build/badge.svg)](https://github.com/evolvisai/evolvishub-db-migration/actions)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage Status](https://coveralls.io/repos/github/evolvisai/evolvishub-db-migration/badge.svg?branch=main)](https://coveralls.io/github/evolvisai/evolvishub-db-migration?branch=main)

<p align="center">
  <img src="assets/png/eviesales.png" alt="Evolvis AI Logo" width="200">
</p>

## About Evolvis AI

Evolvis AI is your partner in making your company a pioneer and leader in your industry. We are co-creators who continuously collaborate with you in developing our solutions. Our mission is to empower you with the necessary tools to make informed and precise decisions by integrating artificial intelligence into your processes.

### Our Approach

- **Co-creation**: We continuously collaborate with you in developing our solutions
- **Open Source Priority**: We reduce costs and develop robust tools using open-source technologies
- **Transparency**: We keep you informed about progress continuously

## Overview

The Evolvis AI Database Migration Tool is a robust and flexible solution for managing database schema changes across multiple database systems. It provides a comprehensive set of features for database version control, migration management, and rollback capabilities.

## Quick Start

### Command-Line Usage

```bash
# List available migrations
db-migrate --list

# Show migration status
db-migrate --status

# Apply pending migrations
db-migrate --apply

# Apply migrations with verbose output
db-migrate --apply -v
```

## Key Features

- **Multi-Database Support**
  - SQLite
  - PostgreSQL
  - MySQL
  - Microsoft SQL Server

- **Advanced Migration Management**
  - Transaction-based migrations
  - Rollback support
  - Migration tracking
  - Version control

- **Professional Features**
  - Configurable logging
  - Transaction timeout control
  - Retry mechanisms
  - Schema management
  - Character set support

- **Development Tools**
  - Command-line interface
  - Python library API
  - SQLAlchemy integration
  - Testing utilities
  - Documentation support

## Features

- 🚀 Multiple Database Support:
  - SQLite (default)
  - PostgreSQL
  - MySQL
  - Microsoft SQL Server (MSSQL)
- 🔄 Version Control:
  - Migration naming convention (vX_description.sql)
  - Automatic tracking of applied migrations
  - Rollback support
- 📝 Flexible Configuration:
  - File-based SQL migrations
  - Inline SQL migrations in config
  - Custom migration directory support
- 🛠️ Advanced Features:
  - Transaction support
  - Error handling and rollback
  - Migration status tracking
- 📱 Command-line Interface:
  - List migrations
  - Apply migrations
  - Status checking

## Installation

### From PyPI

Install the latest release:

```bash
pip install evolvishub-db-migration
```

### From Source

For development or specific versions:

```bash
# Clone the repository
git clone https://github.com/evolvisai/evolvishub-db-migration.git
cd evolvishub-db-migration

# Install in development mode
pip install -e .

# Or install specific version
pip install git+https://github.com/evolvisai/evolvishub-db-migration.git@v0.1.0
```

## Development

### Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=evolvishub_db_migration

# Run specific test file
pytest tests/unit/test_migration_manager.py
```

### Code Style

The code follows the Black code style:

```bash
# Format code
black src/ tests/

# Check code style
black --check src/ tests/
```

### Documentation

Generate documentation using Sphinx:

```bash
# Build documentation
sphinx-build -b html docs/ docs/_build/

# View documentation
open docs/_build/html/index.html
```

## Contributing

Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:

1. Check the [documentation](https://evolvishub-db-migration.readthedocs.io)
2. Search existing issues
3. Create a new issue if needed

## Contact

- Email: info@evolvis.ai
- Phone: 
  - Spain: +34 666 826 619
  - Mexico: +52 818 706 9624
- Locations:
  - Barcelona, Spain
  - Monterrey, Mexico

## Acknowledgments

- SQLAlchemy for database abstraction
- Alembic for migration inspiration
- All contributors and users

### Configuration

Configure the tool using a `migration.ini` file in your project root:

```ini
[DEFAULT]
# Database Configuration
database_type = sqlite  # sqlite, postgresql, mysql, mssql
connection_string = sqlite:///./database.db
migration_directory = migrations

# Optional Settings
transaction_timeout = 30  # seconds
retry_attempts = 3
log_level = INFO  # DEBUG, INFO, WARNING, ERROR

[MIGRATIONS]
# Inline SQL migrations
v1_create_users_table = CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);

# Rollback SQL (optional)
rollback_v1_create_users_table = DROP TABLE users;
```

### Migration Files

Create SQL files in your migrations directory following the naming convention: `vX_description.sql`

```sql
-- migrations/v2_add_profiles_table.sql
-- Description: Add profiles table with user reference
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- rollback.sql
DROP TABLE profiles;
```

### Running Migrations

List available migrations:
```bash
db-migrate --list
```

Apply pending migrations:
```bash
db-migrate --apply
```

Check migration status:
```bash
db-migrate --status
```

## Migration Best Practices

1. Use descriptive version numbers (v1_, v2_, v3_, etc.)
2. Keep migrations atomic and focused
3. Include rollback SQL in comments
4. Use proper SQL formatting
5. Document complex migrations

## Database Support

### SQLite
```ini
[DEFAULT]
database_type = sqlite
connection_string = sqlite:///./database.db
```

### PostgreSQL
```ini
[DEFAULT]
database_type = postgresql
connection_string = postgresql://user:password@localhost:5432/dbname
```

### MySQL
```ini
[DEFAULT]
database_type = mysql
connection_string = mysql://user:password@localhost:3306/dbname
```

### MSSQL
```ini
[DEFAULT]
database_type = mssql
connection_string = mssql://user:password@localhost:1433/dbname
```

## Development

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run tests
5. Submit a PR

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by database migration tools like Alembic and Flyway
- Special thanks to the SQLAlchemy team for their excellent database toolkit