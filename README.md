# Modern English to Shakespearean English 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
[![beautiful-soup-shield][beautifulsoup-shield]][beautifulsoup-url] 
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)



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

Because translated works are technically copywritten, I do not include any of the data files in this repository but will provide example images of the data transformation. 
| Raw data sample  | Cleaned and preprocessed Data Sample  |
|---|---|
| ![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/8ced972a-9e59-4bb6-b72d-e1823dd2f15a)|![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/904e5fbd-c866-44f2-a3b5-cd6ca692aad7)| 

The cleaned data has been tokenized, and the unknown character has been removed. The extra comma in the cleaned data is the resul the CSV file placing a comma to separate columns. 

### [Exploratory Data Analysis](/shakespeare_translation_eda.ipynb) 
Within the exploratory data analysis, I perform a term frequency analysis and synthesize statistics regarding the data itself such as how long untranslated and translated text sequences are. 
The analysis can be found [here](/shakespeare_translation_eda.ipynb)

[beautifulsoup-shield]: https://img.shields.io/badge/-BEAUTIFULSOUP-blue?style=for-the-badge
[beautifulsoup-url]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

