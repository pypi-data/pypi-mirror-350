import logging
import os
import uuid
import threading
import functools
from typing import Callable, Optional

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# Thread-local storage for UUID identifiers
_thread_local = threading.local()


def _get_or_create_uuid() -> str:
    """
    Internal function to get the UUID for the current thread or create a new one if it doesn't exist.

    Returns:
        str: The UUID for the current thread.
    """
    if not hasattr(_thread_local, "uuid"):
        _thread_local.uuid = str(uuid.uuid4())
    return _thread_local.uuid


def generate_new_uuid() -> str:
    """
    Generate a new UUID for the current thread context and return it.
    This is useful when starting a new logical operation that should have its own trace ID.

    Returns:
        str: The new UUID generated for the thread.
    """
    _thread_local.uuid = str(uuid.uuid4())
    return _thread_local.uuid


def with_logging_context(
    func: Optional[Callable] = None, *, new_context: bool = False
) -> Callable:
    """
    Decorator that sets up a logging context with a UUID.

    Args:
        func: The function to decorate.
        new_context: If True, create a new UUID for this function call, otherwise use the existing one.

    Returns:
        The decorated function.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if new_context:
                # Generate a new UUID for this function call
                generate_new_uuid()

            # Execute the function with the UUID already in context for logging
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log any uncaught exceptions with the UUID (via logger adapter)
                sdk_logger.error(f"Exception in {func.__name__}: {str(e)}")
                raise

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


class UUIDLoggerAdapter(logging.LoggerAdapter):
    """
    Adapter for adding UUID identifier to log messages automatically.
    The UUID is transparently added to each log message without exposing it to the code using the logger.
    """

    def process(self, msg, kwargs):
        # Get current UUID or generate new one
        current_uuid = _get_or_create_uuid()
        return f"[{current_uuid}] {msg}", kwargs

    # Override all the logging methods to ensure the adapter is used correctly
    def debug(self, msg, *args, **kwargs):
        super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        super().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        super().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        super().critical(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        super().exception(msg, *args, exc_info=exc_info, **kwargs)


def setup_logger(name: str, log_level: str = "info") -> UUIDLoggerAdapter:
    """
    Sets up the logger for the SDK with configurable log levels and UUID tracking.
    The UUID is automatically included in log messages without requiring any code change.

    Args:
        name: The name of the logger (usually the module name)
        log_level: The log level to set. Can be 'debug', 'info', 'warning', 'error', or 'critical'.

    Returns:
        logger instance with UUID tracking
    """
    log_level = LOG_LEVELS.get(log_level.lower(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Check if the logger already has handlers to avoid duplicates
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        # Modified format to include thread name which helps with multi-threading
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    # Wrap the logger with UUID adapter - UUID is added automatically to every log message
    return UUIDLoggerAdapter(logger, {})


# Create the main SDK logger - all logging will automatically include the UUID
sdk_logger = setup_logger("splore_sdk", log_level=os.getenv("SDK_LOG_LEVEL", "info"))
