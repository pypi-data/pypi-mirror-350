from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="heroku-langchain-aisdk",
    version="0.2.1",
    description="A Python SDK for Heroku's Managed Inference API (MIA), providing easy access to AI models through a LangChain-compatible interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "langchain-core>=0.1.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.8",
    author="Heroku",
    author_email="support@heroku.com",
    url="https://github.com/dsouza-anush/heroku-langchain-aisdk",
    project_urls={
        "Bug Tracker": "https://github.com/dsouza-anush/heroku-langchain-aisdk/issues",
        "Documentation": "https://github.com/dsouza-anush/heroku-langchain-aisdk",
        "Source Code": "https://github.com/dsouza-anush/heroku-langchain-aisdk",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="heroku, ai, langchain, inference, chatbot, llm",
) 