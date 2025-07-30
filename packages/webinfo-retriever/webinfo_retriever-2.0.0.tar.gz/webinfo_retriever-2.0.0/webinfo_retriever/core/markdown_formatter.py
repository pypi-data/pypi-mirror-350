"""
Advanced markdown formatting for search results and comprehensive reports.
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import urlparse


class MarkdownFormatter:
    """Advanced markdown formatter for search results and analysis reports."""
    
    def __init__(self):
        self.emoji_map = {
            "repository": "📦",
            "tutorial": "📚",
            "documentation": "📖",
            "article": "📰",
            "tool": "🛠️",
            "comparison": "⚖️",
            "research": "🔬",
            "general": "🌐"
        }
    
    def format_search_report(
        self,
        aggregated_results: Dict[str, Any],
        processed_results: List[Any],
        executive_summary: str = None
    ) -> str:
        """
        Format a comprehensive search report in markdown.
        
        Args:
            aggregated_results: Aggregated analysis results
            processed_results: List of processed search results
            executive_summary: Optional executive summary
            
        Returns:
            Formatted markdown report
        """
        query = aggregated_results.get("query", "")
        timestamp = aggregated_results.get("timestamp", datetime.now().isoformat())
        
        # Build the report
        report_parts = []
        
        # Header
        report_parts.append(self._format_header(query, timestamp))
        
        # Executive Summary
        if executive_summary:
            report_parts.append(self._format_executive_summary(executive_summary))
        
        # Quick Stats
        report_parts.append(self._format_quick_stats(aggregated_results))
        
        # Top Sources
        report_parts.append(self._format_top_sources(aggregated_results.get("top_sources", [])))
        
        # Categorized Results
        report_parts.append(self._format_categorized_results(
            aggregated_results.get("categorized_results", {}),
            aggregated_results.get("category_summaries", {})
        ))
        
        # Detailed Results
        successful_results = [r for r in processed_results if r.success]
        report_parts.append(self._format_detailed_results(successful_results))
        
        # Key Insights
        report_parts.append(self._format_key_insights(aggregated_results))
        
        # Related Keywords
        report_parts.append(self._format_related_keywords(aggregated_results.get("common_keywords", [])))
        
        # Processing Metadata
        report_parts.append(self._format_processing_metadata(aggregated_results))
        
        return "\n\n".join(report_parts)
    
    def _format_header(self, query: str, timestamp: str) -> str:
        """Format the report header."""
        formatted_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%B %d, %Y at %I:%M %p")
        
        return f"""# 🔍 Web Search Analysis Report

## Query: "{query}"

**Generated on:** {formatted_timestamp}  
**Powered by:** WebInfo Retriever with Gemini AI

---"""
    
    def _format_executive_summary(self, summary: str) -> str:
        """Format the executive summary section."""
        return f"""## 📋 Executive Summary

{summary}

---"""
    
    def _format_quick_stats(self, aggregated_results: Dict[str, Any]) -> str:
        """Format quick statistics."""
        total_results = aggregated_results.get("total_results", 0)
        successful_results = aggregated_results.get("successful_results", 0)
        success_rate = aggregated_results.get("success_rate", 0) * 100
        processing_time = aggregated_results.get("processing_time", 0)
        
        return f"""## 📊 Quick Statistics

| Metric | Value |
|--------|-------|
| 🔍 **Total Results Found** | {total_results} |
| ✅ **Successfully Processed** | {successful_results} |
| 📈 **Success Rate** | {success_rate:.1f}% |
| ⏱️ **Processing Time** | {processing_time:.2f} seconds |

