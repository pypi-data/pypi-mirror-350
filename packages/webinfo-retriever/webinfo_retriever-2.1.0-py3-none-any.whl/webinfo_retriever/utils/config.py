"""
Configuration management for WebInfo Retriever.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from .exceptions import ConfigurationError

load_dotenv()


class Config:
    """Configuration manager for WebInfo Retriever."""

    DEFAULT_CONFIG = {
        "scraping": {
            "timeout": 30,
            "max_retries": 3,
            "retry_delay": 1,
            "user_agent": "WebInfo-Retriever/1.0.0",
            "max_content_length": 10 * 1024 * 1024,
            "follow_redirects": True,
            "verify_ssl": True,
            "max_redirects": 10,
        },
        "ai": {
            "model": "gemini-2.0-flash-exp",
            "temperature": 0.3,
            "max_tokens": 8192,
            "top_p": 0.8,
            "top_k": 40,
            "safety_settings": {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
            },
        },
        "content": {
            "min_content_length": 100,
            "max_summary_length": 2000,
            "extract_images": False,
            "extract_links": True,
            "clean_html": True,
            "preserve_formatting": False,
        },
        "cache": {
            "enabled": True,
            "ttl": 3600,
            "max_size": 1000,
        },
        "rate_limiting": {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "burst_limit": 10,
        },

    }

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self._config = self.DEFAULT_CONFIG.copy()
        if config_dict:
            self._merge_config(config_dict)
        self._load_env_vars()
        self._validate_config()

    def _merge_config(self, config_dict: Dict[str, Any]) -> None:
        """Merge user configuration with default configuration."""
        for key, value in config_dict.items():
            if key in self._config and isinstance(self._config[key], dict) and isinstance(value, dict):
                self._config[key].update(value)
            else:
                self._config[key] = value

    def _load_env_vars(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            "GEMINI_API_KEY": ("ai", "api_key"),
            "WEBINFO_TIMEOUT": ("scraping", "timeout"),
            "WEBINFO_MAX_RETRIES": ("scraping", "max_retries"),
            "WEBINFO_USER_AGENT": ("scraping", "user_agent"),
            "WEBINFO_CACHE_TTL": ("cache", "ttl"),
            "WEBINFO_RATE_LIMIT_RPM": ("rate_limiting", "requests_per_minute"),

        }

        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                if section not in self._config:
                    self._config[section] = {}

                if key in ["timeout", "max_retries", "ttl", "requests_per_minute"]:
                    try:
                        self._config[section][key] = int(value)
                    except ValueError:
                        raise ConfigurationError(f"Invalid integer value for {env_var}: {value}")
                else:
                    self._config[section][key] = value

    def _validate_config(self) -> None:
        """Validate configuration values."""
        if not self.get("ai.api_key"):
            raise ConfigurationError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable or provide it in config."
            )

        if self.get("scraping.timeout") <= 0:
            raise ConfigurationError("Scraping timeout must be positive")

        if self.get("scraping.max_retries") < 0:
            raise ConfigurationError("Max retries must be non-negative")

        if self.get("ai.temperature") < 0 or self.get("ai.temperature") > 2:
            raise ConfigurationError("AI temperature must be between 0 and 2")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()

    @property
    def gemini_api_key(self) -> str:
        """Get Gemini API key."""
        return self.get("ai.api_key")

    @property
    def scraping_config(self) -> Dict[str, Any]:
        """Get scraping configuration."""
        return self.get("scraping", {})

    @property
    def ai_config(self) -> Dict[str, Any]:
        """Get AI configuration."""
        return self.get("ai", {})

    @property
    def content_config(self) -> Dict[str, Any]:
        """Get content configuration."""
        return self.get("content", {})
