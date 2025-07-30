'''
Description:  
Author: Huang J
Date: 2025-05-11 22:40:13
'''


import re
import json
from lxml.html import etree
from html import unescape
from lxml.html import HtmlElement
from typing import Any, Dict, List, Tuple, Union
import numpy as np

from webseer.utils.util import get_longest_common_sub_string,iter_node, pad_host_for_images, get_high_weight_keyword_pattern

TITLE_HTAG_XPATH = '//h1//text() | //h2//text() | //h3//text() | //h4//text()'
TITLE_SPLIT_CHAR_PATTERN = '[-_|]'

AUTHOR_PATTERN = [
            "责编[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "责任编辑[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "作者[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "编辑[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "文[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "原创[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "撰文[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：]",
            "来源[：|:| |丨|/]\s*([\u4E00-\u9FA5a-zA-Z]{2,20})[^\u4E00-\u9FA5|:|：|<]"
]

DATETIME_PATTERN = [
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{4}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{2}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    "(\d{4}年\d{1,2}月\d{1,2}日)",
    "(\d{2}年\d{1,2}月\d{1,2}日)",
    "(\d{1,2}月\d{1,2}日)"
]

PUBLISH_TIME_META = [
    '//meta[starts-with(@property, "rnews:datePublished")]/@content',
    '//meta[starts-with(@property, "article:published_time")]/@content',
    '//meta[starts-with(@property, "og:published_time")]/@content',
    '//meta[starts-with(@property, "og:release_date")]/@content',
    '//meta[starts-with(@itemprop, "datePublished")]/@content',
    '//meta[starts-with(@itemprop, "dateUpdate")]/@content',
    '//meta[starts-with(@name, "OriginalPublicationDate")]/@content',
    '//meta[starts-with(@name, "article_date_original")]/@content',
    '//meta[starts-with(@name, "og:time")]/@content',
    '//meta[starts-with(@name, "apub:time")]/@content',
    '//meta[starts-with(@name, "publication_date")]/@content',
    '//meta[starts-with(@name, "sailthru.date")]/@content',
    '//meta[starts-with(@name, "PublishDate")]/@content',
    '//meta[starts-with(@name, "publishdate")]/@content',
    '//meta[starts-with(@name, "PubDate")]/@content',
    '//meta[starts-with(@name, "pubtime")]/@content',
    '//meta[starts-with(@name, "_pubtime")]/@content',
    '//meta[starts-with(@name, "weibo: article:create_at")]/@content',
    '//meta[starts-with(@pubdate, "pubdate")]/@content',
]

class AuthorExtractor:
    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN

    def extract(self, element: HtmlElement, author_xpath: str = '') -> str:
        """
        Extracts the author from a given HTML element.

        Args:
            element (HtmlElement): The HTML element to search within.
            author_xpath (str): Optional XPath string to directly extract the author.

        Returns:
            str: The extracted author's name, or an empty string if not found.
        """
        if author_xpath:
            author = ''.join(element.xpath(author_xpath))
            return author
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = re.search(pattern, text)
            if author_obj:
                return author_obj.group(1)
        return ''

class TitleExtractor:
    
    def extract_by_xpath(self, element: HtmlElement, title_xpath: str) -> str:
        """
        Extracts the title using a custom XPath expression.

        Args:
            element (HtmlElement): The HTML element to search.
            title_xpath (str): The XPath expression for locating the title.

        Returns:
            str: The extracted title, or an empty string if not found.
        """
        if title_xpath:
            title_list = element.xpath(title_xpath)
            if title_list:
                return title_list[0]
            else:
                return ''
        return ''

    def extract_by_title(self, element: HtmlElement) -> str:
        """
        Extracts the title from the <title> tag in the HTML <head> section.

        If the title contains split characters (like "-", "|"), it tries to return the most relevant part.

        Args:
            element (HtmlElement): The HTML element.

        Returns:
            str: The cleaned-up <title> content, or an empty string.
        """
        
        title_list = element.xpath('//title/text()')
        if not title_list:
            return ''
        title = re.split(TITLE_SPLIT_CHAR_PATTERN, title_list[0])
        if title:
            if len(title[0]) >= 4:
                return title[0]
            return title_list[0]
        else:
            return ''

    def extract_by_htag(self, element: HtmlElement) -> str:
        """
        Extracts the title using H1~H5 tags.

        Args:
            element (HtmlElement): The HTML element.

        Returns:
            str: The first heading found, or an empty string.
        """
        
        title_list = element.xpath(TITLE_HTAG_XPATH)
        if not title_list:
            return ''
        return title_list[0]

    def extract_by_htag_and_title(self, element: HtmlElement) -> str:
        """
        Uses a combination of <title> tag and <h1>-<h5> headings to determine the most relevant title
        by computing the longest common substring.

        Args:
            element (HtmlElement): The HTML element.

        Returns:
            str: The best-matching title based on common substring, or an empty string.
        """
        h_tag_texts_list = element.xpath('(//h1//text() | //h2//text() | //h3//text() | //h4//text() | //h5//text())')
        title_text = ''.join(element.xpath('//title/text()'))
        news_title = ''
        for h_tag_text in h_tag_texts_list:
            lcs = get_longest_common_sub_string(title_text, h_tag_text)
            if len(lcs) > len(news_title):
                news_title = lcs
        return news_title if len(news_title) > 4 else ''

    def extract(self, element: HtmlElement, title_xpath: str = '') -> str:
        """
        General-purpose title extractor. Tries XPath first, then fallback strategies.

        Args:
            element (HtmlElement): The HTML element.
            title_xpath (str): Optional XPath to locate the title directly.

        Returns:
            str: The most likely title, stripped of whitespace.
        """
        title = (
            self.extract_by_xpath(element, title_xpath)
            or self.extract_by_htag_and_title(element)
            or self.extract_by_title(element)
            or self.extract_by_htag(element)
        )
        return title.strip()
    
class TimeExtractor:
    
    def __init__(self):
        self.time_pattern = DATETIME_PATTERN

    def extract(self, element: HtmlElement, publish_time_xpath: str = '') -> str:
        """
        Extracts the publication time using the best available strategy:
        1. User-defined XPath
        2. <meta> tags
        3. General text content

        Args:
            element (HtmlElement): Parsed HTML element.
            publish_time_xpath (str): Optional custom XPath to directly extract the time.

        Returns:
            str: The extracted publish time or an empty string if none found.
        """
        publish_time = (self.extract_from_user_xpath(publish_time_xpath, element)
                        or self.extract_from_meta(element)
                        or self.extract_from_text(element))
        
        return publish_time

    def extract_from_user_xpath(self, publish_time_xpath: str, element: HtmlElement) -> str:
        """
        Extracts publish time using a user-provided XPath.

        Args:
            publish_time_xpath (str): The XPath to evaluate.
            element (HtmlElement): The HTML element.

        Returns:
            str: Publish time string or empty string if not found.
        """
        if publish_time_xpath:
            publish_time = ''.join(element.xpath(publish_time_xpath))
            return publish_time
        return ''

    def extract_from_text(self, element: HtmlElement) -> str:
        """
        Scans all visible text nodes for patterns resembling datetime formats.

        Args:
            element (HtmlElement): The HTML element.

        Returns:
            str: A matched datetime string, or empty if no match is found.
        """
        text = ''.join(element.xpath('.//text()'))
        for dt in self.time_pattern:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return dt_obj.group(1)
        else:
            return ''

    def extract_from_meta(self, element: HtmlElement) -> str:
        """
        Extracts publish time from common <meta> tag patterns used in structured news sites.

        Args:
            element (HtmlElement): The HTML element.

        Returns:
            str: The publish time if found in meta tags, else empty string.
        """
        for xpath in PUBLISH_TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return ''.join(publish_time)
        return ''
    
class ContentExtractor:
    def __init__(self, content_tag: str = 'p'):
        """
        Initialize the content extractor.

        Args:
            content_tag (str): The HTML tag used to represent content blocks.
        """
        self.content_tag = content_tag
        self.node_info = {}
        self.high_weight_keyword_pattern = get_high_weight_keyword_pattern()
        self.punctuation = set('''！，。？、；：“”‘’《》%（）,.?:;'"!%()''')  
        self.element_text_cache = {}

    def extract(
        self,
        selector: HtmlElement,
        host: str = '',
        body_xpath: str = '',
        with_body_html: bool = False,
        use_visiable_info: bool = False
    ) -> List[Tuple[int, Dict[str, Any]]]:
        """
        Extracts the main content blocks from an HTML document.

        Args:
            selector (HtmlElement): The root HTML element.
            host (str): The host URL for resolving image paths.
            body_xpath (str): XPath to the body content.
            with_body_html (bool): Whether to include the full HTML of content blocks.
            use_visiable_info (bool): Whether to consider visibility and coordinate metadata.

        Returns:
            List[Tuple[int, Dict[str, Any]]]: Ranked content node info tuples.
        """
        
        if body_xpath:
            body = selector.xpath(body_xpath)[0]
        else:
            body = selector.xpath('//body')[0]
        for node in iter_node(body):
            if use_visiable_info:
                if not node.attrib.get('is_visiable', True):
                    continue
                coordinate_json = node.attrib.get('coordinate', '{}')
                coordinate = json.loads(coordinate_json)

                if coordinate.get('height', 0) < 150:
                    continue
            node_hash = hash(node)
            density_info = self.calc_text_density(node)
            text_density = density_info['density']
            ti_text = density_info['ti_text']
            text_tag_count = self.count_text_tag(node, tag='p')
            sbdi = self.calc_sbdi(ti_text, density_info['ti'], density_info['lti'])
            images_list = node.xpath('.//img/@src')
            if host:
                images_list = [pad_host_for_images(host, url) for url in images_list]
            node_info = {
                'ti': density_info['ti'],
                'lti': density_info['lti'],
                'tgi': density_info['tgi'],
                'ltgi': density_info['ltgi'],
                'node': node,
                'density': text_density,
                'text': ti_text,
                'images': images_list,
                'text_tag_count': text_tag_count,
                'sbdi': sbdi
            }
            if use_visiable_info:
                node_info['is_visiable'] = node.attrib['is_visiable']
                node_info['coordinate'] = node.attrib.get('coordinate', '')
            if with_body_html:
                body_source_code = unescape(etree.tostring(node, encoding='utf-8').decode())
                node_info['body_html'] = body_source_code
            self.node_info[node_hash] = node_info
        self.calc_new_score()
        result = sorted(self.node_info.items(), key=lambda x: x[1]['score'], reverse=True)
        return result

    def count_text_tag(self, element: HtmlElement, tag: str = 'p') -> int:
        """
        Count the number of given tags and direct text nodes under an element.

        Args:
            element (HtmlElement): The HTML element to inspect.
            tag (str): The tag to count (e.g., 'p').

        Returns:
            int: Number of text and tag nodes.
        """

        tag_num = len(element.xpath(f'.//{tag}'))
        direct_text = len(element.xpath('text()'))
        return tag_num + direct_text

    def get_all_text_of_element(self, element_list: Union[HtmlElement, List[HtmlElement]]) -> List[str]:
        """
        Extract and cache all cleaned text from an element or list of elements.

        Args:
            element_list (HtmlElement | List[HtmlElement]): Target elements.

        Returns:
            List[str]: Cleaned list of text nodes.
        """

        if not isinstance(element_list, list):
            element_list = [element_list]

        text_list = []
        for element in element_list:
            element_flag = element.getroottree().getpath(element)
            if element_flag in self.element_text_cache: # 直接读取缓存的数据，而不是再重复提取一次
                text_list.extend(self.element_text_cache[element_flag])
            else:
                element_text_list = []
                for text in element.xpath('.//text()'):
                    text = text.strip()
                    if not text:
                        continue
                    clear_text = re.sub(' +', ' ', text, flags=re.S)
                    element_text_list.append(clear_text.replace('\n', ''))
                self.element_text_cache[element_flag] = element_text_list
                text_list.extend(element_text_list)
        return text_list

    def need_skip_ltgi(self, ti: int, lti: int) -> bool:
        """
        Determine whether to ignore link text (LTGi) in density calc.

        Args:
            ti (int): Total text length.
            lti (int): Link text length.

        Returns:
            bool: Whether to skip LTGi consideration.
        """
        if lti == 0:
            return False

        return ti // lti > 10  # 正文的字符数量是链接字符数量的十倍以上


    def calc_text_density(self, element):
        """
        Calculate the text density of a given node.

        Returns:
            Dict[str, Any]: Density-related values.
        """
        ti_text = '\n'.join(self.get_all_text_of_element(element))
        ti = len(ti_text)
        ti = self.increase_tag_weight(ti, element)
        a_tag_list = element.xpath('.//a')

        lti = len(''.join(self.get_all_text_of_element(a_tag_list)))
        tgi = len(element.xpath('.//*'))
        ltgi = len(a_tag_list)
        if (tgi - ltgi) == 0:
            if not self.need_skip_ltgi(ti, lti):
                return {'density': 0, 'ti_text': ti_text, 'ti': ti, 'lti': lti, 'tgi': tgi, 'ltgi': ltgi}
            else:
                ltgi = 0
        density = (ti - lti) / (tgi - ltgi)
        return {'density': density, 'ti_text': ti_text, 'ti': ti, 'lti': lti, 'tgi': tgi, 'ltgi': ltgi}

    def increase_tag_weight(self, ti: int, element: HtmlElement) -> int:
        """
        Boost the text length score if the tag contains high-weight keywords.

        Args:
            ti (int): Original text length.
            element (HtmlElement): The HTML node.

        Returns:
            int: Adjusted score.
        """

        tag_class = element.get('class', '')
        if self.high_weight_keyword_pattern.search(tag_class):
            return 2 * ti
        return ti

    def calc_sbdi(self, text: str, ti: int, lti: int) -> float:
        """
        Compute the symbol-based density index (SbDi).

        Returns:
            float: SbDi value (always ≥ 1).
        """
        sbi = self.count_punctuation_num(text)
        sbdi = (ti - lti) / (sbi + 1)
        return sbdi or 1   # sbdi 不能为0，否则会导致求对数时报错。

    def count_punctuation_num(self, text: str) -> int:
        """
        Count the number of punctuation marks in the text.

        Args:
            text (str): The input text.

        Returns:
            int: Punctuation count.
        """
        count = 0
        for char in text:
            if char in self.punctuation:
                count += 1
        return count

    def calc_new_score(self) -> None:
        """
        Calculate final relevance score for each candidate content node.

        Score formula:
            score = density * log10(text_tag_count + 2) * log(sbdi)
        """
        for node_hash, node_info in self.node_info.items():
            score = node_info['density'] * np.log10(node_info['text_tag_count'] + 2) * np.log(
                node_info['sbdi'])
            self.node_info[node_hash]['score'] = score