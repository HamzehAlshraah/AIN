import torch
from ain.model.loader import load_model
model, tokenizer, device = load_model()
MAX_LENGTH = 128
def analyze_message(text: str) -> dict:
    inputs = tokenizer(text,
                      truncation=True,
                      padding="max_length",
                      max_length=MAX_LENGTH,
                      return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    safe_score = probs[0].item()   # index 0 = Safe
    risk_score = probs[1].item()   # index 1 = risky

    label = "risky" if risk_score > safe_score else "Safe"

    return {"label": label,
          "risk_score": round(risk_score, 4),
          "safe_score": round(safe_score, 4)}
