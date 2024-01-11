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

WAIT_TIME = 15
CHROMEDRIVER_PATH = r'E:\notarapidbot\Scrapper\chromedriver.exe'

service = Service(executable_path=CHROMEDRIVER_PATH)

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_book_data(driver, link):
    # Navigate to list of books for certain genre, shown on the left index of toscrape page
    csv_file = r'E:\bookscraper\bookdata\books.csv'

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
    new_data.to_csv(csv_file, mode='a', header=False, index=False)

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
    return genre

def scrape_books(driver):
    driver.get("https://books.toscrape.com/catalogue/category/books_1/index.html")

    genre_index = driver.find_elements(By.XPATH, "/html/body/div/div/div/aside/div[2]/ul/li/ul/li/a")
    links = [genre.get_attribute('href') for genre in genre_index]

    for link in links:
        genre = get_book_data(driver, link)
        print("Done scraping " + genre + " books.")

scrape_books(driver)
