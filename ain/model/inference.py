"""
تحليل الرسائل عن طريق MARBERT.

الموديل ما بيتحمّل هون فور الـ import، لأنه هاد بيبطّئ أي عملية
بالمشروع بتعمل import للملف هاد (حتى لو ما رح تستخدم الموديل).
بدل هيك، بيتحمّل أول مرة حدا يستدعي analyze_message()، وبعدين
منخزّنه بالذاكرة (Cache) عشان ما نعيد تحميله كل مرة.
"""

import torch
from ain.model.loader import load_model

MAX_LENGTH = 128

# بنخزّن الموديل هون بعد أول تحميل، بدل ما نعيد تحميله كل استدعاء
_model = None
_tokenizer = None
_device = None


def _get_model():
    """
    بترجع (model, tokenizer, device).
    أول استدعاء بيحمّل الموديل فعليًا (وهاد بياخد وقت).
    أي استدعاء بعده بيرجع نفس النسخة المحمّلة من الذاكرة مباشرة.
    """
    global _model, _tokenizer, _device
    if _model is None:
        _model, _tokenizer, _device = load_model()
    return _model, _tokenizer, _device


def analyze_message(text: str) -> dict:
    model, tokenizer, device = _get_model()

    inputs = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)[0]
    safe_score = probs[0].item()   # index 0 = Safe
    risk_score = probs[1].item()   # index 1 = risky

    label = "risky" if risk_score > safe_score else "Safe"

    return {
        "label": label,
        "risk_score": round(risk_score, 4),
        "safe_score": round(safe_score, 4),
    }
