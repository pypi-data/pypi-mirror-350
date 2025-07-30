'''
Description:  
Author: Huang J
Date: 2025-04-28 15:04:26
'''
import sys
import os
import re
import uuid
import json
from loguru import logger
from typing import List, Dict, Optional, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer
from tqdm import tqdm 
from json_repair import repair_json
import validators
from datetime import datetime
from langdetect import detect, LangDetectException
from lxml.html import HtmlElement
from urllib.parse import urlparse, urljoin
from chunk_factory import Chunker

from webseer.llm.llm_filter import llm_margin_prob
from webseer.utils.prompts import RELATED_URL_PROMPT, RELATED_CHUNK_PROMPT

SCRIPT_PATTERN = r"<[ ]*script.*?\/[ ]*script[ ]*>"
STYLE_PATTERN = r"<[ ]*style.*?\/[ ]*style[ ]*>"
META_PATTERN = r"<[ ]*meta.*?>"
COMMENT_PATTERN = r"<[ ]*!--.*?--[ ]*>"
LINK_PATTERN = r"<[ ]*link.*?>"
BASE64_IMG_PATTERN = r'<img[^>]+src="data:image/[^;]+;base64,[^"]+"[^>]*>'
SVG_PATTERN = r"(<svg[^>]*>)(.*?)(<\/svg>)"

def get_logger(log_dir:str):
    """
    Configures and returns a logger instance that logs to both stdout and a log file.

    Parameters:
    log_dir (str): The directory where log files will be saved.

    Returns:
    logger: A loguru logger instance configured with stdout and file outputs.
    """
    logger.remove()
    log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file.name}:{line} | {message}"
    logger.add(sys.stdout, format = log_format, level = "INFO", colorize = True)
    logger.add(os.path.join(log_dir, "scraper_{time:YYYY-MM-DD}.log"), format=log_format, level="INFO", rotation="00:00", retention="7 days", compression="zip")
    return logger

