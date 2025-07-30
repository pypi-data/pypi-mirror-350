"""
Input validation utilities for WebInfo Retriever.
"""

import re
import validators
from typing import List, Optional, Union
from urllib.parse import urlparse, urljoin
from .exceptions import ValidationError


class URLValidator:
    """URL validation and normalization utilities."""
    
    ALLOWED_SCHEMES = {"http", "https"}
    BLOCKED_DOMAINS = {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "::1",
    }
    
    @classmethod
    def validate_url(cls, url: str) -> str:
        """Validate and normalize URL."""
        if not url or not isinstance(url, str):
            raise ValidationError("URL must be a non-empty string", field="url", value=str(url))
        
        url = url.strip()
        
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        if not validators.url(url):
            raise ValidationError(f"Invalid URL format: {url}", field="url", value=url)
        
        parsed = urlparse(url)
        
        if parsed.scheme not in cls.ALLOWED_SCHEMES:
            raise ValidationError(
                f"URL scheme '{parsed.scheme}' not allowed. Use http or https.",
                field="url",
                value=url
            )
        
        if parsed.hostname and parsed.hostname.lower() in cls.BLOCKED_DOMAINS:
            raise ValidationError(
                f"Access to domain '{parsed.hostname}' is not allowed",
                field="url",
                value=url
            )
        
        return url
    
    @classmethod
    def validate_urls(cls, urls: List[str]) -> List[str]:
        """Validate and normalize multiple URLs."""
        if not isinstance(urls, list):
            raise ValidationError("URLs must be provided as a list", field="urls")
        
        if len(urls) == 0:
            raise ValidationError("At least one URL must be provided", field="urls")
        
        if len(urls) > 50:
            raise ValidationError("Maximum 50 URLs allowed per request", field="urls")
        
        validated_urls = []
        for i, url in enumerate(urls):
            try:
                validated_url = cls.validate_url(url)
                validated_urls.append(validated_url)
            except ValidationError as e:
                raise ValidationError(f"URL at index {i}: {e.message}", field="urls", value=str(url))
        
        return validated_urls
    
    @classmethod
    def is_same_domain(cls, url1: str, url2: str) -> bool:
        """Check if two URLs belong to the same domain."""
        try:
            domain1 = urlparse(url1).netloc.lower()
            domain2 = urlparse(url2).netloc.lower()
            return domain1 == domain2
        except Exception:
            return False
    
    @classmethod
    def get_base_url(cls, url: str) -> str:
        """Get base URL (scheme + netloc)."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"


class ContentValidator:
    """Content validation utilities."""
    
    MIN_CONTENT_LENGTH = 10
    MAX_CONTENT_LENGTH = 1024 * 1024
    
    @classmethod
    def validate_content(cls, content: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> str:
        """Validate content length and format."""
        if not isinstance(content, str):
            raise ValidationError("Content must be a string", field="content")
        
        min_len = min_length or cls.MIN_CONTENT_LENGTH
        max_len = max_length or cls.MAX_CONTENT_LENGTH
        
        if len(content) < min_len:
            raise ValidationError(
                f"Content too short. Minimum {min_len} characters required.",
                field="content",
                value=f"Length: {len(content)}"
            )
        
        if len(content) > max_len:
            raise ValidationError(
                f"Content too long. Maximum {max_len} characters allowed.",
                field="content",
                value=f"Length: {len(content)}"
            )
        
        return content.strip()
    
    @classmethod
    def validate_query(cls, query: str) -> str:
        """Validate search query."""
        if not query or not isinstance(query, str):
            raise ValidationError("Query must be a non-empty string", field="query", value=str(query))
        
        query = query.strip()
        
        if len(query) < 3:
            raise ValidationError("Query must be at least 3 characters long", field="query", value=query)
        
        if len(query) > 500:
            raise ValidationError("Query must be less than 500 characters", field="query", value=query)
        
        return query
    
    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """Sanitize text content."""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\-.,!?;:()\[\]{}"\'/\\@#$%^&*+=<>|`~]', '', text)
        
        return text.strip()
    
    @classmethod
    def validate_language_code(cls, lang_code: str) -> str:
        """Validate ISO 639-1 language code."""
        if not lang_code or not isinstance(lang_code, str):
            raise ValidationError("Language code must be a non-empty string", field="language", value=str(lang_code))
        
        lang_code = lang_code.lower().strip()
        
        if not re.match(r'^[a-z]{2}$', lang_code):
            raise ValidationError(
                "Language code must be a valid ISO 639-1 code (2 letters)",
                field="language",
                value=lang_code
            )
        
        return lang_code
