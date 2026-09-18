import streamlit as st
from services.api_client import get_dashboard_summary, get_alerts

st.set_page_config(page_title="Dashboard | AIN", page_icon="📊", layout="wide")

st.title("📊 AIN Dashboard")

try:
    summary = get_dashboard_summary()
    alerts = get_alerts()
except Exception as e:
    st.error(f"تعذّر الاتصال بالـ API: {e}")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Messages Analyzed", summary["messages_analyzed"])
col2.metric("Risk Events", summary["risk_events"])
col3.metric("High Risk Alerts", summary["high_risk_events"])
col4.metric("Highest Risk", f"{summary['highest_risk_score'] * 100:.0f}%")

st.divider()
st.subheader("آخر التنبيهات (Alerts)")

if not alerts:
    st.info("لا توجد تنبيهات بعد.")
else:
    table_data = [
        {
            "ID": a["id"],
            "Conversation": a["conversation_id"],
            "Risk": f"{a['risk_score'] * 100:.0f}%",
            "Severity": a["severity"],
            "Status": a["status"],
            "Email Sent": "✅" if a["n8n_sent"] else "❌",
            "Created At": a["created_at"],
        }
        for a in alerts
    ]
    st.dataframe(table_data, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("تطور مستوى الخطورة (آخر التنبيهات)")
    risk_series = [a["risk_score"] * 100 for a in reversed(alerts)]
    st.line_chart(risk_series)