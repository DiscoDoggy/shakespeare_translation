# Modern English to Shakespearean English 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
[![beautiful-soup-shield][beautifulsoup-shield]][beautifulsoup-url] 
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) 
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) 

![NLTK](https://img.shields.io/badge/NLTK-blue)
![Seaborn](https://img.shields.io/badge/Seaborn-red)




## Introduction
The goal of this project is to create an end to end neural machine translation (NMT) that can translate Modern English to Shakespearean English. To apply this model I will
create a discord bot that, when invoked, will translate the caller's message into Shakespearean English and send that as the message. 

Here is an example! 
| Modern English  | Shakespearean English  |
|---|---|
| ![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/12f4bd84-a4b3-4131-92a6-dcc34ffe160d)| ![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/efd1f957-8f67-4224-815a-6d8e06f10c24)| 


### Stages of Development 
* Scrape Shakespearean English and Modern English translation text pairs :white_check_mark:
* Perform data cleaning :white_check_mark:
* Perform data preprocessing :white_check_mark:
* Perform an Exploratory Data Analysis (EDA) :white_check_mark:
* Create model :white_check_mark:
* Train model:white_check_mark:
* Test model :white_check_mark:
* Integrate model into discord bot
 
#### Scraping and Cleaning the Data
The efficacy in which data is scraped and cleaned impacts future deep learning model performance. If the data is collected poorly and cleaned poorly, then the deep learning model will have a harder time learning the "correct" 
representations due to the fact that the data has more poorly formatted and bad samples. Cleaning and good data collection can reduce or make bad data samples into good data samples. 

My data collection and data cleaning forms an ETL (Extract, Transform, Load) data pipeline where: 
* Shakespeares' texts and their translations are scraped from websites. This code is kept in [the data collect py file](https://github.com/DiscoDoggy/shakespeare_translation/blob/main/data_collect.py)
* While the data is being collected it is being transformed into parallel text pairs and staged into a CSV file. The transformation occuring here is that the data is being transformed from its unstructured form to
  a paired text form where one column of the CSV is Modern English and the other is the Shakespearean English. The text being collected is essentially being transformed into data pairs. 
* The data is then loaded into Pandas to be cleaned and this cleaned data is read into another CSV containing cleaned text pairs. [The data cleaning file](https://github.com/DiscoDoggy/shakespeare_translation/blob/main/clean_data.py)
* After cleaning, the data can then be preprocessed by Pytorch and fed into the model to be trained. [Preprocessing file](https://github.com/DiscoDoggy/shakespeare_translation/blob/main/newPreprocess.py)
, [Dataloader for loading preprocessed data into Pytorch](https://github.com/DiscoDoggy/shakespeare_translation/blob/main/dataloader.py) , [Pytorch model and training/eval script.](https://github.com/DiscoDoggy/shakespeare_translation/blob/main/baseline_model.py) 
### Scraping the Data 

To scrape the data, I use a combination of BeautifulSoup and Selenium. There were a few challenges when scraping the data. One of the major differences between Shakespearean English and Modern English is that they are still the same language. 
The translation between the two takes very large liberties in where to place punctuation. This means that the end of a sentence in the Shakesperean English is not necessairly the end of a sentence in the Modern English translation. This is a challenge because
in traditional machine translation between two different languages, the text segments are normally paired by the corresponding end of sentence which matches well across langauges. This is where Selenium solves the problem. The Modern Englsih and Shakesperean English segments are color coded where say a red segment of text in the Modern English translation corresponds to the Shakespearean English red line that it aims to translate. Selenium allows me to grab the color coded javascript attribute while Beautiful Soup allows me to grab the HTML text embedded deeply in the website. 

### Cleaning the Data
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

