from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def scrape_job_listings(driver):
    # Loading the page
    driver.get("https://pracuj.pl")

    # Wait for the page to load
    try:
        #TODO it doesnt catch the exception when the page is not loaded (no internet connection)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Page loaded successfully.")
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()

    cookies_xpath = '//*[@id="__next"]/div[12]/div/div/div[3]/div/button[1]'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,cookies_xpath))).click()

    job_listings = driver.find_elements(By.CLASS_NAME, "job_listing_class_name")
    jobs = []

    # for job in job_listings:
    #     title = job.find_element(By.CLASS_NAME, "job_title_class_name").text
    #     company = job.find_element(By.CLASS_NAME, "company_name_class_name").text
    #     location = job.find_element(By.CLASS_NAME, "location_class_name").text
    #     date_posted = job.find_element(By.CLASS_NAME, "date_posted_class_name").text
    #     jobs.append([title, company, location, date_posted])

    df = pd.DataFrame(jobs, columns=pd.Index(["Title", "Company", "Location", "Date Posted"]))
    df.to_csv("job_listings.csv", index=False)
