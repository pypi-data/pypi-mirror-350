import logging
import sys
from typing import Dict, Any
import re
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('db_migration_tool')

def setup_logger(level: str = 'INFO'):
    """Setup logger with specified level"""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    
    logger.setLevel(numeric_level)
    return logger

def validate_migration_name(name: str) -> bool:
    """Validate migration name format"""
    pattern = r'^v\d+_[a-zA-Z0-9_]+$'
    if not re.match(pattern, name):
        logger.error(f"Invalid migration name format: {name}")
        logger.error("Migration name should follow format: vX_description")
        return False
    return True

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration values"""
    required_keys = ['database_type', 'connection_string', 'migration_directory']
    
    for key in required_keys:
        if key not in config:
            logger.error(f"Missing required configuration: {key}")
            return False
    
    # Validate database type
    supported_databases = ['sqlite', 'postgresql', 'mysql', 'mssql']
    if config['database_type'].lower() not in supported_databases:
        logger.error(f"Unsupported database type: {config['database_type']}")
        logger.error(f"Supported databases: {', '.join(supported_databases)}")
        return False
    
    # Validate connection string
    if not config['connection_string']:
        logger.error("Connection string cannot be empty")
        return False
    
    # Validate migration directory
    if not config['migration_directory']:
        logger.error("Migration directory cannot be empty")
        return False
    
    return True

def parse_version(version: str) -> int:
    """Parse version string from migration name"""
    try:
        return int(version.lstrip('v'))
    except ValueError:
        logger.error(f"Invalid version format: {version}")
        return 0

def format_sql(sql: str) -> str:
    """Format SQL for better readability"""
    return sql.strip().replace('\n', ' ').replace('\t', ' ').strip()
