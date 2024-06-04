from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# The first website has 5 pages while the second has 60. Test the code with any of them
web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=adc4b13b-d074-4e1c-ac46-9f54aa53072b&pf_rd_r=1F7DV0MPHV77Z61RX566"
# web = "https://www.audible.com/search"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

# Pagination 1
pagination = driver.find_element(
    By.XPATH, '//ul[contains(@class, "pagingElements")]')  # locating pagination bar
# locating each page displayed in the pagination bar
pages = pagination.find_elements(By.TAG_NAME, 'li')
# getting the last page with negative indexing (starts from where the array ends)
last_page = int(pages[-2].text)

book_title = []
book_author = []
book_length = []

# Pagination 2
current_page = 1   # this is the page the bot starts scraping

# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    time.sleep(2)  # let the page render correctly
    container = driver.find_element(
        By.CLASS_NAME, 'adbl-impression-container ')
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
    # products = container.find_elements(By.XPATH'./li')

    for product in products:
        book_title.append(product.find_element(
            By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(
            By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(
            By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    # increment the current_page by 1 after the data is extracted
    current_page = current_page + 1
    # Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
    try:
        next_page = driver.find_element(
            By.XPATH, './/span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame(
    {'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_pagination.csv', index=False)
