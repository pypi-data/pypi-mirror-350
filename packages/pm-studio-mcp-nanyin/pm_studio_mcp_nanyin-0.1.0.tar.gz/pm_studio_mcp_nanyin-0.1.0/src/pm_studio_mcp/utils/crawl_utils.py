#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web Crawler Utilities for PM Studio MCP

This module implements web crawling functionality using crawl4ai.
"""

import os
import time
import asyncio
import re
import logging
import sys
from typing import Dict, Any, List, Optional, Union
from contextlib import contextmanager
from io import StringIO

# Configure logging - disable all logging
logging.basicConfig(level=logging.CRITICAL)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)
    logging.getLogger(logger_name).propagate = False
logging.getLogger().setLevel(logging.CRITICAL)

# Context manager to suppress stdout/stderr
@contextmanager
def suppress_stdout_stderr():
    """Context manager to suppress all stdout and stderr output"""
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

# Try to import crawl4ai with suppressed output
with suppress_stdout_stderr():
    try:
        import crawl4ai
        # Try to disable all logging in crawl4ai
        if hasattr(crawl4ai, 'set_verbose'):
            crawl4ai.set_verbose(False)
        if hasattr(crawl4ai, 'set_logging_level'):
            crawl4ai.set_logging_level('CRITICAL')
        # Try to access and disable loggers directly
        for name in logging.root.manager.loggerDict:
            if 'crawl4ai' in name.lower():
                logging.getLogger(name).setLevel(logging.CRITICAL)
                logging.getLogger(name).propagate = False
                logging.getLogger(name).disabled = True
        CRAWL4AI_AVAILABLE = True
    except ImportError:
        CRAWL4AI_AVAILABLE = False

class CrawlerUtils:
    """Utility class for web crawling operations"""
    
    @staticmethod
    async def crawl_website(
        url: str, 
        max_pages: int = 5, 
        timeout: int = 30, 
        selectors: Optional[List[str]] = None,
        working_dir: str = "",
        deep_crawl: Optional[str] = None,
        question: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crawl a website and extract content.
        """
        # Temporarily suppress stdout/stderr
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        try:
            # Ensure working directory exists
            if working_dir:
                os.makedirs(working_dir, exist_ok=True)
                
            # Clean URL and create output filename
            clean_url = url.replace('https://', '').replace('http://', '')
            clean_url = ''.join(c if c.isalnum() or c in '-_.' else '_' for c in clean_url.split('/')[0])
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"crawl_{clean_url}_{timestamp}.md"
            
            if working_dir:
                output_file = os.path.join(working_dir, output_file)
            
            # Result content variables
            content_to_write = ""
            extracted_text = ""
            
            if CRAWL4AI_AVAILABLE:
                try:
                    with suppress_stdout_stderr():
                        # Get crawler class
                        Crawler = getattr(crawl4ai, "AsyncWebCrawler", None) or getattr(crawl4ai, "WebCrawler", None)
                        
                        if Crawler:
                            async with Crawler() as crawler:
                                # Disable logging output
                                kwargs = {
                                    "url": url,
                                    "extract_content": True,
                                    "timeout": timeout,
                                    "show_progress": False,
                                    "verbose": False
                                }
                                
                                if hasattr(crawler, "set_verbose"):
                                    crawler.set_verbose(False)
                                
                                # Pass necessary parameters to get more complete content
                                result = await crawler.arun(**kwargs)
                                
                                # Extract markdown content - using more complete extraction logic
                                if hasattr(result, 'markdown') and result.markdown:
                                    content_to_write = result.markdown
                                    extracted_text = result.text if hasattr(result, 'text') else ""
                                elif hasattr(result, 'content') and result.content:
                                    content_to_write = f"# Content from {url}\n\n{result.content}"
                                    extracted_text = result.content
                                elif hasattr(result, 'text') and result.text:
                                    content_to_write = f"# Content from {url}\n\n{result.text}"
                                    extracted_text = result.text
                                elif hasattr(result, 'html') and result.html:
                                    # If only HTML is available, try to extract the main content
                                    content_to_write, extracted_text = CrawlerUtils._extract_from_html(result.html, url)
                        else:
                            # Use crawl function directly, add more parameters for more complete content
                            result = await crawl4ai.crawl(
                                url,
                                extract_content=True,
                                timeout=timeout
                            )
                            
                            # Same content extraction logic as above
                            if hasattr(result, 'markdown') and result.markdown:
                                content_to_write = result.markdown
                                extracted_text = result.text if hasattr(result, 'text') else ""
                            elif hasattr(result, 'content') and result.content:
                                content_to_write = f"# Content from {url}\n\n{result.content}"
                                extracted_text = result.content
                            elif hasattr(result, 'text') and result.text:
                                content_to_write = f"# Content from {url}\n\n{result.text}"
                                extracted_text = result.text
                            elif hasattr(result, 'html') and result.html:
                                content_to_write, extracted_text = CrawlerUtils._extract_from_html(result.html, url)
                    
                except Exception:
                    # Use requests as fallback method
                    content_to_write, extracted_text = await CrawlerUtils._fallback_http_get(url, timeout)
            else:
                # When crawl4ai is not available, use fallback method
                content_to_write, extracted_text = await CrawlerUtils._fallback_http_get(url, timeout)
                
            # When content is empty or only contains links, use fallback method
            if not content_to_write.strip() or ("Links:" in content_to_write and len(content_to_write.split("\n")) < 5):
                content_to_write_fallback, extracted_text_fallback = await CrawlerUtils._fallback_http_get(url, timeout)
                
                # Only use fallback content when original is empty or contains fewer lines
                if not content_to_write.strip() or content_to_write.count("\n") < content_to_write_fallback.count("\n"):
                    content_to_write = content_to_write_fallback
                    extracted_text = extracted_text_fallback
                
            # Save file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content_to_write)
            
            return {
                "status": "success",
                "pages_crawled": 1,
                "summary_file": os.path.abspath(output_file),
                "output_file": os.path.abspath(output_file),
                "content": content_to_write,
                "extracted_text": extracted_text,
                "markdown_path": os.path.abspath(output_file),
                "html_path": os.path.abspath(output_file)
            }
                
        except Exception as e:
            # Handle error case
            error_content = f"# Error crawling {url}\n\n```\n{str(e)}\n```"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(error_content)
                
            return {
                "status": "error",
                "message": f"Error crawling website: {str(e)}",
                "url": url,
                "output_file": os.path.abspath(output_file),
                "markdown_path": os.path.abspath(output_file)
            }
        finally:
            # Restore stdout/stderr
            sys.stdout, sys.stderr = old_stdout, old_stderr

    @staticmethod
    def _extract_from_html(html: str, url: str) -> tuple:
        """Extract main content and title from HTML"""
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else url
        
        # Try to extract main content area
        main_content_match = re.search(r'<(article|main|div\s+class="[^"]*content[^"]*")[^>]*>(.*?)</\1>', 
                                       html, re.IGNORECASE | re.DOTALL)
        
        content_html = main_content_match.group(2) if main_content_match else html
        
        # Clean HTML
        text = re.sub(r'<script.*?</script>', '', content_html, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Preserve paragraph structure
        text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\n\1', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<br[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<div[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</div>', '\n', text, flags=re.IGNORECASE)
        
        # Remove remaining HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n +', '\n', text)
        text = re.sub(r'\n+', '\n\n', text)
        
        # Create markdown content
        content = f"# {title}\n\n{text}"
        return content, text

    @staticmethod
    async def _fallback_http_get(url: str, timeout: int = 30) -> tuple:
        """Enhanced HTTP request fallback, providing more complete content extraction"""
        try:
            # Use async IO to avoid blocking
            loop = asyncio.get_event_loop()
            
            # Execute synchronous HTTP request in thread pool
            def fetch():
                import requests
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                }
                return requests.get(url, timeout=timeout, headers=headers).text
                
            html = await loop.run_in_executor(None, fetch)
            
            # Use more advanced content extraction methods
            try:
                # Try to use newspaper library to extract article content (if available)
                extract_with_newspaper = await loop.run_in_executor(None, lambda: CrawlerUtils._extract_with_newspaper(html, url))
                if extract_with_newspaper and len(extract_with_newspaper[0]) > 200:
                    return extract_with_newspaper
            except:
                # If newspaper extraction fails, continue with regex method
                pass
                
            # Use regex to extract content
            return CrawlerUtils._extract_from_html(html, url)
            
        except Exception as e:
            return f"# Failed to crawl {url}\n\nError: {str(e)}", ""
            
    @staticmethod
    def _extract_with_newspaper(html: str, url: str) -> tuple:
        """Use newspaper library to extract article content"""
        try:
            from newspaper import Article
            from io import StringIO
            
            # Create Article object and use provided HTML
            article = Article(url)
            article.download_state = 2  # Set as downloaded state
            article.html = html
            article.parse()
            
            title = article.title or url
            text = article.text or ""
            
            # Create markdown content
            content = f"# {title}\n\n{text}"
            
            return content, text
        except ImportError:
            # newspaper library not available
            return "", ""
        except Exception:
            # Other errors
            return "", ""

    @staticmethod
    async def _async_crawl_website(*args, **kwargs):
        """
        Internal async wrapper for crawl_website. 
        This must always be awaited by the caller.
        """
        return await CrawlerUtils.crawl_website(*args, **kwargs)