def generate_unique_id(prefix):
    """
    Generates a unique ID based on the current timestamp and a UUID.

    Parameters:
    prefix (str): A prefix to prepend to the generated ID.

    Returns:
    str: A unique ID in the format: "<prefix><timestamp>_<uuid>".
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex
    return f"{prefix}{now}_{unique_id}"

def get_more_related_url(desc: str,
    links: List[Dict[str, str]],
    encode_model: 'PreTrainedModel',
    logger: 'Logger',
    llm: Optional['PreTrainedModel'] = None,
    tokenizer: Optional['PreTrainedTokenizer'] = None,
    sim_threshold: float = 0.4,
    llm_range: Optional[tuple] = None
) -> Set[str]:
    """
    Finds more related URLs by comparing a description to the links' text using an encoding model 
    and optionally a language model.

    Parameters:
    desc (str): The description or focus point for similarity matching.
    links (List[Dict[str, str]]): A list of dictionaries where each dictionary contains 'href' (URL) and 'text' (URL text).
    encode_model (PreTrainedModel): The model used for encoding the description and URL text for similarity comparison.
    logger (logger): The logger instance to log related URL findings.
    llm (Optional[PreTrainedModel]): A language model used for further checking the relevance of the URLs (default is None).
    tokenizer (Optional[PreTrainedTokenizer]): The tokenizer used for the LLM (default is None).
    sim_threshold (float): The threshold for considering a URL as related based on the similarity score (default is 0.4).
    llm_range (Optional[tuple]): A tuple defining the range of similarity scores for which to use the LLM for additional relevance checks (default is None).

    Returns:
    Set[str]: A set of URLs that are related to the description.
    """
    more_related_urls = set()
    if sim_threshold and llm_range is None:
        llm_range = (sim_threshold-0.1,sim_threshold)
    for link in tqdm(links,desc='Acquire related url...'):
        url = link['href']
        url_text = link['text']
        
        embeddings = encode_model.encode([url_text, desc],task="text-matching",show_progress_bar=False)
        score = embeddings[0] @ embeddings[1].T
        
        if score>sim_threshold:
            logger.info(f'Focus: {desc}; Related URL: {url_text}, {url}; Relevance score: {score}')
            more_related_urls.add(url)
            
        if llm and tokenizer and llm_range[0]<score<llm_range[1]:
            if llm_margin_prob(text1 = desc,text2 = url_text,model = llm,tokenizer = tokenizer,prompt = RELATED_URL_PROMPT):
                more_related_urls.add(url)
                logger.info(f'Focus: {desc}; Related URL: {url_text}, {url}; Relevance score: {score}; Relevance score is low, but the model considers it relevant.')
                
    return more_related_urls

def detect_language(text: str) -> str:
    """
    Detects the language of the given text.

    Parameters:
    text (str): The input text whose language is to be detected.

    Returns:
    str: 'zh' if the text is in Chinese (including mixed language), 'en' if the text is in English.
    """
    if not text.strip():
        return "zh"
    
    try:
        lang = detect(text)
        if lang in ['zh-cn', 'zh-tw']:
            return "zh"
        elif lang == 'en':
            return "en"
    except LangDetectException:
        pass 

    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', text))
    has_english = bool(re.search(r'[a-zA-Z]', text))
    
    if has_chinese:
        return "zh"  
    elif has_english:
        return "en" 
    else:
        return "zh" 

def text_chunk(
    text: str,
    seg_size: int = 200,
    seg_overlap: int = 0,
    llm: Optional['PreTrainedModel'] = None,
    tokenizer: Optional['PreTrainedTokenizer'] = None
) -> List[str]:
    """
    Splits the input text into smaller chunks based on segment size and overlap.

    Parameters:
    text (str): The input text to be chunked.
    seg_size (int, optional): The size of each chunk (default is 200).
    seg_overlap (int, optional): The overlap between chunks (default is 0).
    llm (Optional[PreTrainedModel], optional): The language model to use for chunking (default is None).
    tokenizer (Optional[PreTrainedTokenizer], optional): The tokenizer to use for chunking (default is None).

    Returns:
    List[str]: A list of text chunks.
    """
    
    text_chunks = []
    text_len = len(text.replace('\n','').replace(' ',''))
    
    if text_len>200:
        language = detect_language(text)
        ck = Chunker(text = text,language = language)
        
        if llm and tokenizer:
            segment_chunks = ck.msp_chunk(model = llm,tokenizer = tokenizer,threshold = 0.07)
            text_chunks.extend(segment_chunks)
        else:
            ck = Chunker(text = text,language = language)
            if language=='zh':
                separators = ['\n\n', '\n', '。', '！', '？']
            else:
                separators = ['\n\n', '\n', '.', '!', '?']
            segment_chunks = ck.segment_chunk(seg_size = seg_size,seg_overlap = seg_overlap,separators = separators)
            text_chunks.extend(segment_chunks)
            
    else:
        text_chunks.append(text)
        
    return text_chunks

def get_more_related_chunk(
    desc: str,
    text_chunks: List[str],
    encode_model: 'PreTrainedModel',
    logger: Optional['Logger'] = None,
    llm: Optional['PreTrainedModel'] = None,
    tokenizer: Optional['PreTrainedTokenizer'] = None,
    sim_threshold: float = 0.5,
    llm_range: Optional[tuple] = None
) -> Set[str]:
    """
    Finds chunks of text related to a given description by comparing similarity scores.

    Parameters:
    desc (str): The description to compare against.
    text_chunks (List[str]): A list of text chunks to search for related content.
    encode_model (PreTrainedModel): The model used to encode and compare text.
    logger (Optional[Logger], optional): The logger for logging related chunk information (default is None).
    llm (Optional[PreTrainedModel], optional): The language model to use for further evaluation (default is None).
    tokenizer (Optional[PreTrainedTokenizer], optional): The tokenizer to use with the language model (default is None).
    sim_threshold (float, optional): The similarity threshold for considering a chunk related (default is 0.5).
    llm_range (Optional[tuple], optional): The range of similarity scores to trigger the language model check (default is None).

    Returns:
    Set[str]: A set of related text chunks based on the description.
    """
    
    more_related_chunks = set()
    if sim_threshold and llm_range is None:
        llm_range = (sim_threshold - 0.2,sim_threshold)
        
    for text_chunk in tqdm(text_chunks,desc = 'Acquire related text chunk...'):
        embeddings = encode_model.encode([text_chunk, desc],task = "text-matching",show_progress_bar = False)
        score = embeddings[0] @ embeddings[1].T
        
        if score>sim_threshold:
            logger.info(f'Focus: {desc}; Related text chunk: {text_chunk}; Relevance score: {score}')
            more_related_chunks.add(text_chunk)
            
        if llm and tokenizer and llm_range[0]<score<llm_range[1]:
            if llm_margin_prob(text1 = desc,text2 = text_chunks,model = llm,tokenizer = tokenizer,prompt = RELATED_CHUNK_PROMPT):
                more_related_chunks.add(text_chunk)
                logger.info(f'Focus: {desc}; Related text chunk: {text_chunk}; Relevance score: {score}; Relevance score is low, but the model considers it related to the focus.')
                
    return more_related_chunks

def is_detail_page(
    title: Optional[str],
    author: Optional[str],
    text: Optional[str],
    links: List[str],
    flag_crawled: bool
) -> bool:
    """
    Determines if a page is a detail page based on certain conditions.

    Parameters:
    title (Optional[str]): The title of the page.
    author (Optional[str]): The author of the page.
    text (Optional[str]): The main content text of the page.
    links (List[str]): List of links found on the page.
    flag_crawled (bool): Flag indicating if the page has already been crawled.

    Returns:
    bool: True if the page meets the criteria of a detail page, otherwise False.
    """
    
    if flag_crawled:
        return False
    
    if not title and not author and not text and not links:
        return False
    
    elif not text:
        return False
    
    elif len(text)<10:
        return False
    
    elif len(links)>30:
        return False
    
    elif not title and not author and len(text)<100:
        return False
    
    elif title and author and len(text)>100:
        return True
    
    elif 'var' in text or 'margin-top' in text or 'margin-bottom' in text or 'width' in text or 'background' in text:
        return False

    score = 0
    score+=len(text)/200
    
    if len(links)>15:
        score = score-(len(links)-15)/10
        
    if score>1.5:
        return True
    else:
        return False
    
def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted whitespace, special characters, and unnecessary parts.

    Parameters:
    text (str): The input text to clean.

    Returns:
    str: The cleaned text.
    """
    text_list = text.split('\n')
    cleaned_text = []

    for t in text_list:
        t = t.strip(' ').strip('\u2003').strip('\n')
        if t and t != '分享新闻卡片': 
            cleaned_text.append(t)

    return '\n'.join(cleaned_text)


