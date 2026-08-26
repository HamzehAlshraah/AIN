# -*- coding: utf-8 -*-
"""
تطبيق Streamlit - محادثة افتراضية لعرض موديل كشف الرسائل الخطرة
تشغيل: streamlit run app.py
"""

import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

st.set_page_config(page_title="عين - كشف الرسائل الخطرة", page_icon="👁️", layout="centered")

# ============================================================
# صفحة المعلومات الأولى (قبل بدء المحادثة)
# ============================================================
if "info_submitted" not in st.session_state:
    st.session_state.info_submitted = False

if not st.session_state.info_submitted:
    st.title("👁️ عين")
    st.caption("قبل ما نبلش، عبّي المعلومات التالية")

    with st.form("info_form"):
        contact_name = st.text_input("اسم الشخص اللي يحكي معه الابن *")
        contact_relation = st.selectbox(
            "صلة هذا الشخص بالطفل *",
            ["صديق مدرسة", "قريب/عائلة", "شخص غير معروف (غريب)", "تعرّف عليه أونلاين", "أخرى"]
        )
        platform = st.selectbox(
            "المنصة اللي فيها المحادثة *",
            ["واتساب", "انستغرام", "تيك توك", "سناب شات", "ماسنجر", "ديسكورد", "أخرى"]
        )
        father_name = st.text_input("اسم الأب/الأم (لغايات التنبيه) *")
        contact_method = st.radio("طريقة التواصل المفضلة للتنبيه *", ["إيميل", "تيليجرام"], horizontal=True)

        if contact_method == "إيميل":
            contact_value = st.text_input("الإيميل *", placeholder="name@example.com")
        else:
            contact_value = st.text_input("معرّف تيليجرام (Telegram ID) *", placeholder="@username")

        submitted = st.form_submit_button("ابدأ المراقبة")

        if submitted:
            if not contact_name.strip() or not father_name.strip() or not contact_value.strip():
                st.error("عبّي كل الحقول المطلوبة (*) قبل ما تكمل.")
            else:
                st.session_state.contact_name = contact_name
                st.session_state.contact_relation = contact_relation
                st.session_state.platform = platform
                st.session_state.father_name = father_name
                st.session_state.contact_method = contact_method
                st.session_state.contact_value = contact_value
                st.session_state.info_submitted = True
                st.rerun()

    st.stop()  # يمنع تحميل باقي الصفحة (الموديل + المحادثة) قبل تعبئة النموذج

# ============================================================
# تحميل الموديل (مرة وحدة بس، محفوظ بالذاكرة)
# ============================================================
@st.cache_resource
def load_model():
    model_path = "HazmehAlshraah/marbert-risk-model"  # ✅ من Hugging Face، مش مسار محلي
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return model, tokenizer, device

model, tokenizer, device = load_model()

# ============================================================
# دالة التصنيف
# ============================================================
def predict_risk(text):
    inputs = tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=-1).item()
    prob = torch.softmax(outputs.logits, dim=-1)[0][pred].item()
    label = "risky" if pred == 1 else "Safe"
    return label, prob

# ============================================================
# واجهة الصفحة
# ============================================================
st.title("👁️ عين")
st.caption("محادثة تجريبية — كل رسالة بتتفحص فوراً بموديل كشف الرسائل الخطرة")

with st.expander("📋 معلومات هذه الجلسة"):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**الشخص المتحدث:** {st.session_state.contact_name}")
        st.write(f"**الصلة:** {st.session_state.contact_relation}")
        st.write(f"**المنصة:** {st.session_state.platform}")
    with col2:
        st.write(f"**الأب/الأم:** {st.session_state.father_name}")
        st.write(f"**التنبيه عبر:** {st.session_state.contact_method}")
        st.write(f"**{st.session_state.contact_method}:** {st.session_state.contact_value}")

# تهيئة سجل المحادثة بالذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])
        if msg["role"] == "user":
            if msg["label"] == "risky":
                st.error(f"⚠️ رسالة مشبوهة (ثقة: {msg['confidence']:.1%})")
            else:
                st.success(f"✅ رسالة آمنة (ثقة: {msg['confidence']:.1%})")

# صندوق كتابة الرسالة الجديدة
user_input = st.chat_input("اكتب رسالة هون...")

if user_input:
    # تصنيف الرسالة
    label, confidence = predict_risk(user_input)

    # حفظ الرسالة بسجل المحادثة
    st.session_state.messages.append({
        "role": "user",
        "text": user_input,
        "label": label,
        "confidence": confidence
    })

    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.write(user_input)
        if label == "risky":
            st.error(f"⚠️ رسالة مشبوهة (ثقة: {confidence:.1%})")
        else:
            st.success(f"✅ رسالة آمنة (ثقة: {confidence:.1%})")

    # لو الرسالة خطرة، عين ترد بتنبيه تلقائي (محاكاة تنبيه الأهل)
    if label == "risky":
        with st.chat_message("assistant"):
            alert_text = "🔔 تم رصد رسالة مشبوهة وإرسال تنبيه للأهل."
            st.write(alert_text)
        st.session_state.messages.append({
            "role": "assistant",
            "text": alert_text,
            "label": "Safe",   # رد النظام نفسه ما بيحتاج تصنيف
            "confidence": 1.0
        })

# زر لتصفير المحادثة
with st.sidebar:
    st.header("عن المشروع")
    st.write("نظام يراقب الرسائل الموجهة للأطفال ويكتشف المحتوى الخطر باستخدام موديل MARBERTv2.")
    if st.button("🗑️ تصفير المحادثة"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 بدء جلسة جديدة (معلومات مختلفة)"):
        st.session_state.info_submitted = False
        st.session_state.messages = []
        st.rerun()
