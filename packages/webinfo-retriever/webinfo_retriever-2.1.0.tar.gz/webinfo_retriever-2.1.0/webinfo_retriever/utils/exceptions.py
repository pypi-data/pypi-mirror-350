"""
Custom exception classes for WebInfo Retriever.
"""


class WebInfoRetrieverError(Exception):
    """Base exception class for WebInfo Retriever."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ScrapingError(WebInfoRetrieverError):
    """Exception raised when web scraping fails."""
    
    def __init__(self, message: str, url: str = None, status_code: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.url = url
        self.status_code = status_code


class AIProcessingError(WebInfoRetrieverError):
    """Exception raised when AI processing fails."""
    
    def __init__(self, message: str, model: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.model = model


class ContentExtractionError(WebInfoRetrieverError):
    """Exception raised when content extraction fails."""
    
    def __init__(self, message: str, content_type: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.content_type = content_type


class ConfigurationError(WebInfoRetrieverError):
    """Exception raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.config_key = config_key


class RateLimitError(WebInfoRetrieverError):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ValidationError(WebInfoRetrieverError):
    """Exception raised when input validation fails."""
    
    def __init__(self, message: str, field: str = None, value: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value


class TimeoutError(WebInfoRetrieverError):
    """Exception raised when operations timeout."""
    
    def __init__(self, message: str, timeout_duration: float = None, **kwargs):
        super().__init__(message, **kwargs)
        self.timeout_duration = timeout_duration
