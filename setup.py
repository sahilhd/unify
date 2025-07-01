#!/usr/bin/env python3
"""
Setup script for UniLLM library.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unillm",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Unified API gateway for multiple LLM providers with a single API key",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/unillm",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    keywords="llm, ai, openai, anthropic, gemini, api, gateway, unified",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/unillm/issues",
        "Source": "https://github.com/yourusername/unillm",
        "Documentation": "https://github.com/yourusername/unillm#readme",
    },
) 