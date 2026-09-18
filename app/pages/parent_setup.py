import streamlit as st
import requests
from services.api_client import get_or_create_conversation_id, register_parent

st.set_page_config(page_title="Parent Setup | AIN", page_icon="✉️", layout="centered")
st.title("✉️ تسجيل ولي الأمر")

conversation_id = get_or_create_conversation_id()

st.info(f"معرّف الجلسة الحالية: `{conversation_id}`")

with st.form("register_parent_form"):
    email = st.text_input("إيميلك الشخصي (لاستلام التنبيهات)")
    name = st.text_input("اسمك (اختياري)")
    submitted = st.form_submit_button("سجّل")

if submitted:
    if not email.strip():
        st.error("لازم تدخل إيميل صحيح.")
    else:
        try:
            result = register_parent(conversation_id, email.strip(), name.strip() or None)
            st.success(f"تم التسجيل بنجاح! التنبيهات رح توصل إلى {result['email']}")
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 400:
                st.warning("إنت مسجّل أصلاً لهاي الجلسة.")
            else:
                st.error(f"صار خطأ: {e}")
        except Exception as e:
            st.error(f"تعذّر الاتصال بالـ API: {e}")

st.divider()
st.caption("لازم تسجّل إيميلك هون قبل ما تبلش محادثة بصفحة Live Demo، عشان توصلك التنبيهات.")