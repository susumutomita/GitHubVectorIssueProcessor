from setuptools import setup

with open("requirements.txt", "r") as f:
    required_packages = f.read().splitlines()

setup(
    name="GitHubVectorIssueProcessor",
    version="1.0.0",
    version="0.1",
    packages=[
        "src",
    ],
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "github-vector-issue-processor=main:main",
        ],
    },
)
