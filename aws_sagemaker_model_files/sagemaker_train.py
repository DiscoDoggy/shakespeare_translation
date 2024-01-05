import torch
import torch.nn as nn
import torch.optim as optim

import random
import math
import time

import os
import sys
import json
import argparse
import logging
import shutil

from dataloader import data_loader_main
from model import Encoder, Decoder, Seq2Seq


#AWS interaction code inspired by https://github.com/aws/amazon-sagemaker-examples/tree/main/sagemaker-script-mode/pytorch_script

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def parse_args():
    parser = argparse.ArgumentParser()

    #hyperparameteres sent by client passed as command line arguments
     # parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--epochs", type=int, default=1)

    #data directory locations (either local meaning notebook storage EC3? or on s3)
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))

    # Model directory: we will use the default set by SageMaker, /opt/ml/model
    parser.add_argument("--model_dir", type=str, default=os.environ.get("SM_MODEL_DIR"))

    return parser.parse_known_args()

def get_training_data(train_dir):
    filepath = os.path.join(train_dir, "train.csv")
    return filepath

def baseline_model_main():
    #because of the use of datapipe bucket batch, each element in the dataloader
    #are batches and not individual text sequences
    global mod_eng_vocab

    #get_training_data should return a file path to the s3 or sagemaker notebook data.csv location 
    #this file path gets passed into the data loader which then calls preprocess to load the data 
    #preprocess the data, batch and return everything to the dataloader which returns the training data
    #loader and a valid data loader along with vocabularies
    train_loader, valid_loader, mod_eng_vocab, old_eng_vocab = data_loader_main(get_training_data(args.train))
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

    print("INPUT DIM:", INPUT_DIM)
    print("OUTPUT_DIM:", OUTPUT_DIM)
    print(len(mod_eng_vocab))
    print(len(old_eng_vocab))

    print(f"The model has {count_parameters(model):,} trainable parameters")

    optimizer = optim.Adam(model.parameters(), lr = args.learning_rate)

    PAD_IDX = old_eng_vocab.lookup_indices(["<pad>"])[0]
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_IDX)

    N_EPOCHS = args.epochs
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
            curr_best_epoch = epoch

    # PyTorch requires that the inference script must
    # be in the .tar.gz model file and Step Functions SDK doesn't do this.
    
        logger.info(f'Epoch: {epoch+1:02} | Time: {epoch_mins}m {epoch_secs}s')
        logger.info(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
        logger.info(f'\tValidation Loss:{valid_loss: 3f} | Valid PPL:{math.exp(valid_loss):7.3f}')
        logger.info(f'Best validation loss: {valid_loss} | Best on Epoch: {curr_best_epoch}')

    torch.save(model.state_dict(), args.model_dir + "/model.pth")
    inference_code_path = args.model_dir + '/code/'
    
    if not os.path.exists(inference_code_path):
        os.mkdir(inference_code_path)
        logger.info("Created a folder at {}!".format(inference_code_path))

    shutil.copy("train_deploy_pytorch_without_dependencies.py", inference_code_path)
    shutil.copy("pytorch_model_def.py", inference_code_path)
    logger.info("Saving models files to {}".format(inference_code_path))

def train(model:nn.Module,
        training_loader,
        optimizer:optim.Adam, 
        criterion:nn.modules.loss.CrossEntropyLoss, 
        clip:float,
        DEVICE
        ):
    
    model.train()

    epoch_loss = 0

    for batch in training_loader:

        src, tgt = batch[0], batch[1]

        print(type(src))
        print(type(tgt))
        print("SOURCE TENSOR BEFORE SHAPE:", src.size())
        print("TARGET TENSOR BEFORE SHAPE:", tgt.size())

        # tgt and src have dimensions
        # 1 x batch size x sequence length
        # The model does not like outer redundant dimension of 1
        # So we squeeze to get rid of that dimension
        #we then apply a transpose to create a sequence length x batch size tensor
        src = src.squeeze(0)
        tgt = tgt.squeeze(0)
        src = torch.t(src)
        tgt = torch.t(tgt)

        print(type(src))
        print(type(tgt))
        print("SOURCE TENSOR SHAPE:", src.size())
        print("TARGET TENSOR SHAPE:", tgt.size())

        print_max_values_in_tensor(src,mod_eng_vocab)

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

if __name__ =='__main__':
    args, _ = parse_args()
    baseline_model_main()