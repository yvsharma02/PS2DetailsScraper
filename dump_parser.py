import jsonpickle
import os
import xlsxwriter
import pandas as pd

from common import Station, Project

def load_items(dmpsfldr):
    items = []
    files = os.listdir(dmpsfldr)
    for fpath in files:
        with (open(dmpsfldr + "/" + fpath, "r") as file):
            mp = jsonpickle.decode(file.read())
            mp.station_id = fpath
            items.append(mp)

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
    worksheet.write(0, 10, "Station-ID", header_format)

    # conversion_rates = {
    #     "INR": 1,
    #     "USD": 83.13
    # }

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
            worksheet.write(r, 4, str(stipend) + " " + str(project.stipend_cur))
            worksheet.write(r, 5, ' '.join([x[0:2] for x in project.first_degree.splitlines()]))
            worksheet.write(r, 6, project.holidays)
            worksheet.write(r, 7, f"{project.ofst}")
            worksheet.write(r, 8, f"f{project.ofet}")
            worksheet.write(r, 9, f"{project.desc}")
            worksheet.write(r, 10, f"{station.station_id.replace('.json', '')}")
            r += 1
    
    workbook.close()

def create_json(exelpath, outputpath):
    data = pd.read_excel(exelpath)
    data.reset_index()

    list = []

    for index, row in data.iterrows():
        list.append(row.to_json())

    with open(outputpath, 'w+') as file:
        file.write('[')
        for i in range(0, len(list)):
            file.write(list[i])
            if (i != len(list) - 1):
                file.write(', ')
        file.write(']')
    
items = load_items("generated/dumps")
create_exel("generated/data.xlsx", items)
create_json("generated/data.xlsx", "generated/data.json")