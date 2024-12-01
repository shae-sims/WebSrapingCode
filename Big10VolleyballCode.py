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

#Clean the data to work in the plots

players = data2023.drop(columns= ['Unnamed: 0', 'logo url'])
players = players.rename(columns= {'RK' : 'rank', 'NAME':'name','GP':'games_played',
                            'SETS':'sets_played','KILLS': 'kills', 'KILL/S':'kills_per_set',
                            'PCT': 'hitting_percentage', 'A':'assists', 'A/S': 'assists_per_set',
                            'BLK':'blocks', 'BLK/S':'blocks_per_set', 'DIG':'digs',
                            'DIG/S':'digs_per_set', 'SA':'service_aces', 
                            'SA/S':'service_aces_per_set', 'R%':'reception_percentage'})

#Import packages for plots

import seaborn as sns
import matplotlib.pyplot as plt

#Create Correlation Matrix

correlation_matrix = players.drop(columns=['games_played', 'sets_played', 'name']).corr().round(2)
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True)
plt.title('Correlation Heatmap')
plt.show()

#Ranking Scatterplots

fig, axs = plt.subplots(2, 2, figsize=(10, 10))
axs[0,0].scatter(players['rank'],players['blocks'], color = 'skyblue')
axs[0,0].set_xlabel('Rank of Athlete')
axs[0,0].set_ylabel('Total Number of Blocks')
axs[0,0].set_title('Rank compared to Blocks')

axs[0,1].scatter(players['rank'],players['blocks_per_set'], color = 'skyblue')
axs[0,1].set_xlabel('Rank of Athlete')
axs[0,1].set_ylabel('Total Number of Blocks per Set')
axs[0,1].set_title('Rank compared to Blocks per Set')

axs[1,0].scatter(players['rank'],players['kills'], color = 'skyblue')
axs[1,0].set_xlabel('Rank of Athlete')
axs[1,0].set_ylabel('Total Number of Kills')
axs[1,0].set_title('Rank compared to Kills')

axs[1,1].scatter(players['rank'],players['kills_per_set'], color = 'skyblue')
axs[1,1].set_xlabel('Rank of Athlete')
axs[1,1].set_ylabel('Total Number of Kills per Set')
axs[1,1].set_title('Rank compared to Kills per Set')
plt.show()

#Other Scatterplots

fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].scatter(players['blocks'],players['kills'], color = 'darkcyan')
axs[0].set_xlabel('Number of Blocks')
axs[0].set_ylabel('Number of Kills')
axs[0].set_title('Number of Blocks VS Number of Kills')

axs[1].scatter(players['digs'],players['service_aces'], color = 'darkcyan')
axs[1].set_xlabel('Number of Digs')
axs[1].set_ylabel('Number of Aces')
axs[1].set_title('Digs compared to Aces')
plt.show()

#Barplot

top_hitters = players[0:5]

plt.figure(figsize= (7,7))
sns.barplot(top_hitters, x = 'name', y= 'hitting_percentage')
plt.ylabel('Hitting Percentage')
plt.xlabel('Athletes Name')
plt.title('Top 5 Athletes Hitting Percentage')
plt.show()
