# import sys
# import os
# sys.path.append('/..')
# print(os.listdir('.'))
# from database import get_database
# from newPreprocess import preprocess_main
# import torchtext.vocab

import torch
import sys
import os
parent_directory = os.path.abspath('..')
parent_directory = parent_directory + "\shakespeare_project"
sys.path.append(parent_directory)

from newPreprocess import preprocess_main
from database import get_database

def create_collections():
    """
    Gets the mongodb from get database and creates two collections: one for the modern english vocab
    and one for the old english vocab. Then proceeds to call get_tokens_to_id to get the vocab mappings and posts 
    the documents to the mongodb
    """
    dbname = get_database()
    mod_eng_collection = dbname['mod_eng_vocab']
    old_eng_collection = dbname['old_eng_vocab']

    _,_, mod_eng_vocab, old_eng_vocab = preprocess_main()
    mod_eng_doc_list = get_tokens_to_id(mod_eng_vocab)
    old_eng_doc_list = get_tokens_to_id(old_eng_vocab)

    mod_eng_collection.insert_many(mod_eng_doc_list)
    old_eng_collection.insert_many(old_eng_doc_list)


def get_tokens_to_id(lang_vocab):
    """
    loops through the vocab creating a id : token document and appending them to a list
    which is then returned
    """
    token_mapping = lang_vocab.get_stoi()
    token_doc_list = []

    for token in token_mapping:
        
        vocab_document = {
            "_id":token_mapping[token],
            "token":token
        }

        token_doc_list.append(vocab_document)

    return token_doc_list

if __name__ == "__main__":
    create_collections()

