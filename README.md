# Books to Scrape Showcase

## Overview

Welcome to the "Books to Scrape" showcase project! This repository is a demonstration of the Extract, Transform, Load (ETL) process using Python, Selenium, Pandas, and CSV.

## Project Description

- **Objective:** Showcase the ETL process through web scraping, emphasizing the use of Python and related libraries.
  
- **Technologies Used:**
  - Python
  - Selenium
  - Pandas
  - CSV
  - MySQL Connector Python

## Project Structure

- **Data Directory:** Explore the extracted book data in the `bookdata` directory:
  - Raw data located in the `books.csv` file.
  - Cleaned data located in the `books_cleaned.csv` file.
- **Python File (`scrape.py`):** Implements the core functionality:
  - Data web scraping function using Selenium to extract data.
  - Use of Pandas DataFrames to convert the data into a .csv.
  - Utilizes Pandas library to convert prices from Euros to USD and ratings/availability columns to number formats.
  - Removes duplicate rows from the dataset.
  - Stores the clean data in a MySQL localhost database named `bookstoscrape`.

## Key Features

- **Web Scraping:** Demonstrates the extraction of book data from a website.
- **Data Transformation:** Utilizes Python and Pandas for transforming raw data.
- **Data Storage:** The transformed data is stored in the `bookdata` directory as a CSV file.
- **Data Cleaning:** Converts data into a more usable format and stores it in `books_cleaned.csv`. Duplicates are removed during this process.

## Use Cases

This project is designed to:

- Showcase proficiency in web scraping and ETL processes.
- Highlight expertise in using Python, Selenium, Pandas, and CSV for data manipulation, data scraping, and data cleaning.
