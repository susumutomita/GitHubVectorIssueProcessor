from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    required_packages = f.read().splitlines()

setup(
    name="GitHubVectorIssueProcessor",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "github-vector-issue-processor=src.main:main",
        ],
    },
)
