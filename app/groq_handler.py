"""
This module contains the GroqHandler class,
which is responsible for interacting with the Groq client.
"""

from groq import Groq

from app.config import get_env_var


class GroqHandler:
    """
    A handler class to manage Groq client interactions.

    Attributes:
        groq_client (Groq): An instance of the Groq client.
    """

    def __init__(self):
        """
        Initialize the GroqHandler with the Groq API key.
        """
        api_key = get_env_var("GROQ_API_KEY")
        self.groq_client = Groq(api_key=api_key)
        print("Environment variable GROQ_API_KEY loaded successfully.")

    def get_client(self):
        """
        Get the Groq client instance.

        Returns:
            Groq: The Groq client instance.
        """
        return self.groq_client

    def validate_groq_client(self):
        """
        Validate the Groq client instance to ensure it is properly initialized.

        Raises:
            ValueError: If the Groq client is not properly initialized.
        """
        if not self.groq_client:
            raise ValueError("Groq client is not properly initialized.")
