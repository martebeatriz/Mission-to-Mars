
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# This function differs from the others in that it will:
# 
# Initialize the browser.
# Create a data dictionary.
# End the WebDriver and return the scraped data.



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres" : hemisphere_data(browser),
        "last_modified": dt.datetime.now()
        
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# In[3]:


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
     
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title') # find title and summary text 

        # Use the parent element to find the first <a> tag and save it as  `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

# In[4]:


def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# scrape the table form the website 

def mars_facts():
    
    try:
        # scrape the table form the website 
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # convert DataFrame back into HTML-ready code 
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

    
    
def hemisphere_data(browser):
    # visit url 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
        # list to hold the images and titles.
    hemisphere_image_urls = []

    links = browser.find_by_css('a.product-item img')

    for i in range (len(links)):
        # dictionary to store imgs and titles 
        hemisphere = {}

        # find img and click to next page
        browser.find_by_css('a.product-item img')[i].click()

        # find sample image and extract 
        sample_elem= browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        # get title
        hemisphere['title'] = browser.find_by_css('h2.title').text

        # append list with dictionary
        hemisphere_image_urls.append(hemisphere)

        # back to starter page
        browser.back()
        
        return hemisphere_image_urls
    





