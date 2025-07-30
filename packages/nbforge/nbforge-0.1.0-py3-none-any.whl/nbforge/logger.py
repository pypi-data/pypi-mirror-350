import logging


def setup_logger(name: str = "nbforge"):
    """
    Sets up and returns a logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s : %(module)s : %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
