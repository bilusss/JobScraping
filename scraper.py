import PracujPL
import NoFluffJobs
import JustJoinIT

from selenium import webdriver
from selenium.webdriver.safari.service import Service as SafariService
# from selenium.webdriver.chrome.service import Service as ChromeService
import time

# Safari setup (macOS) - Uncomment the following lines if you want to use Safari
service = SafariService()
driver = webdriver.Safari(service=service)
driver.maximize_window()

# Chrome setup (Windows) - Uncomment the following lines if you want to use Chrome
# chrome_service = ChromeService(executable_path="path/to/chromedriver.exe")
# driver = webdriver.Chrome(service=chrome_service)
# driver.maximize_window()

# PracujPL
PracujPL.scrape_job_listings(driver)


time.sleep(10)
# Zamknięcie przeglądarki
# driver.quit()
