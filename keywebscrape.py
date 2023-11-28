from bs4 import BeautifulSoup 
from selenium import webdriver
import time
import csv

driver = webdriver.Chrome()

driver.get('https://keybank.wd5.myworkdayjobs.com/External_Career_Site')

time.sleep(5)

html_text = driver.page_source

soup = BeautifulSoup(html_text, 'lxml')

driver.close()

jobs = soup.find_all('a', class_ = 'css-19uc56f')
locations = soup.find_all('dd', class_='css-129m7dg')

with open('keybank.csv', 'w') as file:
    csv_writer = csv.writer(file, delimiter='\t')
    csv_writer.writerow(['Company', 'Job Title', 'Job Link', 'Salary', 'Location', 'Date Posted'])

    # [Company, Job Title, Job Link, Salary, Location, Date Posted]
    for job, location in zip(jobs, range(len(jobs))):
        line = 'KeyBank' + '\t' + 'https://keybank.wd5.myworkdayjobs.com' + job.text.split(' -')[0].strip() + '\t' + job.get('href') + '\t' + 'N/A' + '\t' + locations[location * 2].text + '\t' + locations[(location * 2) + 1].text
        csv_writer.writerow(line)
