"""
Advanced search client for intelligent web search and summarization.
"""

import asyncio
import time
from typing import Dict, List, Optional, Union, Any

from ..core.intelligent_search import IntelligentSearchEngine
from ..core.search_processor import SearchResultProcessor
from ..core.markdown_formatter import MarkdownFormatter
from ..core.ai_processor import AIProcessor
from ..core.query_processor import NaturalQueryProcessor
from ..utils.config import Config
from ..utils.exceptions import WebInfoRetrieverError
from ..utils.validators import ContentValidator


class SearchClient:
    """
    Advanced search client with intelligent web search and AI-powered analysis.

    Provides comprehensive search capabilities with:
    - Multi-engine web search
    - Concurrent content processing
    - AI-powered summarization
    - Beautiful markdown reporting
    """

    def __init__(self, config: Config):
        self.config = config
        self.search_engine = IntelligentSearchEngine(config)
        self.search_processor = SearchResultProcessor(config)
        self.markdown_formatter = MarkdownFormatter()
        self.ai_processor = AIProcessor(config)
        self.query_processor = NaturalQueryProcessor(config)

    async def intelligent_search(
        self,
        query: str,
        num_results: int = 15,
        max_concurrent: int = 5,
        include_executive_summary: bool = True,
        output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Perform intelligent web search with comprehensive analysis.

        Args:
            query: Search query
            num_results: Number of results to process

            max_concurrent: Maximum concurrent processing tasks
            include_executive_summary: Whether to generate executive summary
            output_format: Output format ('markdown', 'json', 'both')

        Returns:
            Comprehensive search analysis results
        """
        query = ContentValidator.validate_query(query)
        start_time = time.time()

        try:
            # Step 1: Process natural language query
            print(f"🧠 Processing query: {query}")
            processed_query = self.query_processor.process_natural_query(query)
            optimized_query = processed_query['search_query']

            print(f"🔍 Searching for: {optimized_query}")

            # Step 2: Fast URL discovery
            search_results = await self.search_engine.search(
                query=optimized_query,
                num_results=min(num_results, 8)  # Limit for speed
            )

            if not search_results:
                raise WebInfoRetrieverError("No search results found")

            print(f"📊 Found {len(search_results)} search results")

            # Step 2: Process search results
            print(f"⚙️ Processing {len(search_results)} results...")
            processed_results = await self.search_processor.process_search_results(
                search_results=search_results,
                query=query,
                max_concurrent=max_concurrent
            )

            successful_results = [r for r in processed_results if r.success]
            print(f"✅ Successfully processed {len(successful_results)} results")

            # Step 3: Aggregate results
            print("🧠 Aggregating and analyzing results...")
            aggregated_results = self.search_processor.aggregate_results(
                processed_results=processed_results,
                query=query
            )

            # Step 4: Generate executive summary if requested
            executive_summary = None
            if include_executive_summary and successful_results:
                print("📝 Generating executive summary...")
                executive_summary = await self._generate_executive_summary(
                    successful_results, query, aggregated_results
                )

            # Step 5: Format output
            total_time = time.time() - start_time

            result = {
                "query": query,
                "search_results": [r.search_result.to_dict() for r in processed_results],
                "processed_results": [r.to_dict() for r in processed_results],
                "aggregated_analysis": aggregated_results,
                "executive_summary": executive_summary,
                "processing_metadata": {
                    "total_processing_time": total_time,
                    "search_time": aggregated_results.get("processing_time", 0),
                    "num_results_found": len(search_results),
                    "num_results_processed": len(successful_results),
                    "success_rate": len(successful_results) / len(search_results) if search_results else 0
                }
            }

            # Generate markdown report if requested
            if output_format in ["markdown", "both"]:
                print("📄 Generating markdown report...")
                markdown_report = self.markdown_formatter.format_search_report(
                    aggregated_results=aggregated_results,
                    processed_results=processed_results,
                    executive_summary=executive_summary
                )
                result["markdown_report"] = markdown_report

            print(f"🎉 Search analysis complete! ({total_time:.2f}s)")
            return result

        except Exception as e:
            raise WebInfoRetrieverError(f"Intelligent search failed: {str(e)}")

    async def _generate_executive_summary(
        self,
        successful_results: List[Any],
        query: str,
        aggregated_results: Dict[str, Any]
    ) -> str:
        """Generate an executive summary of all search results."""
        try:
            # Combine key information from all results
            combined_content = []

            # Add top summaries
            for result in successful_results[:5]:  # Top 5 results
                if result.ai_summary and result.ai_summary.get("summary"):
                    combined_content.append(f"Source: {result.search_result.title}")
                    combined_content.append(result.ai_summary["summary"])
                    combined_content.append("")

            # Add category insights
            categorized_results = aggregated_results.get("categorized_results", {})
            if categorized_results:
                combined_content.append("Content Categories Found:")
                for category, results in categorized_results.items():
                    combined_content.append(f"- {category.title()}: {len(results)} results")
                combined_content.append("")

            # Add common keywords
            common_keywords = aggregated_results.get("common_keywords", [])
            if common_keywords:
                combined_content.append(f"Key Terms: {', '.join(common_keywords[:10])}")
                combined_content.append("")

            content_text = "\n".join(combined_content)

            # Generate AI summary
            summary_prompt = f"""
            Create a comprehensive executive summary for the search query: "{query}"

            Based on the following research findings, provide:
            1. A clear overview of what was found
            2. Key insights and main themes
            3. Notable patterns or trends
            4. Practical implications or recommendations

            Keep the summary concise but informative (200-400 words).
            """

            loop = asyncio.get_event_loop()
            summary_result = await loop.run_in_executor(
                None,
                self.ai_processor.summarize_content,
                content_text,
                summary_prompt,
                800
            )

            return summary_result.get("summary", "Executive summary generation failed.")

        except Exception as e:
            return f"Executive summary could not be generated: {str(e)}"

    async def fast_search(
        self,
        user_query: str,
        num_results: int = 5
    ) -> str:
        """
        Super fast search with natural language processing.

        Args:
            user_query: Natural language query from user
            num_results: Number of results to process

        Returns:
            Formatted markdown results
        """
        try:
            # Process natural query
            processed = self.query_processor.process_natural_query(user_query)
            search_query = processed['search_query']
            intent = processed.get('intent', 'general')

            print(f"🚀 Fast search: '{user_query}' → '{search_query}'")

            # Quick URL discovery
            search_results = await self.search_engine.search(
                query=search_query,
                num_results=num_results
            )

            if not search_results:
                return f"# Search Results\n\nNo results found for: {user_query}"

            # Format results quickly
            markdown_parts = [
                f"# 🔍 Search Results: {user_query}\n",
                f"**Optimized Query:** {search_query}",
                f"**Intent:** {intent.title()}",
                f"**Found:** {len(search_results)} results\n",
                "---\n"
            ]

            for i, result in enumerate(search_results, 1):
                markdown_parts.append(f"## {i}. {result.title}")
                markdown_parts.append(f"**URL:** {result.url}")
                if result.snippet:
                    markdown_parts.append(f"**Description:** {result.snippet}")
                markdown_parts.append("")

            return "\n".join(markdown_parts)

        except Exception as e:
            return f"# Search Error\n\nFailed to search for: {user_query}\nError: {str(e)}"

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
        query = ContentValidator.validate_query(query)

        try:
            # Quick URL discovery without full processing
            search_results = await self.search_engine.search(
                query=query,
                num_results=num_results
            )

            if format_output:
                # Format as simple markdown
                markdown_parts = [
                    f"# Quick Search: {query}\n",
                    f"Found {len(search_results)} results:\n"
                ]

                for i, result in enumerate(search_results, 1):
                    markdown_parts.append(f"## {i}. {result.title}")
                    markdown_parts.append(f"**URL:** {result.url}")
                    if result.snippet:
                        markdown_parts.append(f"**Description:** {result.snippet}")
                    markdown_parts.append("")

                return "\n".join(markdown_parts)
            else:
                return {
                    "query": query,
                    "results": [result.to_dict() for result in search_results]
                }

        except Exception as e:
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
        if comparison_criteria is None:
            comparison_criteria = ["Relevance", "Quality", "Category"]

        try:
            # Discover URLs and filter for specific domains
            search_results = await self.search_engine.search(
                query=query,
                num_results=20
            )

            # Filter results for specific domains
            filtered_results = []
            for result in search_results:
                for domain in specific_domains:
                    if domain.lower() in result.url.lower():
                        filtered_results.append(result)
                        break

            if not filtered_results:
                return f"# Comparison Results\n\nNo results found for specified domains: {', '.join(specific_domains)}"

            # Process filtered results
            processed_results = await self.search_processor.process_search_results(
                search_results=filtered_results,
                query=query,
                max_concurrent=3
            )

            # Generate comparison report
            comparison_md = [
                f"# Source Comparison: {query}\n",
                f"Comparing {len(processed_results)} sources from specified domains.\n"
            ]

            # Add comparison table
            comparison_table = self.markdown_formatter.format_comparison_table(
                processed_results, comparison_criteria
            )
            comparison_md.append(comparison_table)

            return "\n".join(comparison_md)

        except Exception as e:
            raise WebInfoRetrieverError(f"Source comparison failed: {str(e)}")

    def close(self):
        """Close the search client and cleanup resources."""
        if hasattr(self.search_processor, 'scraper'):
            self.search_processor.scraper.close()
