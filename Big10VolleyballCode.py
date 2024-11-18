import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


# Getting the URL

pd.set_option('display.max_rows', None)
url = 'https://bigten.org/wvb/stats/'

# Open the Driver

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)


# Change the Year

wait = WebDriverWait(driver, 10)
dropdown = wait.until(EC.element_to_be_clickable((By.ID, "stats-select-season")))
dropdown.click()
year_option = driver.find_element(By.XPATH, ".//li[text()='2023']")
year_option.click()

# Create the Beautiful Soup Object
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the table

table = soup.find('table')

#Create the headers

headers = []
head = table.find('thead')


# Get the Rows

all = head.find_all('th')

for row in all:
    name = row.find('div').text
    headers.append(name)

# Get the body of each row

body = table.find('tbody')
rows = []
for row in body.find_all('tr'):
    data = []
    for item in row.find_all('td'):
        thing = item.text
        data.append(thing)
    rows.append(data)


# Create a pandas data frame

data2023 = pd.DataFrame(rows, columns= headers)

# Make a CSV

data2023.to_csv('data2024withRankingAll.csv')

# Close the Driver

driver.close()
