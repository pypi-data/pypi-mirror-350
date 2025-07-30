from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ragger-simple",
    version="0.1.4",
    author="Anton Pavlenko",
    author_email="apavlenko@hmcorp.fund",
    description="Simple vector database operations with Qdrant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HMCorp-Fund/ragger-simple",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sentence-transformers>=2.0.0",
        "qdrant-client>=1.0.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "ragger-simple=ragger_simple.cli:main",
        ],
    },
    packages=find_packages(),
)