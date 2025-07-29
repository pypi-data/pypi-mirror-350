"""
Configuration of the logging behavior. I used AI to create parts of this code.
"""

import logging
from datetime import datetime
from pathlib import Path

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_console_format = "%(levelname)s:%(message)s"

default_session_name = f"session_{datetime.today().ctime()}"
default_session_name = default_session_name.replace(" ", "_").replace(":", "_")

level_name = {
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL",
}


def get_file_handler(handler_name: str, level: int):
    file_handler = logging.FileHandler(handler_name)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler(level: int):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(_console_format))
    return stream_handler


def get_standard_logger(session_name: str = default_session_name, stream_level: int = logging.INFO):
    """
    Returns a custom logger named 'Scheduler logger' with separate file and console handlers.
    This logger is independent of the root logger so that calls like logging.warning() do not use these settings.
    """
    # Create a dedicated logger
    logger = logging.getLogger("Scheduler logger")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # prevent log messages from being passed to the root logger

    # Clear any existing handlers (if reconfiguring)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a session-specific directory for log files
    base_path = Path(__file__).resolve().parent / "logs"
    session_path = base_path / session_name

    # Create the session_path directory if it doesn't exist
    try:
        session_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.exception("Could not create log directory. Logs may not be saved.")

    # Set up file handlers for each logging level
    for level, name in level_name.items():
        file_name = session_path / f"{session_name}_{name}.log"
        logger.addHandler(get_file_handler(file_name.as_posix(), level))

    # Add stream (console) handler with the desired level and format
    logger.addHandler(get_stream_handler(stream_level))
    return logger


# Create a module-level logger that can be imported as StandardLogger
scheduler_logger = get_standard_logger()

# Optionally, define __all__ to restrict module exports
__all__ = ["get_standard_logger", "scheduler_logger"]


if __name__ == "__main__":
    test_logger = scheduler_logger
    test_logger.debug("Hello World")
    test_logger.info("the end is near")
    test_logger.warning("please prepare for the end!")
    test_logger.exception("Goodbye cruel world :-(")
