# README.md for Web Scraping and Database Storing Script

## Overview

This Python script is designed to extract text content from a given blog URL using Selenium and BeautifulSoup, and then store or update this content in a PostgreSQL database. It's a multi-threaded application that ensures efficient handling of web scraping and database operations.

## Features

- **Web Scraping**: Extracts text from a blog page using Selenium and BeautifulSoup.
- **Database Interaction**: Stores the extracted text in a PostgreSQL database.
- **Multithreading**: Uses a separate thread for the main operation to enhance performance.
- **Error Handling**: Includes robust error handling mechanisms.

## Requirements

- Python 3.x
- PostgreSQL
- Selenium
- BeautifulSoup
- psycopg2
- Chrome WebDriver
- validators

## Installation

1. **Install Python Packages**:
   ```bash
   pip3 install selenium beautifulsoup4 psycopg2-binary validators
   ```
2. **Chrome WebDriver**: Ensure Chrome WebDriver is installed and its path is correctly set in your system.
3. **stgreSQL Database Setup**: Set up a PostgreSQL database and update the connection parameters in the script.

## Usage

1. **Script Execution**: Execute the script by running `python3 main.py`.
2. **Function Call**: Call the `main(url)` function with the desired blog URL as its argument.

## Functions Description

- `extract_blog_text(url)`: Takes a URL, scrapes its content, and returns the cleaned text.
- `store_in_database(url, content)`: Takes a URL and its content, then stores or updates this content in the database.
- `main(url)`: The main function that orchestrates the process. It validates the URL and uses multithreading for scraping and storing data.
- `_main(url, future)`: A helper function for main, used for threading.

## Database Schema

The script uses a PostgreSQL table with the following schema:

```sql
CREATE TABLE IF NOT EXISTS blog_texts (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Notes

- Ensure that the database credentials are correctly set in the script.
- The script uses headless Chrome, which might need proper configuration depending on your system.
- The script includes a random delay between 1 to 5 seconds during web scraping to mimic human interaction and avoid being blocked by the website.

## Troubleshooting

- **WebDriver Issues**: Make sure Chrome WebDriver is installed and its path is correctly set.
- **Database Connection Issues**: Verify the database connection parameters.
- **Python Dependency Issues**: Ensure all required Python packages are installed.