from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import pickle
import os.path
import json

#read from secret.txt
PASSWORD = ""
USERNAME = ""

with (open("secret.txt", "r") as file):
    lines = file.read().splitlines()
    USERNAME = lines[0]
    PASSWORD = lines[1]


driver = webdriver.Chrome()
driver.get("https://psms-web.azureedge.net/login")

wait = ui.WebDriverWait(driver, 100000)

def login():

    uid_field = wait.until(lambda driver: driver.find_elements(By.ID, "userId"))

    uid_field[0].send_keys(USERNAME)

    pass_field = driver.find_element(By.ID, "password")
    pass_field.send_keys(PASSWORD)

    remember_field = driver.find_element(By.CLASS_NAME, "custom-checkbox")
    remember_field.click()

    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()



# def station_details():
#     nav_items = wait.until(lambda driver: driver.find_elements(By.ID, "nav-item"))
#     for item in nav_items:
#         if (item.get_attribute("routerlinkactive") == "stationpreference/student"):
#             item.click()

login()
#station_details()

while (True):
    pass