---"""
    
    def _format_top_sources(self, top_sources: List[Dict[str, Any]]) -> str:
        """Format top sources section."""
        if not top_sources:
            return ""
        
        sources_md = ["## 🏆 Top Sources\n"]
        
        for i, source in enumerate(top_sources, 1):
            emoji = self.emoji_map.get(source.get("category", "general"), "🌐")
            title = source.get("title", "Untitled")
            url = source.get("url", "")
            relevance = source.get("relevance_score", 0) * 100
            quality = source.get("content_quality", 0) * 100
            
            # Truncate long titles
            if len(title) > 80:
                title = title[:77] + "..."
            
            sources_md.append(f"### {i}. {emoji} {title}")
            sources_md.append(f"**URL:** [{self._get_domain(url)}]({url})")
            sources_md.append(f"**Relevance:** {relevance:.0f}% | **Quality:** {quality:.0f}%")
            
            # Add key points if available
            key_points = source.get("key_points", [])
            if key_points:
                sources_md.append("**Key Points:**")
                for point in key_points:
                    sources_md.append(f"- {point}")
            
            sources_md.append("")  # Empty line
        
        sources_md.append("---")
        return "\n".join(sources_md)
    
    def _format_categorized_results(
        self,
        categorized_results: Dict[str, List],
        category_summaries: Dict[str, Any]
    ) -> str:
        """Format categorized results section."""
        if not categorized_results:
            return ""
        
        categories_md = ["## 📂 Results by Category\n"]
        
        # Sort categories by result count
        sorted_categories = sorted(
            categorized_results.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for category, results in sorted_categories:
            emoji = self.emoji_map.get(category, "🌐")
            result_count = len(results)
            
            categories_md.append(f"### {emoji} {category.title()} ({result_count} results)")
            
            # Add category summary if available
            if category in category_summaries:
                summary = category_summaries[category]
                avg_relevance = summary.get("average_relevance", 0) * 100
                categories_md.append(f"**Average Relevance:** {avg_relevance:.0f}%")
                
                # Add common key points
                common_points = summary.get("common_key_points", [])
                if common_points:
                    categories_md.append("**Common Themes:**")
                    for point in common_points[:3]:
                        categories_md.append(f"- {point}")
            
            # List top results in this category
            categories_md.append("**Top Results:**")
            for i, result in enumerate(results[:3], 1):
                title = result.search_result.title
                url = result.search_result.url
                if len(title) > 60:
                    title = title[:57] + "..."
                categories_md.append(f"{i}. [{title}]({url})")
            
            categories_md.append("")  # Empty line
        
        categories_md.append("---")
        return "\n".join(categories_md)
    
    def _format_detailed_results(self, successful_results: List[Any]) -> str:
        """Format detailed results section."""
        if not successful_results:
            return ""
        
        details_md = ["## 📝 Detailed Analysis\n"]
        
        for i, result in enumerate(successful_results[:10], 1):  # Limit to top 10
            search_result = result.search_result
            emoji = self.emoji_map.get(result.content_category, "🌐")
            
            details_md.append(f"### {i}. {emoji} {search_result.title}")
            details_md.append(f"**URL:** [{self._get_domain(search_result.url)}]({search_result.url})")
            details_md.append(f"**Category:** {result.content_category.title()}")
            details_md.append(f"**Source:** {search_result.source.title()}")
            
            # Add relevance scores
            relevance = search_result.relevance_score * 100
            quality = search_result.content_quality * 100
            details_md.append(f"**Relevance:** {relevance:.0f}% | **Quality:** {quality:.0f}%")
            
            # Add snippet
            if search_result.snippet:
                details_md.append(f"**Description:** {search_result.snippet}")
            
            # Add AI summary if available
            if result.ai_summary and result.ai_summary.get("summary"):
                summary = result.ai_summary["summary"]
                if len(summary) > 300:
                    summary = summary[:297] + "..."
                details_md.append(f"**AI Summary:** {summary}")
            
            # Add key points
            if result.key_points:
                details_md.append("**Key Points:**")
                for point in result.key_points[:3]:
                    details_md.append(f"- {point}")
            
            details_md.append("")  # Empty line
        
        details_md.append("---")
        return "\n".join(details_md)
    
    def _format_key_insights(self, aggregated_results: Dict[str, Any]) -> str:
        """Format key insights section."""
        insights_md = ["## 💡 Key Insights\n"]
        
        categorized_results = aggregated_results.get("categorized_results", {})
        
        # Category distribution
        if categorized_results:
            insights_md.append("### 📊 Content Distribution")
            total_results = sum(len(results) for results in categorized_results.values())
            
            for category, results in categorized_results.items():
                percentage = (len(results) / total_results) * 100
                emoji = self.emoji_map.get(category, "🌐")
                insights_md.append(f"- {emoji} **{category.title()}:** {len(results)} results ({percentage:.1f}%)")
        
        # Success rate insights
        success_rate = aggregated_results.get("success_rate", 0) * 100
        if success_rate < 80:
            insights_md.append(f"\n⚠️ **Note:** Success rate is {success_rate:.1f}%. Some sources may have been inaccessible or contained limited content.")
        elif success_rate > 90:
            insights_md.append(f"\n✅ **Excellent:** High success rate of {success_rate:.1f}% indicates comprehensive data coverage.")
        
        insights_md.append("\n---")
        return "\n".join(insights_md)
    
    def _format_related_keywords(self, keywords: List[str]) -> str:
        """Format related keywords section."""
        if not keywords:
            return ""
        
        keywords_md = ["## 🏷️ Related Keywords\n"]
        
        # Group keywords into rows of 5
        keyword_rows = [keywords[i:i+5] for i in range(0, len(keywords), 5)]
        
        for row in keyword_rows:
            keyword_badges = [f"`{keyword}`" for keyword in row]
            keywords_md.append(" ".join(keyword_badges))
        
        keywords_md.append("\n---")
        return "\n".join(keywords_md)
    
    def _format_processing_metadata(self, aggregated_results: Dict[str, Any]) -> str:
        """Format processing metadata section."""
        processing_time = aggregated_results.get("processing_time", 0)
        total_results = aggregated_results.get("total_results", 0)
        
        metadata_md = [
            "## 🔧 Processing Metadata",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| ⏱️ **Total Processing Time** | {processing_time:.2f} seconds |",
            f"| 📊 **Average Time per Result** | {processing_time/max(total_results, 1):.2f} seconds |",
            f"| 🤖 **AI Model** | Gemini 2.0 Flash |",
            f"| 🔍 **Search Engines** | DuckDuckGo, Google, Bing |",
            "",
            "---",
            "",
            "*Report generated by WebInfo Retriever - Advanced Web Information Retrieval & AI Analysis*"
        ]
        
        return "\n".join(metadata_md)
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL for display."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return url
    
    def format_comparison_table(self, results: List[Any], criteria: List[str]) -> str:
        """Format a comparison table for similar results."""
        if len(results) < 2:
            return ""
        
        table_md = ["## ⚖️ Comparison Table\n"]
        
        # Header
        headers = ["Source"] + criteria
        table_md.append("| " + " | ".join(headers) + " |")
        table_md.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # Rows
        for result in results[:5]:  # Limit to 5 results
            row = [f"[{self._get_domain(result.search_result.url)}]({result.search_result.url})"]
            
            for criterion in criteria:
                # Add criterion-specific data
                if criterion == "Relevance":
                    value = f"{result.search_result.relevance_score * 100:.0f}%"
                elif criterion == "Quality":
                    value = f"{result.search_result.content_quality * 100:.0f}%"
                elif criterion == "Category":
                    value = result.content_category.title()
                else:
                    value = "N/A"
                row.append(value)
            
            table_md.append("| " + " | ".join(row) + " |")
        
        table_md.append("")
        return "\n".join(table_md)
