import sys
import os
import streamlit as st

from services.api_client import analyze_message, get_or_create_conversation_id
from components.risk_meter import render_risk_meter
from components.sidebar import render_sidebar


render_sidebar()

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)


st.set_page_config(
    page_title="التجربة المباشرة | AIN",
    page_icon="👁️",
    layout="wide",
)


st.title("👁️ AIN — التجربة المباشرة")


conversation_id = get_or_create_conversation_id()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_risk" not in st.session_state:
    st.session_state.current_risk = 0.0

if "current_severity" not in st.session_state:
    st.session_state.current_severity = "SAFE"


col_chat, col_monitor = st.columns([2, 1])


with col_chat:

    st.subheader("المحادثة")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    user_input = st.chat_input("اكتب رسالة هنا...")

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "text": user_input,
            }
        )

        try:
            result = analyze_message(
                text=user_input,
                conversation_id=conversation_id,
                platform="streamlit",
            )

        except Exception as e:
            st.error(f"تعذّر الاتصال بواجهة API: {e}")
            st.stop()

        st.session_state.messages[-1].update(result)

        st.session_state.current_risk = result["risk_score"]
        st.session_state.current_severity = result["severity"]

        st.rerun()


with col_monitor:

    st.subheader("مراقبة مستوى الخطورة")

    render_risk_meter(
        st.session_state.current_risk,
        st.session_state.current_severity,
    )

    st.divider()

    st.markdown(
        f"**نسبة الخطورة:** "
        f"{st.session_state.current_risk * 100:.0f}%"
    )

    severity_ar = {
        "HIGH": "مرتفع",
        "MEDIUM": "متوسط",
        "LOW": "منخفض",
        "SAFE": "آمن",
    }

    st.markdown(
        f"**مستوى الخطورة:** "
        f"{severity_ar.get(st.session_state.current_severity, st.session_state.current_severity)}"
    )

    if st.session_state.current_severity == "HIGH":
        st.error("🚨 تم اكتشاف رسالة بمستوى خطورة مرتفع")