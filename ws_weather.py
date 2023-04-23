import csv
import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://www.wunderground.com/history/daily/us/pa/imperial/KPIT/date/"
start_date = datetime.date(2018, 1, 1)
end_date = datetime.date(2018, 12, 31)

high_temp_selector = '#inner-content > div.region-content-main > div.row > div:nth-child(3) > div:nth-child(1) > div > lib-city-history-summary > div > div.summary-table > table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)'
low_temp_selector = '#inner-content > div.region-content-main > div.row > div:nth-child(3) > div:nth-child(1) > div > lib-city-history-summary > div > div.summary-table > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)'
precipitation_selector = '#inner-content > div.region-content-main > div.row > div:nth-child(3) > div:nth-child(1) > div > lib-city-history-summary > div > div.summary-table > table > tbody:nth-child(4) > tr > td:nth-child(2)'

def get_weather_data(date):
    url = base_url + date.strftime('%Y-%m-%d')
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, high_temp_selector)))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    high_temp_element = soup.select_one(high_temp_selector)
    low_temp_element = soup.select_one(low_temp_selector)
    precipitation_element = soup.select_one(precipitation_selector)

    if high_temp_element and low_temp_element and precipitation_element:
        high_temp = high_temp_element.text.strip()
        low_temp = low_temp_element.text.strip()
        precipitation = precipitation_element.text.strip()
        return (high_temp, low_temp, precipitation)
    else:
        return (None, None, None)

driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser

with open('pittsburgh_weather_2018.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'high_temp', 'low_temp', 'precipitation']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    current_date = start_date
    while current_date <= end_date:
        high_temp, low_temp, precipitation = get_weather_data(current_date)
        print(f"Processing date: {current_date} - High: {high_temp}, Low: {low_temp}, Precipitation: {precipitation}")
        writer.writerow({'date': current_date, 'high_temp': high_temp, 'low_temp': low_temp, 'precipitation': precipitation})
        current_date += datetime.timedelta(days=1)
        sleep(1)  # Add a delay to avoid overloading the server

driver.quit()
