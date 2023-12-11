from nltk.tokenize import word_tokenize
import torch
import torchdata.datapipes as dp
from torchdata.datapipes.iter import IterDataPipe
from torchtext.vocab import build_vocab_from_iterator

def preprocess_main():
    # INPUT_FILE_PATH = 'cleaned_data_copy.csv'
    OUTPUT_FILE_PATH = 'cleaned_data_no_blanks.csv'

    data_pipe = dp.iter.IterableWrapper([OUTPUT_FILE_PATH])
    data_pipe = dp.iter.FileOpener(data_pipe, mode='rb')
    data_pipe = data_pipe.parse_csv(skip_lines=0, delimiter=',', as_tuple = True)

    print_data_pipe_sample(data_pipe, 30)
    

def print_data_pipe_sample(data_pipe, num_samples):
    cnt = 0

    for sample in data_pipe:
        if cnt == num_samples:
            break
        else:
            print(sample)
            cnt+=1

        

preprocess_main()