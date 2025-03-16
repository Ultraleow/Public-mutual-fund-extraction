import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to select year
def select_year(year,driver):
    # Click on the year selector
    year_selector = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "datepicker-years"))
    )
    year_elements = year_selector.find_elements(By.TAG_NAME, "span")
    for year_element in year_elements:
        if year_element.text == str(year):
            year_element.click()
            break


month_mapping = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

# Function to select month using the old logic
def select_month(month_number,driver):
    month_name = month_mapping[month_number]  # Get month abbreviation
    month_selector = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "datepicker-months"))
    )
    month_elements = month_selector.find_elements(By.TAG_NAME, "span")
    for month_element in month_elements:
        if month_element.text == month_name:
            month_element.click()
            break

# Function to select day
def select_day(month, day, year,driver):
    # Click on the day selector
    day_selector = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "datepicker-days"))
    )
    day_elements = day_selector.find_elements(By.TAG_NAME, "td")

    # Format the day string correctly
    formatted_day = f"{month:02d}/{day:02d}/{year}"

    for day_element in day_elements:
        if day_element.get_attribute("data-day") == formatted_day:
            day_element.click()
            break


# Step-by-step selection
def click_date(date_object,driver):
    year = date_object.year
    month = date_object.month
    day = date_object.day

    select_year(year,driver)  # Select the year
    time.sleep(1)  # Optional wait time to allow for UI update
    select_month(month,driver)  # Select the month
    time.sleep(1)  # Optional wait time to allow for UI update
    select_day(month, day, year,driver)  # Select the day
