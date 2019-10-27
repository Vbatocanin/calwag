from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json


def autocred():
    google_username = input("Enter Google account username: ")  # raw_input() for python 2, use input() for python 3
    google_password = input("Enter Google account password: ")

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
    #driver = webdriver.Safari()

    # navigate to needed web pages and login to Google account
    driver.get("https://developers.google.com/calendar/quickstart/python?authuser=1")
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
    elem.click()
    identifier = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "identifier")))
    identifier.send_keys(google_username)
    nextBtn = driver.find_element_by_id('identifierNext')
    nextBtn.click()
    time.sleep(1)
    password = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "password")))
    password.send_keys(google_password)
    nextBtn = driver.find_element_by_id('passwordNext')
    nextBtn.click()
    time.sleep(2)
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
    elem.click()
    time.sleep(15)
    driver.get("https://developers.google.com/drive/api/v3/quickstart/python")
    time.sleep(2)
    elem1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
    elem1.click()
    time.sleep(10)
    driver.get("https://developers.google.com/gmail/api/quickstart/python")
    time.sleep(2)
    elem1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
    elem1.click()
    time.sleep(10)
    driver.switch_to.frame(0)
    elem1 = driver.find_elements_by_class_name("copy-bar-text")
    clientId = elem1[0].text.strip()
    secret = elem1[1].text.strip()

    # end browser session
    driver.quit()

    # make credentials.json
    data = {'installed': {
        'client_id': clientId,
        'project_id': 'quickstart',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
        'client_secret': secret,
        'redirect_uris': ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }}

    with open('credentials.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    autocred()