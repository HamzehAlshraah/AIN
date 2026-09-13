from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = "HazmehAlshraah/marbert-risk-model"

ID2LABEL = {0: "Safe", 1: "risky"}
LABEL2ID = {"Safe": 0, "risky": 1}

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH,num_labels=2,
            id2label=ID2LABEL,label2id=LABEL2ID)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return model, tokenizer, device
