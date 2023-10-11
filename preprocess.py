import pandas as pd
from nltk.tokenize import word_tokenize

def preprocess_main():
    df = pd.read_csv("cleaned_data.csv")

    input_tokens, target_tokens = tokenize(df)

    for i in range(50):
        print(input_tokens[i])
        print(target_tokens[i])
        print('\n')
    
    return df

def tokenize(df):
    input_lang_tokens = []
    target_lang_tokens = []

    for i in range(len(df)):
        input_untokenized = df.iloc[i, 0]
        target_untokenized = df.iloc[i, 1]

        if type(input_untokenized) == float:
            input_untokenized = str(input_untokenized)
        if type(target_untokenized) == float:
            target_untokenized =  str(target_untokenized)

        input_tokenized = word_tokenize(input_untokenized)
        target_tokenized = word_tokenize(target_untokenized)

        input_tokenized.append("<eos>")
        target_tokenized.append("<eos>")

        input_lang_tokens.append(input_tokenized)
        target_lang_tokens.append(target_tokenized)

    return input_lang_tokens, target_lang_tokens 