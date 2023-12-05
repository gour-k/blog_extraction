from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import psycopg2
from datetime import datetime
from threading import Thread
from psycopg2 import sql
from concurrent.futures import Future
import re
import json
import validators
from random import randint

def extract_blog_text(url):
    print("Webpage is opening in selenium")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(randint(1,5))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        text_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\u0080-\uFFFF]')
        text = text_pattern.sub('', text)
        print("text extracted")
        return text.lower()
    except Exception as e:
        return {"sucess": False, "text":e}
    finally:
        driver.quit()

def store_in_database(url, content):
    print("Storing in database")
    conn_params = {
        "dbname": "sample",
        "user": "", #to be updated
        "host": "localhost",
        "password": "" #to be updated
    }

    create_table_query = """
    CREATE TABLE IF NOT EXISTS blog_texts (
        id SERIAL PRIMARY KEY,
        url VARCHAR(255) NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)

                # Check if URL already exists
                cur.execute("SELECT content FROM blog_texts WHERE url = %s", (url,))
                result = cur.fetchone()

                if result:
                    # Update content if it's different
                    if result[0] != content:
                        update_query = sql.SQL("UPDATE blog_texts SET content = %s, modified_at = %s WHERE url = %s")
                        cur.execute(update_query, (content, datetime.now(), url))
                        conn.commit()
                        return {"sucess": True, "text":"New content is updated for the URL"}
                    else:
                        conn.commit()
                        return {"sucess": True, "text":"URL is already added with latest content"}
                else:
                    # Insert new record if URL does not exist
                    insert_query = sql.SQL("INSERT INTO blog_texts (url, content, created_at, modified_at) VALUES (%s, %s, %s, %s)")
                    cur.execute(insert_query, (url, content, datetime.now(), datetime.now()))
                    conn.commit()
                    return {"sucess": True, "text":"New content is added for the URL"}
    except (Exception, psycopg2.DatabaseError) as error:
        return {"sucess": False, "text":error}


def main(url):
    if not url:
        return json.dumps({"sucess": False, "text":"URL can't be empty"})
    if not isinstance(url, str):
        return json.dumps({"sucess": False, "text":"Only String is allowed in main function"})
    if not validators.url(url):
        return json.dumps({"sucess": False, "text":"Only URL is allowed in main function"})
    try:
        future = Future()
        thread = Thread(target=_main, args=(url, future))
        thread.start()
        audio_result = future.result()
        return audio_result
    except Exception as e:
        return json.dumps({"sucess": False, "text":e})

def _main(url, future):
    try:
        url = url.lower()
        output = extract_blog_text(url)
        if isinstance(output, dict):
            future.set_result(output)
            return
        result = store_in_database(url, output)
        future.set_result(result)
    except Exception as e:
        future.set_exception(e)