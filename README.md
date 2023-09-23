# Modern English to Shakespearean English 

# Tech Stack! 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
[![beautiful-soup-shield][beautifulsoup-shield]][beautifulsoup-url]



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
* Scrape Shakespearean English and Modern English translation text pairs
* Perform data cleaning
* Perform data preprocessing
* Perform an Exploratory Data Analysis (EDA)
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


[beautifulsoup-shield]: https://img.shields.io/badge/-BEAUTIFULSOUP-blue?style=for-the-badge
[beautifulsoup-url]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

