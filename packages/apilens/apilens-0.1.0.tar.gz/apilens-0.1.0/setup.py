from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apilens",
    version="0.1.0",
    author="Thousif Md",
    author_email="your.email@example.com",  # Replace with your email
    description="A Python wrapper for various AI language model APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThousifMd/APILens",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "python-dotenv>=1.0.0",
        "google-generativeai>=0.3.0"
    ],
) 