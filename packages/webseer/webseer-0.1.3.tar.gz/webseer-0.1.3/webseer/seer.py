'''
Description:  
Author: Huang J
Date: 2025-04-28 15:02:42
'''

import os
from pathlib import Path
import asyncio
from typing import List, Dict, Optional, Tuple, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer

from webseer.utils.util import get_logger, get_more_related_url, text_chunk, get_more_related_chunk, generate_unique_id, is_detail_page
from webseer.scraper.playwright_crawler import PlaywrightCrawl
from webseer.store.db_connect import check_database_and_tables, close_db
from webseer.store.db_writer import insert_article, insert_chunk, check_article_exists

# current_dir = os.path.dirname(Path(__file__))
# log_dir = os.path.join(current_dir, 'logs')
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir, exist_ok=True)
    
# logger = get_logger(log_dir=log_dir)

class Seer:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        logger_dir: str,
        encode_model: 'PreTrainedModel',
        extract_method: str,
        max_request_retries: int = 3,
        readerlm: Optional['PreTrainedModel'] = None,
        readertokenizer: Optional['PreTrainedTokenizer'] = None,
        instruction: Optional[str] = None,
        schema: Optional[str] = None,
        clean_svg: bool = True,
        clean_base64: bool = True,
        title_selectors: Optional[List[str]] = None,
        date_selectors: Optional[List[str]] = None,
        author_selectors: Optional[List[str]] = None,
        text_selectors: Optional[List[str]] = None
    ) -> None:
        """
        Initializes the Webseer instance.

        Parameters:
        host (str): The database host address.
        port (int): The database port number.
        user (str): The database username.
        password (str): The database password.
        encode_model (PreTrainedModel): The encoding model used for similarity calculation.
        extract_method (str): The web page extraction method.
        max_request_retries (int): The maximum number of request retries (default is 3).
        readerlm (Optional[PreTrainedModel]): The language model for reading web pages (default is None).
        readertokenizer (Optional[PreTrainedTokenizer]): The tokenizer for the reading language model (default is None).
        instruction (Optional[str]): Instruction prompt for the language model (default is None).
        schema (Optional[str]): The schema definition for data extraction (default is None).
        clean_svg (bool): Whether to clean SVG (default is True).
        clean_base64 (bool): Whether to clean base64 images (default is True).
        title_selectors (Optional[List[str]]): List of CSS selectors for extracting titles (default is None).
        date_selectors (Optional[List[str]]): List of CSS selectors for extracting dates (default is None).
        author_selectors (Optional[List[str]]): List of CSS selectors for extracting authors (default is None).
        text_selectors (Optional[List[str]]): List of CSS selectors for extracting the main text (default is None).
        """
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
        log_dir = os.path.join(logger_dir, 'webseer_logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        logger = get_logger(log_dir=log_dir)
        self.logger = logger
        self.logger.info(f'Log file path: {log_dir}/webseer_logs')
        
        self.encode_model = encode_model
        
        self.extract_method = extract_method
        self.max_request_retries = max_request_retries
        self.readerlm = readerlm
        self.readertokenizer = readertokenizer
        self.instruction = instruction
        self.schema = schema
        self.clean_svg = clean_svg
        self.clean_base64 = clean_base64
        self.title_selectors = title_selectors
        self.date_selectors = date_selectors
        self.author_selectors = author_selectors
        self.text_selectors = text_selectors

    async def crawler(self,
        focus: str,
        urls: List[str],
        db: Optional[Any] = None,
        cursor: Optional[Any] = None,
        llm: Optional['PreTrainedModel'] = None,
        tokenizer: Optional['PreTrainedTokenizer'] = None,
        chunk_sim_threshold: float = 0.5,
        url_sim_threshold: float = 0.5,
        chunk_llm_range: Optional[Tuple[int, int]] = None,
        url_llm_range: Optional[Tuple[int, int]] = None,
        seg_size: int = 200,
        seg_overlap: int = 0,
        multi_focus: bool = True,
        batch_size: int = 5
    ) -> None:
        """
        Retrieves information based on a specific focus point and performs content similarity mining.

        Parameters:
        focus (str): The current focus point for content retrieval.
        urls (List[str]): A list of URLs related to the focus point.
        db (Optional[Any]): The database connection (default is None).
        cursor (Optional[Any]): The database cursor (default is None).
        llm (Optional[PreTrainedModel]): The language model for similarity comparison (default is None).
        tokenizer (Optional[PreTrainedTokenizer]): The tokenizer used for tokenization (default is None).
        chunk_sim_threshold (float): The threshold for content chunk similarity (default is 0.5).
        url_sim_threshold (float): The threshold for URL similarity (default is 0.5).
        chunk_llm_range (Optional[Tuple[int, int]]): The range of comparison for LLM (default is None).
        url_llm_range (Optional[Tuple[int, int]]): The range of comparison for URL LLM (default is None).
        seg_size (int): The size of each text segment (default is 200).
        seg_overlap (int): The overlap size between text segments (default is 0).
        multi_focus (bool): Whether this is a multi-focus task (default is True).
        batch_size (int): The number of URLs to process per batch (default is 5).

        Returns:
        None: This function is asynchronous and does not return a value, as it performs tasks such as database updates.
        """
        if db is None or cursor is None:
            db, cursor = check_database_and_tables(
                host = self.host, 
                port = self.port, 
                user = self.user, 
                password = self.password, 
                logger = self.logger
            )
        
        valid_urls = set(urls)
        invalid_urls = set()
        crawled_urls = set()
        chunk_count = 0
        article_count = 0
        related_url_count = 0
        

        while valid_urls:
            current_batch = list(valid_urls)[:batch_size]
            
            playwrightcrawler = PlaywrightCrawl(
                urls = current_batch,
                logger = self.logger,
                method = self.extract_method,
                max_request_retries = self.max_request_retries,
                readerlm = self.readerlm,
                readertokenizer = self.readertokenizer,
                instruction = self.instruction,
                schema = self.schema,
                clean_svg = self.clean_svg,
                clean_base64 = self.clean_base64,
                title_selectors = self.title_selectors,
                date_selectors = self.date_selectors,
                author_selectors = self.author_selectors,
                text_selectors = self.text_selectors
            )
            
            crawl_results = await playwrightcrawler.fetch_htmls()

            for url in current_batch:
                new_more_related_url = set()
                flag_crawled = False
                
                if url not in crawl_results:
                    self.logger.error(f"Fetch error on {url}")
                    invalid_urls.add(url)
                    valid_urls.discard(url)
                    continue

                if check_article_exists(cursor=cursor, url=url):
                    
                    self.logger.info(f"'{url}' has already been crawled!")
                    crawled_urls.add(url)
                    valid_urls.discard(url)
                    related_url_count+=1
                    flag_crawled = True
                    
                info = crawl_results[url]
                success = info['success']
                
                if success:
                    title = info['title']
                    author = info['author']
                    date = info['date']
                    text = info['text']
                    raw_html = info['raw_html']
                    links = info['links']
                    
                    if is_detail_page(title=title, author=author, text=text, links=links,flag_crawled=flag_crawled):
                        self.logger.info('Chunking text...')
                        text_chunks = text_chunk(
                            text=text, 
                            seg_size=seg_size, 
                            seg_overlap=seg_overlap, 
                            llm=llm, 
                            tokenizer=tokenizer
                        )
                        aid = generate_unique_id('A')
                        text_chunks_str = '\n\n'.join(text_chunks)
                        
                        self.logger.info(f'Focus: {focus}; Add article title: {title}')
                        insert_article(
                            db=db, 
                            cursor=cursor, 
                            id=aid, 
                            title=title, 
                            author=author, 
                            date=date, 
                            url=url, 
                            text=text, 
                            text_chunks=text_chunks_str, 
                            links=links, 
                            logger=self.logger
                        )
                        
                        more_related_chunks = get_more_related_chunk(
                            desc=focus, 
                            text_chunks=text_chunks, 
                            encode_model=self.encode_model, 
                            logger=self.logger, 
                            llm=llm, 
                            tokenizer=tokenizer, 
                            sim_threshold=chunk_sim_threshold, 
                            llm_range=chunk_llm_range
                        )
                        
                        related_chunk_num = len(more_related_chunks)
                        chunk_count += related_chunk_num
                        
                        if more_related_chunks:
                            related_chunks_str = '\n'.join(more_related_chunks)
                            self.logger.info(f'Focus: {focus}; {len(more_related_chunks)} related text chunks:\n{related_chunks_str}')
                            
                            article_count += 1
                            for more_related_chunk in more_related_chunks:
                                cid = generate_unique_id('C')
                                insert_chunk(
                                    db=db, 
                                    cursor=cursor, 
                                    id=cid, 
                                    focus=focus, 
                                    chunk=more_related_chunk, 
                                    article_id=aid, 
                                    logger=self.logger
                                )
                        
                        crawled_urls.add(url)
                    else:
                        crawled_urls.add(url)
                        
                    related_url = get_more_related_url(
                        desc=focus, 
                        links=links, 
                        encode_model=self.encode_model, 
                        logger=self.logger, 
                        llm=llm, 
                        tokenizer=tokenizer, 
                        sim_threshold=url_sim_threshold, 
                        llm_range=url_llm_range
                    )
                    
                    if related_url:
                        related_url_str = '\n'.join(related_url)
                        self.logger.info(f'Focus: {focus}; {len(related_url)} related url:\n{related_url_str}')
                    new_more_related_url.update(related_url)
                    
                else:
                    invalid_urls.add(url)
                
                valid_urls.discard(url)
                related_url_count +=len(new_more_related_url - invalid_urls - crawled_urls)
                valid_urls.update(new_more_related_url - invalid_urls - crawled_urls)
            self.logger.info(f'Focus: {focus}; URLs to crawl: {len(valid_urls)}; URLs crawled: {len(crawled_urls)}; Invalid URLs: {len(invalid_urls)}')
        self.logger.info(f'Focus: {focus}; Fetched {article_count} news articles in this batch; {chunk_count} related text chunks; {related_url_count} related URLs')
        
        if not multi_focus:
            close_db(db=db, cursor=cursor)

    async def multicrawler(
        self,
        focus_urls: Dict[str, List[str]],
        llm: Optional['PreTrainedModel'] = None,
        tokenizer: Optional['PreTrainedTokenizer'] = None,
        chunk_sim_threshold: float = 0.5,
        url_sim_threshold: float = 0.5,
        chunk_llm_range: Optional[Tuple[int, int]] = None,
        url_llm_range: Optional[Tuple[int, int]] = None,
        seg_size: int = 200,
        seg_overlap: int = 0,
        max_focus_tasks: int = 5,
        multi_focus: bool = True
    ) -> None:
        """
        Crawls multiple focus points with their respective URLs, using a language model for content 
        similarity comparison.

        Parameters:
        focus_urls (Dict[str, List[str]]): A dictionary where keys are focus points and values are 
                                           lists of URLs related to each focus point.
        llm (Optional[PreTrainedModel]): The language model for similarity comparison (default is None).
        tokenizer (Optional[PreTrainedTokenizer]): The tokenizer used for tokenization (default is None).
        chunk_sim_threshold (float): The threshold for chunk similarity (default is 0.5).
        url_sim_threshold (float): The threshold for URL similarity (default is 0.5).
        chunk_llm_range (Optional[Tuple[int, int]]): The range of LLM comparison for content chunks 
                                                     (default is None).
        url_llm_range (Optional[Tuple[int, int]]): The range of LLM comparison for URLs (default is None).
        seg_size (int): The size of each text segment (default is 200).
        seg_overlap (int): The overlap between text segments (default is 0).
        max_focus_tasks (int): The maximum number of focus tasks to run concurrently (default is 5).
        multi_focus (bool): Whether the task involves multiple focus points (default is True).

        Returns:
        None: This function is asynchronous and does not return a value, as it performs crawling tasks.
        """
        
        tasks = []
        for focus, urls in focus_urls.items():
            db, cursor = check_database_and_tables(
                host = self.host,
                port = self.port, 
                user = self.user, 
                password = self.password, 
                logger = self.logger
            )
            
            task = asyncio.create_task(
                self.crawler(
                    focus = focus, 
                    urls = urls,
                    db = db,  
                    cursor = cursor, 
                    llm = llm, 
                    tokenizer = tokenizer, 
                    chunk_sim_threshold = chunk_sim_threshold, 
                    url_sim_threshold = url_sim_threshold, 
                    chunk_llm_range = chunk_llm_range, 
                    url_llm_range = url_llm_range, 
                    seg_size = seg_size, 
                    seg_overlap = seg_overlap,
                    multi_focus = multi_focus
                )
            )
            tasks.append(task)
            
        sem = asyncio.Semaphore(max_focus_tasks)
        async def sem_task(task):
            async with sem:
                await task
        
        await asyncio.gather(*(sem_task(t) for t in tasks))
        