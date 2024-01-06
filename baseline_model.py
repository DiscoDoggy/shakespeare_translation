import torch
import torch.nn as nn
import torch.optim as optim
from torch import Tensor
from typing import Tuple

from tqdm import tqdm

import random
import math
import time
from time import sleep


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
        

def baseline_model_main():
    #because of the use of datapipe bucket batch, each element in the dataloader
    #are batches and not individual text sequences
    global mod_eng_vocab
    train_loader, valid_loader, mod_eng_vocab, old_eng_vocab = data_loader_main()
    training_loader_iterator = iter(train_loader)
    valid_loader_iterator = iter(valid_loader)
    #Code attempts to make Pytorch model training and execution reproducible by setting seed
    SEED = 1234
    random.seed(SEED)
    torch.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(type(device))

    #Training 
    # __len__() → int[source]
    INPUT_DIM = len(mod_eng_vocab)
    OUTPUT_DIM = len(old_eng_vocab)
    ENC_EMB_DIM = 256
    DEC_EMB_DIM = 256
    HID_DIM = 512
    N_LAYERS = 2
    ENC_DROPOUT = 0.5
    DEC_DROPOUT = 0.5

    enc = Encoder(INPUT_DIM, ENC_EMB_DIM, HID_DIM, N_LAYERS, ENC_DROPOUT)
    dec = Decoder(OUTPUT_DIM, DEC_EMB_DIM, HID_DIM, N_LAYERS, DEC_DROPOUT)

    model = Seq2Seq(enc,dec,device).to(device)
    print(model.apply(init_weights))

    # print("INPUT DIM:", INPUT_DIM)
    # print("OUTPUT_DIM:", OUTPUT_DIM)
    # print(len(mod_eng_vocab))
    # print(len(old_eng_vocab))

    print(f"The model has {count_parameters(model):,} trainable parameters")

    optimizer = optim.Adam(model.parameters())

    PAD_IDX = old_eng_vocab.lookup_indices(["<pad>"])[0]
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)

    N_EPOCHS = 10
    CLIP = 1
    best_valid_loss = float('inf')

    for epoch in range(N_EPOCHS):
        start_time = time.time()

        train_loss = train(model, training_loader_iterator, optimizer, criterion, CLIP, device)
        valid_loss = evaluate(model, valid_loader_iterator, criterion)

        end_time = time.time()

        epoch_mins, epoch_secs = epoch_time(start_time, end_time)

        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), 'tut1-model.pt')

        print(f'Epoch: {epoch+1:02} | Time: {epoch_mins}m {epoch_secs}s')
        print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')

def train(model:nn.Module,
        training_loader,
        optimizer:optim.Adam, 
        criterion:nn.modules.loss.CrossEntropyLoss, 
        clip:float,
        DEVICE
        ):
    
    model.train()

    epoch_loss = 0

    for batch in tqdm(training_loader, total = 782):
    # for _, batch in tqdm(enumerate(training_loader, 0), unit="batch", total=len(training_loader)):
        sleep(0.01)
        src, tgt = batch[0], batch[1]

        # print(type(src))
        # print(type(tgt))
        # print("SOURCE TENSOR BEFORE SHAPE:", src.size())
        # print("TARGET TENSOR BEFORE SHAPE:", tgt.size())

        # tgt and src have dimensions
        # 1 x batch size x sequence length
        # The model does not like outer redundant dimension of 1
        # So we squeeze to get rid of that dimension
        #we then apply a transpose to create a sequence length x batch size tensor
        src = src.squeeze(0)
        tgt = tgt.squeeze(0)
        src = torch.t(src)
        tgt = torch.t(tgt)

        # print(type(src))
        # print(type(tgt))
        # print("SOURCE TENSOR SHAPE:", src.size())
        # print("TARGET TENSOR SHAPE:", tgt.size())

        # print_max_values_in_tensor(src,mod_eng_vocab)

        optimizer.zero_grad()
        output = model(src, tgt)

        output = output[1:].view(-1, output.shape[-1])
        tgt = tgt[1:].contiguous().view(-1)

        loss = criterion(output, tgt)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()

        epoch_loss += loss.item()

    return epoch_loss / len(training_loader)

def evaluate(model: nn.Module,
             valid_loader,
             criterion:nn.modules.loss.CrossEntropyLoss):
    model.eval()
    epoch_loss = 0

    with torch.no_grad():
        for batch in valid_loader:
            src = batch[0]
            tgt = batch[1]

            output = model(src,tgt,0)

            output = output[1:].view(-1, output.shape[-1])
            tgt = tgt[1:].view(-1)

            loss = criterion(output,tgt)
            epoch_loss += loss.item()
    return epoch_loss / len(valid_loader)

def init_weights(m:nn.Module):
    #intializes weights between -0.08 and 0.08 by sampling from a
    #unifrom distribution
    for name, param in m.named_parameters():
        nn.init.uniform_(param.data, -0.08, 0.08)

def count_parameters(model:nn.Module):
    #calculates the number of trainable parameters by calculating the total 
    #number of elemets with gradients in the model
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def epoch_time(start_time:int, end_time:int):
    
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    
    return elapsed_mins, elapsed_secs

def print_max_values_in_tensor(batch, vocab):
    # # columns = torch.split(batch, 1, dim=1)
    # for column in columns:
    #     print("AS INTEGERS:", column)
    for tens in batch:
        print("AS INTEGERS:", tens)



baseline_model_main()



