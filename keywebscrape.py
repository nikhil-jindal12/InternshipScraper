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
    with open('keybank.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        
        # include the following columns of data
        csv_writer.writerow(['Company', 'Job Title', 'Job Link', 'Salary', 'Location', 'Date Posted'])

        # input the data to the csv in the following format: [Company, Job Title, Job Link, Salary, Location, Date Posted]
        for job, location in zip(jobs, range(len(locations))):
            line = ['KeyBank', job.text.split(' -')[0].strip(), 'https://keybank.wd5.myworkdayjobs.com' + job.get('href'), 'N/A', locations[(location * 2)].text, locations[(location * 2) + 1].text]
            csv_writer.writerow(line)
            
def working_type(job_title):
    job_title = str(job_title)
    if ('hybrid' in job_title.lower()):
        split = job_title.split(' [')
        return split[0], split[1][:-1]
    elif ('remote' in job_title.lower()):
        split = job_title.split(' [')
        return split[0], split[1][:-1]
    elif ('on-site' or 'onsite' in job_title.lower()):
        split = job_title.split(' [')
        return split[0], split[1][:-1]
    return job_title, 'N/A'

def parse_SCE_jobs():
    SCE_first5_pages = ['https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=2',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=3',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=4',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=5']

    SCE_html = []
    SCE_soup = []

    for page, num in zip(SCE_first5_pages, range(len(SCE_first5_pages))):
        driver.get(page)
        time.sleep(1)
        SCE_html.append(driver.page_source)
        SCE_soup.append(BeautifulSoup(SCE_html[num], 'lxml'))
    
    return SCE_html, SCE_soup

def parse_SCE_job_details(SCE_soup):
    SCE_jobs = []
    SCE_locations = []

    for page in range(len(SCE_soup)):
        positions = SCE_soup[page].find_all('div', class_ = 'jobTitle')
        for pos in positions:
            SCE_jobs.append(pos)
            
        places = SCE_soup[page].find_all('div', class_ = 'job-innerwrap g-cols')
        for city_state in places:
            SCE_locations.append(city_state.find('div', class_ = 'flex_column joblist-location fusion-layout-column fusion-one-fifth').text)

    return SCE_jobs, SCE_locations

def write_SCE_job_details(SCE_jobs, SCE_locations):
    with open('keybank.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        for po, place in zip(SCE_jobs, SCE_locations):
            title, work_type = working_type(po.text)
            line = ['Southern California Edison', title, 'https://www.edisoncareers.com' + SCE_jobs[SCE_jobs.index(po)].find('a').get('href'), 'N/A', place + ' (' + work_type + ')', 'N/A']
            csv_writer.writerow(line)

def parse_lenovo_jobs(job_url):
    driver.get('https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016802%5D&13036_format=6621&7715=%5B327885%5D&7715_format=3083&listFilterMode=1&jobRecordsPerPage=10&sort=relevancy')
    time.sleep(0.5)

    lenovo_html = []
    lenovo_soup = []

    lenovo_html.append(driver.page_source)
    lenovo_soup.append(BeautifulSoup(lenovo_html[0], 'lxml'))

    next_page_button = lenovo_soup[0].find_all('a', class_='list-controls__pagination__item paginationLink')
    next_page_button = next_page_button[:int(len(next_page_button)/2)]
        
    for page, i in zip(next_page_button, range(len(next_page_button))):
        driver.get(page['href'])
        time.sleep(1)
        lenovo_html.append(driver.page_source)
        lenovo_soup.append(BeautifulSoup(lenovo_html[i + 1], 'lxml'))
        
    return lenovo_html, lenovo_soup

def parse_lenovo_job_details(lenovo_soup):
    lenovo_jobs = []
    lenovo_locations = []

    for page in range(len(lenovo_soup)):
        internships = lenovo_soup[page].find_all('h3', class_='article__header__text__title article__header__text__title--4')
        for internship in internships:
            lenovo_jobs.append(internship)
            
        subtitles = lenovo_soup[page].find_all('div', class_='article__header__text__subtitle')
        for subtitle in subtitles:
            lenovo_locations.append(subtitle)
            
    return lenovo_jobs, lenovo_locations

def write_lenovo_job_details(lenovo_jobs, lenovo_locations):
    with open('keybank.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        for int, sub in zip(lenovo_jobs, lenovo_locations):
            subs = sub.find_all('span')
            line = ['Lenovo', int.text.strip(), int.find('a').get('href'), 'N/A', subs[0].text.strip(), subs[2].text.strip()]
            csv_writer.writerow(line)


def main():
    # parse all the websites first and then close the driver
    key_html, key_soup = parse_keybank_job('https://keybank.wd5.myworkdayjobs.com/External_Career_Site')
    SCE_html, SCE_soup = parse_SCE_jobs()
    lenovo_html, lenovo_soup = parse_lenovo_jobs('https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016802%5D&13036_format=6621&7715=%5B327885%5D&7715_format=3083&listFilterMode=1&jobRecordsPerPage=10&sort=relevancy')
    driver.close()
    
    # individualize the data for each listing
    key_jobs, key_locations = parse_keybank_job_details(key_soup)
    SCE_jobs, SCE_locations = parse_SCE_job_details(SCE_soup)
    lenovo_jobs, lenovo_locations = parse_lenovo_job_details(lenovo_soup)
    
    # write the individualized data to a csv file
    write_keybank_job_details(key_jobs, key_locations)
    write_SCE_job_details(SCE_jobs, SCE_locations)
    write_lenovo_job_details(lenovo_jobs, lenovo_locations)
    
if __name__ == '__main__':
    main()