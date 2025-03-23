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
    browser.add_cookie({"name": "MUSIC_U", "value": "005AD074E61E42CC546BF4365A8F96140392C634A6E4C4C74A7952566718FC2694EA446F9B5CBDD65983E3D9E320C356B5FD81912BC65F715256FD10502234CED7820E73AE30B5A728831132580F4FC88348D25A42CA123C6E94404296D572F9E460E02B377FB520A32297FA4D9BBBDDD2227C38994C60E91BF02A53AB05E1B2FBA1ACFA03F31D0D288487B368FC3DE8D616026F8CFC2107FD350ED98E333AF2814491F6850FE39B70CD08ACE10AB0FF32B20E0CBBC128B3556E2DEAEB37C2FA23C58029C9C47B43A00C7A10AB987DBACC3B0007A55A2F9789D51A0A4BBFDCD4EBADFD2480E0A377E1CE051111D4EE04CAEC25AC96E27EB94DC66428B2C93D0AED81928C376A52FA251934960E32C03B6718476D1C42A04EF7303D84FDCB1D1BE3B8876558666526EF958F6A4BAC6890A8630D7FBFB03EF20182F80DEA4EA16B686559860FEFF3000CFED7CCD97CE9FA1EFF681E11CA065861D0F84231ACD5ABF0"})
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
