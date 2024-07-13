"""
This module contains the ContentModerator class, which is responsible for moderating content by
validating images and judging text violations using the Groq client.
"""

import regex as re
from requests.exceptions import RequestException


class ContentModerator:
    """
    A class to moderate content by validating images and judging text violations.

    Attributes:
        groq_client (Groq): An instance of the Groq client.
    """

    def __init__(self, groq_client):
        """
        Initialize the ContentModerator with the given Groq client.

        Args:
            groq_client (Groq): An instance of the Groq client.
        """
        self.groq_client = groq_client

    def validate_image(self, text):
        """
        Validate if the image in the text is inappropriate.

        Args:
            text (str): The text content containing the image URL.

        Returns:
            bool: True if the image is inappropriate, False otherwise.
        """
        image_url = self._extract_image_url(text)
        if not image_url:
            return False

        prompt = "この画像が暴力的、もしくは性的な画像の場合trueと返してください。"
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
                max_tokens=1200,
            )
            return "true" in response.choices[0].message.content.lower()
        except RequestException:
            return True

    def judge_violation(self, text):
        """
        Judge if the text content contains inappropriate material.

        Args:
            text (str): The text content to judge.

        Returns:
            bool: True if the text contains inappropriate material, False otherwise.
        """
        prompt = "このテキストが不適切な内容を含む場合trueと返してください。"
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": text},
                ],
                max_tokens=1200,
            )
            return "true" in response.choices[0].message.content.lower()
        except RequestException:
            return True

    @staticmethod
    def _extract_image_url(text):
        """
        Extract the image URL from the given text.

        Args:
            text (str): The text content containing the image URL.

        Returns:
            str: The extracted image URL or an empty string if not found.
        """
        match = re.search(r"!\[[^\s]+\]\((https://[^\s]+)\)", text)
        return match[1] if match and len(match) > 1 else ""
