import openai


class OpenAIModel:
    def __init__(self, client: openai.Client):
        self.client = client

    def create_embedding(self, text: str):
        result = self.client.embeddings.create(
            input=[text], model="text-embedding-3-small"
        )
        return result.data[0].embedding


class AzureOpenAIModel:
    def __init__(self, azure_client):
        self.client = azure_client

    def create_embedding(self, text: str):
        response = self.client.embeddings.create(
            input=[text], model="text-embedding-3-small"
        )
        return response["data"][0]["embedding"]


def load_local_model(model_path: str):
    # ローカルモデルのロード処理を実装
    # ここでは仮の実装を示します
    class MockModel:
        def encode(self, text: str):
            return [0.0] * 512  # ダミーのベクトルを返す

    return MockModel()


class LocalModel:
    def __init__(self, model_path: str):
        self.model = load_local_model(model_path)

    def create_embedding(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()
