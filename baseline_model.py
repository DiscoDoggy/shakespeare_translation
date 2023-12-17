import torch
import torch.nn as nn
import torch.optim as optim
from torch import Tensor
from typing import Tuple

import random
import math
import time

from dataloader import data_loader_main

class Encoder(nn.Module):
    def __init__(self, 
                 input_dim:int, 
                 emb_dim:int, 
                 hid_dim:int, 
                 n_layers:int, 
                 dropout:float):
        super().__init__()
        #intializing class variables 
        self.input_dim = input_dim
        self.emb_dim = emb_dim
        self.hid_dim = hid_dim
        self.n_layers = n_layers
        self.dropout = dropout

        #intializing layers
        self.embedding = nn.Embedding(input_dim, emb_dim)
        self.rnn = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src:Tensor) -> Tuple[Tensor,Tensor]:
        embedded = self.dropout(self.embedding(src))
        outputs, (hidden,cell) = self.rnn(embedded)
        return hidden, cell

class Decoder(nn.Module):
    def __init__(self, output_dim:int, 
                 emb_dim:int, 
                 hid_dim:int, 
                 n_layers:int, 
                 dropout:float):
        super().__init__()
        #intializing class variables
        self.emb_dim = emb_dim
        self.hid_dim = hid_dim
        self.output_dim = output_dim
        self.n_layers = n_layers
        self.dropout = dropout

        #intialzing layers
        self.embedding = nn.Embedding(output_dim, emb_dim)
        self.rnn = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout)
        self.out = nn.Linear(hid_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input:Tensor, hidden:Tensor,cell:Tensor)->Tuple[Tensor,Tensor,Tensor]:
        #input should become  1 x batch size
        input = input.unsqueeze(0)

        #embedded should be 1 x batch size x embeddding dim
        embedded = self.dropout(self.embedding(input))

        #output should be sent len x batchsize x hidden dim*directions
        #hidden is nlayers*numdirections x batch size x hid dim
        #cell is n layers * ndirections x batchsize x hidden dim

        output, (hidden,cell) = self.rnn(embedded,(hidden,cell))

        #prediction becomes batch size x hidden dim
        prediction = self.out(output.squeeze(0))

class 
        

def baseline_model_main():
    #because of the use of datapipe bucket batch, each element in the dataloader
    #are batches and not individual text sequences
    train_loader, valid_loader, mod_eng_vocab, old_eng_vocab = data_loader_main()

    #Code attempts to make Pytorch model training and execution reproducible by setting seed
    SEED = 1234
    random.seed(SEED)
    torch.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(type(device))





