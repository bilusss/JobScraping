from selenium import webdriver
from selenium.webdriver.safari.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

now = datetime.now()
currentDate = now.strftime("%d/%m/%Y")

# Proszę zmodyfikować te zmienne
searchKeyword = "?"
searchLocation = "?"
senderAddress = "?"
senderKey = "?"
receiverAddress = "?"

# Uruchomienie przeglądarki Safari
service = Service()
driver = webdriver.Safari(service=service)
driver.maximize_window()

# Przejście na stronę
driver.get("https://pracuj.pl")
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Akceptuj wszystkie')]"))).click()
advancedSearch = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div/div[3]/form/div[2]/button')

try:
    advancedSearch.click()
except Exception:
    advancedSearch = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div/div[3]/form/div[2]/button')
    advancedSearch.click()

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Rozumiem')]"))).click()
except Exception:
    print("Nie znaleziono przycisku 'Rozumiem'.")

# Wprowadzanie danych
jobSearchKeyword = driver.find_element(By.XPATH,
                                       '/html/body/div[1]/div[2]/div[4]/form/div[1]/div/div[1]/div[1]/div/input[1]')
jobSearchKeyword.send_keys(searchKeyword)
jobSearchPreferredLocation = driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div[2]/div[4]/form/div[1]/div/div[2]/div[1]/div/input[1]')
jobSearchPreferredLocation.send_keys(searchLocation)
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[4]/form/div[1]/div/div[4]/div/button'))).click()

jobOffersList = []

# Pobieranie ofert pracy
while True:
    jobOffers = driver.find_elements(By.CLASS_NAME, "offer__info")

    for offer in jobOffers:
        jobLink = offer.find_element(By.CLASS_NAME, "offer-details__title-link")
        jobTitle = jobLink.text
        jobCompanyName = offer.find_element(By.CLASS_NAME, "offer-company__name").text
        jobOffersList.append({
            'link': jobLink.get_attribute("href"),
            'job title': jobTitle,
            'company name': jobCompanyName
        })

    # Sprawdzenie, czy jest kolejna strona
    try:
        nextPageButton = driver.find_element(By.CSS_SELECTOR, "li[class='pagination_element pagination_element--next']")
        nextPageButton.click()
    except Exception:
        print("Ostatnia strona wyników.")
        break

# Eksport do pliku Excel
df = pd.DataFrame(jobOffersList)
df.to_excel('jobOffers.xlsx', index=False)

# Tworzenie i wysyłanie e-maila
message = MIMEMultipart()
message['From'] = senderAddress
message['To'] = receiverAddress
message['Subject'] = f"{searchKeyword} pracuj.pl - {searchLocation} - najnowsze oferty pracy! {currentDate}"

# Załącznik
jobOffersExcelFile = MIMEBase('application', "octet-stream")
jobOffersExcelFile.set_payload(open("jobOffers.xlsx", "rb").read())
encoders.encode_base64(jobOffersExcelFile)
jobOffersExcelFile.add_header('Content-Disposition', 'attachment; filename="jobOffers.xlsx"')
message.attach(jobOffersExcelFile)

# Wysyłanie e-maila przez SMTP
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(senderAddress, senderKey)
session.sendmail(senderAddress, receiverAddress, message.as_string())
session.quit()
print('Mail wysłany do ' + receiverAddress)

# Zamknięcie przeglądarki
driver.quit()
