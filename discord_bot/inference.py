import torch
import sys
import os
import regex as re

parent_directory = os.path.abspath('..')
parent_directory = parent_directory + "\shakespeare_project"
sys.path.append(parent_directory)

from newPreprocess import tokenize
from database import get_database
from baseline_model import Encoder, Decoder, Seq2Seq 

def perform_inference(text_seg: str, database_obj):
    """
    Essentially the main function for performing inference
    """
    model = load_model()

    mod_eng_col = database_obj['mod_eng_vocab']
    old_eng_col = database_obj['old_eng_vocab']

    message_as_nums = preprocess_text_seg(text_seg, mod_eng_col)
    message_as_str = convert_ints_to_text(message_as_nums, mod_eng_col)
    print(message_as_nums)
    print(message_as_str)

    # output_segment_tensor = model(text_seg) #but like as a tensor

def load_model():
    """
    Defines the encoder and decoder for the model and loads the parameters in returning the 
    model itself
    """

    #for now we are hard coding the vocab size but later we can get that info
    #from the MongoDB being used to store the vocabularies 
    INPUT_DIM = 18202 #len(MOD_ENG_VOCAB)
    OUTPUT_DIM = 24834 #len(OLD_ENG_VOCAB)
    ENC_EMB_DIM = 256
    DEC_EMB_DIM = 256
    HID_DIM = 512
    N_LAYERS = 2
    ENC_DROPOUT = 0.5
    DEC_DROPOUT = 0.5

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    enc = Encoder(INPUT_DIM, ENC_EMB_DIM, HID_DIM, N_LAYERS, ENC_DROPOUT)
    dec = Decoder(OUTPUT_DIM, DEC_EMB_DIM, HID_DIM, N_LAYERS, DEC_DROPOUT)
    model = Seq2Seq(enc,dec,device).to(device)
    model.load_state_dict(torch.load("discord_bot\model.pth", map_location=torch.device(device)))
    model.eval()

    return model

def preprocess_text_seg(text_seg:str, database_col):
    cleaned_text = clean_text_seg(text_seg)
    tokenized_seg = tokenize(cleaned_text)
    text_as_nums = convert_text_to_int(tokenized_seg, database_col)

    return text_as_nums

def convert_text_to_int(tokenized_seg, database_col):
    text_as_nums = []

    for token in tokenized_seg:
        
        query = {"token":f"{token}"} #returns the whole document object
        query_result = database_col.find_one(query)
        token_id = query_result['_id']
        text_as_nums.append(token_id)

    return text_as_nums

def convert_ints_to_text(ints_seg, database_col):
    text_as_ints = []

    for digit in ints_seg:

        query = {"_id": digit}
        query_result = database_col.find_one(query)
        int_as_string = query_result['token']
        text_as_ints.append(int_as_string)

    return text_as_ints

def clean_text_seg(text_seg:str):
    """
    Cleans message and prepares for tokenization by converting to lower case,
    putting spaces between all punctuation, and deleting any instances of extra spaces
    """
    punc_pattern = r'(\'|\.|,|\?|!|:|;|")'
    cleaned_text = text_seg.lower()
    cleaned_text = re.sub(punc_pattern, r" \1 ", cleaned_text)
    cleaned_text = re.sub('   ', " ", cleaned_text)
    cleaned_text = re.sub('  ', " ", cleaned_text)

    return cleaned_text


if __name__ == "__main__":
    perform_inference("in saying goodbye to my son, it's like i'm losing another husband.", get_database())
