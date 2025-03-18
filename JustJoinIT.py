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
        collected_data = set()
        while i < 10 and not flag:
            elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'data-index')]")
            print(elements)
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollBy(0, 50);")
            for el in elements:
                data = el.text
                index = el.get_attribute("display_item_index")
                if data not in collected_data:
                    collected_data.add(data)
                    print(f"Data: {data}, Index: {index}")
            print(collected_data)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(20)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                flag = True
            last_height = new_height
            i += 1

    finally:
        print()
        df = pd.DataFrame(jobs, columns=pd.Index(["Title", "URL"]))
        df.to_csv("job_listings.csv", index=False)
        print("CSV file saved.")
        driver.quit()
        return df
