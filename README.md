# Modern English to Shakespearean English 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
[![beautiful-soup-shield][beautifulsoup-shield]][beautifulsoup-url] 
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) \

![NLTK](https://img.shields.io/badge/NLTK-blue)
![Seaborn](https://img.shields.io/badge/Seaborn-red)




## Introduction 
The goal of this repository is to document an end to end deep learning project involving machine translation. The end goal
is for a user to be able to input modernized English language text to a deep learning model and have the model output
a Shakespearean English translation. 

Here is an example! 
| Modern English  | Shakespearean English  |
|---|---|
| ![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/12f4bd84-a4b3-4131-92a6-dcc34ffe160d)| ![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/efd1f957-8f67-4224-815a-6d8e06f10c24)| 

### Applying the Model 
In order to see the model in live action, I plan on implementing API calls to some celebrity accounts on
X and Threads which will request the text of those posts, translate them to Shakespearean English, and repost them on a social media account
made specifically for this project. 

### Stages of Development 
* Scrape Shakespearean English and Modern English translation text pairs :white_check_mark:
* Perform data cleaning :white_check_mark:
* Perform data preprocessing :white_check_mark:
* Perform an Exploratory Data Analysis (EDA) :white_check_mark:
* Create model
* Train model
* Test model
* Make API calls and repost celebrity content in Shakespearean English

## Development 
### Scraping, Cleaning, and Preprocessing Data 
The process of scraping, cleaning, and preprocessing data forms the basis of this project. How well the data is cleaned and preprocessed can impact
eventual model performance. 

My data collection, cleaning, and preprocessing steps forms an ETL (Extract, Transform, Load) data pipeline where: 
* Shakespeare texts and its translations are collected (extraction) from websites
* This data is then stored (transformed, unstructured --> structured) into a CSV file so I can store it without running the data collection script repeatedly
* The data is then loaded into Pandas to be cleaned and processed

### Scraping the Data 
To scrape the data, I use a combination of Python's request library and Selenium. One of the main challenges when scraping was aligning the untranslated Shakespearean text segment to 
the corresponding translated Shakespearean text segment. Matching by punctuation did not work because the punctuation in a pair of segments could be different. On the website that I scraped though, 
each line of the untranslated text was color coded to a line in the translated text. This meant I could use the HTML/Javascript color codings to align my text sequences. Python's request library does not 
wait for Javascript elements to load, so I used Selenium in this case. The requests library was used to scrape the lists of Shakespeare's plays and acts of those plays storing them in another CSV file which then 
the Selenium scraper would use to enter those links and scrape the actual raw text. 

### Cleaning and Preprocessing 
For cleaning the data, I performed the following tasks:
* Substituted the unknown character symbol for a space. If this created a double or more space, in future
cleaning steps those extra spaces would be removed.
* Shakespeare often uses brackets and parenthesis to indicate actions but this is unlikely to see in social media tweets so I remove text between parenthesis and brackets including the parenthsis and brackets.
* I strip whitespace
* Remove any text pairs that contain French

For preprocessing the data, I tokenize the data where each word and each punctuation is its own token. I then append an 
EOS (end of segment) token to the end of each text sample. To prepare the data for the model, I also pad text segments which are below 10 tokens and truncate those that are over 10 tokens such that the model can batach process multiple text segments at a time. 

Because translated works are technically copywritten, I do not include any of the data files in this repository but will provide example images of the data transformation. 
| Raw data sample  | Cleaned Data Sample  |
|---|---|
|![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/bb152543-3f21-47c0-9ce5-3a5109f3cc96)|![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/3f74850a-aa89-49fb-afc2-4ef4ba759650)| 

The cleaned data has been tokenized, and the unknown character has been removed. The extra comma in the cleaned data is the resul the CSV file placing a comma to separate columns. 

### [Exploratory Data Analysis](/shakespeare_translation_eda.ipynb) 
Within the exploratory data analysis, I perform a term frequency analysis and synthesize statistics regarding the data itself such as how long untranslated and translated text sequences are. 
The analysis can be found [here](/shakespeare_translation_eda.ipynb)

[beautifulsoup-shield]: https://img.shields.io/badge/-BEAUTIFULSOUP-blue?style=for-the-badge
[beautifulsoup-url]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

