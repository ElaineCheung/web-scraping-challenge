from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

#Step 2

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# Execute the scraping code from `mission_to_mars.ipynb` and return a Python dictionary containing  the scraped data
def scrape():
    browser = init_browser()
    mars_dict={}

#Step 1: Web Scraping
## Part 1) Scrape NASA Mars News for latest headline
## URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    html = browser.html
    browser.visit(url)

## Create BeautifulSoup object; parse  with 'html.parser'
    soup = bs(html, "lxml")
    recent_news = soup.find('li', class_='slide')
    news_title = recent_news.find('h3').text
    news_p = recent_news.find(class_='rollover_description_inner').text

    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p


## Part 2) Use Splinter to Scrape JPL Mars Space Images - Featured Image
## URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    html = browser.html
    browser.visit(url)
    soup = bs(html, "lxml")

## Find image URL for current featured Mars image
    base_url = 'https://www.jpl.nasa.gov'
    style = soup.find('div',class_='carousel_items').article["style"]
    featured_image_url = base_url + style.split("url")[1].strip(";(')")
    print(featured_image_url)
    mars_dict["featured_image_url"] = featured_image_url

## Part 3)Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    url = 'https://space-facts.com/mars/'
    
    table = pd.read_html(url)[0]

    table.rename(columns={0:"mars_facts", 1:"data"}, inplace=True)

    html_table = table.to_html(index=False)


    table.rename(columns={0:"mars_facts", 1:"data"}, inplace=True)

    html_table = table.to_html(index=False)
    html_table.replace('\n', '')
    mars_dict["html_table"] = html_table

    # Close the browser after scraping
    browser.quit()
    return mars_dict