import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_all():
    browser = init_browser()
    # visit NASA News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('div', class_="list_text")
    news_title=results.a.text
    news_p=results.find("div",class_='article_teaser_body').text
    browser.quit()


    browser = init_browser()
    # visit twitter to get Mars weather
    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    time.sleep(1)

    response = requests.get(weather_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results=soup.find_all('div',class_="js-tweet-text-container")
    all_tweet=[result.text for result in results]
    weather=[]
    for x in all_tweet:
        if "InSight" in x:
            data={}
            data=x
            weather.append(data)
    weather=weather[0]
    new_weather=weather.replace('\n','')
    mars_weather=new_weather.rsplit('pic', 1)[0]   
    browser.quit()

    browser = init_browser()
    # visit the space site to get the latest pic of Mars
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


    browser = init_browser()
    # Mars Hemispheres
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


    # put all variables into dict 
    all={
    "news_title":news_title,
    "news_p":news_p,
    "mars_weather":mars_weather,
    "featured_image_url":featured_image_url,
    "first_img":img_url[0]['img_url'],
    "first_name":img_url[0]['title'],
    "second_img":img_url[1]['img_url'],
    "second_name":img_url[1]['title'],
    "third_img":img_url[2]['img_url'],
    "third_name":img_url[2]['title'],
    "fourth_img":img_url[3]['img_url'],
    "fourth_name":img_url[3]['title']
}

    return all




