from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vectordbcloud",
    version="1.0.1",  # Major version bump for 100% ECP-native implementation
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pydantic==1.10.8",  # Exact version for compatibility
        "fireducks>=1.2.5",  # High-performance data processing
        "typing-extensions>=4.0.0",
        "aiohttp>=3.8.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "urllib3>=1.26.0",
        "certifi>=2022.0.0",
        "charset-normalizer>=2.0.0",
        "idna>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.991",
            "flake8>=5.0.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "performance": [
            "fireducks>=1.2.5",
            "falcon>=3.1.1",
            "uvloop>=0.17.0",
            "orjson>=3.8.0",
        ],
        "all": [
            "fireducks>=1.2.5",
            "falcon>=3.1.1",
            "uvloop>=0.17.0",
            "orjson>=3.8.0",
            "pytest>=7.0.0",
            "sphinx>=5.0.0",
        ],
    },
    author="VectorDBCloud Team",
    author_email="support@vectordbcloud.com",
    description="Official Python SDK for VectorDBCloud - 100% ECP-Native with Fireducks & Falcon API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VectorDBCloud/vectordbcloud-python",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.8",
    keywords=[
        "vectordb",
        "cloud",
        "embeddings",
        "vector-database",
        "ai",
        "machine-learning",
        "ecp",
        "ephemeral-context-protocol",
        "fireducks",
        "falcon-api",
        "high-performance",
        "enterprise",
        "production-ready",
    ],
    project_urls={
        "Bug Reports": "https://github.com/VectorDBCloud/vectordbcloud-python/issues",
        "Source": "https://github.com/VectorDBCloud/vectordbcloud-python",
        "Documentation": "https://docs.vectordbcloud.com",
        "Homepage": "https://vectordbcloud.com",
        "API Reference": "https://api.vectordbcloud.com/docs",
    },
)




