"""
Fixed Advanced answer formatter for comprehensive search results.
Creates beautiful, structured output with proper color highlighting.
"""

import json
from typing import Dict, List, Any
from datetime import datetime

from .advanced_search_engine import ComprehensiveAnswer, SearchSource


class AdvancedAnswerFormatter:
    """Format comprehensive answers into beautiful, structured output."""

    def __init__(self):
        self.confidence_levels = {
            (0.9, 1.0): "Very High",
            (0.8, 0.9): "High",
            (0.7, 0.8): "Good",
            (0.6, 0.7): "Moderate",
            (0.5, 0.6): "Fair",
            (0.0, 0.5): "Low"
        }

    def format_comprehensive_answer(
        self,
        answer: ComprehensiveAnswer,
        format_type: str = "markdown"
    ) -> str:
        """Format comprehensive answer into specified format."""

        if format_type == "markdown":
            return self._format_markdown(answer)
        elif format_type == "markdown_file":
            return self._format_markdown_file(answer)
        elif format_type == "terminal":
            return self._format_terminal(answer)
        elif format_type == "json":
            return self._format_json(answer)
        elif format_type == "text":
            return self._format_text(answer)
        else:
            return self._format_terminal(answer)

    def _format_markdown(self, answer: ComprehensiveAnswer) -> str:
        """Format answer as beautiful markdown with enhanced colors and full content."""

        confidence_level = self._get_confidence_level(answer.confidence_score)
        confidence_color = self._get_confidence_color(answer.confidence_score)

        # Calculate metrics
        total_sources = len(answer.sources)
        avg_quality = sum(s.quality_score for s in answer.sources) / len(answer.sources) if answer.sources else 0
        processing_time = answer.processing_time
        confidence_score = answer.confidence_score
        key_insights_count = len(answer.key_insights)
        total_words = sum(s.word_count for s in answer.sources)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Start building markdown
        markdown = f"""# 🔍 **COMPREHENSIVE SEARCH ANALYSIS**

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 20px 0;">

## 🎯 **Query:** "{answer.query}"

</div>

---

## 📋 **DIRECT ANSWER**

<div style="background: #f8f9fa; border-left: 5px solid #28a745; padding: 15px; margin: 15px 0; border-radius: 5px;">

### {answer.direct_answer}

</div>

<div style="display: flex; gap: 20px; margin: 20px 0;">
<div style="background: {confidence_color}; color: white; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
<strong>Confidence Level</strong><br>{confidence_level} ({answer.confidence_score:.1%})
</div>
<div style="background: #6c757d; color: white; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
<strong>Answer Type</strong><br>{answer.answer_type.title()}
</div>
<div style="background: #17a2b8; color: white; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
<strong>Processing Time</strong><br>{answer.processing_time:.2f}s
</div>
<div style="background: #fd7e14; color: white; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
<strong>Sources Analyzed</strong><br>{answer.source_count}
</div>
</div>

---

## 📊 **COMPREHENSIVE DETAILED ANALYSIS**

<div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 10px; margin: 20px 0;">

{self._format_detailed_analysis(answer.detailed_analysis)}

</div>

---

## 💡 **KEY INSIGHTS & DISCOVERIES**

<div style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 20px; border-radius: 10px; margin: 20px 0;">

"""

        # Add insights with colors
        for i, insight in enumerate(answer.key_insights, 1):
            insight_color = self._get_insight_color(i)
            markdown += f"""
<div style="background: {insight_color}; color: white; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 5px solid #fff;">
<strong>🔍 Insight {i}:</strong> {insight}
</div>
"""

        markdown += """
</div>

---

## 📚 **COMPREHENSIVE SOURCES ANALYSIS**

<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">

"""

        # Add sources
        for i, source in enumerate(answer.sources, 1):
            quality_indicator = self._get_quality_indicator(source.quality_score)
            content_type_emoji = self._get_content_type_emoji(source.content_type)
            source_color = self._get_source_color(source.quality_score)

            markdown += f"""
<div style="background: white; border: 2px solid {source_color}; padding: 20px; margin: 15px 0; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

### {i}. {content_type_emoji} **{source.title}**

<div style="background: {source_color}; color: white; padding: 10px; border-radius: 8px; margin: 10px 0;">
<strong>🔗 URL:</strong> <a href="{source.url}" style="color: white; text-decoration: underline;">{source.url}</a>
</div>

<div style="display: flex; gap: 15px; margin: 15px 0;">
<div style="background: #28a745; color: white; padding: 8px 12px; border-radius: 6px; text-align: center; flex: 1;">
<strong>Quality</strong><br>{quality_indicator}
</div>
<div style="background: #6f42c1; color: white; padding: 8px 12px; border-radius: 6px; text-align: center; flex: 1;">
<strong>Type</strong><br>{source.content_type.title()}
</div>
<div style="background: #fd7e14; color: white; padding: 8px 12px; border-radius: 6px; text-align: center; flex: 1;">
<strong>Words</strong><br>{source.word_count:,}
</div>
<div style="background: #20c997; color: white; padding: 8px 12px; border-radius: 6px; text-align: center; flex: 1;">
<strong>Relevance</strong><br>{source.relevance_score:.1%}
</div>
</div>

<div style="background: #e9ecef; padding: 15px; border-radius: 8px; margin: 15px 0;">
<strong>📝 Summary:</strong> {source.snippet}
</div>

"""

            if source.key_points:
                markdown += """
<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0;">
<strong>🎯 Key Points:</strong>
<ul style="margin: 10px 0; padding-left: 20px;">
"""
                for point in source.key_points:
                    markdown += f"<li style='margin: 5px 0; color: #495057;'>{point}</li>\n"
                markdown += "</ul>\n</div>\n"

            # Add content preview if available
            if hasattr(source, 'content') and source.content:
                content_preview = source.content[:800] + "..." if len(source.content) > 800 else source.content
                markdown += f"""
<div style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 8px;">
<strong>📄 Content Preview:</strong>
<div style="font-family: monospace; font-size: 0.9em; color: #495057; margin-top: 10px; max-height: 300px; overflow-y: auto;">
{content_preview}
</div>
</div>
"""

            markdown += "</div>\n"

        # Add metrics section
        markdown += "</div>\n\n---\n\n"
        markdown += "## 📈 **COMPREHENSIVE ANALYSIS METRICS**\n\n"
        markdown += '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 20px 0;">\n\n'
        markdown += '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">\n\n'

        # Add metric cards safely
        metrics = [
            (total_sources, "Total Sources"),
            (f"{avg_quality:.0%}", "Avg Quality"),
            (f"{processing_time:.1f}s", "Processing Time"),
            (f"{confidence_score:.0%}", "Confidence Score"),
            (key_insights_count, "Key Insights"),
            (f"{total_words:,}", "Words Analyzed")
        ]

        for value, label in metrics:
            markdown += f'<div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; text-align: center; color: white;">\n'
            markdown += f'<div style="font-size: 2em; font-weight: bold;">{value}</div>\n'
            markdown += f'<div>{label}</div>\n</div>\n\n'

        markdown += '</div>\n\n</div>\n\n---\n\n'

        # Add footer
        markdown += f'<div style="background: #343a40; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">\n'
        markdown += f'<strong>🚀 Generated by WebInfo Retriever Advanced Search Engine</strong><br>\n'
        markdown += f'<em>⏰ Timestamp: {timestamp} | 🔥 Ultra-Fast Parallel Processing</em>\n'
        markdown += f'</div>\n'

        return markdown

    def _format_markdown_file(self, answer: ComprehensiveAnswer) -> str:
        """Format answer as beautiful markdown file with HTML styling."""
        return self._format_markdown(answer)

    def _format_terminal(self, answer: ComprehensiveAnswer) -> str:
        """Format answer for clean terminal display without HTML tags."""

        confidence_level = self._get_confidence_level(answer.confidence_score)

        # Calculate metrics
        total_sources = len(answer.sources)
        avg_quality = sum(s.quality_score for s in answer.sources) / len(answer.sources) if answer.sources else 0
        processing_time = answer.processing_time
        confidence_score = answer.confidence_score
        key_insights_count = len(answer.key_insights)
        total_words = sum(s.word_count for s in answer.sources)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build clean terminal output
        output = f"""
🔍 COMPREHENSIVE SEARCH ANALYSIS
{'='*60}

🎯 QUERY: "{answer.query}"

📋 DIRECT ANSWER:
{'-'*20}
{answer.direct_answer}

📊 SUMMARY METRICS:
• Confidence Level: {confidence_level} ({answer.confidence_score:.1%})
• Answer Type: {answer.answer_type.title()}
• Processing Time: {answer.processing_time:.2f}s
• Sources Analyzed: {answer.source_count}

💡 KEY INSIGHTS & DISCOVERIES:
{'-'*35}
"""

        # Add insights
        for i, insight in enumerate(answer.key_insights, 1):
            output += f"{i}. {insight}\n"

        # Add detailed analysis if available
        if answer.detailed_analysis and answer.detailed_analysis.strip():
            clean_analysis = self._clean_html_tags(answer.detailed_analysis)
            output += f"\n📊 DETAILED ANALYSIS:\n{'-'*25}\n{clean_analysis}\n"

        output += f"\n📚 COMPREHENSIVE SOURCES ANALYSIS:\n{'-'*40}\n"

        # Add sources
        for i, source in enumerate(answer.sources, 1):
            quality_indicator = self._get_quality_indicator_text(source.quality_score)
            content_type_emoji = self._get_content_type_emoji(source.content_type)

            output += f"""
{i}. {content_type_emoji} {source.title}
   🔗 URL: {source.url}
   📊 Quality: {quality_indicator} ({source.quality_score:.1%})
   📝 Type: {source.content_type.title()}
   📄 Words: {source.word_count:,}
   🎯 Relevance: {source.relevance_score:.1%}

   📝 Summary: {source.snippet}
"""

            if source.key_points:
                output += "   🎯 Key Points:\n"
                for point in source.key_points:
                    output += f"   • {point}\n"

            # Add content preview
            if hasattr(source, 'content') and source.content:
                content_preview = source.content[:400] + "..." if len(source.content) > 400 else source.content
                output += f"   📄 Content Preview: {content_preview}\n"

            output += f"   {'-'*50}\n"

        # Add metrics section
        output += f"""
📈 COMPREHENSIVE ANALYSIS METRICS:
{'='*40}
• Total Sources: {total_sources}
• Average Quality: {avg_quality:.0%}
• Processing Time: {processing_time:.1f}s
• Confidence Score: {confidence_score:.0%}
• Key Insights: {key_insights_count}
• Words Analyzed: {total_words:,}

🚀 Generated by WebInfo Retriever Advanced Search Engine
⏰ Timestamp: {timestamp} | 🔥 Ultra-Fast Parallel Processing
"""

        return output

    def _format_json(self, answer: ComprehensiveAnswer) -> str:
        """Format answer as structured JSON."""

        data = {
            "query": answer.query,
            "direct_answer": answer.direct_answer,
            "detailed_analysis": answer.detailed_analysis,
            "key_insights": answer.key_insights,
            "confidence_score": answer.confidence_score,
            "confidence_level": self._get_confidence_level(answer.confidence_score),
            "answer_type": answer.answer_type,
            "processing_time": answer.processing_time,
            "source_count": answer.source_count,
            "sources": [
                {
                    "title": source.title,
                    "url": source.url,
                    "snippet": source.snippet,
                    "content_type": source.content_type,
                    "quality_score": source.quality_score,
                    "relevance_score": source.relevance_score,
                    "domain_authority": source.domain_authority,
                    "word_count": source.word_count,
                    "key_points": source.key_points,
                    "timestamp": source.timestamp
                }
                for source in answer.sources
            ],
            "metadata": {
                "total_words_analyzed": sum(s.word_count for s in answer.sources),
                "average_source_quality": sum(s.quality_score for s in answer.sources) / len(answer.sources) if answer.sources else 0,
                "generated_at": datetime.now().isoformat(),
                "engine_version": "WebInfo Retriever Advanced v1.0"
            }
        }

        return json.dumps(data, indent=2, ensure_ascii=False)

    def _format_text(self, answer: ComprehensiveAnswer) -> str:
        """Format answer as clean text."""

        confidence_level = self._get_confidence_level(answer.confidence_score)

        text = f"""COMPREHENSIVE SEARCH ANALYSIS
{'=' * 50}

Query: {answer.query}

DIRECT ANSWER:
{answer.direct_answer}

Confidence: {confidence_level} ({answer.confidence_score:.1%})
Processing Time: {answer.processing_time:.2f}s
Sources: {answer.source_count}

DETAILED ANALYSIS:
{'-' * 20}
{answer.detailed_analysis}

KEY INSIGHTS:
{'-' * 15}
"""

        for i, insight in enumerate(answer.key_insights, 1):
            text += f"{i}. {insight}\n"

        text += f"\nSOURCES:\n{'-' * 10}\n"

        for i, source in enumerate(answer.sources, 1):
            text += f"""
{i}. {source.title}
   URL: {source.url}
   Quality: {source.quality_score:.1%}
   Type: {source.content_type}
   Summary: {source.snippet}
"""

            if source.key_points:
                text += "   Key Points:\n"
                for point in source.key_points:
                    text += f"   - {point}\n"

        text += f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        return text

    def _get_confidence_level(self, score: float) -> str:
        """Get confidence level description."""
        for (min_score, max_score), level in self.confidence_levels.items():
            if min_score <= score < max_score:
                return level
        return "Unknown"

    def _get_quality_indicator(self, score: float) -> str:
        """Get quality indicator emoji."""
        if score >= 0.9:
            return "🟢 Excellent"
        elif score >= 0.8:
            return "🔵 Very Good"
        elif score >= 0.7:
            return "🟡 Good"
        elif score >= 0.6:
            return "🟠 Fair"
        else:
            return "🔴 Poor"

    def _get_quality_indicator_text(self, score: float) -> str:
        """Get quality indicator text for terminal."""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.8:
            return "Very Good"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        else:
            return "Poor"

    def _get_content_type_emoji(self, content_type: str) -> str:
        """Get emoji for content type."""
        emoji_map = {
            "tutorial": "📚",
            "research": "🔬",
            "news": "📰",
            "documentation": "📖",
            "comparison": "⚖️",
            "general": "📄"
        }
        return emoji_map.get(content_type, "📄")

    def _get_confidence_color(self, score: float) -> str:
        """Get color based on confidence score."""
        if score >= 0.9:
            return "#28a745"  # Green
        elif score >= 0.8:
            return "#20c997"  # Teal
        elif score >= 0.7:
            return "#ffc107"  # Yellow
        elif score >= 0.6:
            return "#fd7e14"  # Orange
        else:
            return "#dc3545"  # Red

    def _get_source_color(self, quality_score: float) -> str:
        """Get color based on source quality."""
        if quality_score >= 0.9:
            return "#28a745"  # Green
        elif quality_score >= 0.8:
            return "#17a2b8"  # Blue
        elif quality_score >= 0.7:
            return "#6f42c1"  # Purple
        elif quality_score >= 0.6:
            return "#fd7e14"  # Orange
        else:
            return "#6c757d"  # Gray

    def _get_insight_color(self, index: int) -> str:
        """Get color for insights based on index."""
        colors = [
            "#007bff",  # Blue
            "#28a745",  # Green
            "#17a2b8",  # Teal
            "#ffc107",  # Yellow
            "#6f42c1",  # Purple
            "#fd7e14",  # Orange
            "#20c997",  # Cyan
            "#e83e8c"   # Pink
        ]
        return colors[(index - 1) % len(colors)]

    def _format_detailed_analysis(self, analysis: str) -> str:
        """Format detailed analysis with enhanced styling."""
        if not analysis:
            return "No detailed analysis available."

        # Split into paragraphs and format each
        paragraphs = analysis.split('\n\n')
        formatted_paragraphs = []

        for paragraph in paragraphs:
            if paragraph.strip():
                # Check if it's a heading
                if paragraph.startswith('#'):
                    # Convert markdown headings to styled divs
                    level = len(paragraph) - len(paragraph.lstrip('#'))
                    text = paragraph.lstrip('# ').strip()
                    color = self._get_heading_color(level)
                    formatted_paragraphs.append(
                        f'<div style="background: {color}; color: white; padding: 10px; '
                        f'border-radius: 6px; margin: 15px 0; font-weight: bold;">{text}</div>'
                    )
                else:
                    # Regular paragraph with enhanced styling
                    formatted_paragraphs.append(
                        f'<p style="line-height: 1.6; margin: 15px 0; color: #495057;">{paragraph.strip()}</p>'
                    )

        return '\n'.join(formatted_paragraphs)

    def _get_heading_color(self, level: int) -> str:
        """Get color for headings based on level."""
        colors = {
            1: "#007bff",  # Blue
            2: "#28a745",  # Green
            3: "#17a2b8",  # Teal
            4: "#ffc107",  # Yellow
            5: "#6f42c1",  # Purple
            6: "#fd7e14"   # Orange
        }
        return colors.get(level, "#6c757d")

    def _clean_html_tags(self, text: str) -> str:
        """Remove HTML tags and clean text for terminal display."""
        import re

        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)

        # Replace HTML entities
        clean_text = clean_text.replace('&nbsp;', ' ')
        clean_text = clean_text.replace('&amp;', '&')
        clean_text = clean_text.replace('&lt;', '<')
        clean_text = clean_text.replace('&gt;', '>')
        clean_text = clean_text.replace('&quot;', '"')

        # Clean up extra whitespace
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
        clean_text = re.sub(r' +', ' ', clean_text)

        return clean_text.strip()

    def create_quick_summary(self, answer: ComprehensiveAnswer) -> str:
        """Create a quick summary for fast display."""

        summary = f"""🔍 **{answer.query}**

**Answer:** {answer.direct_answer}

**Confidence:** {self._get_confidence_level(answer.confidence_score)} ({answer.confidence_score:.1%})
**Sources:** {answer.source_count} | **Time:** {answer.processing_time:.1f}s

**Top Insights:**
"""

        for insight in answer.key_insights[:3]:
            summary += f"• {insight}\n"

        if len(answer.sources) > 0:
            top_source = answer.sources[0]
            summary += f"\n**Top Source:** [{top_source.title}]({top_source.url})"

        return summary

    def create_citation_list(self, answer: ComprehensiveAnswer) -> str:
        """Create a formatted citation list."""

        citations = "## 📚 Citations\n\n"

        for i, source in enumerate(answer.sources, 1):
            citations += f"{i}. **{source.title}**. Retrieved from {source.url}\n"
            citations += f"   *Quality Score: {source.quality_score:.1%}, Content Type: {source.content_type}*\n\n"

        return citations
