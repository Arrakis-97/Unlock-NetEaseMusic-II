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
    browser.add_cookie({"name": "MUSIC_U", "value": "0024CE800F8B505D3023D3182BA61AA86DF7CBFBDF3484A54BA6BAE11644649874C07D5802A1CCAF20710EA72BB95D3FEE98AF59190252F8E95F69EC467EC99F78124317C86C28FB66D1DABE7DEC84713E89BAF323B1EBA0C75F7757CC01D89E4AE1CFA388F20EB685C8776F3BC3F81ED9556A46EAEE4F1FF296A50598CAA82F9754F2D074F518FB5391C52621DD9DC685E3A5D69278E83972BCE115BE47CD3639AC6F9EB3C1EFD7674F425890A9A814F4F5396E2938E11BF188CA56BEB91357AD9341C1D6E3526FC6DA683AF3A658BDC84F3BAEE3AA88BFA2071A00EA2895BCDF1D7D40B8D8D1EC6CF17BEC9BD4A4E35DC35D72F7D1DD865AC7D7AFB2B3C3E71D555BEF871286AD9B7FC43BDB35B8CF0F63B91A5A955B691EE9F677499197B75ACF7DB9AB6A53022ED0DC5F14A6EE088C15E0A0B2F0DE46F669019777D71438648A55D3FB024E10CEE479C9E7870BD113"})
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
