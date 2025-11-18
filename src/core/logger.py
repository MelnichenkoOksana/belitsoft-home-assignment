import logging
import sys


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(name: str = "tests") -> logging.Logger:
    """
    Creates or retrieves a configured logger instance.

    The logger is configured only once per name. Subsequent calls with the same
    name return the existing instance without adding duplicate handlers.

    Logging is directed to stdout, which makes it compatible with CI/CD environments.

    Args:
        name: Logger name (e.g., module, component, or test suite name).

    Returns:
        logging.Logger: A preconfigured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)

    return logger
