"""Logging and debugging utilities for Clouds Detangler.

Provides centralized logging with file output, console output, and debugging support.
Logs are written to user's home directory under logs/clouds-detangler/
"""

import sys
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import traceback


class DebugLogger:
    """Centralized logging for Clouds Detangler with debugging support."""
    
    def __init__(self, script_name: str, enable_debug: bool = False):
        """Initialize logger for a script.
        
        Args:
            script_name: Name of the script (e.g., 'gather_metadata')
            enable_debug: Enable debug-level logging and breakpoint support
        """
        self.script_name = script_name
        self.enable_debug = enable_debug
        self.logger = None
        self.log_file = None
        self._setup_logging()
    
    def _get_log_directory(self) -> Path:
        """Get the logs directory (Username/logs/clouds-detangler)."""
        # Get user's home directory
        home = Path.home()
        
        # Create logs directory structure
        log_dir = home / "logs" / "clouds-detangler"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        return log_dir
    
    def _setup_logging(self):
        """Set up logging to file and console."""
        # Create logger
        self.logger = logging.getLogger(f"clouds_detangler.{self.script_name}")
        self.logger.setLevel(logging.DEBUG if self.enable_debug else logging.INFO)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create log directory
        log_dir = self._get_log_directory()
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = log_dir / f"{self.script_name}_{timestamp}.log"
        
        # File handler (always debug level)
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler (info or debug based on settings)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if self.enable_debug else logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log startup
        self.logger.info(f"Starting {self.script_name}")
        self.logger.debug(f"Log file: {self.log_file}")
        self.logger.debug(f"Debug mode: {self.enable_debug}")
    
    def debug(self, msg: str, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """Log info message."""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """Log error message."""
        self.logger.error(msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(msg, *args, **kwargs)
    
    def breakpoint(self, label: str = "Breakpoint"):
        """Set a breakpoint for debugging.
        
        Args:
            label: Label for the breakpoint
        """
        if self.enable_debug:
            self.logger.debug(f"BREAKPOINT: {label}")
            self.logger.debug(f"Stack trace:")
            for line in traceback.format_stack()[:-1]:
                self.logger.debug(line.strip())
            
            # Use Python's built-in breakpoint() if available (Python 3.7+)
            try:
                breakpoint()  # This will use pdb or PYTHONBREAKPOINT env var
            except NameError:
                # Fallback for older Python versions
                import pdb
                pdb.set_trace()
    
    def log_function_entry(self, func_name: str, **kwargs):
        """Log function entry with arguments.
        
        Args:
            func_name: Name of the function
            **kwargs: Function arguments to log
        """
        if self.enable_debug:
            args_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            self.logger.debug(f"ENTER {func_name}({args_str})")
    
    def log_function_exit(self, func_name: str, result=None):
        """Log function exit with result.
        
        Args:
            func_name: Name of the function
            result: Return value to log
        """
        if self.enable_debug:
            self.logger.debug(f"EXIT {func_name} -> {result}")
    
    def log_variable(self, var_name: str, value):
        """Log variable value for debugging.
        
        Args:
            var_name: Name of the variable
            value: Value to log
        """
        if self.enable_debug:
            self.logger.debug(f"VAR {var_name} = {value}")
    
    def get_log_file_path(self) -> Path:
        """Get the path to the current log file."""
        return self.log_file
    
    def print_log_location(self):
        """Print log file location to console."""
        print(f"\n📝 Logs written to: {self.log_file}")
        print(f"   View logs with: cat {self.log_file}")
        if os.name == 'nt':  # Windows
            print(f"   Or open in Notepad: notepad {self.log_file}\n")
        else:
            print(f"   Or open with: less {self.log_file}\n")


def setup_logger(script_name: str, debug: bool = False) -> DebugLogger:
    """Set up a logger for a script.
    
    Args:
        script_name: Name of the script
        debug: Enable debug mode
        
    Returns:
        Configured DebugLogger instance
    """
    return DebugLogger(script_name, enable_debug=debug)


def enable_debug_mode():
    """Check if debug mode should be enabled.
    
    Returns True if:
    - Environment variable CLOUDS_DETANGLER_DEBUG is set
    - Command line has --debug flag
    """
    # Check environment variable
    if os.environ.get('CLOUDS_DETANGLER_DEBUG', '').lower() in ('1', 'true', 'yes'):
        return True
    
    # Check command line arguments
    if '--debug' in sys.argv:
        return True
    
    return False


# Example usage in scripts:
"""
from scripts.debug_utils import setup_logger, enable_debug_mode

# At the start of your script
debug = enable_debug_mode()
log = setup_logger('my_script', debug=debug)

# Throughout your code
log.info("Starting process...")
log.debug("This only shows in debug mode")

# Log function entry/exit
log.log_function_entry('process_file', filename='test.txt')
result = process_file('test.txt')
log.log_function_exit('process_file', result=result)

# Set breakpoints
if some_condition:
    log.breakpoint("Checking condition")

# Log variables
log.log_variable('file_count', len(files))

# Exception handling
try:
    risky_operation()
except Exception as e:
    log.exception("Operation failed")
    raise

# At the end
log.print_log_location()
"""
