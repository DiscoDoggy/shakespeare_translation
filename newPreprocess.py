from nltk.tokenize import word_tokenize
import torch
import torchtext.transforms
from torchtext.transforms import VocabTransform
import torchdata.datapipes as dp
from torchdata.datapipes.iter import IterDataPipe
from torchtext.vocab import build_vocab_from_iterator

def preprocess_main():
    OUTPUT_FILE_PATH = 'cleaned_data_no_blanks.csv'

    data_pipe = dp.iter.IterableWrapper([OUTPUT_FILE_PATH])
    data_pipe = dp.iter.FileOpener(data_pipe, mode='rb')
    data_pipe = data_pipe.parse_csv(skip_lines=0, delimiter=',', as_tuple = True)

    print_data_pipe_sample(data_pipe, 30)

    mod_eng_vocab = build_vocabulary(data_pipe, 0)
    old_eng_vocab = build_vocabulary(data_pipe, 1)

    print(mod_eng_vocab.get_itos()[:9])
    print(old_eng_vocab.get_itos()[:9])

    print("\nTESTING TRANSFORMS:\n")
    for i in range(30):
        print_transforms_sample(data_pipe, mod_eng_vocab, 0, i)
        print_transforms_sample(data_pipe, old_eng_vocab, 1, i)
        print('\n')


def tokenize(txt_segment):
    segment = txt_segment

    if type(segment) == float:
        segment = str(segment)

    tokenized_segment = word_tokenize(segment)

    return tokenized_segment

def get_tokens(data_iter, place):
    for mod_eng, old_eng in data_iter:
        if place == 0:
            yield tokenize(mod_eng)
        else:
            yield tokenize(old_eng)

def build_vocabulary(data_iter, place):
    """
    When Place = 0, creating a mod english (input) vocab
    When Place = 1, creating a old english (target) vocab
    """
    
    source_vocab = build_vocab_from_iterator(
        get_tokens(data_iter, place),
        min_freq = 1,
        specials=["<pad>", "<bos>", "<eos>", "<unk>"],
        special_first = True
    )

    source_vocab.set_default_index(source_vocab['<unk>'])

    return source_vocab

def build_transforms(vocab):
    text_transform = torchtext.transforms.Sequential(
        VocabTransform(vocab=vocab),
        torchtext.transforms.AddToken(1,begin=True),
        torchtext.transforms.AddToken(2, begin=False)
    )

    return text_transform

def print_data_pipe_sample(data_pipe, num_samples):
    cnt = 0

    for sample in data_pipe:
        if cnt == num_samples:
            break
        else:
            print(sample)
            cnt+=1

def print_transforms_sample(datapipe, vocab, place, sentence_idx):
    for_index = list(datapipe)
    rand_sentence = for_index[sentence_idx][place]
    print("Sentence of interest =", rand_sentence)

    transformed_sentence = build_transforms(vocab)(tokenize(rand_sentence))
    print("Transformed Sentence =", transformed_sentence)

    index_to_string = vocab.get_itos()
    for index in transformed_sentence:
        print(index_to_string[index], end=' ')
        

preprocess_main()