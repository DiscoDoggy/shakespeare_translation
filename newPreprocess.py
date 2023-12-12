from nltk.tokenize import word_tokenize
import torch
import torchtext.transforms
from torchtext.transforms import VocabTransform
import torchdata.datapipes as dp
from torchdata.datapipes.iter import IterableWrapper
from torchtext.vocab import build_vocab_from_iterator

def preprocess_main():
    OUTPUT_FILE_PATH = 'cleaned_data_no_blanks.csv'

    data_pipe = dp.iter.IterableWrapper([OUTPUT_FILE_PATH])
    data_pipe = dp.iter.FileOpener(data_pipe, mode='rb')
    data_pipe = data_pipe.parse_csv(skip_lines=0, delimiter=',', as_tuple = True)

    print_data_pipe_sample(data_pipe,10)

    global mod_eng_vocab
    global old_eng_vocab
    mod_eng_vocab = build_vocabulary(data_pipe, 0)
    old_eng_vocab = build_vocabulary(data_pipe, 1)

    print(mod_eng_vocab.get_itos()[:9])
    print(old_eng_vocab.get_itos()[:9])

    print("\nTESTING TRANSFORMS:\n")
    for i in range(10):
        print_transforms_sample(data_pipe, mod_eng_vocab, 0, i)
        print_transforms_sample(data_pipe, old_eng_vocab, 1, i)
        print('\n')

    data_pipe = data_pipe.map(apply_transforms)
    # temp = list(data_pipe)
    # print(temp[:10])

    data_pipe = data_pipe.bucketbatch(
        batch_size=4, batch_num=5, bucket_num=1,
        use_in_batch_shuffle=False, sort_key = sort_bucket
    )

    data_pipe = data_pipe.map(separate_src_tgt)
    print(list(data_pipe)[1])

    data_pipe = data_pipe.map(apply_padding)

    print('\n')

    print_fully_processed_samples(data_pipe, mod_eng_vocab, old_eng_vocab, 5)

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

def apply_transforms(txt_seg_pair):
    return(
        build_transforms(mod_eng_vocab)(tokenize(txt_seg_pair[0])),
        build_transforms(old_eng_vocab)(tokenize(txt_seg_pair[1]))
    )

def sort_bucket(bucket):
    return sorted(bucket, key=lambda x: (len(x[0]), len(x[1])))

def separate_src_tgt(lang_pairs):
    """
    *Datapipe formats data as ((X1,Y1),...,(Xn,yn))
    *Want data to be formatted as (X1,X2,X3,...,Xn) and (y1,y2,...,yn)
    *and to be aligned
    """
    sources,targets = zip(*lang_pairs)
    return sources, targets

def apply_padding(sequence_pair):
    """
    *Converts each index in tuple to a tensor and adds padding
    *torchtext's ToTensor automatically adds padding and the 0
    *represents the index of the pad token in the overall vocabulary
    """
    return (torchtext.transforms.ToTensor(0)(list(sequence_pair[0])), 
            torchtext.transforms.ToTensor(0)(list(sequence_pair[1]))
    )

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

def print_fully_processed_samples(data_pipe, mod_eng_lex, old_eng_lex, num_samples):
    mod_eng_idx_to_str = mod_eng_lex.get_itos()
    old_eng_idx_to_str = old_eng_lex.get_itos()

    for srcs, tgts in data_pipe:
        if srcs[0][-1] != 0:
            continue
        for i in range(4):
            source = ""
            for token in srcs[i]:
                source += " " + mod_eng_idx_to_str[token]
            target = ""
            for token in tgts[i]:
                target += " " + old_eng_idx_to_str[token]
            print(f"Source: {source}")
            print(f"Target: {target}\n")
        break


preprocess_main()