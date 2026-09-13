import sys
import os

# إضافة جذر المشروع لمسار البحث (نطلع مجلدين: pages/ -> app/ -> جذر المشروع)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from ain.model.inference import analyze_message
from ain.Risk.Engine import evaluate_risk
from components.risk_meter import render_risk_meter

st.set_page_config(page_title="Live Demo | AIN", page_icon="👁️", layout="wide")

st.title("👁️ AIN — Live Demo")

# ============================================================
# تهيئة سجل المحادثة والحالة الحالية بالذاكرة
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []          # كل الرسائل + نتائجها (للـ Dashboard لاحقاً)
if "current_risk" not in st.session_state:
    st.session_state.current_risk = 0.0
if "current_severity" not in st.session_state:
    st.session_state.current_severity = "SAFE"

# ============================================================
# تقسيم الشاشة: محادثة | مراقب خطورة
# ============================================================
col_chat, col_monitor = st.columns([2, 1])

with col_chat:
    st.subheader("Conversation")

    # عرض الرسائل السابقة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    # صندوق كتابة رسالة جديدة
    user_input = st.chat_input("اكتب رسالة هون...")

    if user_input:
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "text": user_input})

        # تحليل الرسالة بالموديل
        result = analyze_message(user_input)              # من inference.py
        risk_info = evaluate_risk(result["risk_score"])    # من engine.py

        # دمج النتيجتين وحفظهم بالسجل (يفيد الـ Dashboard لاحقاً)
        full_result = {**result, **risk_info, "text": user_input}
        st.session_state.messages[-1].update(full_result)

        # تحديث الحالة الحالية للمراقب
        st.session_state.current_risk = risk_info["risk_score"]
        st.session_state.current_severity = risk_info["severity"]

        st.rerun()

with col_monitor:
    st.subheader("AIN Risk Monitor")

    render_risk_meter(
        st.session_state.current_risk,
        st.session_state.current_severity
    )

    st.divider()

    st.markdown(f"**Risk Score:** {st.session_state.current_risk * 100:.0f}%")
    st.markdown(f"**Severity:** {st.session_state.current_severity}")

    # تنبيه واضح لو الرسالة الأخيرة كانت HIGH
    if st.session_state.current_severity == "HIGH":
        st.error("🚨 تم اكتشاف رسالة بمستوى خطورة مرتفع")
