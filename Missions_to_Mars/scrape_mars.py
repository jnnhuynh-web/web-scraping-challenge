# Import dependencies
from bs4 import BeautifulSoup
import requests

from splinter import Browser
import pandas as pd

# open browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape_info():
    browser = init_browser()

    ## SCRAPE THE NEWS ##
    # Visit Nasa
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Scrape page with Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # grab the title
    title = soup.find('div', class_="content_title").a.text
    # grab the paragraph
    paragraph = soup.find('div', class_="article_teaser_body").text


    ## SCRAPE THE IMAGE ##
    # Visit image page
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Scrape page with Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # grab the image url
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_href('spaceimages/images/largesize/')
    featured_image_url = browser.url

    ## SCRAPE THE WEATHER ##
    # Visit twitter page
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # Scrape page with Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # grab the tweet
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    for tweets in latest_tweets:
        mars_weather = tweets.find('p').get_text()
        if "InSight sol" in mars_weather:
            break
        else:
            pass

    ## SCRAPE THE FACTS TABLE ##
    # Visit facts page
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    # Scrape page with Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # grab the table
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    mars_facts = html_table.replace('\n', '')

    ## SCRAPE THE HEMISPHERES ##
    # Visit hemispheres page
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Scrape page with Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    base_url = "https://astrogeology.usgs.gov"

    hemisphere_image_urls = []
    
    #begin scraping

    # for Cerberus
    browser.click_link_by_partial_text('Cerberus')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Cerberus_title = soup.find('h2', class_="title").get_text().replace(' Enhanced', '')

    Cerberus_img = soup.find_all('a')[4]
    Cerberus_url = Cerberus_img.get('href')
    hemisphere_image_urls.append({"title": Cerberus_title, "img_url": Cerberus_url})
    browser.back()


    # for Schiaparelli
    browser.click_link_by_partial_text('Schiaparelli')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Schiaparelli_title = soup.find('h2', class_="title").get_text().replace(' Enhanced', '')

    Schiaparelli_img = soup.find_all('a')[4]
    Schiaparelli_url = Schiaparelli_img.get('href')
    hemisphere_image_urls.append({"title": Schiaparelli_title, "img_url": Schiaparelli_url})
    browser.back()


    # for Syrtis
    browser.click_link_by_partial_text('Syrtis')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Syrtis_title = soup.find('h2', class_="title").get_text().replace(' Enhanced', '')

    Syrtis_img = soup.find_all('a')[4]
    Syrtis_url = Syrtis_img.get('href')
    hemisphere_image_urls.append({"title": Syrtis_title, "img_url": Syrtis_url})
    browser.back()


    # for Valles
    browser.click_link_by_partial_text('Valles')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Valles_title = soup.find('h2', class_="title").get_text().replace(' Enhanced', '')

    Valles_img = soup.find_all('a')[4]
    Valles_url = Valles_img.get('href')
    hemisphere_image_urls.append({"title": Valles_title, "img_url": Valles_url})
    browser.back()


    # Store data in a dictionary
    mars_info = {
        "title": title,
        "paragraph": paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts":mars_facts,
        "hemisphere_image_urls":hemisphere_image_urls,
        }
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info