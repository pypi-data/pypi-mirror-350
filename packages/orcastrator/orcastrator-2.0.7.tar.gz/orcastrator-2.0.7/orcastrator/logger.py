import logging
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Set

# Define log levels with their numeric values for reference
# DEBUG = 10 - Detailed information, typically of interest only when diagnosing problems
# INFO = 20 - Confirmation that things are working as expected
# WARNING = 30 - An indication that something unexpected happened, but the program still works
# ERROR = 40 - Due to a more serious problem, the program has not been able to perform a function
# CRITICAL = 50 - A serious error, indicating that the program itself may be unable to continue running

# Global variables to track logger state
_logger = None
_context_store = threading.local()
_file_handlers: Set[str] = set()  # Track handlers by log file path


def get_logger(name: str = "orcastrator") -> logging.Logger:
    """Get the orcastrator logger instance.

    Args:
        name: Logger name, defaults to 'orcastrator'

    Returns:
        The configured logger instance
    """
    global _logger
    if _logger is not None:
        return _logger

    # Create logger
    logger = logging.getLogger(name)

    # Important: prevent propagation to avoid duplicate logs
    logger.propagate = False

    # Reset handlers to avoid duplicates if this gets called multiple times
    while logger.handlers:
        logger.handlers[0].close()
        logger.removeHandler(logger.handlers[0])

    # Console handler (for standard output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    _logger = logger
    return logger


def set_context(
    molecule: Optional[str] = None, step: Optional[str] = None
) -> Dict[str, str]:
    """Set logging context for the current thread.

    Args:
        molecule: Name of the molecule being processed
        step: Name of the calculation step

    Returns:
        Dictionary with the current context
    """
    if not hasattr(_context_store, "context"):
        _context_store.context = {}

    # Update only non-None values
    if molecule is not None:
        _context_store.context["molecule"] = molecule
    if step is not None:
        _context_store.context["step"] = step

    return _context_store.context


def clear_context() -> None:
    """Clear the current thread's logging context."""
    if hasattr(_context_store, "context"):
        _context_store.context = {}


def get_context() -> Dict[str, str]:
    """Get the current thread's logging context."""
    if not hasattr(_context_store, "context"):
        _context_store.context = {}
    return _context_store.context


def format_with_context(msg: str) -> str:
    """Format message with current context information."""
    context = get_context()
    context_parts = []

    if "molecule" in context:
        context_parts.append(f"{context['molecule']}")
    if "step" in context and "molecule" in context:
        context_parts.append(f"{context['step']}")

    if not context_parts:
        return msg

    return f"[{' | '.join(context_parts)}] {msg}"


def setup_file_logging(
    log_dir: Optional[Path] = None, log_level: int = logging.DEBUG
) -> None:
    """Set up file logging with detailed output.

    Args:
        log_dir: Directory to store log files. If None, logs are stored in ./logs/
        log_level: Logging level for file output (default: DEBUG)
    """
    global _file_handlers
    logger = get_logger()

    if log_dir is None:
        log_dir = Path("logs")

    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f"orcastrator-{timestamp}.log"
    log_file_path = str(log_file)

    # Skip if we've already added a handler for this file
    if log_file_path in _file_handlers:
        return

    # File handler (for detailed logs)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(threadName)-12s | %(module)s:%(funcName)s:%(lineno)d - %(message)s"
    )

    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    _file_handlers.add(log_file_path)

    # Don't change the global logger level based on file logging
    # This keeps console output at INFO by default
    debug(f"File logging initialized: {log_file}")


def set_log_level(level: int, console_only: bool = False) -> None:
    """Set the log level for the orcastrator logger.

    Args:
        level: Logging level (use logging.DEBUG, logging.INFO, etc.)
        console_only: If True, only sets console handler level, not file handler
    """
    logger = get_logger()

    if not console_only:
        logger.setLevel(level)

    # Update handler levels for console
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and not isinstance(
            handler, logging.FileHandler
        ):
            handler.setLevel(level)

    debug(f"Log level set to: {level}")


def debug(msg: str, *args, **kwargs) -> None:
    """Log a debug message with context."""
    get_logger().debug(format_with_context(msg), *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    """Log an info message with context."""
    get_logger().info(format_with_context(msg), *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    """Log a warning message with context."""
    get_logger().warning(format_with_context(msg), *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    """Log an error message with context."""
    get_logger().error(format_with_context(msg), *args, **kwargs)


def critical(msg: str, *args, **kwargs) -> None:
    """Log a critical message with context."""
    get_logger().critical(format_with_context(msg), *args, **kwargs)


def exception(msg: str, *args, **kwargs) -> None:
    """Log an exception message with traceback and context."""
    get_logger().exception(format_with_context(msg), *args, **kwargs)


def configure_from_config(config: dict) -> None:
    """Configure logging based on configuration dictionary.

    Args:
        config: Configuration dictionary
    """
    # Set console log level based on debug flag
    if config.get("main", {}).get("debug", False):
        set_log_level(logging.DEBUG, console_only=False)
        debug("Debug logging enabled from configuration")
    else:
        set_log_level(logging.INFO, console_only=False)
        debug("Standard logging level set (debug disabled)")
