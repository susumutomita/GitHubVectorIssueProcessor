[![ci](https://github.com/susumutomita/GitHubVectorIssueProcessor/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/susumutomita/GitHubVectorIssueProcessor/actions/workflows/ci.yml)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/susumutomita/GitHubVectorIssueProcessor)
![GitHub top language](https://img.shields.io/github/languages/top/susumutomita/GitHubVectorIssueProcessor)
![GitHub pull requests](https://img.shields.io/github/issues-pr/susumutomita/GitHubVectorIssueProcessor)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/susumutomita/GitHubVectorIssueProcessor)
![GitHub repo size](https://img.shields.io/github/repo-size/susumutomita/GitHubVectorIssueProcessor)

# GitHubVectorIssueProcessor

This action provides the following functionality for GitHub Actions users:

- GitHubVectorIssueProcessor is a tool for processing GitHub issues using vector databases and AI models.
- AI reviews your issue and marks it as duplicated if a similar issue already exists.

## Usage

See [action.yml](action.yml)

<!-- start usage -->
```yaml
name: Issue Review

on:
  issues:
    types: [opened]
  workflow_dispatch:

permissions:
  issues: write
  contents: read

jobs:
  review_issue:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Review Issue with LLM
        uses: susumutomita/GitHubVectorIssueProcessor@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          qd-url: ${{ secrets.QD_URL }}
          qd-api-key: ${{ secrets.QD_API_KEY }}
          groq-api-key: ${{ secrets.GROQ_API_KEY }}
          nomic-api-key: ${{ secrets.NOMIC_API_KEY }}
          github-event-issue-number: ${{ github.event.issue.number }}
          github-repository: ${{ github.repository }}
```
<!-- end usage -->

## Main Use Case

The primary use case of GitHubVectorIssueProcessor is to automate the management of GitHub issues. This includes automatically labeling and closing issues based on content moderation, as well as searching for similar issues to avoid duplicates. By leveraging vector databases and advanced AI models, this tool enhances the efficiency and accuracy of issue management.

## Why These Technologies

1. **Vector Databases**: Vector databases allow for efficient similarity search, which is crucial for identifying duplicate issues. By storing issue content as high-dimensional vectors, we can quickly find and compare similar issues.

2. **AI Models**: AI models enable advanced content analysis, such as identifying inappropriate content and generating embeddings for vector search. The flexibility to use different AI models (OpenAI, Azure OpenAI, local models currently support Groq because everything is free so to start it it is reasonable) ensures that the tool can be tailored to various enterprise needs and resource availability.

## Getting API Keys

To use GitHubVectorIssueProcessor, you need to obtain API keys for the following services:

1. **Groq API Key**:
   - Sign up or log in to [Groq](https://groq.com).
   - Navigate to the API section in your account settings.
   - Generate a new API key.

2. **Qdrant API Key and URL**:
   - Sign up or log in to [Qdrant](https://qdrant.tech).
   - Navigate to the API section in your account settings.
   - Generate a new API key and obtain the URL of your Qdrant instance.

3. **Nomic API Key**:
   - Sign up or log in to [Nomic](https://nomic.ai).
   - Navigate to the API section in your account settings.
   - Generate a new API key.

## Installation

### Prerequisites

- Python 3.8+
- pip
- Node.js

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/susumutomita/GitHubVectorIssueProcessor.git
    cd GitHubVectorIssueProcessor
    ```

2. Set up your environment variables:

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

3. Install dependencies:

    ```bash
    make install
    ```

4. To process GitHub issues, run the following command:

    ```bash
    make run
    ```

To run tests:

    ```bash
    make test
    ```

## Supported Vector Databases

- Qdrant
- PostgreSQL (local) (future plan)
- Azure AI search (future plan)

## Supported AI Models

- OpenAI (future plan)
- Azure OpenAI (future plan)
- Groq
- Local models (e.g., Llama3) (future plan)

## Inspiration

This project was inspired by [takahiroanno2024/election2024](https://github.com/takahiroanno2024/election2024), which demonstrated the power of vector databases and AI in processing and analyzing large datasets.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The inspiration for this project, [takahiroanno2024/election2024](https://github.com/takahiroanno2024/election2024), is licensed under the Attribution 4.0 International (CC BY 4.0) License. The full text of this license is included in the [CC_BY_LICENSE](CC_BY_LICENSE) file.

## Contributions

Contributions are welcome. See our [Contributor's Guide](docs/contributors.md).
