'''
Description:  
Author: Huang J
Date: 2025-04-28 15:25:00
'''
# pip install cryptography  这个库必须安装
from typing import List, Tuple
import pymysql

def check_database_and_tables(
    host: str,
    port: int,
    user: str,
    password: str,
    logger: 'Logger',
    database: str = 'webseer',
    tables_to_check: List[str] = ['articles', 'chunks'],
    charset: str = 'utf8mb4'
) -> Tuple[pymysql.connections.Connection, pymysql.cursors.Cursor]:
    """
    Check if the database and required tables exist. Create them if they don't.

    Args:
        host (str): Database host address.
        port (int): Database port.
        user (str): Database username.
        password (str): Database password.
        logger (Logger): Logger instance for logging info and errors.
        database (str): Target database name.
        tables_to_check (List[str]): List of required tables to check/create.
        charset (str): Character set for the database.

    Returns:
        Tuple[Connection, Cursor]: A tuple containing the database connection and cursor.
    """
    try:
        try:
            db = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                charset=charset
            )
            cursor = db.cursor()

            cursor.execute("SHOW DATABASES;")
            databases = [row[0] for row in cursor.fetchall()]
            logger.info(f'Existing databases: {databases}')
        except Exception as e:
            logger.error('❌ Failed to connect to the database!')
            raise ValueError(e)
        
        if database not in databases:
            logger.warning(f"❌ Database '{database}' does not exist. It will be created below!")
            try:
                create_database_sql = f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET {charset};"
                cursor.execute(create_database_sql)
                logger.info(f"✅ Database  '{database}' created successfully!")
            except Exception as e:
                logger.error(f"❌ Failed to create database'{database}'")
                raise ValueError(e)

        cursor.execute(f"USE {database};")
        cursor.execute("SHOW TABLES;")
        existing_tables = [row[0] for row in cursor.fetchall()]
        logger.info(f'Existing databases: {existing_tables}')

        for table in tables_to_check:
            if table in existing_tables:
                logger.info(f"✅ Table '{table}' exists.")
            else:
                logger.warning(f"❌ Table '{table}' does not exist. It will be created below!")
                if table=='articles':
                    try:
                        create_article_table_sql = """
                            CREATE TABLE IF NOT EXISTS articles (
                                id VARCHAR(100) PRIMARY KEY,
                                title VARCHAR(255),
                                author VARCHAR(100),
                                date TEXT,
                                url TEXT,
                                text LONGTEXT,
                                text_chunks LONGTEXT,
                                links LONGTEXT
                            );
                        """
                        cursor.execute(create_article_table_sql)
                        logger.info(f"✅ Table '{table}' created successfully!")
                    except Exception as e:
                        logger.error(f"❌ Failed to create table '{table}'!")
                        raise ValueError(e)
                    
                elif table=='chunks':
                    try:
                        create_chunk_table_sql = """
                            CREATE TABLE IF NOT EXISTS chunks (
                                id VARCHAR(60) PRIMARY KEY,
                                focus TEXT,
                                chunk LONGTEXT,
                                article_id VARCHAR(60),
                                FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
                            );
                        """
                        cursor.execute(create_chunk_table_sql)
                        logger.info(f"✅ Table '{table}' created successfully!")
                    except Exception as e:
                        logger.error(f"❌ Failed to create table '{table}'!")
                        raise ValueError(e)
                    
    except Exception as e:
        logger.error("❌ An unexpected error occurred!")
        raise ValueError(e)
    
    return db,cursor

def close_db(db: pymysql.connections.Connection, cursor: pymysql.cursors.Cursor) -> None:
    """
    Close the database connection and cursor.

    Args:
        db (Connection): The database connection.
        cursor (Cursor): The database cursor.

    Returns:
        None
    """
    cursor.close()
    db.close()