def clean_title(
    titles: Optional[List[str]],
    invalid_titles: List[str] = ['搜狐号', '选择@的用户', '相关推荐', '热点推荐', '相关推荐\n换一换', '发表评论', '安全验证']
) -> Optional[str]:
    """
    Cleans and filters out invalid titles.

    Parameters:
    titles (Optional[List[str]]): A list of titles to filter.
    invalid_titles (List[str], optional): A list of invalid titles to filter out (default includes common unwanted titles).

    Returns:
    Optional[str]: The cleaned title, or None if no valid title is found.
    """

    if titles:
        filter_titles = [t for t in titles if t not in invalid_titles]
        title = filter_titles[0]
        title = title.strip('\n').split('\n')[0]
    else:
        title = None
        
    return title


def clean_date(dates: List[str]) -> Optional[str]:
    """
    Cleans and formats a list of date strings into a standardized format.

    Parameters:
    dates (List[str]): A list of date strings to clean and format.

    Returns:
    Optional[str]: The first valid date in "YYYY-MM-DD" format, or None if no valid date is found.
    """
    
    pattern = r'''
            (?:
                (\d{4})[年/-](\d{1,2})[月/-](\d{1,2})日?
            )
            |
            (?:
                (\d{4})(\d{2})(\d{2})                
            )
        '''
        
    date_list = []
    
    if dates:
        for date in dates:
            date = date.strip().replace('\n','').replace(' ','').replace('/','').replace('\t','').replace('—','').replace('-','')
            match = re.search(pattern, date, re.VERBOSE)
            if not match:
                continue
            y = match.group(1) or match.group(4)
            m = match.group(2) or match.group(5)
            d = match.group(3) or match.group(6)

            if y and m and d:
                tmp_date = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
                if tmp_date not in date_list:
                    date_list.append(tmp_date)
                else:
                    return tmp_date
                
        if date_list:
            return date_list[0]
        
    return None


def clean_author(authors: List[str], invalid_authors: List[str] = ['推荐阅读']) -> Optional[str]:
    """
    Cleans and filters the list of author names to return the longest valid author name.

    Parameters:
    authors (List[str]): A list of author names to clean and filter.
    invalid_authors (List[str], optional): A list of invalid authors to filter out (default includes '推荐阅读').

    Returns:
    Optional[str]: The longest valid author name, or None if no valid author is found.
    """

    if authors:
        filter_authors = [a for a in authors if a not in invalid_authors]
        author = max(filter_authors, key=len)
        author = author.strip().replace('\n','')
        return author
    
    return None


def deduplicate_links(links: List[dict]) -> List[dict]:
    """
    Removes duplicate links based on their 'href' and 'text' attributes.

    Parameters:
    links (List[dict]): A list of links (dictionaries containing 'href' and 'text' keys).

    Returns:
    List[dict]: A list of unique links.
    """
    seen = set()
    unique_links = []
    
    for link in links:
        href = link.get("href", "").strip()
        flag = bool(validators.url(href))
        if flag:
            text = link.get("text", "").strip()
            key = (href, text)
            if key not in seen:
                seen.add(key)
                unique_links.append({"href": href, "text": text})
    
    return unique_links


def replace_svg(html: str, new_content: str = "this is a placeholder") -> str:
    """
    Replaces all SVG elements in the HTML with a placeholder content.

    Parameters:
    html (str): The HTML string to modify.
    new_content (str, optional): The new content to replace the SVG elements with (default is 'this is a placeholder').

    Returns:
    str: The modified HTML string with replaced SVG content.
    """
    return re.sub(
        SVG_PATTERN,
        lambda match: f"{match.group(1)}{new_content}{match.group(3)}",
        html,
        flags=re.DOTALL,
    )


