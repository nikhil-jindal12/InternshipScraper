# Project Title: Internship Web Scraper

This research proposal outlines our idea of making a web scraper for internships that essentially opens each company's job listings for internships and writes them onto a csv file for ease of sorting and searching. This csv file can easily be opened into Excel.

Statement of purpose: We aim for the web scraper to efficiently look through the extensive data available on companies' hiring sites and sort through them to extract information that students often find relevant and pertinent to their job search. For instance, many students often search for internships by location, specific job titles, etc.

**Please look at the `internship_web_scraper.py` file**
- The .py file has updated comments and a main() method, so all that is needed is to run the .py file.
- The file will not output anything to the terminal window, but it should create a file called `Scraped Internships.csv` in the same directory in which it is run which can be easily opened in Microsoft Excel.
- To format the data so that it is easy to read, please press Ctrl+A to select all of the data and then press Alt+H, Alt+O, and Alt+I to adjust the formatting and spacing of the data so that it is easier to read.
- The `internship_web_scraper.ipynb` file is the same code and should do the same thing, however, it is broken up into different sections of code instead of functions. I would not recommend using/running this file, but you are welcome to take a look at it.

## Datasets

For our project's datasets, we will be extracting data from four companies' internship hiring sites. We chose to scrape from KeyBank, Southern California Edison, Lenovo, and FedEx. These datasets represent a diverse selection, highlighting opportunities in banking, energy, technology, and transportation companies.

They are also diverse in the way that their websites are structured and coded in HTML. Some websites are single-page applications (SPAs), where the URL for the website does not change when the button to go to the next page of listings is clicked, and others have static links to the various pages of listings that are available. Below are the home/first pages of the websites from which our datasets are derived:
1. [KeyBank Internship Listings](https://keybank.wd5.myworkdayjobs.com/External_Career_Site?jobFamilyGroup=8a3a66d0b19f1001995eed4900ec0000)
2. [Southern California Edison Internship Listings](https://www.edisoncareers.com/job-search-results/?category=Internship&compliment=SCE)
3. [Lenovo Internship Listings](https://jobs.lenovo.com/en_US/careers/SearchJobsUniversity)
4. [Fedex Internship Listings](https://careers.fedex.com/intern/jobs/categories/Intern?categories=Intern&page=1)

**Note**: The sites for Edison and Fedex are static, and the other two are the homepages.

**Note**: [Selenium for Colab](https://colab.research.google.com/github/restrepo/ComputationalMethods/blob/master/tools/selenium.ipynb#scrollTo=--i6YklVRlIK) helped get this project started and provided a good reference point to start building from.

As discussed in the implications part of this research proposal, the nature of this project allows for future expansion to other/additional internship hiring sites, as well as the ability to leverage different APIs to filter and sort the data for more relevant results based on specific user input.

## Hypothesis
The Python coded web scraper created for this project will be able to successfully and accurately extract the available internship postings from the first five pages of all four sites. The results, which will be formatted in a csv file, will then make it easier for each user to sort through the data and cater to their needs.

## Plan/Methodology

Considering the quantity of data available on hiring sites, the web scraper will focus on the first five pages of job listings on each site, if there are more than five pages.

Outlined steps (similar across websites):

1. Use the Selenium package in Python to simulate a Google Chrome browser window which will open the home/first page of each company's website in consecutive order
2. Parse through the first five pages of listings (if applicable)
3. Close web driver and window
4. Parse the listings taken in order of scraping and clean the data
5. Write the data into a CSV file in the following order: [Company Name, Job Title, Job Link, Location, Date Posted]

**Note**: The nature of this project demands more emphasis on loops than conditionals. However, users can use conditionals to further sort the data according to their search.

## Potential Implications

The internship web scraper this project aims to create has several notable implications for future development and user-specific goals. From a practical standpoint, this webscraper facilitates the process of job searching because it reduces the amount of time and effort many students invest into manually searching different company websites for specific jobs they may be qualified for, or certain job locations they might be interested in. In its present state, this project provides an outline for the uses of large-scale web scraping tehcnology using sample employers.  

## Future Vision
In addition to narrowing down internship opportunities for these four companies, this project can be expanded to include other major employers from various industries. This can broaden the horizons for the distribution of this project in the future. Although beyond the scope of this assignment, we would like to highlight in our proposal other potential data that can be matched to job listings: application deadlines, required graduating year(s), most common major to be employed, benefits package, etc. This can allow for a more widespread adoption of a scraper that facilitates the documentation, search, and systemization of students' job hunt.
