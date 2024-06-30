![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/susumutomita/GitHubVectorIssueProcessor)
![GitHub top language](https://img.shields.io/github/languages/top/susumutomita/GitHubVectorIssueProcessor)
![GitHub pull requests](https://img.shields.io/github/issues-pr/susumutomita/GitHubVectorIssueProcessor)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/susumutomita/GitHubVectorIssueProcessor)
![GitHub repo size](https://img.shields.io/github/repo-size/susumutomita/GitHubVectorIssueProcessor)

# GitHubVectorIssueProcessor

GitHubVectorIssueProcessor is a tool for processing GitHub issues using vector databases and AI models. It supports multiple vector databases and AI models, making it flexible and adaptable for various use cases.

## Main Use Case

The primary use case of GitHubVectorIssueProcessor is to automate the management of GitHub issues. This includes automatically labeling and closing issues based on content moderation, as well as searching for similar issues to avoid duplicates. By leveraging vector databases and advanced AI models, this tool enhances the efficiency and accuracy of issue management.

## Why These Technologies

1. **Vector Databases**: Vector databases allow for efficient similarity search, which is crucial for identifying duplicate issues. By storing issue content as high-dimensional vectors, we can quickly find and compare similar issues.

2. **AI Models**: AI models enable advanced content analysis, such as identifying inappropriate content and generating embeddings for vector search. The flexibility to use different AI models (OpenAI, Azure OpenAI, local models) ensures that the tool can be tailored to various enterprise needs and resource availability.

## Code Structure

```structure.txt
GitHubVectorIssueProcessor/
├── .github/
│   ├── workflows/
│   │   └── main.yml  # GitHub Actionsのワークフロー定義
├── src/
│   ├── handlers/
│   │   ├── qdrant_handler.py  # Qdrantハンドラー
│   │   ├── pgvector_handler.py  # PostgreSQLハンドラー
│   │   └── embedding_models.py  # AIモデルのハンドラー
│   ├── config.py  # 設定クラス
│   ├── github_handler.py  # GitHubハンドラー
│   ├── content_moderator.py  # コンテンツモデレータ
│   ├── issue_processor.py  # Issueプロセッサ
│   └── main.py  # メインエントリーポイント
├── .env.example  # 環境変数のサンプルファイル
├── .gitignore  # Gitの無視ファイル
├── LICENSE  # ライセンスファイル
├── README.md  # 説明ファイル
├── requirements.txt  # 依存関係
└── setup.py  # パッケージ設定

```

## Installation

### Prerequisites

- Python 3.8+
- pip
- Docker (for Qdrant and local testing)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/susumutomita/GitHubVectorIssueProcessor.git
    cd GitHubVectorIssueProcessor
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:

    Create a `.env` file in the root directory and add the following variables:

    ```plaintext
    GITHUB_TOKEN=your_github_token
    QD_API_KEY=your_qdrant_api_key
    QD_URL=your_qdrant_url
    DB_CONNECTION_STR=your_postgresql_connection_string
    GITHUB_REPOSITORY=your_github_repository
    GITHUB_EVENT_ISSUE_NUMBER=your_github_issue_number
    AI_MODEL_TYPE=openai|azure|local
    OPENAI_API_KEY=your_openai_api_key
    AZURE_API_KEY=your_azure_api_key
    LOCAL_MODEL_PATH=path_to_your_local_model
    ```

## Usage

1. To process GitHub issues, run the following command:

    ```bash
    python main.py
    ```

2. You can configure the tool to use different vector databases and AI models by setting the appropriate environment variables in the `.env` file.

## Supported Vector Databases

- Qdrant
- PostgreSQL (local)
- Aurora Serverless PostgreSQL

## Supported AI Models

- OpenAI
- Azure OpenAI
- Local models (e.g., Llama3)

## Inspiration

This project was inspired by [takahiroanno2024/election2024](https://github.com/takahiroanno2024/election2024), which demonstrated the power of vector databases and AI in processing and analyzing large datasets.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The inspiration for this project, [takahiroanno2024/election2024](https://github.com/takahiroanno2024/election2024), is licensed under the Attribution 4.0 International (CC BY 4.0) License. The full text of this license is included in the [CC_BY_LICENSE](CC_BY_LICENSE) file.
