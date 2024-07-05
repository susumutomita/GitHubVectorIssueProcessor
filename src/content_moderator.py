import re
from groq import Groq


class ContentModerator:
    def __init__(self, client: Groq):
        self.client = client

    def validate_image(self, text: str):
        image_url = self._extract_image_url(text)
        if not image_url:
            return False

        prompt = "この画像が暴力的、もしくは性的な画像の場合trueと返してください。"
        try:
            chat_history = [
                {
                    "role": "system",
                    "content": "あなたは便利なアシスタントです。画像の内容をチェックしてください。",
                },
                {"role": "user", "content": f"画像URL: {image_url}\n{prompt}"},
            ]
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=chat_history,
                max_tokens=100,
                temperature=1.2,
            )
            return "true" in response.choices[0].message.content.lower()
        except Exception as e:
            print(f"Error during image validation: {e}")
            return True

    def judge_violation(self, text: str):
        chat_history = [
            {
                "role": "system",
                "content": "あなたは便利なアシスタントです。テキストの内容をチェックしてください。",
            },
            {"role": "user", "content": text},
        ]
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=chat_history,
            max_tokens=100,
            temperature=1.2,
        )
        return "true" in response.choices[
            0
        ].message.content.lower() or self.validate_image(text)

    @staticmethod
    def _extract_image_url(text: str):
        match = re.search(r"!\[[^\s]+\]\((https://[^\s]+)\)", text)
        return match[1] if match and len(match) > 1 else ""
