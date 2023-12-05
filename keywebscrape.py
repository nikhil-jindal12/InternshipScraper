from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

'''
Functions: 11 / 9-12
Loops: 15 / 6-9
Conditionals: 4 / 9-12 
'''

# open the website in a Chrome browser window
driver = webdriver.Chrome()

def parse_keybank_job(job_url):
    '''
    Parses the KeyBank job listing website and goes through the first 5 pages of listings

    Parameters: job_url - the url of the website to be parsed
    Returns: html_text - a list of the HTML code for each page of the website
            key_soup - a list of BeautifulSoup objects for each page of the website
    '''
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
    '''
    Parses the listings taken from the website and cleans the data to include only the parts we need

    Parameters: key_soup - a list of BeautifulSoup objects for each page of the website
    Returns: jobs - a list of the job titles
            locations - a list of the job locations and dates posted
    '''
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
    '''
    Writes the details taken from the previous method to a CSV file which can be opened in Excel or a text editor
    
    Parameters: jobs - a list of the job titles
                locations - a list of the job locations and dates posted
    Returns: None - the data is written to a CSV file
    '''
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
    '''
    Parses the job title to determine if the job is remote, hybrid, or on-site

    Parameters: job_title - the job title to be parsed
    Returns: job_title - the job title with the remote, hybrid, or on-site removed
             working_type - the remote, hybrid, or on-site type of the job
    '''
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
    '''
    Parses the Southern California Edison (SCE) internship listing website and goes through the first 5 pages of listings

    Parameters: None - the links are static and change for each page of listings
    Returns: SCE_html - a list of the HTML code for each page of the website
             SCE_soup - a list of BeautifulSoup objects for each page of the website
    '''
    SCE_first5_pages = ['https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=2',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=3',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=4',
                        'https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE&pg=5']

    # create lists that can be used to store the data scraped from the websites
    SCE_html = []
    SCE_soup = []

    # append the first 5 pages of the SCE website to the html_text list and key_soup list
    for page, num in zip(SCE_first5_pages, range(len(SCE_first5_pages))):
        # keep getting the new page and waiting a second for the page to laod
        driver.get(page)
        time.sleep(1)
        
        # append the new page to the html_text list and key_soup list
        SCE_html.append(driver.page_source)
        SCE_soup.append(BeautifulSoup(SCE_html[num], 'lxml'))
    
    return SCE_html, SCE_soup

def parse_SCE_job_details(SCE_soup):
    '''
    Parses the listings taken from the website and cleans the data to include only the parts we need

    Parameters: SCE_soup - a list of BeautifulSoup objects for each page of the website
    Returns: SCE_jobs - a list of the job titles
             SCE_locations - a list of the job locations and dates posted
    '''
    
    # create lists that can be used to store the individual data scraped from the websites
    SCE_jobs = []
    SCE_locations = []

    # parse the inputs to place each listing's data into the details
    for page in range(len(SCE_soup)):
        # use BeautifulSoup to find all of the links to the job titles
        positions = SCE_soup[page].find_all('div', class_ = 'jobTitle')
        for pos in positions:
            SCE_jobs.append(pos)
            
        # use BeautifulSoup to find all of the job location and dates posted
        places = SCE_soup[page].find_all('div', class_ = 'job-innerwrap g-cols')
        for city_state in places:
            SCE_locations.append(city_state.find('div', class_ = 'flex_column joblist-location fusion-layout-column fusion-one-fifth').text)

    return SCE_jobs, SCE_locations

