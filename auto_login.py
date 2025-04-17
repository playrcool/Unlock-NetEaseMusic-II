# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005815B962B718D0D2B47B40E770AF6C4295B42921FD8D5C555071DFD7E38E5AAF007BB20A2BE582D6C60223CD6D48AD72C7AC7F9518BB9C3688D7A88811DA95788092C5B5CFD21217D4BBF6AED346CBC8FFC620FB204E65FED9947CB570A6FD84932D517436BE5BE6174B9A6C6440E99D36096A0AD21397043D97257F9280374589D57533351D1A2984043E72F2AEF2C1D7DAA9C5215231EFD3C803AE4165182B3B10305432441F729E3F59FD3221BAFED5E177AA93CD1F63376F5B3A7B72E323638381742FAA1830E64377C7AD50B833DAEE51E0EF6BEED68862344CA82A8F100A72C29E5DEF2916C87ACB725246BCE78A2DE5767BA9DF1ACDF94F8681D1C7969686B71EAD080F2A1102AF30BC486A904CA338F28101E13BE6BBDA2194E78438A7693B4073DE40E6C8CC2754307C01E911375AE0500509B29C1E2D20126A99A70CDA74E6BB4A559915F9196654171ABC1D1F0D30E27E08D7CF73B084553A1355"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
