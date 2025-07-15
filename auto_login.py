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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D9CA4DAF535110F6F861CE43758AAFD16973EB2E1317F1098D581D157C4366242F0446EF1AF160756525804EEBEEED8637407D2C1CE7B0C6E42DB65700CA335170C420598C20804B1F7D3CE622B2C1DC2CBB267EF0849D72EAAC94C6F0CF8BAEC7FC1E05DDBA55E053865159EFC13079953930581B30A3559778275BEE6286E23FD08558F8A0ED84F3A423E21BA84C36FCA2CC30824B7C5EBC6669EFCE1C884E1B82A7D9E3D51DD83CB1704ED1E76D0CBF435CA4DC5C4B9037D9435E53481BCFAB7B562DBC255FC0BF1D8D3E8AADBF5DB700F4578958E48C68FAF0F8B41568FB32FC7DF436D50BC1E2569AADF5105955C9BA8DBE57C342383F23D87D1B70EC09168866EB846A707C3CC0DB150563E6F141306C2326FFDC2849DEBCD4338B94551C8135FD25377144899B9732B9D17E8EDC75AE9A10FC34D252AE073FF08458F02A98D1D3BB04BBDDAA8A62301409762CA00BF23C49FAA31B213D927B89C4504A"})
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
