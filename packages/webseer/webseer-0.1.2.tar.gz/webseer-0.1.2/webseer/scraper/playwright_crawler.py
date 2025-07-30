import re
import asyncio
from lxml.html import fromstring
from typing import List, Optional, Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer
from fake_useragent import UserAgent
from playwright.async_api import async_playwright, Playwright
from webseer.scraper.selectors_config import *
from webseer.utils.util import clean_title, clean_date, clean_author, clean_text, deduplicate_links, parse_json
from webseer.llm.readhtml import read_html
from webseer.scraper.xpath_extractor import TitleExtractor, AuthorExtractor, TimeExtractor, ContentExtractor

class PlaywrightCrawl:
    
    def __init__(
        self,
        urls: List[str],
        logger: 'Logger',
        method: str,
        max_request_retries: int = 3,
        readerlm: Optional['PreTrainedModel'] = None,
        readertokenizer: Optional['PreTrainedTokenizer'] = None,
        instruction: Optional[str] = None,
        schema: Optional[dict] = None,
        clean_svg: bool = True,
        clean_base64: bool = True,
        title_selectors: Optional[str] = None,
        date_selectors: Optional[str] = None,
        author_selectors: Optional[str] = None,
        text_selectors: Optional[str] = None
    ):
        
        self.urls = urls
        self.logger = logger
        self.method = method
        self.max_request_retries = max_request_retries
        self.readerlm = readerlm
        self.readertokenizer = readertokenizer
        self.instruction = instruction
        self.schema = schema
        self.clean_svg = clean_svg
        self.clean_base64 = clean_base64
        self.result = {}
        
        self.title_selectors = title_selectors or TITLE_SELECTORS
        self.date_selectors = date_selectors or DATE_SELECTORS
        self.author_selectors = author_selectors or AUTHOR_SELECTORS
        self.text_selectors = text_selectors or TEXT_SELECTORS
            
        self.ua = UserAgent()
        
        self.browser_launch_options = {
            "args": ["--disable-blink-features=AutomationControlled"]
        }
        self.browser_new_context_options = {
            "user_agent": self.ua.random,
            "viewport": {"width": 1280, "height": 800},
            "locale": "zh-CN"
        }

    async def fetch_htmls(self) -> Dict[str, Any]:
        """
        Concurrently fetches the HTML content from all URLs and extracts structured data.

        Returns:
            Dict[str, Any]: A dictionary where each URL is mapped to its extracted content.
        """
        async def fetch_single_url(playwright: Playwright, url: str) -> None:
            browser, context, page = None, None, None
            retries = 0
            success = False
            
            while retries < self.max_request_retries and not success:
                try:
                    browser = await playwright.chromium.launch(**self.browser_launch_options)
                    context = await browser.new_context(**self.browser_new_context_options)
                    page = await context.new_page()
                    
                    await page.goto(url, wait_until='load', timeout=15000)

                    html = await page.content()
                    self.logger.info(f'Fetched HTML from {url}')
                    
                    title, date, author, text, links = None, None, None, None, None
                    
                    if self.method == 'readerlm' and self.readerlm and self.readertokenizer:
                        try:
                            json_result = read_html(
                                html=html,
                                readlm=self.readerlm,
                                readtokenizer=self.readertokenizer,
                                instruction=self.instruction,
                                schema=self.schema,
                                clean_svg=self.clean_svg,
                                clean_base64=self.clean_base64
                            )
                            dict_result = parse_json(json_str=json_result)
                            if dict_result is not None:
                                title = dict_result.get('title')
                                date = dict_result.get('date')
                                author = dict_result.get('author')
                                text = dict_result.get('content')
                                success = True
                        except Exception as e:
                            self.logger.error(f'[✘] ReaderLM Extraction Exception:{e}')
                    
                    elif self.method == 'xpath':
                        try:
                            html = re.sub('</?br.*?>', '', html)
                            element = fromstring(html)
                            
                            title = TitleExtractor().extract(element)
                            date = TimeExtractor().extract(element)
                            author = AuthorExtractor().extract(element)
                            content_result = ContentExtractor().extract(element)
                            text = content_result[0][1]['text'] if content_result else None
                            
                            success = True
                        except Exception as e:
                            self.logger.error(f'[✘] XPath Extraction Exception: {e}')
                    
                    elif self.method == 'selector':
                        try:
                            title_elements = await page.query_selector_all(self.title_selectors)
                            title_texts = [
                                await el.inner_text() 
                                for el in title_elements 
                                if await el.inner_text() and not re.match(r'^(©|大家都在看)', await el.inner_text())
                            ]
                            title = clean_title(title_texts) if title_texts else None
                            
                            date_elements = await page.query_selector_all(self.date_selectors)
                            date_texts = [
                                await el.inner_text() 
                                for el in date_elements 
                                if await el.inner_text()
                            ]
                            date = clean_date(date_texts) if date_texts else None
                            
                            author_elements = await page.query_selector_all(self.author_selectors)
                            author_texts = [
                                await el.inner_text() 
                                for el in author_elements 
                                if await el.inner_text() and '责任编辑' not in await el.inner_text()
                            ]
                            author = clean_author(author_texts) if author_texts else None
                            
                            text_elements = await page.query_selector_all(self.text_selectors)
                            text_contents = [
                                await el.inner_text() 
                                for el in text_elements 
                                if await el.inner_text() and 
                                len(await el.inner_text()) > 20 and 
                                not re.match(r'^(©|广告|导航|返回)', await el.inner_text())
                            ]
                            text = '\n'.join([clean_text(t) for t in text_contents]) if text_contents else None
                            
                            link_elements = await page.query_selector_all('a[href]')
                            links = [
                                {
                                    'href': await el.get_attribute('href'),
                                    'text': await el.inner_text() or ''
                                }
                                for el in link_elements
                                if (await el.inner_text() or '').strip() and len((await el.inner_text() or '').strip()) > 10
                            ]
                            links = deduplicate_links(links)
                            
                            success = True
                        except Exception as e:
                            self.logger.error(f'[✘] Selector Extraction Exception: {e}')
                    
                    self.result[url] = {
                        'title': title,
                        'author': author,
                        'date': date,
                        'text': text,
                        'links': links,
                        'raw_html': html,
                        'success': success
                    }
                    
                    self.logger.info(f"[✔] Successfully scraped URL: {url}")
                
                except Exception as e:
                    self.logger.error(f"[✘] Failed to scrape {url}: {e}", exc_info=True)
                    self.result[url] = {
                        'title': None,
                        'author': None,
                        'date': None,
                        'text': None,
                        'links': None,
                        'raw_html': None,
                        'success': False
                    }
                finally:
                    if page:
                        await page.close()
                    if context:
                        await context.close()
                    if browser:
                        await browser.close()

        async with async_playwright() as playwright:
            await asyncio.gather(*[fetch_single_url(playwright, url) for url in self.urls])
            
        return self.result