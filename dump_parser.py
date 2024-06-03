import jsonpickle
import os
import xlsxwriter

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

    def recreate_projects(self):
        self.projects = jsonpickle.decode(self.projects_json)
        self.projects_json = ''

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
        s = '\n'.join([self.name, self.domain, self.city, self.state, self.country, self.link]) + '\n\n'
        s += 'PROJECTS:'
        for x in self.projects:
            s += str(x)
        s += "_________________________"
        return s
    
    def dump(self, pathname):
        self.projects_json = jsonpickle.encode(self.projects)
        with (open(pathname, "w+") as file):
            file.write(jsonpickle.encode(self))
        self.projects_json = ""


def load_items(dmpsfldr):
    items = []
    files = os.listdir(dmpsfldr)
    for fpath in files:
        with (open(dmpsfldr + "/" + fpath, "r") as file):
            items.append(jsonpickle.decode(file.read()))
            items[-1].recreate_projects()

    return items

#Station, City, Domain, Project, Stipend(fd), stipend(hd), Branch(fd)

def create_exel(path, stations):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    r = 0
    for station in stations:
        for project in station.projects:
            worksheet.write(r, 0, station.name)
            worksheet.write(r, 1, station.city)
            worksheet.write(r, 2, project.domain)
            worksheet.write(r, 3, project.title)
            worksheet.write(r, 4, project.stipend_fd + ' ' + project.stipend_cur)
            worksheet.write(r, 5, project.stipend_hd + ' ' + project.stipend_cur)
            worksheet.write(r, 6, project.stipend_hd + ' ' + project.first_degree)
            r += 1
    
    workbook.close()
    
    


items = load_items("dumps")
create_exel("exel.xlsx", items)