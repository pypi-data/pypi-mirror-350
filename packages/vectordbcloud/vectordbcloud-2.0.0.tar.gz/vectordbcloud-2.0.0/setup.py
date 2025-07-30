from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vectordbcloud",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pydantic==1.10.8",
        "fireducks>=1.2.5",
        "typing-extensions>=4.0.0",
        "aiohttp>=3.8.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "urllib3>=1.26.0",
        "certifi>=2022.0.0",
        "charset-normalizer>=2.0.0",
        "idna>=3.0.0",
        "tenacity>=8.2.2",
        "cachetools>=5.3.0",
        "orjson>=3.8.12",
        "ujson>=5.7.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0", "pytest-asyncio>=0.21.0", "black>=22.0.0"],
    },
    author="VectorDBCloud",
    author_email="support@vectordbcloud.com",
    description="100% ECP-Native Python SDK for VectorDBCloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VectorDBCloud/python-sdk",
    project_urls={
        "Documentation": "https://docs.vectordbcloud.com",
        "Source": "https://github.com/VectorDBCloud/python-sdk",
        "Tracker": "https://github.com/VectorDBCloud/python-sdk/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    keywords="vectordb database api sdk python ecp ephemeral-context-protocol",
)
