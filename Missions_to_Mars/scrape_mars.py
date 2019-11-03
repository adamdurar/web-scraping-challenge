# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd
from sqlalchemy import create_engine
from selenium import webdriver
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info = {}

    # Step 1 - Scraping - NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].get_text()
    news_paragraph = soup.find_all(
        'div', class_='article_teaser_body')[0].get_text()

    # JPL Mars Space Images - Featured Image
    jpl_mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_mars_url)

    time.sleep(5)

    base_url = 'https://www.jpl.nasa.gov'

    jpl_mars_url = browser.html
    soup = BeautifulSoup(jpl_mars_url, 'html.parser')
    images_url = soup.find(id='full_image').get('data-fancybox-href')
    full_image_url = base_url + images_url

    # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    time.sleep(5)

    twitter_url = browser.html
    soup = BeautifulSoup(twitter_url, 'html.parser')
    mars_weather = soup.find(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(mars_facts_url)

    mars_df = tables[1]

    mars_df.columns = ['Attribute', 'Value']

    html_table = mars_df.to_html(header=None, index=False)
    html_table.replace('\n', '')
    html_table

    # Mars Hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    time.sleep(5)

    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]

    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        new_dict = {}

        browser.click_link_by_partial_text(hemisphere)
        hemispheres_url = browser.html
        soup = BeautifulSoup(hemispheres_url, 'html.parser')
        new_dict["title"] = soup.find(
            "h2").get_text().replace("Enhanced", "").strip()
        new_dict["img_url"] = soup.find_all("div", class_="downloads")[
            0].find_all("a")[0]["href"]
        hemisphere_image_urls.append(new_dict)

        browser.back()

    browser.quit()

    # Return one Python dictionary containing all of the scraped data
    mars_info = {
        "nasa_mars_title": news_title,
        "nasa_mars_paragraph": news_paragraph,
        "jpl_image": full_image_url,
        "mars_tweet": mars_weather,
        "mars_specs": html_table,
        "mars_hemispheres": hemisphere_image_urls
    }

    return mars_info


if __name__ == "__main__":
    print(scrape())
