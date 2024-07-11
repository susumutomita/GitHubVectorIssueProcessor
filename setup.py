from setuptools import setup

setup(
    name="GitHubVectorIssueProcessor",
    version="1.0.0",
    entry_points={
        "console_scripts": [
            "github-vector-issue-processor=app.main:main",
        ],
    },
)
