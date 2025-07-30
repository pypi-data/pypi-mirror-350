from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="webinfo-retriever",
    version="2.1.0",
    author="JustM3Sunny",
    author_email="justaskcoding76@gmail.com",
    description="Ultra-fast comprehensive web search and AI-powered analysis with parallel processing and beautiful output formatting",
    long_description="WebInfo Retriever is a state-of-the-art Python library that provides ultra-fast comprehensive web search and analysis capabilities. It combines advanced AI processing with parallel web scraping to deliver Tavily-like comprehensive answers but faster and more powerful. Features include parallel processing of 25+ sources, streaming results, multi-source synthesis, and beautiful dual-format output.",
    long_description_content_type="text/plain",
    url="https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL",
    packages=find_packages(),
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
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "webinfo-retriever=webinfo_retriever.cli:main",
        ],
    },
    keywords="web scraping, ai, summarization, information retrieval, gemini, natural language processing, search, content extraction",
    project_urls={
        "Bug Reports": "https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL/issues",
        "Source": "https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL",
        "Documentation": "https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL#readme",
        "Homepage": "https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL",
    },
)
