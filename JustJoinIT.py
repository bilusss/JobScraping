from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def wait_for_page_load(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        print("Page loaded successfully.")
    except Exception as e:
        print(f"Error: {e}")

def scrape_job_listings(driver):
    jobs = []
    try:
        # Loading the page
        driver.get("https://justjoin.it/job-offers/all-locations?employment-type=internship&orderBy=DESC&sortBy=published")

        # Wait for the page to load
        wait_for_page_load(driver)

        # Accepting cookies
        cookies_xpath = '//*[@id="cookiescript_accept"]'
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cookies_xpath))).click()
            print("Cookies accepted.")
        except Exception as e:
            print(f"Error clicking cookies button: {e}")
            driver.quit()
            return

        # Wait for the page to load
        wait_for_page_load(driver)
        time.sleep(5)

        i = 0
        flag = False
        # while not flag:
        #     i += 1
        #     # Getting job listings
        #     job_listings = driver.find_elements(By.CSS_SELECTOR, "div.MuiBox-root.css-2kppws")
        #     print(f"{i} Found {len(job_listings)} job listings.")
        #     for job in job_listings:
        #         try:
        #             title = job.get_attribute("title")
        #             href = job.get_attribute("href")
        #             jobs.append([title, href])
        #         except Exception as e:
        #             print(f"Error extracting job details: {e}")

        #     # Click the "Next" button
        #     try:
        #         if i != 1:
        #             next_button = driver.find_element(By.XPATH, '//*[@id="offers-list"]/div[5]/div/button[2]')
        #         else:
        #             next_button = driver.find_element(By.XPATH, '//*[@id="offers-list"]/div[5]/div/button')
        #         next_button.click()
        #         wait_for_page_load(driver)
        #         time.sleep(5)
        #     except Exception as e:
        #         print(f"End of the page: {e}")
        #         flag = True
    finally:
        df = pd.DataFrame(jobs, columns=pd.Index(["Title", "URL"]))
        df.to_csv("job_listings.csv", index=False)
        print("CSV file saved.")
        driver.quit()
        return df
