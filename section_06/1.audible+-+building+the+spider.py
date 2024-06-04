from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

web = "https://www.audible.com/search"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

# Locating the box that contains all the audiobooks listed in the page
container = driver.find_element(
    by=By.CLASS_NAME, value='adbl-impression-container')

# Getting all the audiobooks listed (the "/" gives immediate child nodes)
products = container.find_elements(
    By.XPATH, './/li[contains(@class, "productListItem")]')

# Initializing storage
book_title = []
book_author = []
book_length = []
# Looping through the products list (each "product" is an audiobook)
for product in products:
    # We use "contains" to search for web elements that contain a particular text, so we avoid building long XPATH
    book_title.append(product.find_element(
        By.XPATH, './/h3[contains(@class, "bc-heading")]').text)  # Storing data in list
    book_author.append(product.find_element(
        By.XPATH, './/li[contains(@class, "authorLabel")]').text)
    book_length.append(product.find_element(
        By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

driver.quit()
# Storing the data into a DataFrame and exporting to a csv file
df_books = pd.DataFrame(
    {'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)
