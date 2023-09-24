import pandas as pd
import re

#this function removes '�' from the dataset and replaces it with an empty string
def clean_unk_char_ws(data):
    """
    * Purpose: replaces the � character with empty string and 
    * gets rid of trailing and leading whitespace

    Parameters: Pandas Dataframe
    Returns: Cleaned Pandas Dataframe 
    """
    data = data.map(lambda text : re.sub('�',"", str(text)))
    
    data = data.map(lambda text : str(text).lstrip())
    data = data.map(lambda text : str(text).rstrip())

    return data

df = pd.read_csv('shakespeare_and_translation_original_data.csv')
df = clean_unk_char_ws(df)

for i in range(20):
    print('hi'+df['Untranslated Shakespeare'][i])
