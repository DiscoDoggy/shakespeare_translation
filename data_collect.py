from dotenv.main import load_dotenv
import os
import csv

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests

import random
import time

"""
This file collects the raw shakespeare plays and the translated
Shakespeare plays
""" 

load_dotenv('secrets.env')


#Function defines a more realistic header for the scraper
def define_request_headers():
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",\
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",\
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"]

    headers = {
        "User-Agent": random.choice(user_agents),
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
        print(URL)
        # exit()
    
    return shakespeare_html

#For testing User-Agent
# r = requests.get("https://httpbin.org/headers", headers=headers)
# print(r.text)

    

#function calls scrape_shakespeare_page, extracts the HTML
#and parses HTML to obtain a link to each plays' acts which is stored and returned in a list
def get_shakespeare_play_links():
    URL = os.environ['TRANSLATIONS_HOMEPAGE']
    DOMAIN_NAME = os.environ['DOMAIN_NAME']
    shakespeare_home_html = scrape_shakespeare_page(URL)

    soup = BeautifulSoup(shakespeare_home_html, 'html.parser')

    link_to_play_acts = []

    for play in soup.find_all("a", class_="translation hoverable"):

        play_link = DOMAIN_NAME + play.get('href')
        link_to_play_acts.append(play_link)
        # print(play_link)
 
    return link_to_play_acts

#Makes python pause execution for a random time between 2 and 10 seconds
def random_sleep():
    random_sleep_time = random.randint(2,10)
    time.sleep(random_sleep_time)

#For each play and each act within each play, scrape the link to the content for that act
#write the link to a file (avoids storing an array of size 1000 and varying very long strings)
def scrape_acts_links():
    DOMAIN_NAME = os.environ['DOMAIN_NAME']
    content_links_file = open(r"act_content_links.txt", "w")

    link_to_play_acts = get_shakespeare_play_links()
    links_to_acts_content = []

    for link in link_to_play_acts:
        random_sleep()

        shakespeare_play_act_page_html = scrape_shakespeare_page(link)
    
        soup = BeautifulSoup(shakespeare_play_act_page_html, 'html.parser')

        intro_container = soup.find("div", id="intro")
        if intro_container != None:

            table_of_contents = intro_container.find("div", class_="table-of-contents")
            table_of_contents_anchors = table_of_contents.find_all("a")
            
            for act in table_of_contents_anchors:
                act_content_link = DOMAIN_NAME + act.get('href')
                links_to_acts_content.append(act_content_link)
                content_links_file.write(act_content_link + "\n")
                print(act_content_link)
        
    content_links_file.close()

    def scrape_text():
        act_content_links_file = open('act_content_links.txt', 'r')

        for line in act_content_links_file:
            random_sleep()