
#Import splinter and beautifulsoup

from splinter import Browser

from bs4 import BeautifulSoup as soup

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import datetime as dt

#Set up splinter

def scrape_all():
    #Initialize headless driver for deployment

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions and store results in dictionary

    data = {

        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image,
        'facts': mars_facts,
        'last_modified': dt.datetime.now()

    }

    #stop webdriver and return data

    browser.quit()

    return data

def mars_news(browser):

    #visit the mars nasa news site

    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'

    browser.visit(url)

    #optional delay for loading the page

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    #Convert the browser html to a soup object and then quit the browser

    html = browser.html

    news_soup = soup(html, 'html.parser')
    try:

        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_ = 'content_title').get_text()

        # Use the parent element to find the first 'a' tag and save it as 'news_title'

        news_title = slide_elem.find('div', class_='content_title').get_text()

        #Use the parent element to find the paragraph text

        news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
   
    except AttributeError:

        return None, None

    return news_title, news_p

#Define the function for the image

def featured_image(browser):

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(url)

    #Find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()

    #Parse the html from this page in order to get the html contents

    html = browser.html

    img_soup = soup(html, 'html.parser')

    #Get the relative path to the image URL
    try:
        img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')
        


    except AttributeError:

        return None
    #Use the base URL to create an absolute URL

    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

#Mars facts function

def mars_facts():

    #Use pandas to get all the rows in the mars facts webpage
    try:    
        df = pd.read_html('ttps://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:

        return None

    df.columns= ['description', 'Mars', 'Earth']

    df.set_index('description', inplace=True)
   
    #Convert dataFrame into HTML format, add bootstrap

    return df.to_html()


if __name__ == '__main__':
    #if running as script, print scraped data
    print(scrape_all())
