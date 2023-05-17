from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

import pandas as pd

from datetime import datetime, timedelta

# So Edge doesn't close
options = Options()
options.add_experimental_option("detach", True)

# Load driver 
driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options) 

# Set the URL from website we want to scrape 
url = 'https://comprar.gob.ar/BuscarAvanzadoPublicacion.aspx'

# To scrape a website with dynamic content, we'll use Selenium to interact with the website
driver.get(url)

tenders = []
keywords = ["agua", "suelo", "proyecto"]
today = datetime.today()
twoWeeksAgo = today - timedelta(days=14)
twoWeeksAgo = datetime.strftime(twoWeeksAgo, '%d/%m/%Y')
today = datetime.strftime(today, '%d/%m/%Y') 


keyword = "agua"
driver.find_element(By.XPATH, '//*[@id="ctl00_CPH1_txtPublicacionObjeto"]').send_keys(keyword)
driver.find_element(By.XPATH, '//*[@id="ctl00_CPH1_devDteEdtFechaAperturaDesde_I"]').send_keys(twoWeeksAgo)
driver.find_element(By.XPATH, '//*[@id="ctl00_CPH1_devDteEdtFechaAperturaHasta_I"]').send_keys(today)

driver.find_element(By.XPATH, '//*[@id="ctl00_CPH1_btnListarPublicacionAvanzado"]').click()

table = driver.find_element(By.XPATH, '//*[@id="ctl00_CPH1_GridListaPliegos"]')
rows = table.find_elements(By.TAG_NAME, "tr") 

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 0:
        tender = {}
        tender["title"] = cells[0].text
        tender["entity"] = cells[1].text
        tender["date"] = cells[2].text
        tender["link"] = cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
        tenders.append(tender)

