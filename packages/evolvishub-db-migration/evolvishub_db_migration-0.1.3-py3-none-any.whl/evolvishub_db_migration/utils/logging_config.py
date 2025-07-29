import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any

class LoggingConfig:
    """Configuration class for managing logging in the application."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(LoggingConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logging configuration if not already initialized."""
        if not self._initialized:
            self._logger = None
            self._handlers: Dict[str, logging.Handler] = {}
            self._formatter = None
            self._log_level = logging.INFO
            self._initialized = True
    
    def setup(
        self,
        log_level: str = "INFO",
        log_file: Optional[Path] = None,
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ) -> logging.Logger:
        """
        Set up logging configuration for the application.
        
        Args:
            log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional path to log file. If None, logs to stdout
            log_format: Format string for log messages
            
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logger
        self._logger = logging.getLogger("evolvishub_db_migration")
        self._log_level = getattr(logging, log_level.upper())
        self._logger.setLevel(self._log_level)

        # Create formatter
        self._formatter = logging.Formatter(log_format)

        # Clear existing handlers
        self._logger.handlers.clear()
        self._handlers.clear()

        # Add file handler if log file is specified
        if log_file:
            self._add_file_handler(log_file)

        # Add console handler
        self._add_console_handler()

        return self._logger

    def _add_file_handler(self, log_file: Path) -> None:
        """Add a file handler to the logger."""
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(self._formatter)
        self._logger.addHandler(file_handler)
        self._handlers['file'] = file_handler

    def _add_console_handler(self) -> None:
        """Add a console handler to the logger."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._formatter)
        self._logger.addHandler(console_handler)
        self._handlers['console'] = console_handler

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: The name of the module requesting the logger
            
        Returns:
            logging.Logger: Logger instance for the specified module
        """
        if not self._logger:
            self.setup()  # Setup with default values if not already configured
        return logging.getLogger(f"evolvishub_db_migration.{name}")

    def update_log_level(self, log_level: str) -> None:
        """
        Update the log level for all handlers.
        
        Args:
            log_level: The new logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._log_level = getattr(logging, log_level.upper())
        if self._logger:
            self._logger.setLevel(self._log_level)

    def get_current_config(self) -> Dict[str, Any]:
        """
        Get the current logging configuration.
        
        Returns:
            Dict[str, Any]: Current logging configuration
        """
        return {
            'log_level': logging.getLevelName(self._log_level),
            'handlers': list(self._handlers.keys()),
            'formatter': self._formatter._fmt if self._formatter else None
        }

# Create a singleton instance
logging_config = LoggingConfig()

# Convenience functions for backward compatibility
def setup_logging(*args, **kwargs) -> logging.Logger:
    """Convenience function to setup logging."""
    return logging_config.setup(*args, **kwargs)

def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger."""
    return logging_config.get_logger(name) 