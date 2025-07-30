"""
Response generation module for creating comprehensive, contextual responses.
"""

import time
from typing import Dict, List, Optional, Union, Any
from datetime import datetime

from ..utils.config import Config
from ..utils.exceptions import AIProcessingError
from ..utils.validators import ContentValidator


class ResponseGenerator:
    """Generate comprehensive responses based on retrieved and processed content."""
    
    def __init__(self, config: Config):
        self.config = config
        self.max_response_length = config.get("content.max_summary_length", 2000)
    
    def generate_comprehensive_response(
        self,
        query: str,
        extracted_contents: List[Dict[str, Any]],
        ai_summaries: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a comprehensive response combining all processed information."""
        
        query = ContentValidator.validate_query(query)
        
        if not extracted_contents and not ai_summaries:
            raise AIProcessingError("No content available to generate response")
        
        response_data = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "response": "",
            "sources": [],
            "key_insights": [],
            "confidence_score": 0.0,
            "processing_summary": {},
            "metadata": metadata or {},
        }
        
        try:
            main_response = self._build_main_response(query, extracted_contents, ai_summaries)
            response_data["response"] = main_response
            
            response_data["sources"] = self._extract_sources(extracted_contents)
            
            response_data["key_insights"] = self._extract_key_insights(ai_summaries)
            
            response_data["confidence_score"] = self._calculate_confidence_score(extracted_contents, ai_summaries)
            
            response_data["processing_summary"] = self._generate_processing_summary(extracted_contents, ai_summaries)
            
            response_data["word_count"] = len(main_response.split())
            response_data["character_count"] = len(main_response)
            
            return response_data
            
        except Exception as e:
            raise AIProcessingError(f"Response generation failed: {str(e)}")
    
    def _build_main_response(
        self,
        query: str,
        extracted_contents: List[Dict[str, Any]],
        ai_summaries: List[Dict[str, Any]]
    ) -> str:
        """Build the main response text."""
        
        response_parts = []
        
        response_parts.append(f"## Response to: {query}\n")
        
        if ai_summaries:
            primary_summary = self._select_best_summary(ai_summaries)
            if primary_summary and primary_summary.get("summary"):
                response_parts.append("### Summary")
                response_parts.append(primary_summary["summary"])
                response_parts.append("")
        
        relevant_content = self._extract_relevant_content(extracted_contents, query)
        if relevant_content:
            response_parts.append("### Key Information")
            for i, content in enumerate(relevant_content[:3], 1):
                title = content.get("title", f"Source {i}")
                text = content.get("text", "")
                
                if text:
                    truncated_text = self._truncate_text(text, 300)
                    response_parts.append(f"**{title}:**")
                    response_parts.append(truncated_text)
                    response_parts.append("")
        
        additional_insights = self._generate_additional_insights(extracted_contents, ai_summaries)
        if additional_insights:
            response_parts.append("### Additional Insights")
            response_parts.append(additional_insights)
        
        full_response = "\n".join(response_parts)
        
        if len(full_response) > self.max_response_length:
            full_response = self._truncate_response(full_response, self.max_response_length)
        
        return full_response
    
    def _select_best_summary(self, ai_summaries: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Select the best AI summary based on quality metrics."""
        if not ai_summaries:
            return None
        
        best_summary = None
        best_score = 0
        
        for summary in ai_summaries:
            if "error" in summary:
                continue
            
            score = 0
            
            if summary.get("summary"):
                summary_text = summary["summary"]
                score += min(len(summary_text) / 100, 5)
                
                if summary.get("compression_ratio"):
                    ratio = summary["compression_ratio"]
                    if 0.1 <= ratio <= 0.5:
                        score += 3
                
                if summary.get("query_context"):
                    score += 2
                
                if len(summary_text.split()) > 20:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_summary = summary
        
        return best_summary
    
    def _extract_relevant_content(self, extracted_contents: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Extract content most relevant to the query."""
        if not extracted_contents:
            return []
        
        query_words = set(query.lower().split())
        scored_content = []
        
        for content in extracted_contents:
            if "error" in content:
                continue
            
            text = content.get("text", "").lower()
            title = content.get("title", "").lower()
            
            relevance_score = 0
            
            for word in query_words:
                if len(word) > 2:
                    relevance_score += text.count(word) * 1
                    relevance_score += title.count(word) * 3
            
            if content.get("extraction_score"):
                relevance_score += content["extraction_score"] * 0.5
            
            if relevance_score > 0:
                scored_content.append((relevance_score, content))
        
        scored_content.sort(key=lambda x: x[0], reverse=True)
        return [content for _, content in scored_content]
    
    def _generate_additional_insights(
        self,
        extracted_contents: List[Dict[str, Any]],
        ai_summaries: List[Dict[str, Any]]
    ) -> str:
        """Generate additional insights from the processed content."""
        insights = []
        
        total_sources = len([c for c in extracted_contents if "error" not in c])
        if total_sources > 1:
            insights.append(f"Information compiled from {total_sources} sources")
        
        total_words = sum(
            content.get("word_count", 0) 
            for content in extracted_contents 
            if "error" not in content
        )
        if total_words > 0:
            insights.append(f"Total content analyzed: {total_words:,} words")
        
        processing_times = [
            summary.get("processing_time", 0)
            for summary in ai_summaries
            if "error" not in summary and summary.get("processing_time")
        ]
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            insights.append(f"AI processing completed in {avg_time:.2f} seconds")
        
        return " • ".join(insights) if insights else ""
    
    def _extract_sources(self, extracted_contents: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract source information."""
        sources = []
        
        for content in extracted_contents:
            if "error" in content:
                continue
            
            source = {
                "url": content.get("source_url", ""),
                "title": content.get("title", ""),
                "method": content.get("method", ""),
                "content_length": content.get("content_length", 0),
                "word_count": content.get("word_count", 0),
            }
            
            if source["url"]:
                sources.append(source)
        
        return sources
    
    def _extract_key_insights(self, ai_summaries: List[Dict[str, Any]]) -> List[str]:
        """Extract key insights from AI summaries."""
        insights = []
        
        for summary in ai_summaries:
            if "error" in summary:
                continue
            
            if summary.get("key_points"):
                insights.extend(summary["key_points"])
            elif summary.get("summary"):
                summary_text = summary["summary"]
                sentences = [s.strip() for s in summary_text.split('.') if s.strip()]
                insights.extend(sentences[:3])
        
        return insights[:10]
    
    def _calculate_confidence_score(
        self,
        extracted_contents: List[Dict[str, Any]],
        ai_summaries: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall confidence score for the response."""
        
        content_score = 0
        ai_score = 0
        
        successful_extractions = [c for c in extracted_contents if "error" not in c]
        if successful_extractions:
            avg_extraction_score = sum(
                c.get("extraction_score", 0) for c in successful_extractions
            ) / len(successful_extractions)
            content_score = min(avg_extraction_score / 10, 1.0)
        
        successful_summaries = [s for s in ai_summaries if "error" not in s]
        if successful_summaries:
            avg_confidence = sum(
                s.get("confidence", 0.5) for s in successful_summaries
            ) / len(successful_summaries)
            ai_score = avg_confidence
        
        if content_score > 0 and ai_score > 0:
            return (content_score + ai_score) / 2
        elif content_score > 0:
            return content_score * 0.7
        elif ai_score > 0:
            return ai_score * 0.7
        else:
            return 0.3
    
    def _generate_processing_summary(
        self,
        extracted_contents: List[Dict[str, Any]],
        ai_summaries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate summary of processing statistics."""
        
        return {
            "total_sources_attempted": len(extracted_contents),
            "successful_extractions": len([c for c in extracted_contents if "error" not in c]),
            "total_ai_operations": len(ai_summaries),
            "successful_ai_operations": len([s for s in ai_summaries if "error" not in s]),
            "total_content_length": sum(
                c.get("content_length", 0) for c in extracted_contents if "error" not in c
            ),
            "average_extraction_score": sum(
                c.get("extraction_score", 0) for c in extracted_contents if "error" not in c
            ) / max(len([c for c in extracted_contents if "error" not in c]), 1),
        }
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length while preserving word boundaries."""
        if len(text) <= max_length:
            return text
        
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def _truncate_response(self, response: str, max_length: int) -> str:
        """Truncate response while preserving structure."""
        if len(response) <= max_length:
            return response
        
        lines = response.split('\n')
        truncated_lines = []
        current_length = 0
        
        for line in lines:
            if current_length + len(line) + 1 > max_length:
                break
            truncated_lines.append(line)
            current_length += len(line) + 1
        
        truncated_response = '\n'.join(truncated_lines)
        if len(truncated_response) < len(response):
            truncated_response += "\n\n[Response truncated due to length limits]"
        
        return truncated_response
