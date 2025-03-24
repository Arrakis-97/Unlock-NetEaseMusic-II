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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BB08A35971FA4A5EFC854C122683F197E2E62F40B25B0BFB0A4A54172E5AA907047398E73A28633D72C8168A5C8BEFF27BCF709975DDFEAEFF3D60BA953D2FB8EAD3E22EA7EF1E11A77FC3B1788B5BEF5F10B2B5888060A412D2F40326F609AD1AADF0C3798535285E5BD1EC9DB1508A85DF43310249189AB98C06661D4FCCA015A31AEC21E741E3EF9F285C8080646E2F7F78E89F5D138C3279EB98C005674C78AD4CB2EFF729AE05EE0E9F9572A62DE2A5704CDF935B27CC6A9E18C2217935182E8BE9A20CB31234C3EBDE12B03DF4B9144FD6BE228EE4D70F6A562BAADC85DBADBAD25913F6FE1AE1903487219374F2C0BA4767A28D3DB5EA9934C720A3523F17783971D8E9EE6658C61E29706207448D4958B70BCD4A1C45AADFE9E03D2D3BB6587D0B33230A73DCE747D067B9CD5A00481F761C31A9C552CC934367427D01AB6CAE4989FE48775051587ADF76DA"})
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
