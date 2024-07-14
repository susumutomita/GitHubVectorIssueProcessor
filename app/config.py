"""
This module contains common utilities for loading and validating environment variables.
"""

import os

from dotenv import load_dotenv


def load_env(env_file=".env"):
    """
    Load environment variables from a .env file.
    """
    if os.path.exists(env_file):
        load_dotenv(env_file)


def get_env_var(var_name, default=None, required=True, log=True):
    """
    Get an environment variable's value, with optional default and required flag.

    Args:
        var_name (str): The name of the environment variable.
        default (any): The default value if the environment variable is not set.
        required (bool): Whether the environment variable is required.
        log (bool): Whether to log the success or failure of retrieving the variable.

    Returns:
        any: The value of the environment variable.

    Raises:
        ValueError: If a required environment variable is not set.
    """
    value = os.getenv(var_name, default)
    if required and value is None:
        if log:
            print(f"Environment variable {var_name} is missing or empty.")
        raise ValueError(f"Missing required environment variable: {var_name}")
    if log:
        print(f"Environment variable {var_name} loaded successfully.")
    return value
