import pandas as pd
import re
from langdetect import detect_langs
from langdetect import DetectorFactory

#this function removes '�' from the dataset and replaces it with an empty string
def clean_unk_char_ws(data):
    """
    * Purpose: replaces the � character with empty string and 
        * Gets rid of trailing and leading whitespace
        * When reading in from CSV, littered with segments that have 3 spaces
        * Adjusted these 3 spaces to be a single space

    Parameters: Pandas Dataframe
    Returns: Clean Pandas Dataframe 
    """
    data = data.map(lambda text : re.sub('�',"", str(text))) #eliminates unk char

    data = data.map(lambda text : re.sub('   '," ", str(text))) #eliminates triple space

    data = data.map(lambda text : re.sub(r'\((.*)\)', "", str(text))) #eliminates text between and including parenthesis
    data = data.map(lambda text : re.sub(r'\[(.*)\]|\)', "", str(text))) #eliminates text between and including brackets

    data = data.map(lambda text : str(text).lstrip())
    data = data.map(lambda text : str(text).rstrip())

    #eliminating French having sentences
    data = remove_french(data)

    return data
    

def remove_french(data):
    eliminated_french = []
    DetectorFactory.seed = 0
    for i in range(len(df)):

        if re.search("[a-z]+", data.loc[i, "Untranslated Shakespeare"]):
            untranslated_phrase = data.loc[i, "Untranslated Shakespeare"]
            print(untranslated_phrase)

            detected_languages = detect_langs(untranslated_phrase)
            if "fr" in detected_languages:
                eliminated_french.append(data.loc[i, 'Untranslated Shakespeare'])
                data = data.drop(i)
        else:
            data = data.drop(i)

    print("FRENCH ELIMINATED:", eliminated_french)

    return data

df = pd.read_csv('shakespeare_and_translation_original_data.csv')
print(df['Translated Shakespeare'][40334])
df = clean_unk_char_ws(df)

for i in range(len(df['Translated Shakespeare'])):

    if '(' in df['Translated Shakespeare'][i]:
        print('hi'+df['Translated Shakespeare'][i])
        print(i)
print(df.duplicated())



