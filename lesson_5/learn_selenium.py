import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

chrome_options = Options()
chrome_options.add_argument('--window-size=760,1080')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://gb.ru/login")

login = driver.find_element_by_id('user_email')
login.send_keys('login')

password = driver.find_element_by_id('user_password')
password.send_keys('password')
password.send_keys(Keys.ENTER)

menu = driver.find_element_by_xpath('//span[contains(text(), "меню")]')
menu.click()

dropdown = driver.find_element_by_xpath('//button[@data-test-id="user_dropdown_menu"]')
dropdown.click()

# profile = driver.find_element_by_xpath('//span[contains(text(), "Профиль")]')
# profile.click()
link_profile = driver.find_element_by_xpath('//span[contains(text(), "Профиль")]/..')
url = link_profile.get_attribute('href')

driver.get(url)

# close_widget = driver.find_element_by_xpath('button[@data-fl-track="close"]')
# close_widget.click()

edit_profile = driver.find_element_by_class_name('text-sm')
driver.get(edit_profile.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
select = Select(gender)
select.select_by_value('unknown')
time.sleep(3)
select.select_by_visible_text('Мужской')

gender.submit()

driver.back()
driver.forward()
driver.refresh()

print()
