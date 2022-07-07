import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

FACEBOOK_EMAIL = os.environ.get("FACEBOOK_EMAIL")
FACEBOOK_PASSWORD = os.environ.get("FACEBOOK_PASSWORD")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
driver.get("https://tinder.com/")
driver.maximize_window()

time.sleep(3)

tinder_login_btn = driver.find_element("link text", "Log in")
tinder_login_btn.click()

time.sleep(3)
facebook_login_btn = driver.find_element("xpath", '//*[@id="q1569938320"]/div/div/div[1]'
                                                  '/div/div/div[3]/span/div[2]/button'
                                         )
facebook_login_btn.click()

base_window = driver.window_handles[0]
try:
    fb_login_window = driver.window_handles[1]
except IndexError:
    time.sleep(5)
    fb_login_window = driver.window_handles[1]

driver.switch_to.window(fb_login_window)

time.sleep(2)

email = driver.find_element("xpath", '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
email.send_keys(FACEBOOK_EMAIL)

password = driver.find_element("xpath", '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
password.send_keys(FACEBOOK_PASSWORD)
password.send_keys(Keys.ENTER)

time.sleep(10)

driver.switch_to.window(base_window)

time.sleep(2)
allow_location_btn = driver.find_element("xpath", '//*[@id="q1569938320"]/div/div/div/div/div[3]/button[1]')
allow_location_btn.click()

time.sleep(2)

dismiss_notification_btn = driver.find_element("xpath", '//*[@id="q1569938320"]/div/div/div/div/'
                                                        'div[3]/button[2]'
                                               )
dismiss_notification_btn.click()

time.sleep(2)

accept_cookies_btn = driver.find_element("xpath", '//*[@id="q-996647900"]/div/div[2]/div/div/div[1]/div[1]/button')
accept_cookies_btn.click()

time.sleep(10)

actions = ActionChains(driver)

for i in range(11):
    time.sleep(3)
    try:
        actions.send_keys(Keys.ARROW_RIGHT)
        actions.perform()
        try:
            driver.find_element("xpath", '//*[@id="q-996647900"]/div/div[1]/div/'
                                         'main/div[1]/div/div/div[1]/div[1]/div/div[5]/div/div[4]'
                                ).click()
        except NoSuchElementException:
            print("no such element")
            time.sleep(2)
            continue
    except ElementClickInterceptedException:
        try:
            match_btn = driver.find_element("css selector", ".itsAMatch a")
            match_btn.click()
        except NoSuchElementException:
            add_home_screen_btn = driver.find_element("xpath", '//*[@id="q1569938320"]/div/div/div[2]/button[2]')
            add_home_screen_btn.click()
            time.sleep(2)

time.sleep(3)
driver.quit()
