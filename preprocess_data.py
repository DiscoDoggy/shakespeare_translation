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
    #data = remove_french(data)

    data = remove_unclosed_symbs(data)

    data = data.drop_duplicates()

    return data
    

def remove_french(data):
    eliminated_french = []
    DetectorFactory.seed = 0
    for i in range(len(data)):

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

def remove_unclosed_symbs(data):
    for i in range(len(data)):
        untranslated_cell = data.loc[i, "Untranslated Shakespeare"]
        translated_cell = data.loc[i, "Translated Shakespeare"]

        if ("(" in untranslated_cell) or ("(" in translated_cell) or ("[" in untranslated_cell) or ("[" in translated_cell):
            data = data.drop(i)
    
    return data

def check_unclosed_symbs(data):
    for i in range(len(data)):

        untranslated_cell = data.iloc[i, 0]
        translated_cell = data.iloc[i, 1]
        
        if '[' in untranslated_cell:
            print(untranslated_cell)
            print('\n')
        if '[' in translated_cell:
            print(translated_cell)
            print('\n')
        if '(' in untranslated_cell:
            print(untranslated_cell)
            print('\n')
        if '(' in translated_cell:
            print(translated_cell)
            print('\n')
        
def check_duplicate_rows(data):
    duplicates_rows = data.duplicated()
    duplicates_items = data.loc[duplicates_rows]

    if(len(duplicates_items) == 0):
        print("NO DUPLICATES FOUND")
    else:
        print(duplicates_items)


df = pd.read_csv('shakespeare_and_translation_original_data.csv')

df = clean_unk_char_ws(df)

check_unclosed_symbs(df)
check_duplicate_rows(df)



