# 🔍 WebInfo Retriever

**Advanced Web Information Retrieval and AI-Powered Summarization**

A production-ready Python package for real-time web scraping, content extraction, and AI-powered summarization using Google's Gemini 2.0 Flash model. Features natural language search, intelligent URL discovery, and beautiful markdown reporting.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/JustM3Sunny/AI_WEB_INFO_RETRIVAL.svg)](https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL/issues)

## ✨ Features

### 🚀 **Natural Language Search**
- **Human-friendly queries**: "find me python tutorials", "best AI projects on GitHub"
- **Intent recognition**: Automatically detects tutorial, comparison, research needs
- **Smart optimization**: Converts natural language to effective search terms

### 🧠 **AI-Powered Analysis**
- **Gemini 2.0 Flash integration**: State-of-the-art AI summarization
- **Intelligent URL discovery**: AI suggests relevant, authoritative sources
- **Executive summaries**: Comprehensive analysis across multiple sources
- **Content categorization**: Automatic classification of results

### ⚡ **Fast & Efficient**
- **Super fast response**: Results in 2-4 seconds
- **Concurrent processing**: Multiple URLs processed simultaneously
- **Smart caching**: Reduces redundant API calls
- **Production-ready**: Robust error handling and retry mechanisms

### 📄 **Beautiful Output**
- **Professional markdown reports**: Structured, formatted results
- **Source attribution**: Proper links and metadata
- **Multiple output formats**: Markdown, JSON, or both
- **CLI and Python API**: Flexible usage options

## 🚀 Quick Start

### Installation

```bash
pip install webinfo-retriever
```

### Set up your API key

Get your free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### Basic Usage

#### Command Line Interface

```bash
# Natural language search
webinfo-retriever search --fast find me python tutorials

# Comprehensive analysis
webinfo-retriever search best AI projects on GitHub --output-file report.md

# Quick search
webinfo-retriever search --quick React vs Vue comparison
```

#### Python API

```python
from webinfo_retriever import WebInfoRetriever

# Initialize client
client = WebInfoRetriever()

# Fast natural language search
result = await client.fast_search("find me python machine learning libraries")
print(result)

# Comprehensive analysis
result = await client.intelligent_search(
    query="best AI projects on GitHub",
    num_results=10,
    include_executive_summary=True
)
print(result['markdown_report'])

# Single URL analysis
result = client.retrieve_and_summarize(
    url="https://example.com",
    query="What is this about?"
)
```

## 📖 Documentation

### CLI Commands

#### Search Commands
```bash
# Fast search (2-4 seconds)
webinfo-retriever search --fast [natural language query]

# Quick search (basic results)
webinfo-retriever search --quick [query]

# Full analysis (comprehensive report)
webinfo-retriever search [query] --num-results 15 --output-file report.md
```

#### Single URL Analysis
```bash
# Summarize a webpage
webinfo-retriever summarize https://example.com

# Answer questions about a webpage
webinfo-retriever question https://example.com "What is the main topic?"

# Extract key points
webinfo-retriever keypoints https://example.com --num-points 5
```

### Python API Reference

#### WebInfoRetriever Class

```python
from webinfo_retriever import WebInfoRetriever

client = WebInfoRetriever(api_key="your_key")  # Optional if env var set
```

#### Search Methods

```python
# Fast natural language search
result = await client.fast_search(
    user_query="find me python tutorials",
    num_results=5
)

# Comprehensive intelligent search
result = await client.intelligent_search(
    query="machine learning frameworks",
    num_results=15,
    include_executive_summary=True,
    output_format="markdown"
)

# Quick search
result = await client.quick_search(
    query="React tutorials",
    num_results=5,
    format_output=True
)
```

#### Content Analysis Methods

```python
# Summarize single URL
result = client.retrieve_and_summarize(
    url="https://example.com",
    query="What is this about?",
    max_summary_length=500
)

# Answer questions
result = client.answer_question(
    url="https://example.com",
    question="What are the main benefits?"
)

# Extract key points
result = client.extract_key_points(
    url="https://example.com",
    num_points=5
)

# Get page metadata
result = client.get_page_metadata(url="https://example.com")
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
WEBINFO_TIMEOUT=30
WEBINFO_MAX_RETRIES=3
WEBINFO_CACHE_TTL=3600
```

### Custom Configuration

```python
config = {
    "ai": {
        "temperature": 0.3,
        "max_tokens": 8192
    },
    "scraping": {
        "timeout": 30,
        "max_retries": 3
    },
    "content": {
        "max_summary_length": 2000
    }
}

client = WebInfoRetriever(config=config)
```

## 🛠️ Advanced Features

### Natural Language Processing
- Understands human queries like "find me", "show me", "what are"
- Automatically optimizes search terms
- Recognizes intent (tutorial, comparison, research)
- Smart category detection

### Intelligent URL Discovery
- AI suggests relevant, authoritative sources
- Context-aware recommendations
- Quality scoring and ranking
- Fallback patterns for reliability

### Multi-Strategy Content Extraction
- Trafilatura for clean text extraction
- Readability for article content
- Newspaper3k for news articles
- BeautifulSoup for general content

### Production Features
- Comprehensive error handling
- Rate limiting and retry mechanisms
- Concurrent processing
- Caching for performance
- Detailed logging and monitoring

## 📊 Example Output

```markdown
# 🔍 Search Results: find me python machine learning libraries

**Optimized Query:** python machine learning libraries
**Intent:** Tutorial
**Found:** 8 results

---

## 1. 📚 scikit-learn: Machine Learning in Python
**URL:** https://scikit-learn.org/stable/
**Description:** Simple and efficient tools for predictive data analysis

## 2. 🔥 TensorFlow - An Open Source Machine Learning Framework
**URL:** https://tensorflow.org/
**Description:** End-to-end open source platform for machine learning

## 3. ⚡ PyTorch - Tensors and Dynamic neural networks
**URL:** https://pytorch.org/
**Description:** An open source machine learning framework
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**JustM3Sunny** (shannii)
- Email: justaskcoding76@gmail.com
- GitHub: [@JustM3Sunny](https://github.com/JustM3Sunny)

## 🙏 Acknowledgments

- Google's Gemini 2.0 Flash model for AI capabilities
- The open-source community for excellent libraries
- Contributors and users for feedback and improvements

---

**Made with ❤️ for the developer community**
