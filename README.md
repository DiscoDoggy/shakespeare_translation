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
* Train model :white_check_mark:
* Validate model :white_check_mark:
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
| Example of aligning color coded text segments |
|---|
|![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/0fa65347-3ea1-4a2b-9da8-9b79aba32f69)|


### Cleaning the Data
For cleaning the data, I performed the following tasks:
* Substituted the unknown character symbol for a space. If this created a double or more space, in future
cleaning steps those extra spaces would be removed.
* Converted all text to lowercase and utilized regular expressions to identify punctuation and add a space between it and other words so that it can be tokenized. 
* Eliminate double and triple spaces
* Parenthesis are not used a lot in modern speech nor are brackets so I eliminated any text between brackets, parenthesis, and braces and including the braces, parenthesis, and brackets.
* Strip leading and trailing whitespace
* Because of how text segments are aligned there are a lot of open parenthsis, and its counterparts, without closing. I accounted for this by removing unpaired parenthesis, and its counterparts, pairs.
* Dropped duplicate segments
* Because text is aligned by color and not by sentence, some segments end in semicolons, commas, and other punctuation that would not ever end a sentence. I remove these non ending sentence punctuations.
* Remove any text pairs that contain French

Because translated works are technically copywritten, I do not include any of the data files in this repository but will provide example images of the data transformation and a very small sample. 

| Raw data sample  | Cleaned Data Sample  |
|---|---|
|![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/bb152543-3f21-47c0-9ce5-3a5109f3cc96)|![image](https://github.com/DiscoDoggy/shakespeare_translation/assets/110149934/51d042cc-74cd-4180-8e61-5be2ca93c6d2)| 

### Preprocessing the Data 
Preprocessing the data is just another way of saying preparing the data so that it can be used by Pytorch. Because I am using a custom dataset that I created and I'm writing the data from a CSV, I use PyTorch's datapipe which will essentially house the transformed, preprocessed data and wrap an iterable over it so that it can be used by PyTorch's DataLoader in the model. 
To preprocess the data I did the following: 
* Split the data into a training and validation set
* Tokenize the data (splitting text segments into a list of its individual words and punctuatoins)
* Created a vocabulary for both the modern english training data and Shakespearean training data.
* Created batches of text data that is then padded so that each text segment in the batch is equal to the longest segment in the batch.
* Converted the batches to tensors.

All of the above is wrapped into a dataloader which is then eventually used by the PyTorch model to read its training and validation data in. 


### [Exploratory Data Analysis](/shakespeare_translation_eda.ipynb) 
Within the exploratory data analysis, I perform a term frequency analysis and synthesize statistics regarding the data itself such as how long untranslated and translated text sequences are. 
The analysis can be found [here](/shakespeare_translation_eda.ipynb) 

### The Model 
The PyTorch model is an encoder-decoder architecture built upon 2-layer LSTM RNNs. The model is roughly 31,000,000 parameters. I use dropout to reduce overfitting. The model is inspired by the seminal 2014 paper from Sutskever et al. [Sequence to Sequence Learning with Neural Networks ](https://arxiv.org/abs/1409.3215) 

For training, because I do not have an NVIDIA GPU, I utilized Amazon Sagemaker's scriptmode which allows you to train a custom model by interfacing with their cloud backend and PyTorch containers. I trained on their NVIDIA T4 GPU for 100 EPOCHS taking around 8 hours with a learning rate of 0.01 and a batch size of 64.To use Sagemaker I had to change some of the code that I had written locally. This is why there is a folder called [aws_sagemaker_model_files](https://github.com/DiscoDoggy/shakespeare_translation/tree/main/aws_sagemaker_model_files) . Some of the main changes between the sagemaker model files and the local files I use are: 
* I created a small requirements.txt to have Sagemaker install any libraries that are not housed locally
* I split the model logic from the training and validation script since the training script is my EntryPoint script while the model is not.
* The entrypoint script contains a method to receieve hyperparameters and environment variables such as the cloud location of the training data and scripts
* Note: the Sagemaker Jupyter notebook I use to interface with Sagemaker is not included here 

[beautifulsoup-shield]: https://img.shields.io/badge/-BEAUTIFULSOUP-blue?style=for-the-badge
[beautifulsoup-url]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

