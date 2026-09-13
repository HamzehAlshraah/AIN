import sys
import os

# إضافة جذر المشروع لمسار البحث عشان يشتغل import ain.* بغض النظر من وين شغّلنا الملف
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
col_1,col_2=st.columns(2)
with col_1:
    st.image("app/AIN logo.jpg")
with col_2:
    st.set_page_config(page_title="عين | AIN")

st.markdown(
    "<h1 style='text-align:center; font-size:64px;'>👁️ AIN</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:20px; color:#555;'>"
    "نظام ذكاء اصطناعي عربي للمساعدة في اكتشاف<br>"
    "الرسائل الخطرة الموجهة للأطفال"
    "</p>",
    unsafe_allow_html=True
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Accuracy", value="91.4%")

with col2:
    st.metric(label="Risk Recall", value="94%")

with col3:
    st.metric(label="Arabic Messages", value="22K+")

st.write("")
st.write("")

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("ابدأ تجربة AIN", use_container_width=True, type="primary"):
        st.switch_page("pages/live_demo.py")
