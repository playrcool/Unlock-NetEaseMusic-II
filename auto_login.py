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
    browser.add_cookie({"name": "MUSIC_U", "value": "0059E4F316A1E5291900E43C95684B72A81F39411D1302CB1837EB5120C085AA971666841AA7C45E8282338049DD6D15A3CF003C7771A4146ED4BAF9A98F149F1A1A6682B9A045359564F2AF7E9C5CBBBA082B9FB0B699C04D33533E9142729F551AAF4BF9A39CC13CDD24719CF26D7BDBAD12DEAECFEE18BD20C67319E4C969C8B5C818858232E31113DB08A90E1704D0C967202F407E32BEB0D3580F9764695C92B6053044C62D41785FC337B7DC142931F46B76F6CE5E61182871DF4B3BA29F6D92AEFEF5CA2227348554DA6D4B5BE9241730D1933311D7523FA613878D41AC5A3F9678A738A0ADB154ADAC820635F0701436937B9947C19CCE424F8D06BDB02E0103B48AFCF14049CE20C821EC913CD4565A57CBA35479BA35838EACA1BCFEFB2B8CD3F13BB9AADB3B423C3A6869EBFEAD0A7372E77EE88EEF158C19075591A54A6823B411E119B931E7F6CB16DB62142C3ADA4BB3499FB9BC891EA5023AB6"})
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
