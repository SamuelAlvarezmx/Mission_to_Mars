
#Import splinter and beautifulsoup

from splinter import Browser

from bs4 import BeautifulSoup as soup

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://redplanetscience.com'

browser.visit(url)

#Optional delay for loading the page

browser.is_element_present_by_css('div.list_text', wait_time=1)

#Set the html parser

html = browser.html

new_soup = soup(html, 'html.parser')

slide_elem = new_soup.select_one('div.list_text')

slide_elem.find('div', class_ = 'content_title')


#Use the parent elements to find the first 'a' tag and save it as 'news_title'

news_title = slide_elem.find('div', class_ = 'content_title').get_text()


#use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()



# ### Featured Images

#visit the URL to take the image for our code

url = 'https://spaceimages-mars.com'

browser.visit(url)

#Find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]

full_image_elem.click()

#Parse the html from this page in order to get the html contents

html = browser.html

img_soup = soup(html, 'html.parser')

#Get the relative path to the image URL

img_url_rel = img_soup.find('img', class_= 'fancybox-image').get('src')
img_url_rel

#Use the base URL to create an absolute URL

img_url = f'https://spaceimages-mars.com/{img_url_rel}'

img_url

#Use pandas to get all the rows in the mars facts webpage

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns= ['description', 'Mars', 'Earth']

df.set_index('description', inplace=True)

browser.quit()

df.to_html()

# ## Hemispheres
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.


html = browser.html

page_soup = soup(html, 'html.parser')

mars_soup = page_soup.find('div', class_ = 'collapsible results')
    
h_links = mars_soup.find_all('h3')

#itle_soup = mars_soup.find_all('h3')[0].text

for link in h_links:
    #Get the title
    title = link.text
    img_link = browser.find_by_text(link.text)
    img_link.click()
    html1 = browser.html
    img_soup= soup(html1, 'html.parser')
    
    #scrape the image link
    
    img_url = 'https://marshemispheres.com/' + str(img_soup.find('img', class_ = 'wide-image')['src'])
    #Appende to the dictionary
    
    url_title = {'title': title, 'img_url': img_url}
    
    hemisphere_image_urls.append(url_title)
    
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()



