from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart_mrag",
    version="0.1.0",
    author="Aditya Narvekar",  # Replace with professor's name
    author_email=" Aditya.narvekar@gmail.com",  # Replace with professor's email
    description="A smart Multi-Retrieval Augmented Generation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adity-narvekar/smart_mrag",  
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.3.14",
        "langchain-community>=0.3.14",
        "langchain-openai>=0.3.0",
        "langchain-core>=0.3.29",
        "faiss-cpu>=1.9.0",
        "pymupdf>=1.25.1",
        "Pillow>=10.4.0",
        "pypdf>=5.1.0",
        "python-dotenv>=1.0.1",
        "openai>=1.59.6",
        "numpy>=1.26.2",
        "anthropic>=0.5.0",
        "google-generativeai>=0.3.0"
    ],
) 