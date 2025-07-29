#!/usr/bin/env python3
"""Setup script for the MCP Python Client package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mcp-python-client",
    version="0.1.8",
    description="A reusable Python client for interacting with MCP servers and LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MCP Client Team",
    author_email="email@ling-li.com",
    url="https://github.com/lingster/mcp-python-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[
        "anyio>=4.8.0",
        "litellm>=1.63.14",
        "loguru>=0.7.3",
        "mcp>=0.0.17",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
)
