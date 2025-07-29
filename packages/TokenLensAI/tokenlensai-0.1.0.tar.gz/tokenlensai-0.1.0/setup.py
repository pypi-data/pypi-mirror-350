from setuptools import setup, find_packages
import os

# Read the contents of the README file
current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="TokenLensAI",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tiktoken>=0.5.0",            # For GPT tokenization
        "pyyaml>=6.0",                # For configuration files
        "requests>=2.28.0",           # For API calls
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
        ],
        "llama": ["llama-index>=0.9.0"],
        "all": [
            "anthropic>=0.5.0",
            "openai>=1.0.0",
            "google-generativeai>=0.3.0",
            "mistralai>=0.0.7",
            "cohere>=4.0.0",
            "llama-index>=0.9.0",
        ],
    },
    author="TokenLens Team",
    author_email="tokenlens@example.com",  # Replace with your email
    description="An agentic AI-based library for token counting and analysis across multiple LLM standards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tokenlens/tokenlens",  # Replace with your actual repository
    project_urls={
        "Documentation": "https://tokenlens.readthedocs.io",
        "Bug Tracker": "https://github.com/tokenlens/tokenlens/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="nlp, llm, tokenization, gpt, claude, llama, gemini, mistral, tokens, language models",
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "tokenlensai": ["config/*.yaml"],
    },
)