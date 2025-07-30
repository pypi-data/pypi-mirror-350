import logging


def setup_logger(name: str | None = None) -> logging.Logger:
    """Set up the logger for the module."""
    _logger = logging.getLogger(name)

    if not _logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(logging.DEBUG)
    return _logger


# Set up the logger for the module
logger = setup_logger(__name__)
