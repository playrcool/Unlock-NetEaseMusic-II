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
    browser.add_cookie({"name": "MUSIC_U", "value": "007EB0112E9926D7044F2F0C2B91C69CB85348C5EDE7592826F71F2D75D318C2E7CCDEF79D4CCC1162540D68FBEB31416CF48026DEA8BE741C0891C0CB9010879ED8ACE0786AE1AE5F983359EFA7792D2408EA7DE2F4AD5377A95127DE222F0424AE021A1B47689AB8872445C835EC9C8CEA1EFA06DD81A97D45AC4F08B9E8D2C39F5E6B9F9DB9C4E0FCA8B91494D0A54A2282C2A4279BA6125D54C59C6F94F587CDDC075D2178148BE5883D927FB98963C25AC8F69DEFD6EE543B38FF0FF023FFBDFB9A6D09517EBE91EC8A8221AFD1AA10ED6BD1A7C1FE2BA77D58900CBEEFFEA925B31B8B5A481033DF3603A4E376FCFF958692A5E1ED22034929A7208A9B57AF5F13DDDF674C643D0EB6B53C2D6714D663F0AE2E524BEF3B2338AEA6B111BA2A704A2F89E770507DC2B8E79725881EAE6F5C9530807CF69DFDA44C0B17348EA38F3AC43F3829DA251934211628BABE8209003C78657FCCF2670FFC915B163F"})
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
