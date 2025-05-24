from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


path = r"C:\Users\TEMITOPE\Desktop\DataEpic\Capstone_project\chromedriver.exe"
options = Options()

options.add_argument("--headless")

service = Service(path)
driver = webdriver.Chrome(service=service,options=options)

url = "https://aitoolsdirectory.com"

driver.get(url)

try:
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sv-badge sv-badge__1 sv-badge__1__1 clickable"))
    )

    result = driver.find_elements(By.CLASS_NAME, "sv-badge sv-badge__1 sv-badge__1__1 clickable")
    for i in result:
        print(i.text)

except Exception as e:
    print("Timed out waiting for page to load:", e)

