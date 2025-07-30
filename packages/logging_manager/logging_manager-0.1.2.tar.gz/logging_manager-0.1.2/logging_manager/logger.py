import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str,
    log_file: str = "app.log",
    level: int = logging.INFO,
    dry_run: bool = False,
) -> logging.Logger:
    """
    Sets up a logger that logs to both console and file.

    Args:
        name (str): The name of the logger.
        log_file (str): The log file path.
        level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
        dry_run (bool): If True, logs will include a DRY_RUN prefix.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers if logger is already set up
    if logger.hasHandlers():
        return logger

    # Formatter with optional dry-run prefix
    prefix = "[DRY_RUN] " if dry_run else ""
    formatter = logging.Formatter(f"%(levelname)s - {prefix}%(name)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_action(
    logger: logging.Logger,
    action: str,
    experiment_name: str,
    details: Optional[str] = None,
):
    """
    Logs actions for auditability using the provided logger.

    Args:
        logger (logging.Logger): The logger to use for logging actions.
        action (str): The action performed.
        experiment_name (str): The name of the experiment associated with the action.
        details (Optional[str]): Additional details about the action.
    """
    log_message = f"{action} action performed on {experiment_name}. Details: {details}"
    logger.info(log_message)


def log_progress(logger: logging.Logger, details: Optional[str] = None):
    """
    Logs progress for auditability using the provided logger.

    Args:
        logger (logging.Logger): The logger to use for logging actions.
        details (Optional[str]): Additional details about the progress.
    """
    logger.info(details)


def log_error(
    logger: logging.Logger,
    error_message: str,
    details: Optional[str] = None,
    exc_info: Optional[Exception] = None,
):
    """
    Logs an error for auditability using the provided logger.

    Args:
        logger (logging.Logger): The logger to use for logging errors.
        error_message (str): A brief description of the error.
        details (Optional[str]): Additional details about the error (default: None).
        exc_info (Optional[Exception]): The exception information to include in the log (default: None).
    """
    log_message = f"ERROR: {error_message}. Details: {details}"
    logger.error(log_message, exc_info=exc_info)
