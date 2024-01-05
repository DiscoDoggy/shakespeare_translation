import torch
import torch.nn as nn
import torch.optim as optim
from torch import Tensor
from typing import Tuple

import random

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
        self.embedding = nn.Embedding(input_dim, emb_dim) #18202 x 256
        self.rnn = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src:Tensor) -> Tuple[Tensor,Tensor]:
        # print("Tensor shape:", src.size())
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

        return prediction,hidden,cell

class Seq2Seq(nn.Module):
    def __init__(self, 
                 encoder:nn.Module, 
                 decoder:nn.Module, 
                 device:torch.device):
        super().__init__()

        #initalizing class variables
        self.encoder = encoder
        self.decoder = decoder
        self.device = device

        assert encoder.hid_dim == decoder.hid_dim, \
            "Hidden dim of encoder and decoder need to be equal"
        assert encoder.n_layers == decoder.n_layers, \
            "Encoder and decoder need to maintain the same number of layers"
    
    def forward(self, src:Tensor, trg:Tensor, teacher_forcing_ratio: float = 0.75):
        #src = [src sent len x batch size]
        #trg = [trg sent len x batch size]

        batch_size = trg.shape[1]
        max_len = trg.shape[0]

        trg_vocab_size = self.decoder.output_dim

        #tensor storing decoder outputs
        outputs = torch.zeros(max_len, batch_size, trg_vocab_size).to(self.device)

        #last hidden state of encoder used as intial hidden state of deocder
        hidden, cell = self.encoder(src)

        #first input to the decoder is <sos>token
        input = trg[0,:]

        for i in range(1, max_len):
            output, hidden, cell = self.decoder(input, hidden, cell)
            outputs[i] = output
            teacher_force = random.random() < teacher_forcing_ratio
            top1 = output.max(1)[1]
            input = (trg[i] if teacher_force else top1)

        return outputs