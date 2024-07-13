[![ci](https://github.com/susumutomita/GitHubVectorIssueProcessor/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/susumutomita/GitHubVectorIssueProcessor/actions/workflows/ci.yml)
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

```plaintext
GitHubVectorIssueProcessor/
├── .github/
│   ├── workflows/
│   │   └── ci.yml  # GitHub Actions workflow definition
├── app/
│   ├── __init__.py  # For package initialization
│   ├── config.py  # Configuration class
│   ├── content_moderator.py  # Content Moderator
│   ├── github_handler.py  # GitHub Handler
│   ├── issue_processor.py  # Issue Processor
│   ├── main.py  # Main entry point
│   └── qdrant_handler.py  # Qdrant Handler
├── tests/  # Test files
│   ├── __init__.py  # For package initialization
│   ├── test_config.py  # Tests for Config class
│   ├── test_content_moderator.py  # Tests for ContentModerator class
│   ├── test_github_handler.py  # Tests for GithubHandler class
│   ├── test_issue_processor.py  # Tests for IssueProcessor class
│   └── test_qdrant_handler.py  # Tests for QdrantHandler class
├── .env.example  # Sample environment variables file
├── .gitignore  # Git ignore file
├── LICENSE  # License file
├── README.md  # Documentation file
├── requirements.txt  # Dependencies
├── setup.py  # Package setup
└── Makefile  # Makefile for build and management
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

2. Install dependencies:

    ```bash
    make install
    ```

3. Set up your environment variables:

    Create a `.env` file in the root directory based on the `.env.example` file and add the necessary variables:

    ```plaintext
    # Groq API Key
    GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Qdrant URL and API Key
    QD_URL=https://xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.us-east4-0.gcp.cloud.qdrant.io
    QD_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # GitHub Event Issue Number
    GITHUB_EVENT_ISSUE_NUMBER=7

    # Nomic API Key
    NOMIC_API_KEY=nk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ```

    Replace the placeholder values (`XXXXXXXXXXXX...`) with your actual API keys and relevant information.

## Usage

1. To process GitHub issues, run the following command:

    ```bash
    make run
    ```

2. To run tests:

    ```bash
    make test
    ```

## Supported Vector Databases

- Qdrant
- PostgreSQL (local)
- Azure AI search

## Supported AI Models

- OpenAI
- Azure OpenAI
- Groq
- Local models (e.g., Llama3)

## Inspiration

This project was inspired by [takahiroanno2024/election2024](https://github.com/takahiroanno2024/election2024), which demonstrated the power of vector databases and AI in processing and analyzing large datasets.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The inspiration for this project, [takahiroanno2024/election2024](https://github.com/takahiroanno2024/election2024), is licensed under the Attribution 4.0 International (CC BY 4.0) License. The full text of this license is included in the [CC_BY_LICENSE](CC_BY_LICENSE) file.
