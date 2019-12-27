# Import dependencies
from bs4 import BeautifulSoup
import requests

from splinter import Browser
import pandas as pd

def open_driver():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def collect_news():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # grab the title
    title = soup.find('div', class_="content_title").a.text
    # grab the paragraph
    paragraph = soup.find('div', class_="article_teaser_body").text
