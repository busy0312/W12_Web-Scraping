import os
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_news():
    browser = init_browser()
    # visit NASA News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('div', class_="list_text")
    time.sleep(2)

    news_title=results.find('div',class_="content_title").a.text
    news_p=results.find('div', class_='article_teaser_body').text

    mars_data = {
        "news_title": news_title,
        "news_p":news_p 
    }
    browser.quit()

    return mars_data

def scrape_weather():
    browser = init_browser()
    # visit twitter to get Mars weather
    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    time.sleep(1)

    response = requests.get(weather_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    weather=soup.find("div",class_="js-tweet-text-container").p.text
    new_weather=weather.replace('\n',',')
    mars_weather=new_weather.rstrip("pic.twitter.com/tWmeti4FBg")
    
    browser.quit()

    return mars_weather

def scrape_space_img():
    browser = init_browser()
    space_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_url)
    
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text("FULL IMAGE")
    browser.find_by_css('a.fancybox-next').click() 
    browser.click_link_by_partial_href('/spaceimages/detail')
    browser.find_by_css('img.main_image').click()
    featured_image_url=browser.url
    
    browser.quit()

    return featured_image_url



def mars_hemispheres():
    browser = init_browser()
    hem_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    time.sleep(1)

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = []

    for each_products in range(0,4):
        products = {}   
        browser.find_by_css("a.product-item h3")[each_products].click()  
        products["title"] = browser.find_by_css("h2.title").text 
        button = browser.find_link_by_text("Sample")
        products["img_url"] = button["href"]
        img_url.append(products)
        browser.back() 



    browser.quit()

    return img_url

    


