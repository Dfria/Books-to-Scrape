from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import os

WAIT_TIME = 15
CHROMEDRIVER_PATH = r'E:\notarapidbot\Scrapper\chromedriver.exe'

service = Service(executable_path=CHROMEDRIVER_PATH)

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=chrome_options)

RAW_CSV_FILE = r'E:\bookscraper\bookdata\books.csv'

def get_book_data(driver, link):
    print(f"Navigating to: {link}")
    driver.get(link)

    genre = driver.find_element(By.XPATH, '//*[@id="default"]/div/div/div/div/div[1]').text

    time.sleep(1)

    books_on_page = driver.find_elements(By.XPATH, "//section/div[2]/ol/li/article/h3/a")
    links = [book.get_attribute('href') for book in books_on_page]

    data = []
    for row in links:
        driver.get(row)

        upc = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[1]/td").text
        title = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1").text
        price = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[3]/td").text
        price_with_tax = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[4]/td").text
        rating = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[3]").get_attribute("class")
        rating = rating.split(' ', 1)[1] if rating else ""
        availability = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[6]/td").text
        
        book_data = {
            'upc': upc,
            'title': title,
            'genre': genre,
            'price': price,
            'price-with-tax': price_with_tax,
            'rating': rating,
            'availability': availability
        }

        data.append(book_data)
    new_data = pd.DataFrame(data)
    new_data.to_csv(RAW_CSV_FILE, mode='a', header=False, index=False)

    driver.get(link)
    time.sleep(2)

    try:
        next_li_element = driver.find_element(By.XPATH, "//section/div[2]/div/ul/li[contains(@class, 'next')]")
    except:
        pass
    else:
        next_page_link = next_li_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(next_page_link)

        if next_page_link:
            get_book_data(driver, next_page_link)


def scrape_books(driver):
    if os.path.exists(RAW_CSV_FILE):
        print(f"The file '{RAW_CSV_FILE}' already exists.")
    else:
        driver.get("https://books.toscrape.com/catalogue/category/books_1/index.html")

        genre_index = driver.find_elements(By.XPATH, "/html/body/div/div/div/aside/div[2]/ul/li/ul/li/a")
        links = [genre.get_attribute('href') for genre in genre_index]

        for link in links:
            get_book_data(driver, link)
            print("Done scraping section.")

def clean_data():
    df = pd.read_csv(RAW_CSV_FILE)

    replace_rating = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

    # Replace values based on the mapping
    df['rating'] = df['rating'].replace(replace_rating)

    df['price'] = pd.to_numeric(df['price'].str.replace('£', ''), errors='coerce')
    df['price-with-tax'] = pd.to_numeric(df['price-with-tax'].str.replace('£', ''), errors='coerce')

    # Hypothetical exchange rate
    exchange_rate = 1.12  # 1 Euro = 1.12 US Dollars

    # Convert 'price' and 'price-with-tax' columns to US dollars and round to 2 decimal places
    df['price'] = (df['price'] * exchange_rate).round(2)
    df['price-with-tax'] = (df['price-with-tax'] * exchange_rate).round(2)

    df.rename(columns={'price_usd': 'price'}, inplace=True)
    df.rename(columns={'price-with-tax-usd': 'price-with-tax'}, inplace=True)

    df['availability'] = df['availability'].str.extract(r'\((\d+) available\)').astype(int)

    cleaned_csv_file = r'E:\bookscraper\bookdata\books_cleaned.csv'

    # Check if the file already exists
    if os.path.exists(cleaned_csv_file):
        print(f"The file '{cleaned_csv_file}' already exists.")
    else:
        # Export the DataFrame to a new CSV file
        df.to_csv(cleaned_csv_file, index=False)
        print(f"The DataFrame has been successfully exported to '{cleaned_csv_file}'.")

def main():
    scrape_books(driver)
    clean_data()

if __name__ == "__main__":
    main()