def write_SCE_job_details(SCE_jobs, SCE_locations):
    '''
    Writes the details taken from the previous method to a CSV file which can be opened in Excel or a text editor
    
    Parameters: SCE_jobs - a list of the job titles
                SCE_locations - a list of the job locations and dates posted
    Returns: None - the data is written to a CSV file
    '''
    
    # write the scraped data to a csv file
    with open('keybank.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        
        # include the following columns of data: [Company, Job Title, Job Link, Salary, Location, Date Posted]
        for po, place in zip(SCE_jobs, SCE_locations):
            # parse the job title to determine if the job is remote, hybrid, or on-site
            title, work_type = working_type(po.text)
            
            # add the line to the csv in the given format
            line = ['Southern California Edison', title, 'https://www.edisoncareers.com' + SCE_jobs[SCE_jobs.index(po)].find('a').get('href'), 'N/A', place + ' (' + work_type + ')', 'N/A']
            csv_writer.writerow(line)

def parse_lenovo_jobs(job_url):
    '''
    Parses the Lenovo Careers website and goes through the first 5 pages of internship listings in the USA

    Parameters: job_url - the url of the website to be scraped
    Returns: lenovo_html - a list of the HTML code for each page of the website
             lenovo_soup - a list of BeautifulSoup objects for each page of the website
    '''
    
    # get the first page of the website and wait half of a second for the page to load
    driver.get('https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016802%5D&13036_format=6621&7715=%5B327885%5D&7715_format=3083&listFilterMode=1&jobRecordsPerPage=10&sort=relevancy')
    time.sleep(0.5)

    # create lists that can be used to store the data scraped from the websites
    lenovo_html = []
    lenovo_soup = []

    # append the first page of the website to the html_text list and key_soup list
    lenovo_html.append(driver.page_source)
    lenovo_soup.append(BeautifulSoup(lenovo_html[0], 'lxml'))

    # find the next page button and only use the first half of the results (page buttons on top and bottom of website)
    next_page_button = lenovo_soup[0].find_all('a', class_='list-controls__pagination__item paginationLink')
    next_page_button = next_page_button[:int(len(next_page_button)/2)]
        
    # go through the first 5 pages of the website and wait a second for each page to load
    for page, i in zip(next_page_button, range(len(next_page_button))):
        # break if more than 5 pages are parsed to ensure that the csv is not dominated with Lenovo listing
        if (i >= 5):
            break
        
        # keep getting the new page and waiting a second for the page to load
        driver.get(page['href'])
        time.sleep(1)
        
        # append the new page to the html_text list and key_soup list
        lenovo_html.append(driver.page_source)
        lenovo_soup.append(BeautifulSoup(lenovo_html[i + 1], 'lxml'))
        
    return lenovo_html, lenovo_soup

def parse_lenovo_job_details(lenovo_soup):
    '''
    Parses the listings taken from the website and cleans the data to include only the parts we need

    Parameters: lenovo_soup - a list of BeautifulSoup objects for each page of the website
    Returns: lenovo_jobs - a list of the job titles
             lenovo_locations - a list of the job locations and dates posted
    '''
    
    # create lists that can be used to store the individual data scraped from the websites
    lenovo_jobs = []
    lenovo_locations = []

    # parse the inputs to place each listing's data into the details
    for page in range(len(lenovo_soup)):
        # use BeautifulSoup to find all of the links to the listings
        internships = lenovo_soup[page].find_all('h3', class_='article__header__text__title article__header__text__title--4')
        for internship in internships:
            lenovo_jobs.append(internship)
        
        # use BeautifulSoup to find all of the job location and dates posted
        subtitles = lenovo_soup[page].find_all('div', class_='article__header__text__subtitle')
        for subtitle in subtitles:
            lenovo_locations.append(subtitle)
            
    return lenovo_jobs, lenovo_locations

def write_lenovo_job_details(lenovo_jobs, lenovo_locations):
    '''
    Writes the details taken from the previous method to a CSV file which can be opened in Excel or a text editor
    
    Parameters: lenovo_jobs - a list of the job titles
                lenovo_locations - a list of the job locations and dates posted
    Returns: None - the data is written to a CSV file
    '''
    
    # write the scraped data to a csv file
    with open('keybank.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        
        # include the following columns of data: [Company, Job Title, Job Link, Salary, Location, Date Posted]
        for int, sub in zip(lenovo_jobs, lenovo_locations):
            # break the subtitles up into their respective categories
            subs = sub.find_all('span')
            
            # add the line to the csv in the given format: [Company, Job Title, Job Link, Salary, Location, Date Posted]
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