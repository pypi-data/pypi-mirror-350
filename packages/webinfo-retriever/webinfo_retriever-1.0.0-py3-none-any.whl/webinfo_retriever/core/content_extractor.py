"""
Intelligent content extraction from web pages using multiple strategies.
"""

import re
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Comment
from readability import Document
import trafilatura
from newspaper import Article
from markdownify import markdownify

from ..utils.config import Config
from ..utils.exceptions import ContentExtractionError
from ..utils.validators import ContentValidator


class ContentExtractor:
    """Intelligent content extractor with multiple extraction strategies."""

    def __init__(self, config: Config):
        self.config = config
        self.min_content_length = config.get("content.min_content_length", 100)
        self.extract_images = config.get("content.extract_images", False)
        self.extract_links = config.get("content.extract_links", True)
        self.clean_html = config.get("content.clean_html", True)
        self.preserve_formatting = config.get("content.preserve_formatting", False)

    def extract_content(self, scraped_data: Dict[str, Union[str, int, Dict]]) -> Dict[str, Union[str, List, Dict]]:
        """Extract structured content from scraped webpage data."""
        url = scraped_data.get("url", "")
        content = scraped_data.get("content", "")

        if not content:
            raise ContentExtractionError("No content to extract", content_type="empty")

        try:
            strategies = [
                self._extract_with_trafilatura,
                self._extract_with_readability,
                self._extract_with_newspaper,
                self._extract_with_beautifulsoup,
            ]

            best_result = None
            best_score = 0

            for strategy in strategies:
                try:
                    result = strategy(content, url)
                    score = self._score_extraction(result)

                    if score > best_score:
                        best_score = score
                        best_result = result

                except Exception:
                    continue

            if not best_result or best_score == 0:
                raise ContentExtractionError("All extraction strategies failed", content_type="html")

            best_result.update({
                "extraction_score": best_score,
                "source_url": url,
                "content_length": len(best_result.get("text", "")),
                "word_count": len(best_result.get("text", "").split()),
            })

            if self.extract_links:
                best_result["links"] = self._extract_links(content, url)

            if self.extract_images:
                best_result["images"] = self._extract_images(content, url)

            return best_result

        except Exception as e:
            raise ContentExtractionError(f"Content extraction failed: {str(e)}", content_type="html")

    def _extract_with_trafilatura(self, content: str, url: str) -> Dict[str, str]:
        """Extract content using trafilatura library."""
        extracted = trafilatura.extract(
            content,
            include_comments=False,
            include_tables=True,
            include_formatting=self.preserve_formatting,
            output_format='txt' if not self.preserve_formatting else 'xml'
        )

        if not extracted or len(extracted) < self.min_content_length:
            raise ContentExtractionError("Trafilatura extraction insufficient")

        metadata = trafilatura.extract_metadata(content)

        return {
            "text": extracted,
            "title": metadata.title if metadata else "",
            "author": metadata.author if metadata else "",
            "date": metadata.date if metadata else "",
            "method": "trafilatura",
        }

    def _extract_with_readability(self, content: str, url: str) -> Dict[str, str]:
        """Extract content using readability library."""
        doc = Document(content)

        extracted_html = doc.summary()
        if not extracted_html:
            raise ContentExtractionError("Readability extraction failed")

        soup = BeautifulSoup(extracted_html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        if len(text) < self.min_content_length:
            raise ContentExtractionError("Readability extraction insufficient")

        return {
            "text": text,
            "title": doc.title(),
            "author": "",
            "date": "",
            "method": "readability",
        }

    def _extract_with_newspaper(self, content: str, url: str) -> Dict[str, str]:
        """Extract content using newspaper3k library."""
        article = Article(url)
        article.set_html(content)
        article.parse()

        if not article.text or len(article.text) < self.min_content_length:
            raise ContentExtractionError("Newspaper extraction insufficient")

        return {
            "text": article.text,
            "title": article.title or "",
            "author": ", ".join(article.authors) if article.authors else "",
            "date": article.publish_date.isoformat() if article.publish_date else "",
            "method": "newspaper",
        }

    def _extract_with_beautifulsoup(self, content: str, url: str) -> Dict[str, str]:
        """Extract content using BeautifulSoup as fallback."""
        soup = BeautifulSoup(content, 'html.parser')

        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        title = ""
        if soup.title:
            title = soup.title.get_text().strip()

        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))

        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)

        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) < self.min_content_length:
            raise ContentExtractionError("BeautifulSoup extraction insufficient")

        return {
            "text": text,
            "title": title,
            "author": "",
            "date": "",
            "method": "beautifulsoup",
        }

    def _score_extraction(self, result: Dict[str, str]) -> float:
        """Score extraction result quality."""
        text = result.get("text", "")
        title = result.get("title", "")

        if not text:
            return 0

        score = 0

        score += min(len(text) / 1000, 10)

        if title:
            score += 2

        if result.get("author"):
            score += 1

        if result.get("date"):
            score += 1

        word_count = len(text.split())
        if word_count > 50:
            score += 2

        sentence_count = len([s for s in text.split('.') if s.strip()])
        if sentence_count > 5:
            score += 1

        if re.search(r'\b(article|story|news|blog|post)\b', text.lower()):
            score += 1

        return score

    def _extract_links(self, content: str, base_url: str) -> List[Dict[str, str]]:
        """Extract all links from content."""
        soup = BeautifulSoup(content, 'html.parser')
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)

            if href.startswith(('http://', 'https://')):
                absolute_url = href
            else:
                absolute_url = urljoin(base_url, href)

            if text and absolute_url:
                links.append({
                    "url": absolute_url,
                    "text": text,
                    "title": link.get('title', ''),
                })

        return links[:50]

    def _extract_images(self, content: str, base_url: str) -> List[Dict[str, str]]:
        """Extract all images from content."""
        soup = BeautifulSoup(content, 'html.parser')
        images = []

        for img in soup.find_all('img', src=True):
            src = img['src']
            alt = img.get('alt', '')

            if src.startswith(('http://', 'https://')):
                absolute_url = src
            else:
                absolute_url = urljoin(base_url, src)

            images.append({
                "url": absolute_url,
                "alt": alt,
                "title": img.get('title', ''),
                "width": img.get('width', ''),
                "height": img.get('height', ''),
            })

        return images[:20]

    def extract_structured_data(self, content: str) -> Dict[str, Union[str, List, Dict]]:
        """Extract structured data (JSON-LD, microdata, etc.)."""
        soup = BeautifulSoup(content, 'html.parser')
        structured_data = {}

        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        if json_ld_scripts:
            import json
            json_ld_data = []
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    json_ld_data.append(data)
                except json.JSONDecodeError:
                    continue
            structured_data['json_ld'] = json_ld_data

        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        structured_data['meta_tags'] = meta_tags

        return structured_data

    def convert_to_markdown(self, content: str) -> str:
        """Convert HTML content to Markdown."""
        try:
            markdown = markdownify(content, heading_style="ATX")
            return markdown.strip()
        except Exception as e:
            raise ContentExtractionError(f"Markdown conversion failed: {str(e)}")

    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()

        return ContentValidator.sanitize_text(text)
