import streamlit as st

from services.api_client import (
    get_alert,
    get_alerts,
    get_conversation_messages,
    get_dashboard_summary,
    update_alert,
)


st.set_page_config(
    page_title="Dashboard | AIN",
    page_icon="📊",
    layout="wide",
)


st.title("📊 AIN Parent Dashboard")


# =========================
# Load dashboard data
# =========================

try:
    summary = get_dashboard_summary()
    alerts = get_alerts()

except Exception as e:
    st.error(
        f"تعذّر الاتصال بالـ API: {e}"
    )
    st.stop()


# =========================
# Summary
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Messages Analyzed",
    summary["messages_analyzed"],
)

col2.metric(
    "Risk Events",
    summary["risk_events"],
)

col3.metric(
    "High Risk Alerts",
    summary["high_risk_events"],
)

col4.metric(
    "Highest Risk",
    f"{summary['highest_risk_score'] * 100:.0f}%",
)


st.divider()


# =========================
# Alerts
# =========================

st.subheader("🚨 Alerts")


if not alerts:
    st.info("لا توجد تنبيهات بعد.")

else:
    table_data = [
        {
            "ID": alert["id"],
            "Conversation": alert["conversation_id"],
            "Risk": f"{alert['risk_score'] * 100:.0f}%",
            "Severity": alert["severity"],
            "Status": alert["status"],
            "n8n": (
                "✅"
                if alert["n8n_sent"]
                else "❌"
            ),
            "Created At": alert["created_at"],
        }
        for alert in alerts
    ]

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )


    st.divider()


    # =========================
    # Select Alert
    # =========================

    alert_options = {
        (
            f"Alert #{alert['id']} — "
            f"{alert['severity']} — "
            f"{alert['risk_score'] * 100:.0f}%"
        ): alert["id"]
        for alert in alerts
    }

    selected_label = st.selectbox(
        "اختر Alert لعرض التفاصيل",
        list(alert_options.keys()),
    )

    selected_alert_id = alert_options[selected_label]


    try:
        selected_alert = get_alert(
            selected_alert_id
        )

    except Exception as e:
        st.error(
            f"تعذّر تحميل تفاصيل الـ Alert: {e}"
        )
        st.stop()


    # =========================
    # Alert Details
    # =========================

    st.subheader(
        f"🔎 Alert #{selected_alert['id']}"
    )

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.write(
            f"**Conversation ID:** "
            f"{selected_alert['conversation_id']}"
        )

        st.write(
            f"**Message ID:** "
            f"{selected_alert['message_id']}"
        )

        st.write(
            f"**Severity:** "
            f"{selected_alert['severity']}"
        )

        st.write(
            f"**Risk Score:** "
            f"{selected_alert['risk_score'] * 100:.2f}%"
        )

    with detail_col2:
        st.write(
            f"**Status:** "
            f"{selected_alert['status']}"
        )

        st.write(
            f"**n8n Sent:** "
            f"{'Yes' if selected_alert['n8n_sent'] else 'No'}"
        )

        st.write(
            f"**Created At:** "
            f"{selected_alert['created_at']}"
        )

        st.write(
            f"**Reviewed At:** "
            f"{selected_alert['reviewed_at'] or '-'}"
        )


    # =========================
    # Alert Actions
    # =========================

    st.subheader("⚙️ Alert Actions")

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.button(
            "✅ Mark as Reviewed",
            use_container_width=True,
        ):
            try:
                update_alert(
                    alert_id=selected_alert["id"],
                    status="REVIEWED",
                )

                st.success(
                    "تم تعليم الـ Alert كمُراجَع."
                )

                st.rerun()

            except Exception as e:
                st.error(
                    f"تعذّر تحديث الـ Alert: {e}"
                )


    with action_col2:
        if st.button(
            "🗑️ Dismiss Alert",
            use_container_width=True,
        ):
            try:
                update_alert(
                    alert_id=selected_alert["id"],
                    status="DISMISSED",
                )

                st.success(
                    "تم إغلاق الـ Alert."
                )

                st.rerun()

            except Exception as e:
                st.error(
                    f"تعذّر تحديث الـ Alert: {e}"
                )


    # =========================
    # Conversation Messages
    # =========================

    st.divider()

    st.subheader("💬 Conversation Messages")

    try:
        messages = get_conversation_messages(
            selected_alert["conversation_id"]
        )

    except Exception as e:
        st.error(
            f"تعذّر تحميل الرسائل: {e}"
        )
        messages = []


    if not messages:
        st.info(
            "لا توجد رسائل لهذه المحادثة."
        )

    else:
        for message in messages:
            with st.container():
                st.markdown(
                    f"**{message['severity']}** — "
                    f"Risk: "
                    f"{message['risk_score'] * 100:.2f}%"
                )

                st.write(
                    message["text"]
                )

                st.caption(
                    f"Platform: "
                    f"{message['platform'] or '-'} | "
                    f"Created: "
                    f"{message['created_at']}"
                )

                st.divider()


    # =========================
    # Risk Timeline
    # =========================

    st.subheader(
        "📈 Risk Timeline"
    )

    risk_series = [
        alert["risk_score"] * 100
        for alert in reversed(alerts)
    ]

    if risk_series:
        st.line_chart(
            risk_series
        )