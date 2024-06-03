from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
import time
import pickle
import jsonpickle
#import json

#read from secret.txt
PASSWORD = ""
USERNAME = ""

class Project:
    title               = ''
    desc                = ''

    stipend_fd          = ''
    stipend_hd          = ''
    stipend_cur         = ''

    domain              = ''
    subdomain           = ''

    degree_type         = ''
    graduate_type       = ''

    tech_skills         = ''
    non_tech_skills     = ''

    first_degree        = ''

    courses             = ''
    grades              = ''

    ofst                = ''
    ofet                = ''
    holidays            = ''

    def __str__(self) -> str:
        return f"Title: {self.title}\n" \
               f"Description: {self.desc}\n" \
               f"Stipend (For First Degree): {self.stipend_fd}\n" \
               f"Stipend (For Higher Degree): {self.stipend_hd}\n" \
               f"Stipend Currency: {self.stipend_cur}\n" \
               f"Domain: {self.domain}\n" \
               f"Subdomain: {self.subdomain}\n" \
               f"Degree Type: {self.degree_type}\n" \
               f"Graduate Type: {self.graduate_type}\n" \
               f"Technical Skills: {self.tech_skills}\n" \
               f"Non-Technical Skills: {self.non_tech_skills}\n" \
               f"First Degree: {self.first_degree}\n" \
               f"Courses: {self.courses}\n" \
               f"Grades: {self.grades}\n" \
               f"Start Date: {self.ofst}\n" \
               f"End Date: {self.ofet}\n" \
               f"Holidays: {self.holidays}"

    def __init__(self, title='', desc='', stipend_fd='', stipend_hd='', stipend_cur='',
                 domain='', subdomain='', degree_type='', graduate_type='', tech_skills='',
                 non_tech_skills='', first_degree='', courses='', grades='', ofst='', ofet='',
                 holidays='') -> None:
        self.title = title
        self.desc = desc
        self.stipend_fd = stipend_fd
        self.stipend_hd = stipend_hd
        self.stipend_cur = stipend_cur
        self.domain = domain
        self.subdomain = subdomain
        self.degree_type = degree_type
        self.graduate_type = graduate_type
        self.tech_skills = tech_skills
        self.non_tech_skills = non_tech_skills
        self.first_degree = first_degree
        self.courses = courses
        self.grades = grades
        self.ofst = ofst
        self.ofet = ofet
        self.holidays = holidays
        

class Station:
    name = ""
    domain = ""
    city = ""
    state = ""
    country = ""
    link = ""

    projects = []

    projects_json = ""

    def add_projects(self, p):
        self.projects.append(p)

    def __init__(self, name, domain, city, state, country, link):
        self.name = name
        self.domain = domain
        self.state = state
        self.city = city
        self.country = country
        self.link = link

    def __str__(self) -> str:
        return '\n'.join([self.name, self.domain, self.city, self.state, self.country, self.link]) + '\n\n'
    
    def dump(self, pathname):
        self.projects_json = jsonpickle.encode(self.projects)
        with (open(pathname, "w+") as file):
            file.write(jsonpickle.encode(self))
        self.projects_json = ""

    # def load(self, pathname):
    #     with (open(pathname, "w+") as file):
    #         picke.dump(self, file, picke.HIGHEST_PRIORITY)
        



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

