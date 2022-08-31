import pandas as pd
import numpy

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os
load_dotenv()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(
    os.environ["chrome_webdriver_path"], chrome_options=options)
params = {
    "latitude": 51.507351,
    "longitude": -0.127758,
    "accuracy": 100
}
contact_number = os.environ["contact_number"]

driver.execute_cdp_cmd("Emulation.clearGeolocationOverride", params)

driver.get(
    'https://web.telegram.org/k')

time.sleep(5)  # change time if telegram is unblocked in your region
login_button = driver.find_element_by_css_selector('button')
login_button.click()
time.sleep(5)

div = driver.find_elements_by_css_selector('div[contenteditable="true"]')
# Enter your phone number to continue
div[1].send_keys(Keys.BACK_SPACE, contact_number)
time.sleep(2)

driver.find_element_by_css_selector('button').click()
input('OTP entered?')

# group link where you would like to scrap data
driver.get(f'https://web.telegram.org/k/#@{os.environ["group_name"]}')
time.sleep(5)

content_div = driver.find_element_by_class_name('content')
content_div.click()
time.sleep(3)

is_channel = driver.find_element_by_css_selector('.info>span')
is_channel = "subscribers" in is_channel.text

last_count = 0
while True and is_channel == False:
    current = driver.find_element_by_css_selector(
        '.search-super-content-members>.chatlist>a:nth-last-child(1)')
    scroll = 'document.querySelector(".search-super-content-members>.chatlist>a:nth-last-child(1)").scrollIntoView()'
    driver.execute_script(scroll)  # execute the js scroll
    anchor_count = len(driver.find_elements_by_css_selector(
        '.search-super-content-members > .chatlist > a'))
    print(anchor_count)
    time.sleep(4)  # wait for page to load new content
    if (last_count == anchor_count):
        break
    else:
        last_count = anchor_count

user_name = list()
a_list = driver.find_elements_by_css_selector(
    '.search-super-content-members > .chatlist > a')
id_list = list()
for i in range(0, last_count):
    id_list.append(a_list[i].get_attribute('data-peer-id'))

for i in range(0, last_count):
    id = id_list[i]
    driver.get(f'https://web.telegram.org/k/#{id}')
    time.sleep(1)
    if '@' in driver.current_url:
        user = driver.current_url.split('@')
        user_name.append(f'@{user[1]}')
    else:
        user_name.append(f'@{id}')

df = pd.DataFrame(user_name, columns=['Users'])
df.to_csv('tgUsers.csv')
input("Press any key to exit...")
