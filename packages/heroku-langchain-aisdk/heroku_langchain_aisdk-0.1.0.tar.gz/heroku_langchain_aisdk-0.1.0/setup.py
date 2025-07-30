from setuptools import setup, find_packages

setup(
    name="heroku-langchain-aisdk",
    version="0.1.0",
    description="Heroku MIA SDK for Python",
    packages=find_packages(),
    install_requires=[
        "langchain-core>=0.1.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.8",
    author="Heroku",
    author_email="support@heroku.com",
    url="https://github.com/heroku/heroku-langchain-aisdk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 