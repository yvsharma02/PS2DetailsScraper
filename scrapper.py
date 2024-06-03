from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
import time
#import json

#read from secret.txt
PASSWORD = ""
USERNAME = ""


class Station:
    name = ""
    domain = ""
    city = ""
    state = ""
    country = ""
    link = ""

    def __init__(self, name, domain, city, state, country, link):
        self.name = name
        self.domain = domain
        self.state = state
        self.city = city
        self.country = country
        self.link = link

    # def toJSON(self):
    #     return json.dumps(
    #         self,
    #         default=lambda o: o.__dict__)

    def __str__(self) -> str:
        return '\n'.join([self.name, self.domain, self.city, self.state, self.country, self.link]) + '\n\n'


with (open("secret.txt", "r") as file):
    lines = file.read().splitlines()
    USERNAME = lines[0]
    PASSWORD = lines[1]


driver = webdriver.Chrome()
driver.get("https://psms-web.azureedge.net/login")

wait = ui.WebDriverWait(driver, 100000)


def login():
    print("Perfomring Login")
    uid_field = wait.until(lambda driver: driver.find_elements(By.ID, "userId"))

    uid_field[0].send_keys(USERNAME)

    pass_field = driver.find_element(By.ID, "password")
    pass_field.send_keys(PASSWORD)

    remember_field = driver.find_element(By.CLASS_NAME, "custom-checkbox")
    remember_field.click()

    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()

def goto_station_details_page():
    print("Going to Stations Page")
    nav_items = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, "nav-item"))
    for item in nav_items:
        inner = item.find_element(By.TAG_NAME, "a")
        if (inner.get_attribute("routerlink") == "/stationpreference/student"):
            item.click()
            break
    
    
    print("Going to Details Page")
    details_btn = wait.until(lambda driver: driver.find_elements(By.ID, "pills-profile-tab"))
    details_btn[0].click()

def extract_stations():
    print ("Extracting Data. This step may take a while")
    table_parent = wait.until(lambda driver: driver.find_elements(By.ID, "pills-profile"))
    items_raw = table_parent[0].find_elements(By.TAG_NAME, "tr")
    while (len(items_raw) <= 2):
        time.sleep(1)
        table_parent = wait.until(lambda driver: driver.find_elements(By.ID, "pills-profile"))
        items_raw = table_parent[0].find_elements(By.TAG_NAME, "tr")
    
    items = []
    items_raw.remove(items_raw[0])
    c = 0
    for raw in items_raw:
        print("Extracting: " + str(c) + "/" + str(len(items_raw)))
        c += 1
        fields = raw.find_elements(By.TAG_NAME, "td")
        # print("\n".join([fields[0].find_element(By.TAG_NAME, "a").text,
        #         fields[1].text,
        #         fields[2].text,
        #         fields[3].text,
        #         fields[4].text,
        #         fields[5].find_element(By.TAG_NAME, "a").get_attribute("href")]) + "\n")
        items.append(
            Station(
                fields[0].find_element(By.TAG_NAME, "a").text,
                fields[1].text,
                fields[2].text,
                fields[3].text,
                fields[4].text,
                fields[5].find_element(By.TAG_NAME, "a").get_attribute("href")
            )
        )
    
    return items

def save_stations_to_file(path, stations):
    print("Writing Stations File")
    with (open(path, "w+") as file):
        for station in stations:
#            print(str(station))
            file.write(str(station))

def read_stations_from_list(path) -> list[Station]:
    print("Reading Stations File")
    with (open(path, "r") as file):
        stations_raw = file.read().split("\n\n")
        res = []
        for raw in stations_raw:
#            print(raw)
            fields = raw.splitlines()
            if (len(fields) < 6): continue
            res.append(Station(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]))
    return res

login()
#goto_station_details_page()
#save_stations_to_file("stations.txt", extract_stations())

items = read_stations_from_list("stations.txt")

#def wait_for_options(driver):



for item in items:
    # Waits for login to complete
    nav_items = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, "nav-item"))
    time.sleep(1) # This is needed else we might get stuck at loading
    driver.get(item.link)

    dropdowns = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, "row"))
    dropdowns = dropdowns[1]
    select_bank = dropdowns.find_elements(By.TAG_NAME, "select")[0]
#    select_proj = dropdowns.find_elements(By.TAG_NAME, "select")[1]
    
    time.sleep(1)# The simlest solution I can think of right now. Not very effective
    bank_options = wait.until(lambda x : select_bank.find_elements(By.TAG_NAME, "option"))


#    select_bank = dropdowns.find_elements(By.TAG_NAME, "select")[0]

    for i in range(1, len(bank_options)):
        select_bank_element = Select(select_bank)
        select_bank_element.select_by_index(i)
        time.sleep(1)

        select_proj = driver.find_elements(By.CLASS_NAME, "row")[1].find_elements(By.TAG_NAME, "select")[1]
        proj_options = select_proj.find_elements(By.TAG_NAME, "option")
        print(len(proj_options))
        for j in range(1, len(proj_options)):
            select_proj_element = Select(select_proj)
            select_proj_element.select_by_index(j)
            time.sleep(5)


    while (True):
        pass

while (True):
    pass