"""
Logging utilities for the DevOps MCP Server.
"""
import logging
import sys
from config.settings import LOG_LEVEL, LOG_FORMAT


def setup_logger(name, level=None):
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: The name of the logger
        level: The logging level (default: from settings)
        
    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level from parameter or settings
    level = level or getattr(logging, LOG_LEVEL)
    logger.setLevel(level)
    
    # Create handler if not already set up
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    
    return logger


# Create a default logger for the server
logger = setup_logger("devops_mcp_server")


def log_exception(logger, exc, message=None):
    """
    Log an exception with an optional message.
    
    Args:
        logger: The logger to use
        exc: The exception to log
        message: An optional message to include
    """
    if message:
        logger.error(f"{message}: {str(exc)}")
    else:
        logger.error(str(exc))
    
    # Log the stack trace at debug level
    logger.debug("Exception details:", exc_info=exc)


def log_request(logger, method, params=None):
    """
    Log an incoming request.
    
    Args:
        logger: The logger to use
        method: The request method
        params: The request parameters
    """
    if params:
        logger.debug(f"Received request: {method} with params: {params}")
    else:
        logger.debug(f"Received request: {method}")


def log_response(logger, method, result=None, error=None):
    """
    Log an outgoing response.
    
    Args:
        logger: The logger to use
        method: The request method
        result: The response result
        error: The response error
    """
    if error:
        logger.debug(f"Sending error response for {method}: {error}")
    elif result:
        logger.debug(f"Sending successful response for {method}")
    else:
        logger.debug(f"Sending empty response for {method}")