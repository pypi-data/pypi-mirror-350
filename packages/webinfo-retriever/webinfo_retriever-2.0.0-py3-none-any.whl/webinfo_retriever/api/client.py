"""
Main client interface for WebInfo Retriever package.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Union, Any

from ..core.scraper import WebScraper
from ..core.content_extractor import ContentExtractor
from ..core.ai_processor import AIProcessor
from ..core.response_generator import ResponseGenerator
from ..core.advanced_search_engine import AdvancedSearchEngine
from ..core.answer_formatter import AdvancedAnswerFormatter
from .search_client import SearchClient
from ..utils.config import Config
from ..utils.exceptions import WebInfoRetrieverError, ConfigurationError
from ..utils.validators import URLValidator, ContentValidator

# Set up logging
logger = logging.getLogger(__name__)


class WebInfoRetriever:
    """
    Main client interface for WebInfo Retriever.

    A production-ready tool for web information retrieval and AI-powered summarization.
    """

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize WebInfo Retriever.

        Args:
            api_key: Google Gemini API key (can also be set via GEMINI_API_KEY env var)
            config: Optional configuration dictionary to override defaults
        """
        try:
            logger.info("Initializing WebInfo Retriever client")

            config_dict = config or {}
            if api_key:
                if "ai" not in config_dict:
                    config_dict["ai"] = {}
                config_dict["ai"]["api_key"] = api_key
                logger.debug("API key provided via parameter")

            self.config = Config(config_dict)

            self.scraper = WebScraper(self.config)
            self.content_extractor = ContentExtractor(self.config)
            self.ai_processor = AIProcessor(self.config)
            self.response_generator = ResponseGenerator(self.config)
            self.search_client = SearchClient(self.config)
            self.advanced_search = AdvancedSearchEngine(self.config)
            self.answer_formatter = AdvancedAnswerFormatter()

            logger.info("WebInfo Retriever client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize WebInfo Retriever: {str(e)}")
            raise ConfigurationError(f"Failed to initialize WebInfo Retriever: {str(e)}")

    def retrieve_and_summarize(
        self,
        url: str,
        query: Optional[str] = None,
        max_summary_length: Optional[int] = None,
        use_selenium: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieve content from a URL and generate an AI-powered summary.

        Args:
            url: URL to scrape and summarize
            query: Optional query to focus the summary
            max_summary_length: Maximum length of the summary
            use_selenium: Whether to use Selenium for scraping (for dynamic content)

        Returns:
            Dictionary containing the summary and metadata
        """
        try:
            url = URLValidator.validate_url(url)

            scraped_data = self.scraper.scrape_url(url, use_selenium=use_selenium)

            extracted_content = self.content_extractor.extract_content(scraped_data)

            content_text = extracted_content.get("text", "")
            if not content_text:
                raise WebInfoRetrieverError("No content could be extracted from the URL")

            summary_result = self.ai_processor.summarize_content(
                content_text,
                query=query,
                max_length=max_summary_length
            )

            response = self.response_generator.generate_comprehensive_response(
                query or f"Summary of {url}",
                [extracted_content],
                [summary_result],
                metadata={
                    "url": url,
                    "scraping_method": scraped_data.get("method"),
                    "extraction_method": extracted_content.get("method"),
                }
            )

            return response

        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Failed to retrieve and summarize {url}: {str(e)}")

    def retrieve_multiple_and_summarize(
        self,
        urls: List[str],
        query: Optional[str] = None,
        max_summary_length: Optional[int] = None,
        max_concurrent: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve content from multiple URLs and generate a combined summary.

        Args:
            urls: List of URLs to scrape and summarize
            query: Optional query to focus the summary
            max_summary_length: Maximum length of the summary
            max_concurrent: Maximum number of concurrent requests

        Returns:
            Dictionary containing the combined summary and metadata
        """
        try:
            urls = URLValidator.validate_urls(urls)

            scraped_results = asyncio.run(
                self.scraper.scrape_urls_async(urls, max_concurrent=max_concurrent)
            )

            extracted_contents = []
            for scraped_data in scraped_results:
                if scraped_data.get("content"):
                    try:
                        extracted_content = self.content_extractor.extract_content(scraped_data)
                        extracted_contents.append(extracted_content)
                    except Exception:
                        continue

            if not extracted_contents:
                raise WebInfoRetrieverError("No content could be extracted from any of the URLs")

            content_data = [
                {"content": content.get("text", ""), "query": query}
                for content in extracted_contents
                if content.get("text")
            ]

            summary_results = asyncio.run(
                self.ai_processor.process_multiple_contents(content_data, operation="summarize")
            )

            response = self.response_generator.generate_comprehensive_response(
                query or f"Summary of {len(urls)} URLs",
                extracted_contents,
                summary_results,
                metadata={
                    "urls": urls,
                    "successful_extractions": len(extracted_contents),
                    "total_urls": len(urls),
                }
            )

            return response

        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Failed to retrieve and summarize multiple URLs: {str(e)}")

    def answer_question(self, url: str, question: str, use_selenium: bool = False) -> Dict[str, Any]:
        """
        Answer a specific question based on content from a URL.

        Args:
            url: URL to scrape for information
            question: Question to answer
            use_selenium: Whether to use Selenium for scraping

        Returns:
            Dictionary containing the answer and metadata
        """
        try:
            url = URLValidator.validate_url(url)
            question = ContentValidator.validate_query(question)

            scraped_data = self.scraper.scrape_url(url, use_selenium=use_selenium)

            extracted_content = self.content_extractor.extract_content(scraped_data)

            content_text = extracted_content.get("text", "")
            if not content_text:
                raise WebInfoRetrieverError("No content could be extracted from the URL")

            answer_result = self.ai_processor.answer_question(content_text, question)

            response = {
                "question": question,
                "answer": answer_result.get("answer", ""),
                "confidence": answer_result.get("confidence", 0.0),
                "source": {
                    "url": url,
                    "title": extracted_content.get("title", ""),
                    "content_length": len(content_text),
                    "extraction_method": extracted_content.get("method"),
                },
                "processing_time": answer_result.get("processing_time", 0),
                "model": answer_result.get("model", ""),
                "timestamp": answer_result.get("timestamp"),
            }

            return response

        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Failed to answer question from {url}: {str(e)}")

    def extract_key_points(self, url: str, num_points: int = 5, use_selenium: bool = False) -> Dict[str, Any]:
        """
        Extract key points from content at a URL.

        Args:
            url: URL to scrape for information
            num_points: Number of key points to extract
            use_selenium: Whether to use Selenium for scraping

        Returns:
            Dictionary containing key points and metadata
        """
        try:
            url = URLValidator.validate_url(url)

            scraped_data = self.scraper.scrape_url(url, use_selenium=use_selenium)

            extracted_content = self.content_extractor.extract_content(scraped_data)

            content_text = extracted_content.get("text", "")
            if not content_text:
                raise WebInfoRetrieverError("No content could be extracted from the URL")

            key_points_result = self.ai_processor.extract_key_points(content_text, num_points)

            response = {
                "url": url,
                "title": extracted_content.get("title", ""),
                "key_points": key_points_result.get("key_points", []),
                "num_points_requested": num_points,
                "num_points_extracted": len(key_points_result.get("key_points", [])),
                "source_info": {
                    "content_length": len(content_text),
                    "word_count": len(content_text.split()),
                    "extraction_method": extracted_content.get("method"),
                },
                "processing_time": key_points_result.get("processing_time", 0),
                "model": key_points_result.get("model", ""),
            }

            return response

        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Failed to extract key points from {url}: {str(e)}")

    def get_page_metadata(self, url: str, use_selenium: bool = False) -> Dict[str, Any]:
        """
        Get metadata and basic information about a webpage.

        Args:
            url: URL to analyze
            use_selenium: Whether to use Selenium for scraping

        Returns:
            Dictionary containing page metadata
        """
        try:
            url = URLValidator.validate_url(url)

            metadata = self.scraper.get_page_metadata(url)

            scraped_data = self.scraper.scrape_url(url, use_selenium=use_selenium)
            extracted_content = self.content_extractor.extract_content(scraped_data)

            structured_data = self.content_extractor.extract_structured_data(scraped_data.get("content", ""))

            response = {
                "url": url,
                "metadata": metadata,
                "content_info": {
                    "content_length": extracted_content.get("content_length", 0),
                    "word_count": extracted_content.get("word_count", 0),
                    "extraction_score": extracted_content.get("extraction_score", 0),
                    "extraction_method": extracted_content.get("method", ""),
                },
                "structured_data": structured_data,
                "scraping_info": {
                    "method": scraped_data.get("method", ""),
                    "status_code": scraped_data.get("status_code"),
                    "final_url": scraped_data.get("final_url", url),
                },
            }

            if extracted_content.get("links"):
                response["links"] = extracted_content["links"][:10]

            if extracted_content.get("images"):
                response["images"] = extracted_content["images"][:5]

            return response

        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Failed to get metadata for {url}: {str(e)}")

    async def intelligent_search(
        self,
        query: str,
        num_results: int = 15,
        include_executive_summary: bool = True,
        output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Perform intelligent web search with comprehensive AI analysis.

        Args:
            query: Search query to execute
            num_results: Number of results to process (default: 15)
            include_executive_summary: Whether to generate AI executive summary
            output_format: Output format ("markdown", "json", or "both")

        Returns:
            Comprehensive search analysis with markdown report
        """
        try:
            return await self.search_client.intelligent_search(
                query=query,
                num_results=num_results,
                include_executive_summary=include_executive_summary,
                output_format=output_format
            )
        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Intelligent search failed: {str(e)}")

    async def fast_comprehensive_search(
        self,
        query: str,
        num_sources: int = 12,
        output_format: str = "markdown",
        answer_type: str = "comprehensive",
        stream_results: bool = True
    ) -> Union[str, Dict[str, Any]]:
        """
        Ultra-fast comprehensive search with parallel processing and streaming results.

        Args:
            query: User's search query
            num_sources: Number of sources to analyze (default: 12)
            output_format: Output format ("markdown", "json", "text", or "both")
            answer_type: Type of answer needed (comprehensive, factual, comparative)
            stream_results: Whether to stream results as they come

        Returns:
            Comprehensive answer with full detailed analysis and beautiful formatting
        """
        try:
            logger.info(f"🚀 Starting ULTRA-FAST comprehensive search for: {query}")

            # Perform ultra-fast advanced search
            answer = await self.advanced_search.fast_comprehensive_search(
                query=query,
                num_sources=num_sources,
                include_analysis=True,
                answer_type=answer_type,
                stream_results=stream_results
            )

            # Format response with enhanced styling
            if output_format == "json":
                return self.answer_formatter.format_comprehensive_answer(answer, "json")
            elif output_format == "text":
                return self.answer_formatter.format_comprehensive_answer(answer, "text")
            elif output_format == "both":
                return {
                    "terminal_output": self.answer_formatter.format_comprehensive_answer(answer, "terminal"),
                    "markdown_report": self.answer_formatter.format_comprehensive_answer(answer, "markdown_file"),
                    "json_data": self.answer_formatter.format_comprehensive_answer(answer, "json"),
                    "quick_summary": self.answer_formatter.create_quick_summary(answer),
                    "citations": self.answer_formatter.create_citation_list(answer),
                    "answer_object": answer
                }
            else:  # terminal (default)
                return self.answer_formatter.format_comprehensive_answer(answer, "terminal")

        except Exception as e:
            logger.error(f"Fast comprehensive search failed: {str(e)}")
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Fast comprehensive search failed: {str(e)}")

    async def comprehensive_search(
        self,
        query: str,
        num_sources: int = 12,
        output_format: str = "markdown",
        answer_type: str = "comprehensive"
    ) -> Union[str, Dict[str, Any]]:
        """
        Perform comprehensive search with multi-source answer synthesis.
        Similar to Tavily AI but faster and more advanced.

        Args:
            query: User's search query
            num_sources: Number of sources to analyze (default: 12)
            output_format: Output format ("markdown", "json", "text", or "both")
            answer_type: Type of answer needed (comprehensive, factual, comparative)

        Returns:
            Comprehensive answer with detailed analysis and source attribution
        """
        try:
            logger.info(f"Starting comprehensive search for: {query}")

            # Perform advanced search
            answer = await self.advanced_search.comprehensive_search(
                query=query,
                num_sources=num_sources,
                include_analysis=True,
                answer_type=answer_type
            )

            # Format response
            if output_format == "json":
                return self.answer_formatter.format_comprehensive_answer(answer, "json")
            elif output_format == "text":
                return self.answer_formatter.format_comprehensive_answer(answer, "text")
            elif output_format == "both":
                return {
                    "terminal_output": self.answer_formatter.format_comprehensive_answer(answer, "terminal"),
                    "markdown_report": self.answer_formatter.format_comprehensive_answer(answer, "markdown_file"),
                    "json_data": self.answer_formatter.format_comprehensive_answer(answer, "json"),
                    "quick_summary": self.answer_formatter.create_quick_summary(answer),
                    "citations": self.answer_formatter.create_citation_list(answer),
                    "answer_object": answer
                }
            else:  # terminal (default)
                return self.answer_formatter.format_comprehensive_answer(answer, "terminal")

        except Exception as e:
            logger.error(f"Comprehensive search failed: {str(e)}")
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Comprehensive search failed: {str(e)}")

    async def fast_search(
        self,
        user_query: str,
        num_results: int = 5
    ) -> str:
        """
        Super fast search with natural language processing.

        Args:
            user_query: Natural language query from user (e.g., "find me python tutorials")
            num_results: Number of results to return

        Returns:
            Formatted markdown results
        """
        try:
            return await self.search_client.fast_search(
                user_query=user_query,
                num_results=num_results
            )
        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Fast search failed: {str(e)}")

    async def quick_search(
        self,
        query: str,
        num_results: int = 5,
        format_output: bool = True
    ) -> Union[str, Dict[str, Any]]:
        """
        Perform a quick search with minimal processing.

        Args:
            query: Search query
            num_results: Number of results to return
            format_output: Whether to format as markdown

        Returns:
            Quick search results
        """
        try:
            return await self.search_client.quick_search(
                query=query,
                num_results=num_results,
                format_output=format_output
            )
        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Quick search failed: {str(e)}")

    async def compare_sources(
        self,
        query: str,
        specific_domains: List[str],
        comparison_criteria: List[str] = None
    ) -> str:
        """
        Compare specific sources for a given query.

        Args:
            query: Search query
            specific_domains: List of domains to compare
            comparison_criteria: Criteria for comparison

        Returns:
            Markdown comparison report
        """
        try:
            return await self.search_client.compare_sources(
                query=query,
                specific_domains=specific_domains,
                comparison_criteria=comparison_criteria
            )
        except Exception as e:
            if isinstance(e, WebInfoRetrieverError):
                raise
            else:
                raise WebInfoRetrieverError(f"Source comparison failed: {str(e)}")

    def close(self) -> None:
        """Close the client and cleanup resources."""
        if hasattr(self, 'scraper'):
            self.scraper.close()
        if hasattr(self, 'search_client'):
            self.search_client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
