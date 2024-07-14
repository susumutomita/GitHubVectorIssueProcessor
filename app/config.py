"""
This module contains common utilities for loading and validating environment variables.
"""

import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_env(env_file=".env"):
    """
    Load environment variables from a .env file.
    """
    if os.path.exists(env_file):
        load_dotenv(env_file)


def get_env_var(var_name, default=None, required=True):
    """
    Get an environment variable's value, with optional default and required flag.

    Args:
        var_name (str): The name of the environment variable.
        default (any): The default value if the environment variable is not set.
        required (bool): Whether the environment variable is required.

    Returns:
        any: The value of the environment variable.

    Raises:
        ValueError: If a required environment variable is not set.
    """
    value = os.getenv(var_name, default)
    if required and value is None:
        logger.error("Missing required environment variable: %s", var_name)
        raise ValueError(f"Missing required environment variable: {var_name}")
    if value is not None:
        logger.info("Environment variable %s loaded successfully.", var_name)
    return value
