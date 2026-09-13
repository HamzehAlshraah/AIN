import streamlit as st

st.set_page_config(page_title="Dashboard | AIN", page_icon="📊", layout="wide")

st.title("📊 AIN Dashboard")

messages = [m for m in st.session_state.get("messages", []) if "risk_score" in m]

if not messages:
    st.info("لا توجد رسائل محلّلة بعد. جرّب صفحة Live Demo أولاً.")
    st.stop()


total_messages = len(messages)
risk_events = sum(1 for m in messages if m["severity"] in ("MEDIUM", "HIGH"))
highest_risk = max(m["risk_score"] for m in messages)
current_status = messages[-1]["severity"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Messages Analyzed", total_messages)
col2.metric("Risk Events", risk_events)
col3.metric("Highest Risk", f"{highest_risk * 100:.0f}%")
col4.metric("Current Status", current_status)

st.divider()

st.subheader("سجل الرسائل")

table_data = [
    {
        "Message": m["text"],
        "Risk": f"{m['risk_score'] * 100:.0f}%",
        "Severity": m["severity"],
    }
    for m in messages
]
st.dataframe(table_data, use_container_width=True, hide_index=True)

st.divider()

st.subheader("تطور مستوى الخطورة")

risk_series = [m["risk_score"] * 100 for m in messages]
st.line_chart(risk_series)
