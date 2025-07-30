"""
AI processing module using Google's Gemini 2.0 Flash model for content analysis and summarization.
"""

import asyncio
import time
from typing import Dict, List, Optional, Union, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..utils.config import Config
from ..utils.exceptions import AIProcessingError, ConfigurationError, RateLimitError
from ..utils.validators import ContentValidator


class AIProcessor:
    """AI processor using Google's Gemini 2.0 Flash model."""
    
    def __init__(self, config: Config):
        self.config = config
        self.model_name = config.get("ai.model", "gemini-2.0-flash-exp")
        self.api_key = config.gemini_api_key
        
        if not self.api_key:
            raise ConfigurationError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        
        self.generation_config = {
            "temperature": config.get("ai.temperature", 0.3),
            "top_p": config.get("ai.top_p", 0.8),
            "top_k": config.get("ai.top_k", 40),
            "max_output_tokens": config.get("ai.max_tokens", 8192),
        }
        
        self.safety_settings = self._get_safety_settings()
        
        try:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
        except Exception as e:
            raise AIProcessingError(f"Failed to initialize Gemini model: {str(e)}", model=self.model_name)
    
    def _get_safety_settings(self) -> List[Dict[str, Any]]:
        """Get safety settings for the model."""
        safety_config = self.config.get("ai.safety_settings", {})
        
        default_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        
        safety_settings = []
        for category, threshold in default_settings.items():
            safety_settings.append({
                "category": category,
                "threshold": threshold
            })
        
        return safety_settings
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    def summarize_content(self, content: str, query: Optional[str] = None, max_length: Optional[int] = None) -> Dict[str, Union[str, int, float]]:
        """Summarize content with optional query context."""
        content = ContentValidator.validate_content(content)
        
        if query:
            query = ContentValidator.validate_query(query)
        
        max_summary_length = max_length or self.config.get("content.max_summary_length", 2000)
        
        prompt = self._build_summarization_prompt(content, query, max_summary_length)
        
        try:
            start_time = time.time()
            response = self.model.generate_content(prompt)
            processing_time = time.time() - start_time
            
            if not response.text:
                raise AIProcessingError("Empty response from Gemini model", model=self.model_name)
            
            summary = response.text.strip()
            
            return {
                "summary": summary,
                "original_length": len(content),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(content),
                "processing_time": processing_time,
                "model": self.model_name,
                "query_context": query or "",
            }
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate limit" in str(e).lower():
                raise RateLimitError(f"Gemini API rate limit exceeded: {str(e)}")
            else:
                raise AIProcessingError(f"Gemini summarization failed: {str(e)}", model=self.model_name)
    
    def _build_summarization_prompt(self, content: str, query: Optional[str], max_length: int) -> str:
        """Build prompt for content summarization."""
        base_prompt = f"""
You are an expert content summarizer. Your task is to create a comprehensive, accurate, and well-structured summary of the provided content.

INSTRUCTIONS:
1. Create a summary that captures the main points, key insights, and important details
2. Maintain factual accuracy and preserve the original meaning
3. Use clear, concise language that is easy to understand
4. Structure the summary with proper paragraphs and logical flow
5. Keep the summary under {max_length} characters
6. Focus on the most valuable and relevant information

"""
        
        if query:
            base_prompt += f"""
SPECIFIC FOCUS: Pay special attention to information related to this query: "{query}"
Ensure the summary addresses this query while maintaining overall content coverage.

"""
        
        base_prompt += f"""
CONTENT TO SUMMARIZE:
{content}

SUMMARY:"""
        
        return base_prompt
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    def answer_question(self, content: str, question: str) -> Dict[str, Union[str, float]]:
        """Answer a specific question based on the provided content."""
        content = ContentValidator.validate_content(content)
        question = ContentValidator.validate_query(question)
        
        prompt = self._build_qa_prompt(content, question)
        
        try:
            start_time = time.time()
            response = self.model.generate_content(prompt)
            processing_time = time.time() - start_time
            
            if not response.text:
                raise AIProcessingError("Empty response from Gemini model", model=self.model_name)
            
            answer = response.text.strip()
            
            return {
                "question": question,
                "answer": answer,
                "confidence": self._estimate_confidence(answer),
                "processing_time": processing_time,
                "model": self.model_name,
            }
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate limit" in str(e).lower():
                raise RateLimitError(f"Gemini API rate limit exceeded: {str(e)}")
            else:
                raise AIProcessingError(f"Gemini Q&A failed: {str(e)}", model=self.model_name)
    
    def _build_qa_prompt(self, content: str, question: str) -> str:
        """Build prompt for question answering."""
        return f"""
You are an expert information analyst. Your task is to answer the given question based solely on the provided content.

INSTRUCTIONS:
1. Answer the question accurately and comprehensively based on the content
2. If the content doesn't contain enough information to answer the question, clearly state this
3. Provide specific details and examples from the content when relevant
4. Use clear, direct language in your response
5. If there are multiple perspectives or answers in the content, present them fairly
6. Cite specific parts of the content when making claims

QUESTION: {question}

CONTENT:
{content}

ANSWER:"""
    
    def _estimate_confidence(self, answer: str) -> float:
        """Estimate confidence level of the answer."""
        confidence_indicators = {
            "high": ["clearly", "definitely", "certainly", "specifically states", "explicitly"],
            "medium": ["likely", "probably", "suggests", "indicates", "appears"],
            "low": ["unclear", "insufficient information", "cannot determine", "not enough", "ambiguous"]
        }
        
        answer_lower = answer.lower()
        
        high_count = sum(1 for indicator in confidence_indicators["high"] if indicator in answer_lower)
        medium_count = sum(1 for indicator in confidence_indicators["medium"] if indicator in answer_lower)
        low_count = sum(1 for indicator in confidence_indicators["low"] if indicator in answer_lower)
        
        if low_count > 0:
            return 0.3
        elif high_count > medium_count:
            return 0.9
        elif medium_count > 0:
            return 0.6
        else:
            return 0.7
    
    def extract_key_points(self, content: str, num_points: int = 5) -> Dict[str, Union[List[str], float]]:
        """Extract key points from content."""
        content = ContentValidator.validate_content(content)
        
        prompt = f"""
Extract the {num_points} most important key points from the following content. 
Present each point as a clear, concise bullet point that captures essential information.

CONTENT:
{content}

KEY POINTS:"""
        
        try:
            start_time = time.time()
            response = self.model.generate_content(prompt)
            processing_time = time.time() - start_time
            
            if not response.text:
                raise AIProcessingError("Empty response from Gemini model", model=self.model_name)
            
            key_points_text = response.text.strip()
            key_points = [point.strip().lstrip('•-*').strip() for point in key_points_text.split('\n') if point.strip()]
            
            return {
                "key_points": key_points[:num_points],
                "processing_time": processing_time,
                "model": self.model_name,
            }
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate limit" in str(e).lower():
                raise RateLimitError(f"Gemini API rate limit exceeded: {str(e)}")
            else:
                raise AIProcessingError(f"Gemini key point extraction failed: {str(e)}", model=self.model_name)
    
    async def process_multiple_contents(self, contents: List[Dict[str, str]], operation: str = "summarize") -> List[Dict[str, Any]]:
        """Process multiple contents asynchronously."""
        if not contents:
            return []
        
        semaphore = asyncio.Semaphore(5)
        
        async def process_single(content_data: Dict[str, str]) -> Dict[str, Any]:
            async with semaphore:
                loop = asyncio.get_event_loop()
                
                content = content_data.get("content", "")
                query = content_data.get("query")
                
                if operation == "summarize":
                    return await loop.run_in_executor(None, self.summarize_content, content, query)
                elif operation == "extract_key_points":
                    return await loop.run_in_executor(None, self.extract_key_points, content)
                else:
                    raise AIProcessingError(f"Unknown operation: {operation}")
        
        tasks = [process_single(content_data) for content_data in contents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "error": str(result),
                    "content_index": i,
                    "model": self.model_name,
                })
            else:
                processed_results.append(result)
        
        return processed_results
