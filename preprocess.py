import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.lm import Vocabulary
import torch
from torchtext.vocab import build_vocab_from_iterator

from collections import Counter
from itertools import chain

def preprocess_main():
    df = pd.read_csv("cleaned_data.csv")

    input_tokens, target_tokens = tokenize(df)

    for i in range(50):
        print(input_tokens[i])
        print(target_tokens[i])
        print('\n')


    input_vocab = create_vocab(input_tokens)
    target_vocab = create_vocab(input_tokens)

    # print(input_vocab[input_tokens[0]])
    # print(target_vocab[target_tokens[0]])
    
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


def create_vocab(dataset):

    def yield_tokens(data_iter):
        for text in data_iter:
            yield text
    
    vocab = build_vocab_from_iterator(yield_tokens(dataset), specials=["<unk>", "<pad>", "<eos>"])
    vocab.set_default_index(vocab["<unk>"])
    vocab.set_default_index(vocab["<pad>"])
    vocab.set_default_index(vocab["<eos>"])

    return vocab

def pad_and_truncate():
    """
    make it so it takes in one class of tokens
    """
    pass

    
