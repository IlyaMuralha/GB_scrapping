import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
# chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://lenta.com/catalog/myaso-ptica-kolbasa/")

time.sleep(3)
button_delivery = driver.find_element_by_class_name('close-control__icon')
# button_delivery = driver.find_element_by_xpath(
#     '//button[@class="button button--primary button--small buttons-control__button delivery-flow__submit"]')
button_delivery.click()

# # time.sleep(2)
# cookie_button = driver.find_element_by_class_name('cookie-usage-notice__button-inner--desktop')
# # cookie_button = driver.find_element_by_class_name('cookie-usage-notice__button-inner--mobile')
# cookie_button.click()

# button_cookie = driver.find_element_by_xpath(
#     '//button[@class="cookie-usage-notice__button button button--primary button--small"]')

i = 0
while i < 5:
    i += 1
    try:
        button_wait = WebDriverWait(driver, 10)
        button_click = button_wait.until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                     'catalog-grid-container__pagination-button')))

        # button = driver.find_element_by_class_name('catalog-grid-container__pagination-button')
        button_click.click()
    except Exception as e:
        print(e)
        break

products = driver.find_elements_by_class_name('sku-card-small-container')

for prod in products:
    print(prod.find_element_by_class_name('sku-card-small__title').text)