def replace_base64_images(html: str, new_image_src: str = "#") -> str:
    """
    Replaces all base64 encoded images in the HTML with a placeholder image source.

    Parameters:
    html (str): The HTML string to modify.
    new_image_src (str, optional): The new image source to replace the base64 images with (default is '#').

    Returns:
    str: The modified HTML string with replaced base64 images.
    """
    return re.sub(BASE64_IMG_PATTERN, f'<img src="{new_image_src}"/>', html)

def clean_html(html: str, clean_svg: bool = True, clean_base64: bool = True) -> str:
    """
    Cleans the HTML by removing unwanted elements and optionally replacing SVG and base64 images.

    Parameters:
    html (str): The HTML string to clean.
    clean_svg (bool, optional): Whether to replace SVG elements (default is True).
    clean_base64 (bool, optional): Whether to replace base64 images (default is True).

    Returns:
    str: The cleaned HTML string.
    """

    html = re.sub(
        SCRIPT_PATTERN, "", html, flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        STYLE_PATTERN, "", html, flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        META_PATTERN, "", html, flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        COMMENT_PATTERN, "", html, flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        LINK_PATTERN, "", html, flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    if clean_svg:
        html = replace_svg(html)
    if clean_base64:
        html = replace_base64_images(html)
        
    return html

def parse_json(json_str: str) -> Optional[dict]:
    """
    Parses a JSON string into a Python dictionary.

    Parameters:
    json_str (str): The JSON string to parse.

    Returns:
    Optional[dict]: The parsed dictionary, or None if parsing fails.
    """

    json_str = repair_json(json_str)
    try:
        data = json.loads(json_str)
        return data
    
    except json.JSONDecodeError:
        return None
    
def get_longest_common_sub_string(str1: str, str2: str) -> str:
    """
    Finds the longest common substring between two strings.

    This function constructs a matrix where the horizontal axis is `str1` 
    and the vertical axis is `str2`. The longest common substring is located 
    along the diagonal with the maximum length.

    Args:
        str1 (str): The first input string.
        str2 (str): The second input string.

    Returns:
        str: The longest common substring.
    """

    if not all([str1, str2]):
        return ''
    
    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    max_length = 0
    start_position = 0
    
    for index_of_str1 in range(1, len(str1) + 1):
        for index_of_str2 in range(1, len(str2) + 1):
            
            if str1[index_of_str1 - 1] == str2[index_of_str2 - 1]:
                matrix[index_of_str1][index_of_str2] = matrix[index_of_str1 - 1][index_of_str2 - 1] + 1
                if matrix[index_of_str1][index_of_str2] > max_length:
                    max_length = matrix[index_of_str1][index_of_str2]
                    start_position = index_of_str1 - max_length
            else:
                matrix[index_of_str1][index_of_str2] = 0
                
    return str1[start_position: start_position + max_length]

def iter_node(element: HtmlElement) -> HtmlElement:
    """
    Recursively yields an HTML element and its sub-elements.

    This function is a generator that iterates through an HTML element and
    its child elements recursively.

    Args:
        element (HtmlElement): The root HTML element to start iteration from.

    Yields:
        HtmlElement: A single HTML element in the tree.
    """
    
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)
            
            
def pad_host_for_images(host: str, url: str) -> str:
    """
    Pads the provided URL with a host if it's a relative or incomplete URL.

    This function handles different formats of image URLs:
    - Full absolute URLs: https://example.com/1.jpg
    - Relative URLs: /1.jpg
    - Host without scheme: example.com/1.jpg or ://example.com/1.jpg

    Args:
        host (str): The host URL that will be used to complete relative URLs.
        url (str): The URL to be padded.

    Returns:
        str: The full, padded URL.
    """
    if url.startswith('http'):
        return url
    parsed_uri = urlparse(host)
    scheme = parsed_uri.scheme
    if url.startswith(':'):
        return f'{scheme}{url}'
    if url.startswith('//'):
        return f'{scheme}:{url}'
    return urljoin(host, url)

def get_high_weight_keyword_pattern() -> re.Pattern:
    """
    Returns a compiled regular expression pattern to match high-weight keywords.

    The keywords represent important parts of web content, such as articles and news text.

    Returns:
        re.Pattern: A compiled regular expression pattern for matching high-weight keywords.
    """
    
    HIGH_WEIGHT_ARRT_KEYWORD = ['content','article','news_txt','pages_content','post_text']
    return re.compile('|'.join(HIGH_WEIGHT_ARRT_KEYWORD), flags=re.I)