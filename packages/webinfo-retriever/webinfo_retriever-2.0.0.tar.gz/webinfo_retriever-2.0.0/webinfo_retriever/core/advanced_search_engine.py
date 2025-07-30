"""
Advanced Search Engine - Tavily-like comprehensive search with answer synthesis.
Provides detailed, contextual answers to user queries with proper source attribution.
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai

from .intelligent_search import IntelligentSearchEngine
from .query_processor import NaturalQueryProcessor
from .content_extractor import ContentExtractor
from .scraper import WebScraper
from ..utils.config import Config
from ..utils.exceptions import AIProcessingError, WebInfoRetrieverError
from ..utils.validators import ContentValidator

logger = logging.getLogger(__name__)

@dataclass
class SearchSource:
    """Enhanced search source with relevance scoring."""
    title: str
    url: str
    content: str
    snippet: str
    relevance_score: float
    quality_score: float
    domain_authority: float
    content_type: str
    timestamp: str
    word_count: int
    key_points: List[str]

@dataclass
class ComprehensiveAnswer:
    """Comprehensive answer with multi-source synthesis."""
    query: str
    direct_answer: str
    detailed_analysis: str
    key_insights: List[str]
    sources: List[SearchSource]
    confidence_score: float
    processing_time: float
    source_count: int
    answer_type: str  # factual, analytical, comparative, etc.

class AdvancedSearchEngine:
    """
    Advanced search engine that provides comprehensive, contextual answers
    similar to Tavily AI but faster and more powerful.
    """

    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.gemini_api_key

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=config.get("ai.model", "gemini-2.0-flash"),
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 8192,
                }
            )
        else:
            self.model = None

        # Initialize components
        self.intelligent_search = IntelligentSearchEngine(config)
        self.query_processor = NaturalQueryProcessor(config)
        self.content_extractor = ContentExtractor(config)
        self.scraper = WebScraper(config)

        # Performance settings - Optimized for speed
        self.max_concurrent_sources = 25  # Increased for faster parallel processing
        self.target_response_time = 2.0  # Faster target
        self.fast_mode_sources = 8  # Quick results first
        self.enable_streaming = True  # Stream results as they come

    async def fast_comprehensive_search(
        self,
        query: str,
        num_sources: int = 12,
        include_analysis: bool = True,
        answer_type: str = "comprehensive",
        stream_results: bool = True
    ) -> ComprehensiveAnswer:
        """
        Ultra-fast comprehensive search with parallel processing and streaming results.

        Args:
            query: User's search query
            num_sources: Number of sources to analyze
            include_analysis: Whether to include detailed analysis
            answer_type: Type of answer needed
            stream_results: Whether to stream results as they come

        Returns:
            ComprehensiveAnswer with full detailed information
        """
        start_time = time.time()

        try:
            logger.info(f"🚀 Starting FAST comprehensive search for: {query}")

            # Step 1: Quick query analysis (parallel with source discovery)
            query_analysis_task = asyncio.create_task(self._analyze_query_intent(query))

            # Step 2: Fast parallel source discovery
            sources_task = asyncio.create_task(self._fast_discover_sources(query, num_sources))

            # Wait for both to complete
            query_analysis, initial_sources = await asyncio.gather(
                query_analysis_task, sources_task
            )

            # Step 3: Ultra-fast parallel content processing
            if stream_results:
                processed_sources = await self._stream_process_sources(initial_sources, query)
            else:
                processed_sources = await self._batch_process_sources(initial_sources, query)

            # Step 4: Comprehensive answer synthesis with full content
            answer = await self._synthesize_full_answer(
                query, query_analysis, processed_sources, answer_type
            )

            # Step 5: Final quality assessment
            final_answer = await self._assess_answer_quality(answer, processed_sources)

            processing_time = time.time() - start_time
            final_answer.processing_time = processing_time

            logger.info(f"⚡ FAST comprehensive search completed in {processing_time:.2f}s")
            return final_answer

        except Exception as e:
            logger.error(f"Fast comprehensive search failed: {str(e)}")
            raise WebInfoRetrieverError(f"Fast advanced search failed: {str(e)}")

    async def comprehensive_search(
        self,
        query: str,
        num_sources: int = 12,
        include_analysis: bool = True,
        answer_type: str = "comprehensive"
    ) -> ComprehensiveAnswer:
        """
        Perform comprehensive search with multi-source answer synthesis.

        Args:
            query: User's search query
            num_sources: Number of sources to analyze (default: 12)
            include_analysis: Whether to include detailed analysis
            answer_type: Type of answer needed (comprehensive, factual, comparative)

        Returns:
            ComprehensiveAnswer with synthesized information
        """
        start_time = time.time()

        try:
            logger.info(f"Starting comprehensive search for: {query}")

            # Step 1: Advanced query processing and understanding
            query_analysis = await self._analyze_query_intent(query)

            # Step 2: Multi-strategy source discovery
            sources = await self._discover_and_score_sources(query, query_analysis, num_sources)

            # Step 3: Concurrent content extraction and processing
            processed_sources = await self._process_sources_concurrently(sources, query)

            # Step 4: Multi-source answer synthesis
            answer = await self._synthesize_comprehensive_answer(
                query, query_analysis, processed_sources, answer_type
            )

            # Step 5: Quality assessment and confidence scoring
            final_answer = await self._assess_answer_quality(answer, processed_sources)

            processing_time = time.time() - start_time
            final_answer.processing_time = processing_time

            logger.info(f"Comprehensive search completed in {processing_time:.2f}s")
            return final_answer

        except Exception as e:
            logger.error(f"Comprehensive search failed: {str(e)}")
            raise WebInfoRetrieverError(f"Advanced search failed: {str(e)}")

    async def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze query intent and determine search strategy."""
        if not self.model:
            return {"intent": "general", "complexity": "simple", "keywords": query.split()}

        analysis_prompt = f"""
Analyze this search query and provide detailed intent analysis:

Query: "{query}"

Provide analysis in this exact format:
INTENT: [factual/analytical/comparative/research/tutorial/news/product]
COMPLEXITY: [simple/moderate/complex]
KEYWORDS: [comma-separated key terms]
CONTEXT: [brief context description]
SEARCH_STRATEGY: [broad/focused/multi-angle]
EXPECTED_SOURCES: [academic/news/official/commercial/tutorial]
"""

        try:
            response = self.model.generate_content(analysis_prompt)
            return self._parse_query_analysis(response.text)
        except Exception as e:
            logger.warning(f"Query analysis failed: {e}")
            return {"intent": "general", "complexity": "simple", "keywords": query.split()}

    def _parse_query_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse AI query analysis response."""
        analysis = {}
        lines = analysis_text.strip().split('\n')

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "keywords":
                    analysis[key] = [k.strip() for k in value.split(',')]
                else:
                    analysis[key] = value

        return analysis

    async def _discover_and_score_sources(
        self,
        query: str,
        query_analysis: Dict[str, Any],
        num_sources: int
    ) -> List[Dict[str, Any]]:
        """Discover sources using multiple strategies and score them."""

        # Strategy 1: AI-powered URL discovery
        ai_sources = await self.intelligent_search.discover_relevant_urls(query, num_sources)

        # Strategy 2: Query expansion for broader coverage
        expanded_queries = await self._generate_query_variations(query, query_analysis)

        all_sources = []

        # Collect sources from AI discovery
        for source in ai_sources:
            all_sources.append({
                "url": source.url,
                "title": source.title,
                "snippet": source.snippet,
                "relevance_score": getattr(source, 'relevance_score', 0.7),
                "source_type": "ai_discovery"
            })

        # Add sources from expanded queries (if needed)
        if len(all_sources) < num_sources:
            for expanded_query in expanded_queries[:2]:  # Limit to 2 expansions
                additional_sources = await self.intelligent_search.discover_relevant_urls(
                    expanded_query, max(3, num_sources - len(all_sources))
                )
                for source in additional_sources:
                    if source.url not in [s["url"] for s in all_sources]:
                        all_sources.append({
                            "url": source.url,
                            "title": source.title,
                            "snippet": source.snippet,
                            "relevance_score": getattr(source, 'relevance_score', 0.6),
                            "source_type": "expanded_query"
                        })

        # Score and rank sources
        scored_sources = await self._score_source_quality(all_sources, query)

        # Return top sources
        return sorted(scored_sources, key=lambda x: x["total_score"], reverse=True)[:num_sources]

    async def _generate_query_variations(self, query: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate query variations for broader source discovery."""
        if not self.model:
            return [query]

        variation_prompt = f"""
Generate 3 alternative search queries for: "{query}"

Focus on:
- Different phrasings of the same question
- Related aspects of the topic
- More specific or broader versions

Format as:
1. [variation 1]
2. [variation 2]
3. [variation 3]
"""

        try:
            response = self.model.generate_content(variation_prompt)
            variations = []
            for line in response.text.strip().split('\n'):
                if line.strip() and any(line.startswith(str(i)) for i in range(1, 4)):
                    variation = line.split('.', 1)[1].strip()
                    variations.append(variation)
            return variations
        except Exception:
            return [query]

    async def _score_source_quality(self, sources: List[Dict], query: str) -> List[Dict]:
        """Score source quality based on multiple factors."""
        for source in sources:
            # Domain authority scoring (simplified)
            domain = source["url"].split("//")[1].split("/")[0]
            domain_score = self._calculate_domain_authority(domain)

            # Content relevance scoring
            relevance_score = source.get("relevance_score", 0.5)

            # Title relevance scoring
            title_score = self._calculate_title_relevance(source["title"], query)

            # Combined scoring
            source["domain_authority"] = domain_score
            source["title_relevance"] = title_score
            source["total_score"] = (
                relevance_score * 0.4 +
                domain_score * 0.3 +
                title_score * 0.3
            )

        return sources

    def _calculate_domain_authority(self, domain: str) -> float:
        """Calculate domain authority score (simplified)."""
        high_authority_domains = {
            "wikipedia.org": 0.95,
            "github.com": 0.90,
            "stackoverflow.com": 0.90,
            "docs.python.org": 0.95,
            "developer.mozilla.org": 0.90,
            "tensorflow.org": 0.90,
            "pytorch.org": 0.90,
            "scikit-learn.org": 0.90,
            "realpython.com": 0.85,
            "medium.com": 0.75,
            "towardsdatascience.com": 0.80,
            "arxiv.org": 0.95,
            "nature.com": 0.95,
            "ieee.org": 0.90,
        }

        for auth_domain, score in high_authority_domains.items():
            if auth_domain in domain:
                return score

        # Default scoring based on domain characteristics
        if any(tld in domain for tld in [".edu", ".gov", ".org"]):
            return 0.80
        elif any(tld in domain for tld in [".com", ".net"]):
            return 0.60
        else:
            return 0.50

    def _calculate_title_relevance(self, title: str, query: str) -> float:
        """Calculate title relevance to query."""
        title_lower = title.lower()
        query_lower = query.lower()
        query_words = query_lower.split()

        # Count matching words
        matches = sum(1 for word in query_words if word in title_lower)

        # Calculate relevance score
        if len(query_words) == 0:
            return 0.5

        return min(matches / len(query_words), 1.0)

    async def _fast_discover_sources(self, query: str, num_sources: int) -> List[Dict[str, Any]]:
        """Ultra-fast source discovery with parallel processing."""

        # Create multiple discovery strategies in parallel
        tasks = [
            # Primary AI discovery
            self.intelligent_search.discover_relevant_urls(query, num_sources),
            # Quick query variations
            self._quick_query_expansion(query, max(3, num_sources // 3))
        ]

        # Execute all discovery methods in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_sources = []

        # Process primary results
        if not isinstance(results[0], Exception):
            for source in results[0]:
                all_sources.append({
                    "url": source.url,
                    "title": source.title,
                    "snippet": source.snippet,
                    "relevance_score": getattr(source, 'relevance_score', 0.8),
                    "source_type": "ai_primary"
                })

        # Process expanded query results
        if not isinstance(results[1], Exception):
            for source in results[1]:
                if source.url not in [s["url"] for s in all_sources]:
                    all_sources.append({
                        "url": source.url,
                        "title": source.title,
                        "snippet": source.snippet,
                        "relevance_score": getattr(source, 'relevance_score', 0.7),
                        "source_type": "expanded"
                    })

        # Fast quality scoring
        scored_sources = await self._fast_score_sources(all_sources, query)

        # Return top sources sorted by score
        return sorted(scored_sources, key=lambda x: x["total_score"], reverse=True)[:num_sources]

    async def _quick_query_expansion(self, query: str, num_results: int) -> List[Any]:
        """Quick query expansion for additional sources."""
        try:
            # Simple query variations
            variations = [
                f"{query} tutorial",
                f"{query} guide",
                f"best {query}",
                f"{query} comparison"
            ]

            # Pick the best variation and search
            best_variation = variations[0]  # Simple selection for speed
            return await self.intelligent_search.discover_relevant_urls(best_variation, num_results)
        except Exception:
            return []

    async def _fast_score_sources(self, sources: List[Dict], query: str) -> List[Dict]:
        """Fast source quality scoring."""
        for source in sources:
            # Quick domain scoring
            domain = source["url"].split("//")[1].split("/")[0]
            domain_score = self._calculate_domain_authority(domain)

            # Quick relevance scoring
            relevance_score = source.get("relevance_score", 0.5)

            # Fast title scoring
            title_score = self._calculate_title_relevance(source["title"], query)

            # Combined scoring (optimized weights)
            source["domain_authority"] = domain_score
            source["title_relevance"] = title_score
            source["total_score"] = (
                relevance_score * 0.5 +
                domain_score * 0.3 +
                title_score * 0.2
            )

        return sources

    async def _stream_process_sources(self, sources: List[Dict], query: str) -> List[SearchSource]:
        """Stream process sources as they complete for faster results."""

        # Create semaphore for controlled concurrency
        semaphore = asyncio.Semaphore(self.max_concurrent_sources)

        async def process_single_source_fast(source_data: Dict) -> Optional[SearchSource]:
            async with semaphore:
                try:
                    # Fast scraping with timeout
                    loop = asyncio.get_event_loop()
                    result = await asyncio.wait_for(
                        loop.run_in_executor(None, self.scraper.scrape_url, source_data["url"]),
                        timeout=10.0  # Fast timeout
                    )

                    if not result.get("success"):
                        return None

                    # Fast content extraction
                    content = self.content_extractor.extract_content(result)

                    if not content.get("text") or len(content["text"]) < 50:  # Lower threshold for speed
                        return None

                    # Quick key points and snippet generation
                    key_points = await self._fast_extract_key_points(content["text"], query)
                    snippet = await self._fast_generate_snippet(content["text"], query)

                    return SearchSource(
                        title=source_data["title"],
                        url=source_data["url"],
                        content=content["text"][:8000],  # Increased content length
                        snippet=snippet,
                        relevance_score=source_data["total_score"],
                        quality_score=source_data["domain_authority"],
                        domain_authority=source_data["domain_authority"],
                        content_type=self._classify_content_type(content["text"]),
                        timestamp=str(time.time()),
                        word_count=len(content["text"].split()),
                        key_points=key_points
                    )

                except asyncio.TimeoutError:
                    logger.warning(f"Timeout processing source: {source_data['url']}")
                    return None
                except Exception as e:
                    logger.warning(f"Failed to process source {source_data['url']}: {e}")
                    return None

        # Process all sources concurrently
        tasks = [process_single_source_fast(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter successful results
        processed_sources = []
        for result in results:
            if isinstance(result, SearchSource):
                processed_sources.append(result)

        logger.info(f"⚡ Fast processed {len(processed_sources)}/{len(sources)} sources")
        return processed_sources

    async def _batch_process_sources(self, sources: List[Dict], query: str) -> List[SearchSource]:
        """Batch process sources in optimized chunks."""

        # Process in smaller batches for better control
        batch_size = 8
        all_processed = []

        for i in range(0, len(sources), batch_size):
            batch = sources[i:i + batch_size]
            batch_results = await self._stream_process_sources(batch, query)
            all_processed.extend(batch_results)

            # Quick progress update
            logger.info(f"📊 Processed batch {i//batch_size + 1}, total sources: {len(all_processed)}")

        return all_processed

    async def _fast_extract_key_points(self, content: str, query: str) -> List[str]:
        """Fast key points extraction with optimized processing."""
        if not self.model or len(content) < 50:
            # Fallback: extract sentences containing query keywords
            query_words = query.lower().split()
            sentences = content.split('.')
            relevant_sentences = []

            for sentence in sentences[:10]:  # Check first 10 sentences
                if any(word in sentence.lower() for word in query_words):
                    relevant_sentences.append(sentence.strip())

            return relevant_sentences[:3]

        # Quick content sampling for speed
        content_sample = content[:1500] if len(content) > 1500 else content

        # Optimized prompt for faster processing
        key_points_prompt = f"""
Extract 3 key points from this content for query: "{query}"

Content: {content_sample}

Points:
1.
2.
3.
"""

        try:
            response = self.model.generate_content(key_points_prompt)
            points = []
            for line in response.text.strip().split('\n'):
                if line.strip() and (line.strip().startswith(('1.', '2.', '3.', '-', '•'))):
                    point = line.strip()
                    # Clean up numbering
                    for prefix in ['1.', '2.', '3.', '-', '•']:
                        if point.startswith(prefix):
                            point = point[len(prefix):].strip()
                            break
                    if point:
                        points.append(point)
            return points[:3]  # Limit to 3 for speed
        except Exception:
            return []

    async def _fast_generate_snippet(self, content: str, query: str) -> str:
        """Fast snippet generation with fallback."""
        if not self.model:
            # Fallback: find most relevant paragraph
            paragraphs = content.split('\n\n')
            query_words = query.lower().split()

            best_paragraph = ""
            best_score = 0

            for paragraph in paragraphs[:5]:  # Check first 5 paragraphs
                if len(paragraph) > 100:
                    score = sum(1 for word in query_words if word in paragraph.lower())
                    if score > best_score:
                        best_score = score
                        best_paragraph = paragraph

            return best_paragraph[:300] + "..." if len(best_paragraph) > 300 else best_paragraph

        # Quick AI snippet generation
        content_sample = content[:1000] if len(content) > 1000 else content

        snippet_prompt = f"""
Create a 2-sentence summary of this content for query: "{query}"

Content: {content_sample}

Summary:"""

        try:
            response = self.model.generate_content(snippet_prompt)
            snippet = response.text.strip()
            return snippet if len(snippet) < 400 else snippet[:400] + "..."
        except Exception:
            return content[:200] + "..." if len(content) > 200 else content

    async def _synthesize_full_answer(
        self,
        query: str,
        query_analysis: Dict[str, Any],
        sources: List[SearchSource],
        answer_type: str
    ) -> ComprehensiveAnswer:
        """Synthesize comprehensive answer with full content and no truncation."""

        if not self.model or not sources:
            return self._create_fallback_answer(query, sources)

        # Prepare comprehensive source summaries with full content
        source_summaries = []
        for i, source in enumerate(sources, 1):
            # Include more content for comprehensive analysis
            summary = f"""
Source {i}: {source.title}
URL: {source.url}
Content Type: {source.content_type}
Quality Score: {source.quality_score:.2f}
Word Count: {source.word_count}

Key Points:
{chr(10).join(f"- {point}" for point in source.key_points)}

Content Summary: {source.snippet}

Full Content Sample: {source.content[:2000]}...
"""
            source_summaries.append(summary)

        # Enhanced synthesis prompt for comprehensive answers
        synthesis_prompt = f"""
You are an expert research analyst. Provide a comprehensive, detailed answer to this query using ALL the provided sources.

Query: "{query}"
Query Intent: {query_analysis.get('intent', 'general')}
Answer Type: {answer_type}

Sources ({len(sources)} total):
{chr(10).join(source_summaries)}

Provide your response in this exact format:

DIRECT_ANSWER:
[Provide a clear, comprehensive answer to the query in 3-4 sentences. Include specific details and examples from the sources.]

DETAILED_ANALYSIS:
[Provide an extensive analysis synthesizing information from ALL sources. Include:
- Specific details, examples, and insights from each source
- Comparisons and contrasts between different sources
- Technical details and explanations
- Practical applications and recommendations
- Reference sources naturally throughout the text
- Make this section comprehensive and detailed - do NOT truncate or summarize briefly]

KEY_INSIGHTS:
- [Key insight 1 with specific details]
- [Key insight 2 with specific details]
- [Key insight 3 with specific details]
- [Key insight 4 with specific details]
- [Key insight 5 with specific details]

CONFIDENCE_ASSESSMENT:
[Rate confidence from 0.1 to 1.0 based on source quality, consistency, and comprehensiveness]

Requirements:
- Use information from ALL {len(sources)} sources
- Provide comprehensive, detailed analysis - do NOT truncate
- Include specific examples, technical details, and practical information
- Reference sources naturally throughout the text
- Synthesize information, don't just list facts
- Make the analysis thorough and complete
- Ensure no important information is cut off or abbreviated
"""

        try:
            response = self.model.generate_content(synthesis_prompt)
            return self._parse_comprehensive_answer(query, response.text, sources)
        except Exception as e:
            logger.error(f"Answer synthesis failed: {e}")
            return self._create_enhanced_fallback_answer(query, sources)

    def _create_enhanced_fallback_answer(self, query: str, sources: List[SearchSource]) -> ComprehensiveAnswer:
        """Create enhanced fallback answer with full content."""

        if not sources:
            return ComprehensiveAnswer(
                query=query,
                direct_answer="I couldn't find sufficient information to answer your query.",
                detailed_analysis="No reliable sources were found for this query.",
                key_insights=[],
                sources=[],
                confidence_score=0.1,
                processing_time=0.0,
                source_count=0,
                answer_type="insufficient_data"
            )

        # Create comprehensive answer from all sources
        top_source = sources[0]
        direct_answer = f"Based on {len(sources)} comprehensive sources, {top_source.snippet}"

        # Detailed analysis with full content from all sources
        detailed_analysis = f"Comprehensive Analysis based on {len(sources)} sources:\n\n"

        for i, source in enumerate(sources, 1):
            detailed_analysis += f"## Source {i}: {source.title}\n"
            detailed_analysis += f"**URL:** {source.url}\n"
            detailed_analysis += f"**Quality Score:** {source.quality_score:.1%}\n"
            detailed_analysis += f"**Content Type:** {source.content_type}\n"
            detailed_analysis += f"**Word Count:** {source.word_count:,}\n\n"

            detailed_analysis += f"**Summary:** {source.snippet}\n\n"

            if source.key_points:
                detailed_analysis += "**Key Points:**\n"
                for point in source.key_points:
                    detailed_analysis += f"- {point}\n"
                detailed_analysis += "\n"

            # Include substantial content sample
            detailed_analysis += f"**Content Analysis:** {source.content[:1500]}...\n\n"
            detailed_analysis += "---\n\n"

        # Collect all key insights
        key_insights = []
        for source in sources:
            key_insights.extend(source.key_points)

        return ComprehensiveAnswer(
            query=query,
            direct_answer=direct_answer,
            detailed_analysis=detailed_analysis,
            key_insights=key_insights[:8],  # More insights
            sources=sources,
            confidence_score=0.7,
            processing_time=0.0,
            source_count=len(sources),
            answer_type="enhanced_fallback"
        )

    async def _process_sources_concurrently(
        self,
        sources: List[Dict],
        query: str
    ) -> List[SearchSource]:
        """Process multiple sources concurrently for speed."""

        async def process_single_source(source_data: Dict) -> Optional[SearchSource]:
            try:
                # Extract content from URL
                result = self.scraper.scrape_url(source_data["url"])
                if not result.get("success"):
                    return None

                # Extract and process content
                content = self.content_extractor.extract_content(result)

                if not content.get("text") or len(content["text"]) < 100:
                    return None

                # Generate key points and snippet
                key_points = await self._extract_key_points(content["text"], query)
                snippet = await self._generate_contextual_snippet(content["text"], query)

                return SearchSource(
                    title=source_data["title"],
                    url=source_data["url"],
                    content=content["text"][:5000],  # Limit content length
                    snippet=snippet,
                    relevance_score=source_data["total_score"],
                    quality_score=source_data["domain_authority"],
                    domain_authority=source_data["domain_authority"],
                    content_type=self._classify_content_type(content["text"]),
                    timestamp=str(time.time()),
                    word_count=len(content["text"].split()),
                    key_points=key_points
                )

            except Exception as e:
                logger.warning(f"Failed to process source {source_data['url']}: {e}")
                return None

        # Process sources concurrently with limited concurrency
        semaphore = asyncio.Semaphore(self.max_concurrent_sources)

        async def process_with_semaphore(source_data):
            async with semaphore:
                return await process_single_source(source_data)

        # Execute concurrent processing
        tasks = [process_with_semaphore(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter successful results
        processed_sources = []
        for result in results:
            if isinstance(result, SearchSource):
                processed_sources.append(result)

        logger.info(f"Successfully processed {len(processed_sources)}/{len(sources)} sources")
        return processed_sources

    async def _extract_key_points(self, content: str, query: str) -> List[str]:
        """Extract key points relevant to the query."""
        if not self.model or len(content) < 100:
            return []

        # Truncate content if too long
        content_sample = content[:2000] if len(content) > 2000 else content

        key_points_prompt = f"""
Extract 3-5 key points from this content that are most relevant to the query: "{query}"

Content: {content_sample}

Format as:
- [key point 1]
- [key point 2]
- [key point 3]
"""

        try:
            response = self.model.generate_content(key_points_prompt)
            points = []
            for line in response.text.strip().split('\n'):
                if line.strip().startswith('-'):
                    point = line.strip()[1:].strip()
                    if point:
                        points.append(point)
            return points[:5]  # Limit to 5 points
        except Exception:
            return []

    async def _generate_contextual_snippet(self, content: str, query: str) -> str:
        """Generate a contextual snippet relevant to the query."""
        if not self.model:
            # Fallback: return first 200 characters
            return content[:200] + "..." if len(content) > 200 else content

        content_sample = content[:1500] if len(content) > 1500 else content

        snippet_prompt = f"""
Create a concise 2-3 sentence snippet from this content that directly answers or relates to: "{query}"

Content: {content_sample}

Snippet:"""

        try:
            response = self.model.generate_content(snippet_prompt)
            snippet = response.text.strip()
            return snippet if len(snippet) < 300 else snippet[:300] + "..."
        except Exception:
            return content[:200] + "..." if len(content) > 200 else content

    def _classify_content_type(self, content: str) -> str:
        """Classify content type based on content analysis."""
        content_lower = content.lower()

        if any(word in content_lower for word in ["tutorial", "how to", "step by step", "guide"]):
            return "tutorial"
        elif any(word in content_lower for word in ["research", "study", "analysis", "findings"]):
            return "research"
        elif any(word in content_lower for word in ["news", "breaking", "reported", "announced"]):
            return "news"
        elif any(word in content_lower for word in ["documentation", "docs", "api", "reference"]):
            return "documentation"
        elif any(word in content_lower for word in ["review", "comparison", "vs", "versus"]):
            return "comparison"
        else:
            return "general"

    async def _synthesize_comprehensive_answer(
        self,
        query: str,
        query_analysis: Dict[str, Any],
        sources: List[SearchSource],
        answer_type: str
    ) -> ComprehensiveAnswer:
        """Synthesize comprehensive answer from multiple sources."""

        if not self.model or not sources:
            return self._create_fallback_answer(query, sources)

        # Prepare source summaries for synthesis
        source_summaries = []
        for i, source in enumerate(sources[:10], 1):  # Limit to top 10 sources
            summary = f"""
Source {i}: {source.title}
URL: {source.url}
Key Points: {'; '.join(source.key_points[:3])}
Snippet: {source.snippet}
Quality Score: {source.quality_score:.2f}
"""
            source_summaries.append(summary)

        # Create synthesis prompt
        synthesis_prompt = f"""
You are an expert research analyst. Provide a comprehensive answer to this query using the provided sources.

Query: "{query}"
Query Intent: {query_analysis.get('intent', 'general')}
Answer Type: {answer_type}

Sources:
{chr(10).join(source_summaries)}

Provide your response in this exact format:

DIRECT_ANSWER:
[Provide a clear, direct answer to the query in 2-3 sentences]

DETAILED_ANALYSIS:
[Provide a comprehensive analysis synthesizing information from multiple sources. Include specific details, examples, and insights. Reference sources naturally in the text.]

KEY_INSIGHTS:
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]
- [Key insight 4]

CONFIDENCE_ASSESSMENT:
[Rate confidence from 0.1 to 1.0 based on source quality and consistency]

Requirements:
- Synthesize information from multiple sources, don't just summarize individual sources
- Provide specific, actionable information
- Maintain factual accuracy and cite sources naturally
- Identify patterns and connections across sources
- Address the query comprehensively
"""

        try:
            response = self.model.generate_content(synthesis_prompt)
            return self._parse_comprehensive_answer(query, response.text, sources)
        except Exception as e:
            logger.error(f"Answer synthesis failed: {e}")
            return self._create_fallback_answer(query, sources)

    def _parse_comprehensive_answer(
        self,
        query: str,
        response_text: str,
        sources: List[SearchSource]
    ) -> ComprehensiveAnswer:
        """Parse the AI-generated comprehensive answer."""

        sections = {}
        current_section = None
        current_content = []

        lines = response_text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if line.endswith(':') and line.replace(':', '').replace('_', '').isalpha():
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.replace(':', '').lower()
                current_content = []
            else:
                current_content.append(line)

        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        # Extract key insights
        key_insights = []
        insights_text = sections.get('key_insights', '')
        for line in insights_text.split('\n'):
            if line.strip().startswith('-'):
                insight = line.strip()[1:].strip()
                if insight:
                    key_insights.append(insight)

        # Extract confidence score
        confidence_score = 0.7  # Default
        confidence_text = sections.get('confidence_assessment', '')
        try:
            import re
            confidence_match = re.search(r'(\d+\.?\d*)', confidence_text)
            if confidence_match:
                confidence_score = float(confidence_match.group(1))
                if confidence_score > 1.0:
                    confidence_score = confidence_score / 10  # Handle percentage format
        except:
            pass

        return ComprehensiveAnswer(
            query=query,
            direct_answer=sections.get('direct_answer', ''),
            detailed_analysis=sections.get('detailed_analysis', ''),
            key_insights=key_insights,
            sources=sources,
            confidence_score=min(max(confidence_score, 0.1), 1.0),
            processing_time=0.0,  # Will be set later
            source_count=len(sources),
            answer_type=self._determine_answer_type(sections.get('direct_answer', ''))
        )

    def _determine_answer_type(self, direct_answer: str) -> str:
        """Determine the type of answer based on content."""
        answer_lower = direct_answer.lower()

        if any(word in answer_lower for word in ["compare", "versus", "difference", "better"]):
            return "comparative"
        elif any(word in answer_lower for word in ["how to", "steps", "process", "method"]):
            return "instructional"
        elif any(word in answer_lower for word in ["because", "due to", "reason", "caused"]):
            return "explanatory"
        elif any(word in answer_lower for word in ["is", "are", "definition", "means"]):
            return "factual"
        else:
            return "comprehensive"

    def _create_fallback_answer(self, query: str, sources: List[SearchSource]) -> ComprehensiveAnswer:
        """Create fallback answer when AI synthesis fails."""

        if not sources:
            return ComprehensiveAnswer(
                query=query,
                direct_answer="I couldn't find sufficient information to answer your query.",
                detailed_analysis="No reliable sources were found for this query.",
                key_insights=[],
                sources=[],
                confidence_score=0.1,
                processing_time=0.0,
                source_count=0,
                answer_type="insufficient_data"
            )

        # Create basic answer from top sources
        top_source = sources[0]
        direct_answer = f"Based on available sources, {top_source.snippet}"

        detailed_analysis = f"Analysis based on {len(sources)} sources:\n\n"
        for i, source in enumerate(sources[:5], 1):
            detailed_analysis += f"{i}. {source.title}: {source.snippet}\n\n"

        key_insights = []
        for source in sources[:3]:
            key_insights.extend(source.key_points[:2])

        return ComprehensiveAnswer(
            query=query,
            direct_answer=direct_answer,
            detailed_analysis=detailed_analysis,
            key_insights=key_insights[:5],
            sources=sources,
            confidence_score=0.6,
            processing_time=0.0,
            source_count=len(sources),
            answer_type="basic"
        )

    async def _assess_answer_quality(
        self,
        answer: ComprehensiveAnswer,
        sources: List[SearchSource]
    ) -> ComprehensiveAnswer:
        """Assess and potentially improve answer quality."""

        # Quality metrics
        source_quality_avg = sum(s.quality_score for s in sources) / len(sources) if sources else 0
        content_completeness = min(len(answer.detailed_analysis) / 500, 1.0)  # Target 500+ chars
        insight_count = len(answer.key_insights)

        # Adjust confidence based on quality metrics
        quality_adjustment = (
            source_quality_avg * 0.4 +
            content_completeness * 0.3 +
            min(insight_count / 4, 1.0) * 0.3
        )

        answer.confidence_score = min(answer.confidence_score * quality_adjustment, 1.0)

        return answer
