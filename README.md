# PSMS Website Scraper.

The is the webscraper that I made along the PS 2 Helper extension, that scrapers the PSMS Website for all the details of every project, for each station. The Scraper is written using Selenium.<br/>

To run this locally, you first need to create a file "scret.txt". The first line of the file will contain your username (BITS Email ID), while the section line will contain will contain your password. <br/>
The file should look like this: <br>
email_id@pilani.bists-pilani.ac.in <br>
PASSWORD <br/>

Also make sure the following folders are present in the directory (for output):
generated
generated/dumps

The extension works in three phases.
1st phase: Scrapes the list of all projects from PSD website. Outputs a text file 'stations.txt' <br/>
2nd phase: Scrapes the projects of each of the project scraped in the earlier step. Outputs dumps as json files (each station has it's own file) in folder 'generated/dumps' <br/>
3rd phase: Converts all the dumps into a single exel and a single json (generated/data.txt, generated/data.json) <br/>

The first step is skipped if stations.txt is present. This means if the list of stations is updated, stations.txt needs to be deleted.
To run the first and second step, just run: <br/>
python scraper.py <br/>

To run the third step:
python dump_parser.py