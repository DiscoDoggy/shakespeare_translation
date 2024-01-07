import torch
import sys

sys.path.append('/..')
from baseline_model import Encoder, Decoder, Seq2Seq 

def perform_inference(text_seg: str):
    #*load the model in

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
    model = torch.load("model.pth")
    model.eval()

    # output_segment_tensor = model(text_seg) #but like as a tensor



if __name__ == "__main__":
    pass
