"""
Natural query processing for intelligent search.
Converts natural language queries into optimized search terms.
"""

import re
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

from ..utils.config import Config
from ..utils.exceptions import AIProcessingError


class NaturalQueryProcessor:
    """Process natural language queries for better search results."""
    
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.gemini_api_key
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=config.get("ai.model", "gemini-2.0-flash"),
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 200,
                }
            )
        else:
            self.model = None
    
    def process_natural_query(self, user_input: str) -> Dict[str, str]:
        """
        Process natural language input and extract search intent.
        
        Args:
            user_input: Natural language query from user
            
        Returns:
            Dict with processed query and intent
        """
        # Clean the input
        cleaned_input = self._clean_input(user_input)
        
        # Quick pattern matching for common queries
        quick_result = self._quick_pattern_match(cleaned_input)
        if quick_result:
            return quick_result
        
        # Use AI for complex queries if available
        if self.model:
            try:
                ai_result = self._ai_process_query(cleaned_input)
                if ai_result:
                    return ai_result
            except:
                pass  # Fall back to rule-based processing
        
        # Fallback to rule-based processing
        return self._rule_based_processing(cleaned_input)
    
    def _clean_input(self, user_input: str) -> str:
        """Clean and normalize user input."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', user_input.strip())
        
        # Remove common filler words but keep important ones
        filler_words = ['um', 'uh', 'like', 'you know', 'basically', 'actually']
        for word in filler_words:
            cleaned = re.sub(rf'\b{word}\b', '', cleaned, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _quick_pattern_match(self, query: str) -> Optional[Dict[str, str]]:
        """Quick pattern matching for common query types."""
        query_lower = query.lower()
        
        # Programming language queries
        if re.search(r'\b(python|javascript|java|react|node)\b', query_lower):
            if 'tutorial' in query_lower or 'learn' in query_lower:
                return {
                    "search_query": query,
                    "intent": "tutorial",
                    "category": "programming",
                    "urgency": "normal"
                }
            elif 'library' in query_lower or 'package' in query_lower:
                return {
                    "search_query": query,
                    "intent": "tools",
                    "category": "programming",
                    "urgency": "normal"
                }
        
        # AI/ML queries
        if re.search(r'\b(ai|machine learning|ml|data science)\b', query_lower):
            return {
                "search_query": query,
                "intent": "research",
                "category": "ai_ml",
                "urgency": "normal"
            }
        
        # Project/repository queries
        if re.search(r'\b(project|repo|github|code)\b', query_lower):
            return {
                "search_query": query,
                "intent": "projects",
                "category": "development",
                "urgency": "normal"
            }
        
        return None
    
    def _ai_process_query(self, query: str) -> Optional[Dict[str, str]]:
        """Use AI to process complex natural language queries."""
        prompt = f"""
Analyze this user query and extract the search intent: "{query}"

Respond with ONLY this format:
SEARCH: [optimized search terms]
INTENT: [tutorial/tools/research/projects/comparison/general]
CATEGORY: [programming/ai_ml/web_dev/data_science/general]

Query: {query}
"""
        
        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                return None
            
            # Parse AI response
            lines = response.text.strip().split('\n')
            result = {}
            
            for line in lines:
                if line.startswith('SEARCH:'):
                    result['search_query'] = line.replace('SEARCH:', '').strip()
                elif line.startswith('INTENT:'):
                    result['intent'] = line.replace('INTENT:', '').strip()
                elif line.startswith('CATEGORY:'):
                    result['category'] = line.replace('CATEGORY:', '').strip()
            
            if 'search_query' in result:
                result['urgency'] = 'normal'
                return result
            
        except Exception:
            pass
        
        return None
    
    def _rule_based_processing(self, query: str) -> Dict[str, str]:
        """Rule-based query processing as fallback."""
        query_lower = query.lower()
        
        # Determine intent based on keywords
        intent = "general"
        category = "general"
        
        if any(word in query_lower for word in ['how to', 'tutorial', 'learn', 'guide']):
            intent = "tutorial"
        elif any(word in query_lower for word in ['best', 'top', 'compare', 'vs']):
            intent = "comparison"
        elif any(word in query_lower for word in ['project', 'repo', 'github', 'example']):
            intent = "projects"
        elif any(word in query_lower for word in ['library', 'package', 'tool', 'framework']):
            intent = "tools"
        
        # Determine category
        if any(word in query_lower for word in ['python', 'javascript', 'java', 'programming']):
            category = "programming"
        elif any(word in query_lower for word in ['ai', 'machine learning', 'ml', 'data science']):
            category = "ai_ml"
        elif any(word in query_lower for word in ['web', 'html', 'css', 'react', 'frontend']):
            category = "web_dev"
        
        # Optimize search query
        optimized_query = self._optimize_search_terms(query)
        
        return {
            "search_query": optimized_query,
            "intent": intent,
            "category": category,
            "urgency": "normal"
        }
    
    def _optimize_search_terms(self, query: str) -> str:
        """Optimize search terms for better results."""
        # Remove question words
        question_words = ['what', 'how', 'where', 'when', 'why', 'which', 'who']
        words = query.split()
        
        filtered_words = []
        for word in words:
            if word.lower() not in question_words:
                filtered_words.append(word)
        
        # Remove common stop words but keep important ones
        stop_words = ['is', 'are', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with']
        important_words = ['best', 'top', 'good', 'fast', 'easy', 'simple', 'advanced', 'free', 'open source']
        
        final_words = []
        for word in filtered_words:
            if word.lower() not in stop_words or word.lower() in important_words:
                final_words.append(word)
        
        return ' '.join(final_words) if final_words else query
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """Get search suggestions based on query analysis."""
        processed = self.process_natural_query(query)
        base_query = processed['search_query']
        intent = processed['intent']
        category = processed['category']
        
        suggestions = [base_query]
        
        # Add intent-based suggestions
        if intent == "tutorial":
            suggestions.extend([
                f"{base_query} tutorial",
                f"{base_query} guide",
                f"learn {base_query}"
            ])
        elif intent == "tools":
            suggestions.extend([
                f"best {base_query}",
                f"{base_query} library",
                f"{base_query} framework"
            ])
        elif intent == "projects":
            suggestions.extend([
                f"{base_query} github",
                f"{base_query} project",
                f"{base_query} example"
            ])
        
        return suggestions[:5]  # Return top 5 suggestions
