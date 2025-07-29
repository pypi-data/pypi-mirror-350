from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="syntera-ai",
    version="0.1.1",
    author="Fouad Mahmoud",
    author_email="fouadmahmoud281@gmail.com",
    description="An AI-powered DevOps toolkit for infrastructure automation and analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fouadmahmoud281/syntera-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "openai>=1.0.0",
        "rich>=13.0.0",
        "typer>=0.9.0",
        "python-dotenv>=1.0.0",
        "boto3>=1.28.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "syntera-ai=devops_ai.cli:app",
        ],
    },
) 
