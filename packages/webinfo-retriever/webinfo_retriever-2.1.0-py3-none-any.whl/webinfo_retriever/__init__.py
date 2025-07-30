"""
WebInfo Retriever - Advanced Web Information Retrieval and AI Summarization

A production-ready Python package for real-time web scraping, content extraction,
and AI-powered summarization using Google's Gemini 2.0 Flash model.
"""

__version__ = "1.0.0"
__author__ = "JustM3Sunny"
__email__ = "justaskcoding76@gmail.com"
__maintainer__ = "shannii"
__license__ = "MIT"
__url__ = "https://github.com/JustM3Sunny/AI_WEB_INFO_RETRIVAL"

from .api.client import WebInfoRetriever
from .core.ai_processor import AIProcessor
from .core.scraper import WebScraper
from .core.content_extractor import ContentExtractor
from .core.response_generator import ResponseGenerator
from .utils.exceptions import (
    WebInfoRetrieverError,
    ScrapingError,
    AIProcessingError,
    ContentExtractionError,
    ConfigurationError,
    RateLimitError,
)

__all__ = [
    "WebInfoRetriever",
    "AIProcessor",
    "WebScraper",
    "ContentExtractor",
    "ResponseGenerator",
    "WebInfoRetrieverError",
    "ScrapingError",
    "AIProcessingError",
    "ContentExtractionError",
    "ConfigurationError",
    "RateLimitError",
]
