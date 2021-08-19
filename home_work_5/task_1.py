from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
collect_new_products = db.new_products

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://www.mvideo.ru/?cityId=CityCZ_1024")

button_wait = WebDriverWait(driver, 10)
try:
    button_click = button_wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-init="sticky"]')))
except Exception as err:
    print(f'{type(err)}:\n{err}')
    pass
else:
    button_click.click()

# try:
#     button_cl = button_wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="close"]')))
#     button_cl.click()
# except Exception as err:
#     print(f'{type(err)}:\n{err}')
#     pass

actions = ActionChains(driver)
move_to_mew_prod = driver.find_element_by_xpath('//div[contains(h2, "Новинки")]')
actions.move_to_element(move_to_mew_prod)
actions.perform()

while True:
    try:
        button_next = button_wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(h2, "Новинки")]/../..//a[contains(@class, "next-btn")]')))
        button_next.click()
    except Exception as err:
        print(f'{type(err)}:\n{err}')
        break

new_products = driver.find_elements_by_xpath(
    '//div[contains(h2, "Новинки")]/../..//a[contains(@class, "fl-product-tile-picture__link")]')

products = []
for item in new_products:
    product = {}
    info = item.get_attribute('data-product-info')
    link = item.get_attribute('href')

    product['info'] = info
    product['link'] = link

    products.append(product)

for prod in products:
    collect_new_products.update_one(
        {'link': prod['link']},
        {'$set': prod},
        upsert=True
    )

for doc in collect_new_products.find({}):
    pprint(doc)
