from setuptools import find_packages, setup

setup(
    name="GitHubVectorIssueProcessor",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask==1.1.2",
        "flask-cors==3.0.10",
        "psycopg2-binary==2.8.6",
        "openai==0.5.0",
        "qdrant-client==0.9.0",
        "python-dotenv==0.15.0",
        "regex==2021.4.4",
        "PyGithub==1.55",
    ],
    entry_points={
        "console_scripts": [
            "github-vector-issue-processor=main:main",
        ],
    },
)
