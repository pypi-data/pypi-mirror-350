import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class Utils:
    """Utility class for common operations in the database migration tool."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Utils, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the utility class if not already initialized."""
        if not self._initialized:
            self._initialized = True
    
    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate a timestamp string in the format YYYYMMDDHHMMSS.
        
        Returns:
            str: Timestamp string
        """
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Sanitize a string to be used as a filename.
        
        Args:
            name: The string to sanitize
            
        Returns:
            str: Sanitized filename
        """
        # Replace invalid characters with underscores
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip('. ')
        return sanitized
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            path: Path to the directory
            
        Returns:
            Path: Path object for the directory
        """
        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Get the extension of a file.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: File extension (including the dot)
        """
        return os.path.splitext(filename)[1]
    
    @staticmethod
    def is_valid_sql_file(filename: str) -> bool:
        """
        Check if a file is a valid SQL file.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            bool: True if the file is a valid SQL file
        """
        return filename.lower().endswith('.sql')
    
    @staticmethod
    def parse_migration_filename(filename: str) -> Dict[str, str]:
        """
        Parse a migration filename into its components.
        
        Args:
            filename: Name of the migration file
            
        Returns:
            Dict[str, str]: Dictionary containing version and name
        """
        match = re.match(r'^(\d+)_(.+)\.sql$', filename)
        if not match:
            raise ValueError(f"Invalid migration filename format: {filename}")
        return {
            'version': match.group(1),
            'name': match.group(2)
        }
    
    @staticmethod
    def format_migration_filename(version: str, name: str) -> str:
        """
        Format a migration filename from its components.
        
        Args:
            version: Version string
            name: Name of the migration
            
        Returns:
            str: Formatted filename
        """
        return f"{version}_{name}.sql"
    
    @staticmethod
    def read_file_content(file_path: Union[str, Path]) -> str:
        """
        Read the content of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Content of the file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file_content(file_path: Union[str, Path], content: str) -> None:
        """
        Write content to a file.
        
        Args:
            file_path: Path to the file
            content: Content to write
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def get_relative_path(path: Union[str, Path], base_path: Union[str, Path]) -> Path:
        """
        Get the relative path of a file or directory.
        
        Args:
            path: Path to get relative path for
            base_path: Base path to calculate relative path from
            
        Returns:
            Path: Relative path
        """
        return Path(path).relative_to(Path(base_path))

# Create a singleton instance
utils = Utils()

# Convenience functions for backward compatibility
def generate_timestamp() -> str:
    """Convenience function to generate timestamp."""
    return utils.generate_timestamp()

def sanitize_filename(name: str) -> str:
    """Convenience function to sanitize filename."""
    return utils.sanitize_filename(name)

def ensure_directory(path: Union[str, Path]) -> Path:
    """Convenience function to ensure directory exists."""
    return utils.ensure_directory(path)

def get_file_extension(filename: str) -> str:
    """Convenience function to get file extension."""
    return utils.get_file_extension(filename)

def is_valid_sql_file(filename: str) -> bool:
    """Convenience function to check if file is valid SQL."""
    return utils.is_valid_sql_file(filename)

def parse_migration_filename(filename: str) -> Dict[str, str]:
    """Convenience function to parse migration filename."""
    return utils.parse_migration_filename(filename)

def format_migration_filename(version: str, name: str) -> str:
    """Convenience function to format migration filename."""
    return utils.format_migration_filename(version, name)

def read_file_content(file_path: Union[str, Path]) -> str:
    """Convenience function to read file content."""
    return utils.read_file_content(file_path)

def write_file_content(file_path: Union[str, Path], content: str) -> None:
    """Convenience function to write file content."""
    return utils.write_file_content(file_path, content)

def get_relative_path(path: Union[str, Path], base_path: Union[str, Path]) -> Path:
    """Convenience function to get relative path."""
    return utils.get_relative_path(path, base_path) 