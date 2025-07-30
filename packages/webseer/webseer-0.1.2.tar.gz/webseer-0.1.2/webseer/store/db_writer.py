'''
Description:  
Author: Huang J
Date: 2025-04-28 15:25:13
'''
import json
from typing import List

def insert_article(
    db, 
    cursor, 
    id: str, 
    title: str, 
    author: str, 
    date: str, 
    url: str, 
    text: str, 
    text_chunks: str, 
    links: List[str], 
    logger: 'Logger'
) -> None:
    """
    Inserts an article into the database.

    Args:
        db: The database connection object.
        cursor: The database cursor object used for executing queries.
        id (str): The unique identifier of the article.
        title (str): The title of the article.
        author (str): The author of the article.
        date (str): The publication date of the article.
        url (str): The URL of the article.
        text (str): The full text of the article.
        text_chunks (str): The article text chunks.
        links (List[str]): The associated links for the article.
        logger (logging.Logger): The logger instance for logging success or failure messages.

    Returns:
        None
    """

    insert_sql = """
        INSERT INTO articles (id, title, author, date, url, text, text_chunks, links)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        if isinstance(links,list):
            links = json.dumps(links,ensure_ascii=False)
        
        cursor.execute(insert_sql, (id, title, author, date, url, text, text_chunks,links))
        
        db.commit()
        logger.info(f"✅ Data added successfully; Article Title: {title}")
    except Exception as e:
        logger.error(f"❌ Data addition failed:{e}")
        db.rollback()    

def insert_chunk(
    db, 
    cursor, 
    id: str, 
    focus: str, 
    chunk: str, 
    article_id: str, 
    logger: 'Logger'
) -> None:
    """
    Inserts a chunk of text into the chunks table in the database.

    Args:
        db: The database connection object.
        cursor: The database cursor object used for executing queries.
        id (str): The unique identifier of the chunk.
        focus (str): The focus or topic of the chunk.
        chunk (str): The content of the chunk.
        article_id (str): The article ID this chunk belongs to.
        logger (logging.Logger): The logger instance for logging success or failure messages.

    Returns:
        None
    """

    insert_sql = """
    INSERT INTO chunks (id, focus, chunk, article_id)
    VALUES (%s, %s, %s, %s);
    """

    try:
        cursor.execute(insert_sql, (id, focus, chunk, article_id))
        db.commit()
        logger.info(f"✅ Data added successfully; Chunk ID: {id}; Chunk content: {chunk}")
    except Exception as e:
        logger.error(f"❌ Data addition failed:：{e}")
        db.rollback()
        
def check_article_exists(cursor, url: str) -> bool:
    """
    Checks if an article with the given URL already exists in the database.

    Args:
        cursor: The database cursor object used for executing queries.
        url (str): The URL of the article to check for existence.

    Returns:
        bool: True if the article exists, otherwise False.
    """
    
    sql = "SELECT COUNT(*) FROM articles WHERE url = %s"
    cursor.execute(sql, (url,))
    count = cursor.fetchone()[0]
    
    return count > 0
        
