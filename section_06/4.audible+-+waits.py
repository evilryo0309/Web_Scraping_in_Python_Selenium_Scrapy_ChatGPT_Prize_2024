from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=adc4b13b-d074-4e1c-ac46-9f54aa53072b&pf_rd_r=1F7DV0MPHV77Z61RX566"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

pagination = driver.find_element(
    By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

book_title = []
book_author = []
book_length = []
current_page = 1

while current_page <= last_page:
    # Implicit Wait
    # time.sleep(2)
    # Explicit Wait
    # container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
    container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    # products = container.find_elements_by_xpath('.//li[contains(@class, "productListItem")]')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located(
        (By.XPATH, './/li[contains(@class, "productListItem")]')))

    for product in products:
        book_title.append(product.find_element(
            By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(
            By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(
            By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page + 1
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
