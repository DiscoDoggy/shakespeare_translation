from dotenv.main import load_dotenv
import os

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import random
import time
import csv


"""
This file requests from a specific website the untranslated text of all shakespeare works and the translated texts
-First, For each play, grab the links that leads to a list of acts in each play and write it to a text file so we 
do not need to store it in RAM
-Then, for each link in the text file, open and collect all the character dialogue, translated and untranslated,
and write that information to a CSV.
""" 

load_dotenv('secrets.env')


#Function defines a more realistic header for the scraper
def define_request_headers():
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",\
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",\
        "HTC: Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",\
        "Google Nexus: Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7"]

    headers = {
        "User-Agent": random.choice(user_agents),
        # "Accept-Encoding" : "gzip, deflate, br",
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
        print("ERROR CODE:", response.status_code, response.reason)
        print(URL)
        # exit()
    
    return shakespeare_html

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

#For more dynamic webpages, need to wait for JS to render updated HTML
#This function 

def scrape_shakespeare_dynamic(URL):
    headers = define_request_headers()

    chrome_options = Options()

    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    chrome_options.add_experimental_option("useAutomationExtension", False)
    for header, value in headers.items():
        chrome_options.add_argument(f'--header={header}: {value}')
    

    WEB_DRIVER_PATH = os.environ['WEB_DRIVER_PATH']
    webdriver_service = Service(WEB_DRIVER_PATH)

    driver = webdriver.Chrome(service = webdriver_service, options=chrome_options)

    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(URL)

    driver.implicitly_wait(10)

    html = driver.page_source
    driver.quit()

    return html

def text_list_preprocess(color_codes, text_lines):
    color_code_words_tuple = zip(color_codes, text_lines)
    color_code_words_tuple = tuple(color_code_words_tuple)
    print("Code words tuple:", color_code_words_tuple)

    prev_num = None
    processed_words = []
    process_string = ""

    for i, code_str_tuple in enumerate(color_code_words_tuple):
        color_code = code_str_tuple[0]
        words = code_str_tuple[1]

        if prev_num == None: 
            process_string += words
            prev_num = color_code

        elif prev_num != color_code:
            processed_words.append(process_string)

            process_string = ""
            process_string += words
            prev_num = color_code
        
        elif prev_num == color_code:
            process_string = process_string + " " + words
            prev_num = color_code


        if i == len(color_code_words_tuple) - 1:
            processed_words.append(process_string)

    return processed_words

#Function opens the file which contains all the links to textual content
#queries that file to get the link then sends a get request to the link to get the textual content
#With the textual content, it is parsed into untranslated and translated text
#The text is then written to a CSV file

def scrape_text():
    act_content_links_file = open('act_content_links.txt', 'r')
    translated_untranslated_csv = open('shakespeare_and_translation.csv', 'w')

    csv_writer = csv.writer(translated_untranslated_csv)
    csv_writer.writerow(["Untranslated Shakespeare", "Translated Shakespeare"])

    for line in act_content_links_file:
        random_sleep()

        url_new_line_striped = line.rstrip()
        shakespeare_content_html = scrape_shakespeare_dynamic(url_new_line_striped)

        soup = BeautifulSoup(shakespeare_content_html, 'html.parser')
        list_of_comparison_rows = soup.find_all("div", class_="comparison-row")

        for row in list_of_comparison_rows:
            untranslated_column = row.find("div", class_="original-content")
            translated_column = row.find("div", class_= "translation-content")

            if untranslated_column == None or translated_column == None:
                continue

            untranslated_column_text = untranslated_column.find("p", class_="speaker-text") 
            translated_column_text = translated_column.find("p", class_="speaker-text")

            if untranslated_column_text == None or translated_column_text == None:
                continue

            untranslated_dc_span = untranslated_column_text.find_all("span", class_="line-mapping")
            translated_dc_span = translated_column_text.find_all("span", class_ = "line-mapping")
            print("\nuntranslated_dc_span:", untranslated_dc_span)
            print("translated_dc_span:", translated_dc_span, '\n')

            untranslated_data_color_list = [int(span.get('data-color')) for span in untranslated_dc_span if span != None]
            translated_data_color_list = [int(span.get('data-color')) for span in translated_dc_span if span != None]

            untranslated_data_text = [text_line.get_text() for text_line in untranslated_dc_span if text_line != None]
            translated_data_text = [text_line.get_text() for text_line in translated_dc_span if text_line != None]

            print("untranslated data color codes:", untranslated_data_color_list)
            print("translated data color codes:", translated_data_color_list, '\n')

            print("Untranslated Text Line:", untranslated_data_text)
            print("Translated Text Line:", translated_data_text)

            processed_ut_data_text = text_list_preprocess(untranslated_data_color_list, untranslated_data_text)
            processed_t_data_text = text_list_preprocess(translated_data_color_list, translated_data_text)

            print("processed_ut_data_text:", processed_ut_data_text, '\n')
            print("processed_t_data_text:", processed_t_data_text, '\n')

            print(len(processed_ut_data_text))
            print(len(processed_t_data_text))
            print('\n')
            assert len(processed_ut_data_text) == len(processed_t_data_text)

            processed_ut_t_pair = zip(processed_ut_data_text, processed_t_data_text)

            for pair in processed_ut_t_pair:
                csv_writer.writerow([pair[0], pair[1]])

    
    act_content_links_file.close()
    translated_untranslated_csv.close()


#For testing User-Agent
# r = requests.get("https://httpbin.org/headers", headers=headers)
# print(r.text)

#class comparison row consists of ORIGINAL PLAY (class is original-play)
#and also consists of class = modern-translation
#idea what if we get text from comparison row and stick it into an one each array

#for csvs, if there is a comma in the source sentence, quotes will be added to the text sequence to differentiate
#its commas from the csv commas

#experimentation with line to line scraping
#did not work because the lines of the untranslated do not pair consistently with the translated lines

            # untranslated_column_text = untranslated_column.find_all("span", class_ = "line-mapping")
            # translated_column_text = translated_column.find_all("span", class_="line-mapping")

            # print("\nuntranslated_column_text:", untranslated_column_text)
            # print("translated_column_text:", untranslated_column_text)

            # for (untranslated_text, translated_text) in zip(untranslated_column_text, translated_column_text):
            #     if untranslated_text != None and translated_text != None:
            #         untranslated_text_to_csv = untranslated_text.get_text()
            #         translated_text_to_csv = translated_text.get_text()

            #         csv_writer.writerow([untranslated_text_to_csv, translated_text_to_csv])