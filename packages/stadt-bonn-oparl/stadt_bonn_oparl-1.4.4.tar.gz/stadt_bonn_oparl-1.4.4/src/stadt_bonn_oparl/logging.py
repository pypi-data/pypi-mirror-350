import sys

import logfire
from loguru import logger

# load vars from env
from dotenv import load_dotenv

load_dotenv()

logfire.configure()
logfire.instrument_pydantic()


def configure_logging(verbosity: int):
    """
    Configures the Loguru logger based on the specified verbosity level.

    Removes the default handler and adds a stderr handler with the appropriate
    log level (INFO, DEBUG, or TRACE).

    Args:
        verbosity: An integer representing the desired verbosity level (0-3+).
    """
    logger.remove()  # Remove default handler
    log_level = "WARNING"
    if verbosity == 1:
        log_level = "INFO"
    elif verbosity == 2:
        log_level = "DEBUG"
    elif verbosity >= 3:
        log_level = "TRACE"
    logger.add(sys.stderr, level=log_level)
    logger.debug(f"Log level set to {log_level}")

    logger.configure(handlers=[logfire.loguru_handler()])
