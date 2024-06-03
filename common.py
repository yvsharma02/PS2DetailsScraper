import jsonpickle

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

    projects = None

    def add_projects(self, p):
        self.projects.append(p)

    def __init__(self, name, domain, city, state, country, link):
        self.projects = []
        self.name = name
        self.domain = domain
        self.state = state
        self.city = city
        self.country = country
        self.link = link

    def __str__(self) -> str:
        return '\n'.join([self.name, self.domain, self.city, self.state, self.country, self.link]) + '\n\n'
    
    def dump(self, pathname):
        with (open(pathname, "w+") as file):
            file.write(jsonpickle.encode(self))