def extract_proj():
    title = driver.find_element(By.XPATH, "//*[contains(text(), 'Project Title')]/following-sibling::*").text
    desc = driver.find_element(By.XPATH, "//*[contains(text(), ' Project Description')]/following-sibling::*").text
    #Stipend For First Degree

    stipend_fd = driver.find_element(By.XPATH, "//*[contains(text(), 'Stipend For First Degree')]/following-sibling::*").text
    stipend_hd = driver.find_element(By.XPATH, "//*[contains(text(), 'Stipend For Higher Degree')]/following-sibling::*").text
    stipend_cur = driver.find_element(By.XPATH, "//*[contains(text(), 'Currency')]/following-sibling::*").text

    domain = driver.find_element(By.XPATH, "//*[contains(text(), 'Project Domain')]/following-sibling::*").text
    subdomain = driver.find_element(By.XPATH, "//*[contains(text(), 'Project Sub Domain')]/following-sibling::*").text

    degree_type = driver.find_element(By.XPATH, "//*[contains(text(), 'Degree Type')]/following-sibling::*").text
    graduate_type = driver.find_element(By.XPATH, "//*[contains(text(), ' Graduate Type')]/following-sibling::*").text

    tech_skills = driver.find_element(By.XPATH, "//*[contains(text(), 'Technical Skills')]/following-sibling::*").text
    non_tech_skills = driver.find_element(By.XPATH, "//*[contains(text(), 'Non Technical Skills')]/following-sibling::*").text

    first_degree = driver.find_element(By.XPATH, "//*[contains(text(), ' First Degree')]/following-sibling::*").text

    courses = ""
    grades = ""
    try:
        courses = driver.find_element(By.XPATH, "//*[contains(text(), 'Course(s)')]/following-sibling::*").text
        grades = driver.find_element(By.XPATH, "//*[contains(text(), 'Grade')]/following-sibling::*").text
    except:
        courses = "-"
        grades = "-"
        
    ofst = driver.find_element(By.XPATH, "//*[contains(text(), 'Office Start Time')]/following-sibling::*").text
    ofet = driver.find_element(By.XPATH, "//*[contains(text(), 'Office End Time')]/following-sibling::*").text
    holidays = driver.find_element(By.XPATH, "//*[contains(text(), 'Weekly Holidays')]/following-sibling::*").text
    
    project_instance = Project(title=title, desc=desc, stipend_fd=stipend_fd, stipend_hd=stipend_hd,
                           stipend_cur=stipend_cur, domain=domain, subdomain=subdomain,
                           degree_type=degree_type, graduate_type=graduate_type,
                           tech_skills=tech_skills, non_tech_skills=non_tech_skills,
                           first_degree=first_degree, courses=courses, grades=grades,
                           ofst=ofst, ofet=ofet, holidays=holidays)


    return project_instance
#    print(str(project_instance))
#    print('\n'.join([title, desc, stipend_fd, stipend_hd, stipend_cur, domain, subdomain, degree_type, graduate_type, tech_skills, non_tech_skills, first_degree]) + "___________________")

def extract_info(item):
    # Waits for login to complete
    nav_items = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, "nav-item"))
    time.sleep(1) # This is needed else we might get stuck at loading
    driver.get(item.link)
    wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "lds-roller")) == 0)

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
#        print(len(proj_options))
        for j in range(1, len(proj_options)):
            select_proj_element = Select(select_proj)
            select_proj_element.select_by_index(j)
            time.sleep(.75)
            wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "lds-roller")) == 0)
            item.add_projects(extract_proj())

login()
#goto_station_details_page()
#save_stations_to_file("stations.txt", extract_stations())

items = read_stations_from_list("stations.txt")

#def wait_for_options(driver):

def scrape(statefilepath, dumpsfold):
    with (open(statefilepath, "w+") as statefile):
        for i in range(0, len(items)):
            statefile.write("START__ITEM__({i})\n")
            statefile.write(f"Starting Extraction\n")
            try:
                extract_info(items[i])
            except:
                statefile.write(f"Extraction Failed:\n")
                return
            statefile.write(f"Dumping\n")
            try:
                items[i].dump(dumpsfold +  "/" + str(i) + ".json")
            except:
                statefile.write(f"Dump Failed\n")
                return
            statefile.write(f"Dump Successful\n")
            statefile.write("END__ITEM__({i})\n")

scrape("state.txt", "dumps")

#extract_info(items[0])
#items[0].dump("item0.json")

#restored = jsonpickle.decode(file.read("item0.json")) as Station