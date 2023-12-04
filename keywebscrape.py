from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

'''
Functions: 3 / 9-12
Loops: 5 / 6-9
Conditionals: / 9-12 
'''

# open the website in a Chrome browser window
driver = webdriver.Chrome()

def parse_keybank_job(job_url):
    # open the single-page application (SPA) in a browser window
    driver.get(job_url)
    time.sleep(2)

    # find a list of buttons on the page that can be clicked to change the HTML on the SPA
    pages = driver.find_elements(By.CLASS_NAME, 'css-1j096s0')
    
    # create lists that can be used to store the data scraped from the websites
    html_text = []
    key_soup = []
    
    # append the first page of the SPA to the html_text list and key_soup list
    html_text.append(driver.page_source)
    key_soup.append(BeautifulSoup(html_text[0], 'lxml'))
    
    # click on each of the buttons on the page and append the new HTML to the html_text list and key_soup list
    for page in range(1,len(pages)):
        pages[page].click()
        time.sleep(1)
        html_text.append(driver.page_source)
        key_soup.append(BeautifulSoup(html_text[page], 'lxml'))
        
    return html_text, key_soup

def parse_keybank_job_details(key_soup):
    # create lists that can be used to store the individual data scraped from the websites
    jobs = []
    locations = []
    
    # parse the inputs to place each listing's data into the details
    for page in range(len(key_soup)):
        # use BeautifulSoup to find all of the links to the job titles
        listing = key_soup[page].find_all('a', class_ = 'css-19uc56f')
        for title in listing:
            jobs.append(title)

        # use BeautifulSoup to find all of the job location and dates posted
        place = key_soup[page].find_all('dd', class_='css-129m7dg')
        for citystate in place:
            locations.append(citystate)
            
    return jobs, locations

def write_keybank_job_details(jobs, locations):
    # write the scraped data to a csv file
    with open('keybank.csv', 'w') as file:
        csv_writer = csv.writer(file, delimiter=',')
        
    # include the following columns of data
    csv_writer.writerow(['Company', 'Job Title', 'Job Link', 'Salary', 'Location', 'Date Posted'])

    # input the data to the csv in the following format: [Company, Job Title, Job Link, Salary, Location, Date Posted]
    for job, location in zip(jobs, range(len(locations))):
        line = ['KeyBank', job.text.split(' -')[0].strip(), 'https://keybank.wd5.myworkdayjobs.com' + job.get('href'), 'N/A', locations[(location * 2)].text, locations[(location * 2) + 1].text]
        csv_writer.writerow(line)

def main():
    # parse all the websites first and then close the driver
    key_html, key_soup = parse_keybank_job('https://keybank.wd5.myworkdayjobs.com/External_Career_Site')
    driver.close()
    
    # individualize the data for each listing
    key_jobs, key_locations = parse_keybank_job_details(key_soup)
    
    # write the individualized data to a csv file
    write_keybank_job_details(key_jobs, key_locations)
    
if __name__ == '__main__':
    main()