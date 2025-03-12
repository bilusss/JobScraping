import PracujPL
import JustJoinIT
from selenium import webdriver
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.safari.options import Options
from multiprocessing import Process, Queue
import time

def scrape_pracujpl(queue):
    options = Options()
    service = SafariService()
    driver = webdriver.Safari(service=service, options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 600)
    result = PracujPL.scrape_job_listings(driver)
    queue.put(result)
    driver.quit()

def scrape_justjoinit(queue):
    options = Options()
    service = SafariService()
    driver = webdriver.Safari(service=service, options=options)
    driver.set_window_position(800, 0)
    driver.set_window_size(800, 600)
    result = JustJoinIT.scrape_job_listings(driver)
    queue.put(result)
    driver.quit()

if __name__ == '__main__':
    queue = Queue()
    # p1 = Process(target=scrape_pracujpl, args=(queue,))
    p2 = Process(target=scrape_justjoinit, args=(queue,))

    # p1.start()
    p2.start()

    # p1.join()
    # p2.join()

    # results = [queue.get() for _ in range(2)]
    results = [queue.get() for _ in range(1)]
    for res in results:
        print(res)

    print("All processes completed.")
