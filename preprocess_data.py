import pandas as pd
import re

#this function removes '�' from the dataset and replaces it with an empty string
def clean_unk_char_ws(data):
    """
    * Purpose: replaces the � character with empty string and 
        * Gets rid of trailing and leading whitespace
        * When reading in from CSV, littered with segments that have 3 spaces
        * Adjusted these 3 spaces to be a single space

    Parameters: Pandas Dataframe
    Returns: Cleaned Pandas Dataframe 
    """
    data = data.map(lambda text : re.sub('�',"", str(text)))

    data = data.map(lambda text : re.sub('   '," ", str(text)))

    data = data.map(lambda text : str(text).lstrip())
    data = data.map(lambda text : str(text).rstrip())

    return data

df = pd.read_csv('shakespeare_and_translation_original_data.csv')
df = clean_unk_char_ws(df)

for i in range(20):
    print('hi'+df['Translated Shakespeare'][i])
# for char in df['Untranslated Shakespeare'][4]:
#     print(ord(char))


