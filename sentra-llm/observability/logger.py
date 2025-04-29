import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logger():
    logger = logging.getLogger("SentraLLM")
    logger.setLevel(LOG_LEVEL)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
