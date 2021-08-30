import time
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# client = MongoClient('127.0.0.1', 27017)
# db = client['gb_mail']
# collect_mail = db.mail

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://mail.ru")


login = driver.find_element_by_xpath('//input[@data-testid="login-input"]')
login.send_keys('kuzmenko.ilya84')
time.sleep(1)
button_password = driver.find_element_by_xpath('//button[@data-testid="enter-password"]')
button_password.click()
time.sleep(1)
password = driver.find_element_by_xpath('//input[@data-testid="password-input"]')
password.send_keys('kuzmenko010884')
password.send_keys(Keys.ENTER)

post = WebDriverWait(driver, 10)
post.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')))

links_to_mail = set()

while True:
    links_to_mail_len = len(links_to_mail)
    links = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')

    for link in links:
        links_to_mail.add(link.get_attribute('href'))

    actions = ActionChains(driver)
    actions.move_to_element(links[-1])
    actions.perform()

    if len(links_to_mail) == links_to_mail_len:
        break

for link in links_to_mail:
    driver.get(link)
    pass

pprint(links_to_mail)
