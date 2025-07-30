"""
Advanced search result processing and intelligent content aggregation.
"""

import asyncio
import time
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
import re
from collections import defaultdict, Counter

from .intelligent_search import SearchResult
from .scraper import WebScraper
from .content_extractor import ContentExtractor
from .ai_processor import AIProcessor
from ..utils.config import Config
from ..utils.exceptions import WebInfoRetrieverError
from ..utils.validators import ContentValidator


class ProcessedSearchResult:
    """Represents a processed search result with extracted content."""

    def __init__(self, search_result: SearchResult):
        self.search_result = search_result
        self.extracted_content = None
        self.ai_summary = None
        self.key_points = []
        self.processing_time = 0.0
        self.success = False
        self.error_message = None
        self.content_category = "general"
        self.relevance_keywords = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "search_result": self.search_result.to_dict(),
            "extracted_content": self.extracted_content,
            "ai_summary": self.ai_summary,
            "key_points": self.key_points,
            "processing_time": self.processing_time,
            "success": self.success,
            "error_message": self.error_message,
            "content_category": self.content_category,
            "relevance_keywords": self.relevance_keywords
        }


class SearchResultProcessor:
    """Advanced processor for search results with intelligent aggregation."""

    def __init__(self, config: Config):
        self.config = config
        self.scraper = WebScraper(config)
        self.content_extractor = ContentExtractor(config)
        self.ai_processor = AIProcessor(config)

        # Content categories for intelligent grouping
        self.content_categories = {
            "tutorial": ["tutorial", "guide", "how-to", "step-by-step", "learn"],
            "documentation": ["docs", "documentation", "api", "reference", "manual"],
            "repository": ["github", "gitlab", "repo", "source code", "project"],
            "article": ["article", "blog", "post", "news", "medium"],
            "tool": ["tool", "software", "app", "platform", "service"],
            "comparison": ["vs", "comparison", "compare", "best", "top"],
            "research": ["paper", "research", "study", "analysis", "academic"]
        }

    async def process_search_results(
        self,
        search_results: List[SearchResult],
        query: str,
        max_concurrent: int = 5
    ) -> List[ProcessedSearchResult]:
        """
        Process search results with concurrent content extraction and AI analysis.

        Args:
            search_results: List of search results to process
            query: Original search query for context
            max_concurrent: Maximum concurrent processing tasks

        Returns:
            List of ProcessedSearchResult objects
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_single_result(search_result: SearchResult) -> ProcessedSearchResult:
            async with semaphore:
                return await self._process_single_result(search_result, query)

        # Process all results concurrently
        tasks = [process_single_result(result) for result in search_results]
        processed_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions and filter successful results
        successful_results = []
        for i, result in enumerate(processed_results):
            if isinstance(result, Exception):
                # Create failed result
                failed_result = ProcessedSearchResult(search_results[i])
                failed_result.error_message = str(result)
                successful_results.append(failed_result)
            else:
                successful_results.append(result)

        return successful_results

    async def _process_single_result(self, search_result: SearchResult, query: str) -> ProcessedSearchResult:
        """Process a single search result."""
        processed_result = ProcessedSearchResult(search_result)
        start_time = time.time()

        try:
            # Extract content from URL
            loop = asyncio.get_event_loop()
            scraped_data = await loop.run_in_executor(
                None, self.scraper.scrape_url, search_result.url
            )

            extracted_content = await loop.run_in_executor(
                None, self.content_extractor.extract_content, scraped_data
            )

            processed_result.extracted_content = extracted_content

            # Categorize content
            processed_result.content_category = self._categorize_content(
                search_result, extracted_content
            )

            # Extract relevance keywords
            processed_result.relevance_keywords = self._extract_relevance_keywords(
                extracted_content.get("text", ""), query
            )

            # Generate AI summary if content is substantial
            content_text = extracted_content.get("text", "")
            if len(content_text) > 200:
                ai_summary = await loop.run_in_executor(
                    None,
                    self.ai_processor.summarize_content,
                    content_text,
                    f"Summarize this content in relation to: {query}",
                    500
                )
                processed_result.ai_summary = ai_summary

                # Extract key points
                key_points_result = await loop.run_in_executor(
                    None,
                    self.ai_processor.extract_key_points,
                    content_text,
                    3
                )
                processed_result.key_points = key_points_result.get("key_points", [])

            processed_result.success = True

        except Exception as e:
            processed_result.error_message = str(e)
            processed_result.success = False

        processed_result.processing_time = time.time() - start_time
        return processed_result

    def _categorize_content(self, search_result: SearchResult, extracted_content: Dict) -> str:
        """Categorize content based on URL, title, and content."""
        url = search_result.url.lower()
        title = search_result.title.lower()
        content = extracted_content.get("text", "").lower()[:1000]  # First 1000 chars

        # Combine all text for analysis
        combined_text = f"{url} {title} {content}"

        # Score each category
        category_scores = {}
        for category, keywords in self.content_categories.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                category_scores[category] = score

        # Return highest scoring category or 'general'
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return "general"

    def _extract_relevance_keywords(self, content: str, query: str) -> List[str]:
        """Extract keywords relevant to the search query."""
        if not content:
            return []

        # Simple keyword extraction based on query terms
        query_words = set(word.lower() for word in query.split() if len(word) > 2)
        content_words = re.findall(r'\b\w+\b', content.lower())

        # Find words that appear near query terms
        relevant_keywords = set()
        for i, word in enumerate(content_words):
            if word in query_words:
                # Add surrounding words
                start = max(0, i - 3)
                end = min(len(content_words), i + 4)
                for j in range(start, end):
                    if len(content_words[j]) > 3 and content_words[j] not in query_words:
                        relevant_keywords.add(content_words[j])

        # Return most common relevant keywords
        keyword_counts = Counter(relevant_keywords)
        return [word for word, count in keyword_counts.most_common(10)]

    def aggregate_results(
        self,
        processed_results: List[ProcessedSearchResult],
        query: str
    ) -> Dict[str, Any]:
        """
        Aggregate processed results into a comprehensive analysis.

        Args:
            processed_results: List of processed search results
            query: Original search query

        Returns:
            Aggregated analysis with categorized results and insights
        """
        successful_results = [r for r in processed_results if r.success]

        # Group results by category
        categorized_results = defaultdict(list)
        for result in successful_results:
            categorized_results[result.content_category].append(result)

        # Extract common themes and keywords
        all_keywords = []
        for result in successful_results:
            all_keywords.extend(result.relevance_keywords)

        common_keywords = [word for word, count in Counter(all_keywords).most_common(15)]

        # Generate category summaries
        category_summaries = {}
        for category, results in categorized_results.items():
            if len(results) >= 2:  # Only summarize categories with multiple results
                category_summaries[category] = self._generate_category_summary(results, query)

        # Calculate processing statistics
        total_processing_time = sum(r.processing_time for r in processed_results)
        success_rate = len(successful_results) / len(processed_results) if processed_results else 0

        return {
            "query": query,
            "total_results": len(processed_results),
            "successful_results": len(successful_results),
            "success_rate": success_rate,
            "categorized_results": dict(categorized_results),
            "category_summaries": category_summaries,
            "common_keywords": common_keywords,
            "processing_time": total_processing_time,
            "timestamp": datetime.now().isoformat(),
            "top_sources": self._get_top_sources(successful_results)
        }

    def _generate_category_summary(self, results: List[ProcessedSearchResult], query: str) -> Dict[str, Any]:
        """Generate a summary for a specific category of results."""
        # Combine all summaries from the category
        summaries = []
        key_points = []

        for result in results:
            if result.ai_summary and result.ai_summary.get("summary"):
                summaries.append(result.ai_summary["summary"])
            key_points.extend(result.key_points)

        # Get most common key points
        common_points = [point for point, count in Counter(key_points).most_common(5)]

        return {
            "result_count": len(results),
            "common_key_points": common_points,
            "top_sources": [r.search_result.title for r in results[:3]],
            "average_relevance": sum(r.search_result.relevance_score for r in results) / len(results)
        }

    def _get_top_sources(self, results: List[ProcessedSearchResult]) -> List[Dict[str, Any]]:
        """Get top sources based on relevance and content quality."""
        # Sort by combined relevance and quality score
        sorted_results = sorted(
            results,
            key=lambda r: r.search_result.relevance_score + r.search_result.content_quality,
            reverse=True
        )

        top_sources = []
        for result in sorted_results[:5]:
            source_info = {
                "title": result.search_result.title,
                "url": result.search_result.url,
                "relevance_score": result.search_result.relevance_score,
                "content_quality": result.search_result.content_quality,
                "category": result.content_category,
                "key_points": result.key_points[:2]  # Top 2 key points
            }
            top_sources.append(source_info)

        return top_sources
