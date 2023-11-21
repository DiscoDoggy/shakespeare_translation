import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.lm import Vocabulary
import torch
from torchtext.vocab import build_vocab_from_iterator
from sklearn.model_selection import train_test_split

from collections import Counter
from itertools import chain

def preprocess_main():
    df = pd.read_csv("cleaned_data.csv")

    input_tokens, target_tokens = tokenize(df)
    input_tokens = append_bos_tokens(input_tokens)
    target_tokens = append_bos_tokens(target_tokens)

    for i in range(10):
        print(input_tokens[i])
        print(target_tokens[i])
        print('\n')



    #for 50,000 samples 5% (0.05) is about 2500 samples for the test set and validation set
    #this  means 1250 for both the test set and validation set
    X_train, X_test, y_train, y_test = train_test_split(input_tokens, target_tokens, test_size=0.05, shuffle=True)

    X_test = append_eos(X_test)
    y_test = append_eos(y_test)

    X_test, X_valid, y_test, y_valid = train_test_split(X_test, y_test, test_size = 0.5)

    input_vocab = create_vocab(X_train)
    target_vocab = create_vocab(y_train)

    as_ints = input_vocab(X_train[0])
    print(as_ints)
    as_str = input_vocab.lookup_tokens(as_ints)
    print(as_str)
    

    print("X_Train[:10]", X_train[0])
    print("y_train[:10]", y_train[0])

    pad_trunc_X_train = pad_and_truncate(X_train)
    pad_trunc_y_train = pad_and_truncate(y_train)

    pad_trunc_X_train = append_eos(pad_trunc_X_train)
    pad_trunc_y_train = append_eos(pad_trunc_y_train)

    print('\n')

    for i in range(25):
        print(pad_trunc_X_train[i])

    
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

        # input_tokenized.append("<eos>")
        # target_tokenized.append("<eos>")

        input_lang_tokens.append(input_tokenized)
        target_lang_tokens.append(target_tokenized)

    return input_lang_tokens, target_lang_tokens 


def create_vocab(dataset):

    def yield_tokens(data_iter):
        for text in data_iter:
            yield text
    
    vocab = build_vocab_from_iterator(yield_tokens(dataset), specials=["<unk>", "<pad>", "<bos>" "<eos>"])
    vocab.set_default_index(vocab["<unk>"])
    vocab.set_default_index(vocab["<pad>"])
    vocab.set_default_index(vocab["<eos>"])

    return vocab

def append_bos_tokens(dataset):
    processed_dataset = []

    for seq in dataset:
        temp = ["<bos>"] + seq
        processed_dataset.append(temp)
    
    return processed_dataset

def append_eos(dataset):
    processed_dataset = []

    for seq in dataset:
        temp = seq + ['<eos>']
        processed_dataset.append(temp)
    
    return processed_dataset

def pad_and_truncate(training_input, max_steps=10):
    """

    """
    
    padded_truncated = []

    for seq in training_input:
        temp = seq
        
        if len(temp) < max_steps:
            while len(temp) < max_steps:
                temp.append("<pad>")
        elif len(temp) > max_steps:
            temp = temp[:max_steps]
        
        padded_truncated.append(temp)
    
    return padded_truncated