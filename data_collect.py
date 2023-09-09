from dotenv.main import load_dotenv
import os

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

"""
This file collects the raw shakespeare plays and the translated
Shakespeare plays
""" 

load_dotenv('secrets.env')


#Function defines a more realistic header for the scraper
def define_request_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "en-US,en;q=0.5",
        "Connection" : "keep-alive",
        "Referer" : "https://www.google.com/",
    }

    return headers

#Function scrapes the HTML of a inputted URL and returns that HTML
def scrape_shakespeare_page(URL):

    headers = define_request_headers()
    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        shakespeare_html = response.content
    else:
        print("In data_collect.py, scrape_shakespeare_links, response status not 200")
        exit()
    
    return shakespeare_html

    #r = requests.get("https://httpbin.org/headers", headers=headers)
    #print(r.text)

#function calls scrape_shakespeare_page, extracts the HTML
#and parses HTML to obtain a link to each play which is stored and returned in a list
def get_shakespeare_play_links():
    URL = os.environ['TRANSLATIONS_HOMEPAGE']
    DOMAIN_NAME = os.environ['DOMAIN_NAME']
    shakespeare_home_html = scrape_shakespeare_page(URL)

    soup = BeautifulSoup(shakespeare_home_html, 'html.parser')

    link_to_play_acts = []

    for play in soup.find_all("a", class_="translation hoverable"):

        play_link = DOMAIN_NAME + play.get('href')
        print(type(play_link))
        link_to_play_acts.append(play_link)
 
    print(link_to_play_acts)

    