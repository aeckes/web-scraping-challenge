from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import re
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)


def scrape ():

    browser = init_browser()
    #URLs

    nasa_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    jpl_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_weather_twitter = 'https://twitter.com/marswxreport?lang=en'
    mars_facts = 'https://space-facts.com/mars/'
    USGS = 'https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    #Mars News

    response = requests.get(nasa_news_url)
    soup = bs(response.text, 'lxml')

    news_titles = soup.find_all('div', class_='content_title')
    blurbs = soup.find_all('div', class_='rollover_description_inner')

    news_title = news_titles[0].get_text(strip='True')
    blurb = blurbs[0].get_text(strip='True')

    mars_news = {'title': news_title, 'blurb': blurb}

    # print(news_title)
    # print(blurb)


    #JPL Mars Space Images - Featured Image

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(jpl_images_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image = soup.find('img', class_= 'fancybox-image')

    time.sleep(3)


    img_source = featured_image['src']
    img_name = img_source.split('/')[4]

    img_name_hires = img_name.split('_')[0] + "_hires.jpg"
    JPL_image_src = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/' + img_name_hires
        
    #print(JPL_image_src)

    featured_mars_image = {'url': JPL_image_src}


    #Mars Weather from latest tweet

    response = requests.get(mars_weather_twitter)
    soup = bs(response.text, 'lxml')

    tweets = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    tweets.a.decompose()
    latest_weather = tweets.get_text()

    #print(latest_weather)

    mars_weather_text = {'tweet': latest_weather}

    # Mars Facts

    tables = pd.read_html(mars_facts)
    df = tables[0]
    df.columns = ['Category', 'Value']



    html_table = df.to_html(index=False)
    html_table.replace('\n', '')
    #print(html_table)



    mars_facts_html = open('mars_facts.html','w')
    mars_facts_html.write(html_table)

    mars_facts_table = {'html': html_table}

    #Mars Hemispheres

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "..."},
        {"title": "Cerberus Hemisphere", "img_url": "..."},
        {"title": "Schiaparelli Hemisphere", "img_url": "..."},
        {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    ]

    browser.visit(USGS)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(2)

    for x in range (0,4):

        link_text = hemisphere_image_urls[x]['title']
        browser.click_link_by_partial_text(link_text)
        time.sleep(3)
        link_ref = browser.find_link_by_text('Sample')['href']    
        hemisphere_image_urls[x]['img_url'] = link_ref 
        print(hemisphere_image_urls[x]['img_url'])
        browser.back()
        time.sleep(2)


    mars_dict = {'mars_news': mars_news, 'featured_image': featured_mars_image, 'mars_weather': mars_weather_text, 'mars_facts': mars_facts_table, 'mars_images': hemisphere_image_urls}

    return mars_dict


