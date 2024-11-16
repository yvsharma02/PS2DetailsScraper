from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
import time
import jsonpickle
#import os.path
import os

from common import Station, Project

#import json

#read from secret.txt
PASSWORD = ""
USERNAME = ""

with (open("secret.txt", "r") as file):
    lines = file.read().splitlines()
    USERNAME = lines[0]
    PASSWORD = lines[1]


driver = webdriver.Chrome()
driver.get("https://psms.bits-pilani.ac.in/")

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
            file.write(str(station))

def read_stations_from_list(path) -> list[Station]:
    print("Reading Stations File")
    with (open(path, "r") as file):
        stations_raw = file.read().split("\n\n")
        res = []
        for raw in stations_raw:
            fields = raw.splitlines()
            if (len(fields) < 6): continue
            res.append(Station(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]))
    return res

def extract_detail(detail_name, link):
    try:
        val = driver.find_element(By.XPATH, f"//*[contains(text(), '{detail_name}')]/following-sibling::*").text
        return val
    except Exception as e:
        msg = f"[${link}]: {detail_name}"
        print(f"Failed to [${msg}], due to [${str(e)}]")
        with (open ("generated/failure.txt", "a+") as f):
            f.write(msg)
        return ""


def extract_proj(link):
    title = extract_detail('Project Title', link)
    desc = extract_detail(' Project Description', link)
    #Stipend For First Degree

    stipend_fd = extract_detail('Stipend For First Degree', link)
    stipend_hd = extract_detail('Stipend For Higher Degree', link)
    stipend_cur = extract_detail('Currency', link)

    stipend_cur = stipend_cur if stipend_cur != "" else "0"
    stipend_hd = stipend_hd if stipend_hd != "" else "0"
    stipend_fd = stipend_fd if stipend_fd != "" else "0"

    domain = extract_detail('Project Domain', link)
    subdomain = extract_detail('Project Sub Domain', link)

    degree_type = extract_detail('Degree Type', link)
    graduate_type = extract_detail(' Graduate Type', link)

    tech_skills = extract_detail('Technical Skills', link)
    non_tech_skills = extract_detail('Non Technical Skills', link)

    first_degree = extract_detail(' First Degree', link)

    ofst = extract_detail('Office Start Time', link)
    ofet = extract_detail('Office End Time', link)
    holidays = extract_detail('Weekly Holidays', link)

    courses = extract_detail('Course(s)', link)
    grades = extract_detail('Grade', link)
    
    project_instance = Project(title=title, desc=desc, stipend_fd=stipend_fd, stipend_hd=stipend_hd,
                           stipend_cur=stipend_cur, domain=domain, subdomain=subdomain,
                           degree_type=degree_type, graduate_type=graduate_type,
                           tech_skills=tech_skills, non_tech_skills=non_tech_skills,
                           first_degree=first_degree, courses=courses, grades=grades,
                           ofst=ofst, ofet=ofet, holidays=holidays)


    return project_instance

def get_scrapped_stations_link_set(dmpsfldr):
    items = set()
    files = os.listdir(dmpsfldr)
    for fpath in files:
        with (open(dmpsfldr + "/" + fpath, "r") as file):
            items.add(jsonpickle.decode(file.read()).link)

    return items

def extract_info(item):
    # Waits for login to complete
    nav_items = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, "nav-item"))
    time.sleep(2) # This is needed else we might get stuck at loading
    print(item.link)
    driver.get(item.link)
    wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "lds-roller")) == 0)

    dropdowns = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, "row"))
    
    dropdowns = dropdowns[1]
    select_bank = dropdowns.find_elements(By.TAG_NAME, "select")[0]
    
    time.sleep(2)# The simlest solution I can think of right now. Not very effective
    bank_options = wait.until(lambda x : select_bank.find_elements(By.TAG_NAME, "option"))

    for i in range(1, len(bank_options)):
        select_bank_element = Select(select_bank)
        select_bank_element.select_by_index(i)
        time.sleep(2)

        select_proj = driver.find_elements(By.CLASS_NAME, "row")[1].find_elements(By.TAG_NAME, "select")[1]
        proj_options = select_proj.find_elements(By.TAG_NAME, "option")
        for j in range(1, len(proj_options)):
            select_proj_element = Select(select_proj)
            select_proj_element.select_by_index(j)
            time.sleep(2)
            wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "lds-roller")) == 0)
            try:
                item.add_projects(extract_proj(item.link))
            except Exception as e:
                print(f"Failed to add project for {item.link} due to {str(e)}")
                with (open ("generated/failed.txt", "a+") as f):
                    f.write(item.link)

def get_dmpfile_name(index):
    link = stations[index].link
    link = link[0:link.rfind('/')]
    return link[link.rfind('/') + 1:]

def scrape(statefilepath, dumpsfold, stations):

    if (not os.path.isdir(dumpsfold)):
        os.makedirs(dumpsfold)

    scraped_set = get_scrapped_stations_link_set("generated/dumps")
    with (open(statefilepath, "w+") as statefile):
        for i in range(0, len(stations)):
            print (f"Working on {i + 1}/{len(stations)}")

            if (stations[i].link in scraped_set):
                statefile.write("EXISTS__({i})\n")
                continue

            statefile.write(f"START__ITEM__({i})\n")
            statefile.write(f"Starting Extraction\n")
            try:
                extract_info(stations[i])
            except Exception as e:
                statefile.write(f"Extraction Failed:\n")
                statefile.write(str(e))
                return
            statefile.write(f"Dumping\n")
            print(dumpsfold +  "/" + get_dmpfile_name(i) + ".json")
            try:
                stations[i].dump(dumpsfold +  "/" + get_dmpfile_name(i) + ".json")
            except:
                statefile.write(f"Dump Failed\n")
                return
            statefile.write(f"Dump Successful\n")
            statefile.write(f"END__ITEM__({i})\n")
            scraped_set.add(stations[i].link)

login()

if (not os.path.exists("generated/stations.txt")):
    goto_station_details_page()
    save_stations_to_file("generated/stations.txt", extract_stations())

stations = read_stations_from_list("generated/stations.txt")
scrape("generated/state.txt", "generated/dumps", stations)