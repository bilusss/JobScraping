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
        driver.get("https://it.pracuj.pl/praca?et=17")

        # Wait for the page to load
        wait_for_page_load(driver)

        # Accepting cookies
        cookies_xpath = '//*[@id="__next"]/div[4]/div/div/div[3]/div/button[1]'
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
        span_path = '//*[@id="offers-list"]/div[4]/div[4]/div/div/div[1]/div[2]/div[1]/div/span[2]'
        i = 0
        flag = False
        while not flag:
            i += 1
            # Getting job listings
            job_listings = driver.find_elements(By.CSS_SELECTOR, "a.tiles_cnb3rfy.core_n194fgoq")
            print(f"{i} Found {len(job_listings)} job listings.")
            for job in job_listings:
                try:
                    title = job.get_attribute("title")
                    href = job.get_attribute("href")

                    try:
                        span = job.find_element(By.XPATH, span_path)
                        span_text = span.text
                    except Exception:
                        span_text = "Brak danych"
                    #TODO: Dodaj tryb zatudnienia(stacjonary, zdalne, hybrydowe), lokalizacje, firme

                    jobs.append([title[14:], span_text, href])
                except Exception as e:
                    print(f"Error extracting job details: {e}")

            # Click the "ok zamknij" button
            przycisk_xpath = '//*[@id="popupContainer"]/div/div/div/button'
            przyciski = driver.find_elements(By.XPATH, przycisk_xpath)
            if przyciski:
                przyciski[0].click()
                print("Przycisk kliknięty.")
            else:
                print("Przycisk nie znaleziony.")

            try:
                if i != 1:
                    next_button = driver.find_element(By.XPATH, '//*[@id="offers-list"]/div[5]/div/button[2]')
                else:
                    next_button = driver.find_element(By.XPATH, '//*[@id="offers-list"]/div[5]/div/button')
                next_button.click()
                wait_for_page_load(driver)
                time.sleep(5)
            except Exception as e:
                print(f"End of the page: {e}")
                flag = True
    finally:
        df = pd.DataFrame(jobs, columns=pd.Index(["Title", "Salary", "URL"]))
        df.to_csv("job_listings.csv", index=False)
        print("CSV file saved.")
        driver.quit()
        return df
