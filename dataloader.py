from newPreprocess import preprocess_main
import torch
from torch.utils.data import DataLoader

def data_loader_main():
    NUM_ROWS = 50670

    train_dp, valid_dp, mod_eng_vocab, old_eng_vocab = preprocess_main()

    train_loader = DataLoader(dataset=train_dp)
    valid_loader = DataLoader(dataset=valid_dp)

    print('\n')
    show_some_data(train_loader)
    print('\n')
    show_some_data(valid_loader)

    return train_loader, valid_loader, mod_eng_vocab, old_eng_vocab

def show_some_data(loaded_data):
    first = next(iter(loaded_data))
    old_eng, mod_eng = first[0], first[1]
    print(f"Labels batch shape: {old_eng.size()}")
    print(f"Mod_eng batch shape: {mod_eng.size()}")
    print(f"{old_eng = }\n{mod_eng = }")
    
    #N_samples here is capturing the number of batches.
    #the actual number of elements is number of samples * batch_size
    n_sample = 0 
    for row in iter(loaded_data):
        n_sample += 1
    
    print(f"{n_sample = }")
