import regex as re


class ContentModerator:
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def validate_image(self, text):
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
        except:
            return True

    def judge_violation(self, text):
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
        except:
            return True

    @staticmethod
    def _extract_image_url(text):
        match = re.search(r"!\[[^\s]+\]\((https://[^\s]+)\)", text)
        return match[1] if match and len(match) > 1 else ""
