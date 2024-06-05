import jsonpickle
import os
import xlsxwriter

from common import Station, Project

def load_items(dmpsfldr):
    items = []
    files = os.listdir(dmpsfldr)
    for fpath in files:
        with (open(dmpsfldr + "/" + fpath, "r") as file):
            items.append(jsonpickle.decode(file.read()))

    return items

#Station, City, Domain, Project, Stipend(fd), stipend(hd), Branch(fd)

def create_exel(path, stations):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({'bold': True})
    worksheet.write(0, 0, "Station Name", header_format)
    worksheet.write(0, 1, "City", header_format)
    worksheet.write(0, 2, "Domain", header_format)
    worksheet.write(0, 3, "Title", header_format)
    worksheet.write(0, 4, "Stipend", header_format)
    worksheet.write(0, 5, "Degree", header_format)
    worksheet.write(0, 6, "Holidays", header_format)
    worksheet.write(0, 7, "Office-Start-Time", header_format)
    worksheet.write(0, 8, "Office-End-Time", header_format)
    worksheet.write(0, 9, "Project Details", header_format)

    conversion_rates = {
        "INR": 1,
        "USD": 83.13
    }

    r = 1
    for station in stations:
        for project in station.projects:

            stipend = max(int(project.stipend_fd), int(project.stipend_hd))
            
            if (project.domain == "Yet to be finalized"):
                project.domain = station.domain

            worksheet.write(r, 0, station.name)
            worksheet.write(r, 1, station.city)
            worksheet.write(r, 2, project.domain)
            worksheet.write(r, 3, project.title)
            worksheet.write(r, 4, stipend * conversion_rates[project.stipend_cur])
            worksheet.write(r, 5, ' '.join([x[0:2] for x in project.first_degree.splitlines()]))
            worksheet.write(r, 6, project.holidays)
            worksheet.write(r, 7, f"{project.ofst}")
            worksheet.write(r, 8, f"f{project.ofet}")
            worksheet.write(r, 9, f"{project.desc}")
            r += 1
    
    workbook.close()
    
    
items = load_items("generated/dumps")
create_exel("generated/exel.xlsx", items)