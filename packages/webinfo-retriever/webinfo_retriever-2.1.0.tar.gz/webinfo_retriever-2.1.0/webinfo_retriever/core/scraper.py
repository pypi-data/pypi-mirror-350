"""
Advanced web scraping module with multiple strategies and robust error handling.
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin, urlparse
import aiohttp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from cachetools import TTLCache

from ..utils.config import Config
from ..utils.exceptions import ScrapingError, TimeoutError, RateLimitError
from ..utils.validators import URLValidator


class WebScraper:
    """Advanced web scraper with multiple strategies and robust error handling."""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent()
        self.cache = TTLCache(
            maxsize=config.get("cache.max_size", 1000),
            ttl=config.get("cache.ttl", 3600)
        ) if config.get("cache.enabled", True) else None
        self._setup_session()
        self._rate_limiter = {}

    def _setup_session(self) -> None:
        """Setup requests session with proper headers and configuration."""
        self.session.headers.update({
            'User-Agent': self.config.get("scraping.user_agent", self.ua.random),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        self.session.max_redirects = self.config.get("scraping.max_redirects", 10)

        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.adapters.Retry(
                total=self.config.get("scraping.max_retries", 3),
                backoff_factor=self.config.get("scraping.retry_delay", 1),
                status_forcelist=[429, 500, 502, 503, 504]
            )
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _check_rate_limit(self, domain: str) -> None:
        """Check and enforce rate limiting per domain."""
        current_time = time.time()

        if domain not in self._rate_limiter:
            self._rate_limiter[domain] = []

        requests_in_minute = [
            req_time for req_time in self._rate_limiter[domain]
            if current_time - req_time < 60
        ]

        if len(requests_in_minute) >= self.config.get("rate_limiting.requests_per_minute", 60):
            raise RateLimitError(
                f"Rate limit exceeded for domain {domain}",
                retry_after=60
            )

        self._rate_limiter[domain] = requests_in_minute + [current_time]

    def scrape_url(self, url: str, use_selenium: bool = False) -> Dict[str, Union[str, int, Dict, bool]]:
        """Scrape a single URL with fallback strategies."""
        try:
            url = URLValidator.validate_url(url)

            if self.cache and url in self.cache:
                return self.cache[url]

            domain = urlparse(url).netloc
            self._check_rate_limit(domain)

            try:
                if use_selenium:
                    result = self._scrape_with_selenium(url)
                else:
                    result = self._scrape_with_requests(url)

                result["success"] = True

                if self.cache:
                    self.cache[url] = result

                return result

            except Exception as e:
                if not use_selenium:
                    try:
                        result = self._scrape_with_selenium(url)
                        result["success"] = True
                        if self.cache:
                            self.cache[url] = result
                        return result
                    except Exception as selenium_error:
                        return {
                            "url": url,
                            "success": False,
                            "error": f"Failed with both requests and selenium: {str(e)}, {str(selenium_error)}",
                            "timestamp": time.time()
                        }
                else:
                    return {
                        "url": url,
                        "success": False,
                        "error": str(e),
                        "timestamp": time.time()
                    }
        except Exception as e:
            return {
                "url": url,
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }

    def _scrape_with_requests(self, url: str) -> Dict[str, Union[str, int, Dict]]:
        """Scrape URL using requests library."""
        try:
            response = self.session.get(
                url,
                timeout=self.config.get("scraping.timeout", 30),
                verify=self.config.get("scraping.verify_ssl", True),
                allow_redirects=self.config.get("scraping.follow_redirects", True)
            )

            response.raise_for_status()

            if len(response.content) > self.config.get("scraping.max_content_length", 10 * 1024 * 1024):
                raise ScrapingError(
                    f"Content too large: {len(response.content)} bytes",
                    url=url
                )

            return {
                "url": url,
                "final_url": response.url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "encoding": response.encoding,
                "method": "requests",
                "timestamp": time.time(),
            }

        except requests.Timeout:
            raise TimeoutError(f"Request timeout for {url}", timeout_duration=self.config.get("scraping.timeout"))
        except requests.RequestException as e:
            raise ScrapingError(f"Request failed for {url}: {str(e)}", url=url, status_code=getattr(e.response, 'status_code', None))

    def _scrape_with_selenium(self, url: str) -> Dict[str, Union[str, int, Dict]]:
        """Scrape URL using Selenium WebDriver."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-agent={self.ua.random}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            driver.set_page_load_timeout(self.config.get("scraping.timeout", 30))
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            time.sleep(2)

            content = driver.page_source
            final_url = driver.current_url

            return {
                "url": url,
                "final_url": final_url,
                "status_code": 200,
                "headers": {},
                "content": content,
                "encoding": "utf-8",
                "method": "selenium",
                "timestamp": time.time(),
            }

        except Exception as e:
            raise ScrapingError(f"Selenium scraping failed for {url}: {str(e)}", url=url)
        finally:
            if driver:
                driver.quit()

    async def scrape_urls_async(self, urls: List[str], max_concurrent: int = 5) -> List[Dict[str, Union[str, int, Dict]]]:
        """Scrape multiple URLs asynchronously."""
        urls = URLValidator.validate_urls(urls)

        semaphore = asyncio.Semaphore(max_concurrent)

        async def scrape_single(url: str) -> Dict[str, Union[str, int, Dict]]:
            async with semaphore:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self.scrape_url, url)

        tasks = [scrape_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "url": urls[i],
                    "error": str(result),
                    "status_code": None,
                    "content": None,
                    "method": "failed",
                    "timestamp": time.time(),
                })
            else:
                processed_results.append(result)

        return processed_results

    def get_page_metadata(self, url: str) -> Dict[str, str]:
        """Extract basic metadata from a webpage."""
        try:
            result = self.scrape_url(url)
            content = result.get("content", "")

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            metadata = {
                "title": "",
                "description": "",
                "keywords": "",
                "author": "",
                "canonical_url": url,
            }

            if soup.title:
                metadata["title"] = soup.title.get_text().strip()

            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                name = tag.get('name', '').lower()
                property_attr = tag.get('property', '').lower()
                content_attr = tag.get('content', '')

                if name == 'description' or property_attr == 'og:description':
                    metadata["description"] = content_attr
                elif name == 'keywords':
                    metadata["keywords"] = content_attr
                elif name == 'author':
                    metadata["author"] = content_attr

            canonical = soup.find('link', rel='canonical')
            if canonical and canonical.get('href'):
                metadata["canonical_url"] = urljoin(url, canonical['href'])

            return metadata

        except Exception as e:
            raise ScrapingError(f"Failed to extract metadata from {url}: {str(e)}", url=url)

    def close(self) -> None:
        """Close the scraper and cleanup resources."""
        if hasattr(self, 'session'):
            self.session.close()
