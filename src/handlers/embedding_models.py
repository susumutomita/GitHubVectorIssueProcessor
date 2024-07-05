from groq import Groq


class GroqModel:
    def __init__(self, client: Groq):
        self.client = client

    def create_embedding(self, text: str):
        chat_history = [
            {
                "role": "system",
                "content": "あなたは便利なアシスタントです。テキストの埋め込みを生成してください。",
            },
            {"role": "user", "content": text},
        ]
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=chat_history,
            max_tokens=100,
            temperature=1.2,
        )
        # Assuming the response contains the embedding in a field named 'embedding'
        # return response.choices[0].message.content
        return [0.0] * 512
