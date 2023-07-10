import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json

# URL and other constants
url = 'https://hf.dribl.com/ladders/'
season = "Winter 2023"
competition = "Premiership" #change to desired comp
league = "AAMen 11" #change to desired league
chrome_driver_path = '' #input file path to chromeDriver 
data_file_path = 'data.json'

# Initialize the web driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get(url)

time.sleep(5)

# Wait for the filter group element to be visible
filter_group = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "filter-group")))

# Click on the filter for "Filter by Competition"
filter_by_competition = filter_group.find_element(By.XPATH, ".//*[contains(text(), 'Filter by Competition')]")
filter_by_competition.click()

# Click on the "Premiership" option
premiership_option = filter_group.find_element(By.XPATH, ".//*[text()='Premiership']")
premiership_option.click()

# Click on the filter group for "Filter by League"
filter_by_league_group = driver.find_element(By.XPATH, "//*[contains(text(), 'Filter by League')]")
filter_by_league_group.click()

time.sleep(1)

# Find the search input field
search_input = driver.find_element(By.CSS_SELECTOR, 'div.el-input.el-input--mini.el-input--suffix input.el-input__inner')

# Clear the input field (optional)
search_input.clear()

# Type "AAMen 11" in the input field
search_input.send_keys("AAMen 11")

# Press Enter to perform the search
search_input.send_keys(Keys.ENTER)

time.sleep(1)

# Find the "AAMen 11" option from the search results
aamen_11_option = driver.find_element(By.XPATH, "//li[contains(text(), 'AAMen 11')]")
aamen_11_option.click()

time.sleep(1)

# Find all rows in the table
rows = driver.find_elements(By.XPATH, "//tr[contains(@class, 'shrink-text')]")
data = []

# Iterate over each row and extract the values
for row in rows:
    club_name = row.find_element(By.XPATH, ".//td[3]").text.strip()
    games_played = row.find_element(By.XPATH, ".//td[4]").text.strip()
    won = row.find_element(By.XPATH, ".//td[5]").text.strip()
    drawn = row.find_element(By.XPATH, ".//td[6]").text.strip()
    lost = row.find_element(By.XPATH, ".//td[7]").text.strip()
    points = row.find_element(By.XPATH, ".//td[14]").text.strip()
    goal_difference = row.find_element(By.XPATH, ".//td[12]").text.strip()

    row_data = {
        "Club": club_name,
        "Games Played": games_played,
        "Won": won,
        "Drawn": drawn,
        "Lost": lost,
        "Points": points,
        "Goal Difference": goal_difference
    }

    data.append(row_data)

    # Print the extracted values for each row
    print("Club:", club_name)
    print("Games Played:", games_played)
    print("Won:", won)
    print("Drawn:", drawn)
    print("Lost:", lost)
    print("Points:", points)
    print("Goal Difference:", goal_difference)
    print("--------------------------------")
    time.sleep(0.1)

# Compare the new data with the previous data
with open(data_file_path, 'r') as file:
    previous_data = json.load(file)

if data != previous_data:
    print("Data has changed!")
    
    # Save the new data to the data file
    with open(data_file_path, 'w') as file:
        json.dump(data, file)
else:
    print("No changes in data.")

# Close the web driver
driver.quit()
