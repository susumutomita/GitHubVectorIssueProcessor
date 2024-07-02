import re

import openai


class ContentModerator:
    def __init__(self, openai_client: openai.Client):
        self.openai_client = openai_client

    # src/content_moderator.py
    def validate_image(self, text: str):
        image_url = self._extract_image_url(text)
        if not image_url:
            return False

        prompt = "この画像が暴力的、もしくは性的な画像の場合trueと返してください。"
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
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
        except Exception as e:
            print(f"Error during image validation: {e}")
            return True

    def judge_violation(self, text: str):
        response = self.openai_client.moderations.create(input=text)
        return response.results[0].flagged or self.validate_image(text)

    @staticmethod
    def _extract_image_url(text: str):
        match = re.search(r"!\[[^\s]+\]\((https://[^\s]+)\)", text)
        return match[1] if match and len(match) > 1 else ""
