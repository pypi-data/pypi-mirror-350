"""
Intelligent URL discovery and search using Gemini AI.
Uses AI to identify relevant URLs and performs web scraping for content analysis.
"""

import asyncio
import time
from typing import Dict, List, Optional, Union, Any
import re
from urllib.parse import urlparse
import google.generativeai as genai

from ..utils.config import Config
from ..utils.exceptions import WebInfoRetrieverError, AIProcessingError
from ..utils.validators import URLValidator, ContentValidator


class SearchResult:
    """Represents a single search result."""

    def __init__(self, title: str, url: str, snippet: str, source: str, rank: int):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source
        self.rank = rank
        self.relevance_score = 0.0
        self.content_quality = 0.0
        self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "rank": self.rank,
            "relevance_score": self.relevance_score,
            "content_quality": self.content_quality,
            "metadata": self.metadata
        }


class IntelligentSearchEngine:
    """Intelligent search engine using Gemini AI for URL discovery and content analysis."""

    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.gemini_api_key

        if not self.api_key:
            raise AIProcessingError("Gemini API key is required for intelligent search")

        genai.configure(api_key=self.api_key)

        # Initialize Gemini model
        self.model = genai.GenerativeModel(
            model_name=config.get("ai.model", "gemini-2.0-flash-exp"),
            generation_config={
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )

    async def discover_relevant_urls(self, query: str, num_urls: int = 10) -> List[SearchResult]:
        """
        Fast URL discovery using optimized Gemini prompts.
        """
        query = ContentValidator.validate_query(query)

        # Optimized short prompt for faster response
        discovery_prompt = f"""
For query "{query}", list {num_urls} real URLs with titles. Format:
URL: [url]
TITLE: [title]
---

Focus on: official docs, GitHub repos, tutorials, Stack Overflow, Wikipedia.
Query: {query}
"""

        try:
            response = self.model.generate_content(discovery_prompt)

            if not response.text:
                # Fast fallback
                return self._generate_smart_urls(query, num_urls)

            # Parse response quickly
            discovered_urls = self._parse_url_discovery_response(response.text, query)

            if not discovered_urls:
                return self._generate_smart_urls(query, num_urls)

            return discovered_urls[:num_urls]

        except Exception as e:
            # Fast fallback on any error
            return self._generate_smart_urls(query, num_urls)

    def _parse_url_discovery_response(self, response_text: str, query: str) -> List[SearchResult]:
        """Parse Gemini's response to extract URLs, titles, and snippets."""
        results = []

        # Split response into sections
        sections = response_text.split('---')

        for i, section in enumerate(sections):
            if not section.strip():
                continue

            # Extract URL, title, and snippet using regex
            url_match = re.search(r'URL:\s*(.+)', section, re.IGNORECASE)
            title_match = re.search(r'TITLE:\s*(.+)', section, re.IGNORECASE)
            snippet_match = re.search(r'SNIPPET:\s*(.+)', section, re.IGNORECASE | re.DOTALL)

            if url_match:
                url = url_match.group(1).strip()
                title = title_match.group(1).strip() if title_match else f"Resource for {query}"
                snippet = snippet_match.group(1).strip() if snippet_match else f"Relevant information about {query}"

                # Clean up the snippet (remove extra whitespace and newlines)
                snippet = re.sub(r'\s+', ' ', snippet).strip()

                # Validate URL
                try:
                    validated_url = URLValidator.validate_url(url)

                    result = SearchResult(
                        title=title,
                        url=validated_url,
                        snippet=snippet,
                        source="gemini_ai",
                        rank=i + 1
                    )

                    # Calculate relevance score based on query terms
                    result.relevance_score = self._calculate_relevance_score(title, snippet, query)
                    result.content_quality = self._estimate_content_quality(url, title)

                    results.append(result)

                except Exception:
                    # Skip invalid URLs
                    continue

        return results

    def _generate_smart_urls(self, query: str, num_urls: int) -> List[SearchResult]:
        """Generate smart URLs based on query analysis."""
        results = []
        query_lower = query.lower()

        # Smart URL patterns based on query content
        if any(word in query_lower for word in ['python', 'programming', 'code', 'library']):
            urls = [
                ("https://docs.python.org/3/", f"Python Documentation - {query}"),
                ("https://github.com/topics/python", f"Python Projects on GitHub - {query}"),
                ("https://stackoverflow.com/questions/tagged/python", f"Python Questions - {query}"),
                ("https://pypi.org/search/?q=" + query.replace(' ', '+'), f"PyPI Packages - {query}"),
                ("https://realpython.com/search/?q=" + query.replace(' ', '+'), f"Real Python - {query}"),
            ]
        elif any(word in query_lower for word in ['javascript', 'js', 'react', 'node']):
            urls = [
                ("https://developer.mozilla.org/en-US/docs/Web/JavaScript", f"MDN JavaScript - {query}"),
                ("https://github.com/topics/javascript", f"JavaScript Projects - {query}"),
                ("https://stackoverflow.com/questions/tagged/javascript", f"JavaScript Questions - {query}"),
                ("https://www.npmjs.com/search?q=" + query.replace(' ', '+'), f"NPM Packages - {query}"),
                ("https://reactjs.org/docs/getting-started.html", f"React Documentation - {query}"),
            ]
        elif any(word in query_lower for word in ['ai', 'machine learning', 'ml', 'data science']):
            urls = [
                ("https://scikit-learn.org/stable/", f"Scikit-learn - {query}"),
                ("https://tensorflow.org/", f"TensorFlow - {query}"),
                ("https://pytorch.org/", f"PyTorch - {query}"),
                ("https://github.com/topics/machine-learning", f"ML Projects - {query}"),
                ("https://kaggle.com/search?q=" + query.replace(' ', '+'), f"Kaggle - {query}"),
            ]
        else:
            # General fallback
            urls = [
                ("https://en.wikipedia.org/wiki/" + query.replace(' ', '_'), f"Wikipedia - {query}"),
                ("https://github.com/search?q=" + query.replace(' ', '+'), f"GitHub - {query}"),
                ("https://stackoverflow.com/search?q=" + query.replace(' ', '+'), f"Stack Overflow - {query}"),
                ("https://www.reddit.com/search/?q=" + query.replace(' ', '+'), f"Reddit - {query}"),
                ("https://medium.com/search?q=" + query.replace(' ', '+'), f"Medium - {query}"),
            ]

        for i, (url, title) in enumerate(urls[:num_urls]):
            result = SearchResult(
                title=title,
                url=url,
                snippet=f"Relevant information about {query}",
                source="smart_fallback",
                rank=i + 1
            )
            result.relevance_score = 0.8
            result.content_quality = 0.7
            results.append(result)

        return results

    def _calculate_relevance_score(self, title: str, snippet: str, query: str) -> float:
        """Calculate relevance score based on query term matches."""
        query_words = set(word.lower() for word in query.split() if len(word) > 2)
        title_words = set(word.lower() for word in title.split())
        snippet_words = set(word.lower() for word in snippet.split())

        # Calculate matches
        title_matches = len(query_words.intersection(title_words))
        snippet_matches = len(query_words.intersection(snippet_words))

        # Weight title matches higher
        total_matches = (title_matches * 2) + snippet_matches
        max_possible = len(query_words) * 3  # 2 for title + 1 for snippet

        return min(total_matches / max(max_possible, 1), 1.0)

    def _estimate_content_quality(self, url: str, title: str) -> float:
        """Estimate content quality based on URL and title characteristics."""
        quality_score = 0.5  # Base score

        # Domain-based quality indicators
        domain = urlparse(url).netloc.lower()

        high_quality_domains = [
            'wikipedia.org', 'github.com', 'stackoverflow.com',
            'docs.python.org', 'developer.mozilla.org', '.edu',
            'arxiv.org', 'ieee.org', 'acm.org'
        ]

        medium_quality_domains = [
            'medium.com', 'dev.to', 'hackernoon.com',
            'towardsdatascience.com', 'freecodecamp.org'
        ]

        for hq_domain in high_quality_domains:
            if hq_domain in domain:
                quality_score += 0.3
                break

        for mq_domain in medium_quality_domains:
            if mq_domain in domain:
                quality_score += 0.2
                break

        # HTTPS bonus
        if url.startswith('https://'):
            quality_score += 0.1

        # Title quality indicators
        if len(title) > 20 and len(title) < 100:
            quality_score += 0.1

        return min(quality_score, 1.0)

    async def search(self, query: str, num_results: int = 15) -> List[SearchResult]:
        """
        Perform intelligent search using Gemini AI for URL discovery.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of SearchResult objects
        """
        try:
            # Discover relevant URLs using Gemini AI
            discovered_urls = await self.discover_relevant_urls(query, num_results)

            # Sort by relevance and quality
            discovered_urls.sort(
                key=lambda r: r.relevance_score + r.content_quality,
                reverse=True
            )

            return discovered_urls

        except Exception as e:
            raise WebInfoRetrieverError(f"Intelligent search failed: {str(e)}")
