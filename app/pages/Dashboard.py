import streamlit as st

import pandas as pd
from components.sidebar import render_sidebar

render_sidebar()
from app.services.api_client import APIClient


# =====================================================
# إعداد الصفحة
# =====================================================

st.set_page_config(
    page_title="لوحة تحكم AIN",
    page_icon="📊",
    layout="wide",
)


# =====================================================
# دوال الترجمة
# =====================================================

def translate_severity(severity):
    translations = {
        "HIGH": "مرتفع",
        "MEDIUM": "متوسط",
        "LOW": "منخفض",
        "SAFE": "آمن",
    }

    return translations.get(
        str(severity).upper(),
        str(severity),
    )


def translate_status(status):
    translations = {
        "NEW": "جديد",
        "REVIEWED": "تمت المراجعة",
        "DISMISSED": "تم التجاهل",
    }

    return translations.get(
        str(status).upper(),
        str(status),
    )


def risk_label(risk_score):
    if risk_score >= 0.75:
        return "مرتفع"

    if risk_score >= 0.50:
        return "متوسط"

    if risk_score >= 0.25:
        return "منخفض"

    return "آمن"


# =====================================================
# تنسيق الصفحة
# =====================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .dashboard-title {
        direction: rtl;
        text-align: right;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        direction: rtl;
        text-align: right;
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .metric-card {
        direction: rtl;
        text-align: right;
        padding: 20px;
        border-radius: 16px;
        background: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
        min-height: 120px;
    }

    .metric-title {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 12px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #111827;
    }

    .section-title {
        direction: rtl;
        text-align: right;
        font-size: 22px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# الاتصال بالـ API
# =====================================================

client = APIClient()


# =====================================================
# عنوان لوحة التحكم
# =====================================================

st.markdown(
    """
    <div class="dashboard-title">
        📊 لوحة تحكم AIN
    </div>

    <div class="dashboard-subtitle">
        متابعة الرسائل ومستويات الخطورة والتنبيهات الأمنية
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# جلب الملخص
# =====================================================

try:
    summary = client.get_dashboard_summary()

except Exception as exc:
    st.error(f"تعذر الاتصال بخادم AIN: {exc}")
    st.stop()


# =====================================================
# استخراج بيانات الملخص
# =====================================================

total_messages = summary.get("messages_analyzed", 0)
risk_events = summary.get("risk_events", 0)
high_risk_events = summary.get("high_risk_events", 0)

highest_risk = summary.get(
    "highest_risk_score",
    0,
)

if highest_risk is None:
    highest_risk = 0

highest_risk = float(highest_risk)


# =====================================================
# البطاقات الأربعة
# =====================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        label="الرسائل التي تم تحليلها",
        value=total_messages,
    )


with col2:
    st.metric(
        label="أحداث الخطورة",
        value=risk_events,
    )


with col3:
    st.metric(
        label="تنبيهات الخطورة العالية",
        value=high_risk_events,
    )


with col4:
    st.metric(
        label="أعلى مستوى للخطورة",
        value=f"{highest_risk * 100:.1f}%",
    )
    
# =====================================================
# جلب التنبيهات
# =====================================================

try:
    alerts = client.get_alerts()

except Exception as exc:
    st.error(f"تعذر تحميل التنبيهات: {exc}")
    alerts = []


# =====================================================
# مستوى الخطورة مع مرور الوقت
# =====================================================

st.markdown(
    """
    <div class="section-title">
        📈 مستوى الخطورة مع مرور الوقت
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# جلب جميع الرسائل من جميع المحادثات المرتبطة بالتنبيهات
# =====================================================

all_messages = []
seen_messages = set()


for alert in alerts:

    conversation_id = alert.get("conversation_id")

    if not conversation_id:
        continue

    try:
        conversation_messages = client.get_conversation_messages(
            conversation_id
        )

    except Exception:
        continue

    for message in conversation_messages:

        message_id = message.get("id")

        if message_id in seen_messages:
            continue

        seen_messages.add(message_id)

        all_messages.append(
            {
                "id": message_id,
                "conversation_id": conversation_id,
                "risk_score": message.get(
                    "risk_score",
                    0,
                ),
                "created_at": message.get(
                    "created_at",
                    "",
                ),
                "severity": message.get(
                    "severity",
                    "UNKNOWN",
                ),
            }
        )


# =====================================================
# ترتيب الرسائل حسب الوقت
# =====================================================

all_messages.sort(
    key=lambda message: message.get(
        "created_at",
        "",
    )
)


# =====================================================
# تجهيز بيانات الرسم
# =====================================================

chart_rows = []


for index, message in enumerate(
    all_messages,
    start=1,
):

    risk_score = float(
        message.get(
            "risk_score",
            0,
        )
    )

    chart_rows.append(
        {
            "الرسالة": index,
            "مستوى الخطورة (%)": risk_score * 100,
        }
    )


risk_df = pd.DataFrame(chart_rows)


# =====================================================
# عرض الرسم البياني
# =====================================================

if not risk_df.empty:

    st.line_chart(
        risk_df.set_index("الرسالة"),
        y="مستوى الخطورة (%)",
        width="stretch",
    )

else:

    st.info(
        "لا توجد رسائل كافية لعرض مستوى الخطورة مع مرور الوقت."
    )


# =====================================================
# HTML - دليل مستويات الخطورة
# =====================================================

st.html(
    """
    <div style="
        direction: rtl;
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 12px;
        margin: 15px 0 20px 0;
    ">

        <div style="
            padding: 8px 16px;
            border-radius: 20px;
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #b91c1c;
            font-weight: 700;
            white-space: nowrap;
        ">
            🔴 مرتفع — 75% فأعلى
        </div>

        <div style="
            padding: 8px 16px;
            border-radius: 20px;
            background: #fff7ed;
            border: 1px solid #fed7aa;
            color: #c2410c;
            font-weight: 700;
            white-space: nowrap;
        ">
            🟠 متوسط — 50% إلى 74%
        </div>

        <div style="
            padding: 8px 16px;
            border-radius: 20px;
            background: #fefce8;
            border: 1px solid #fde68a;
            color: #a16207;
            font-weight: 700;
            white-space: nowrap;
        ">
            🟡 منخفض — 25% إلى 49%
        </div>

        <div style="
            padding: 8px 16px;
            border-radius: 20px;
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #15803d;
            font-weight: 700;
            white-space: nowrap;
        ">
            🟢 آمن — أقل من 25%
        </div>

    </div>
    """
)


# =====================================================
# تحديد آخر مستوى خطورة فعلي
# =====================================================

if all_messages:

    latest_message = all_messages[-1]

    latest_ratio = float(
        latest_message.get(
            "risk_score",
            0,
        )
    )

    latest_risk = latest_ratio * 100

else:

    latest_ratio = highest_risk
    latest_risk = highest_risk * 100


# =====================================================
# HTML - مستوى الخطورة الحالي
# =====================================================

if latest_ratio >= 0.75:

    risk_title = "🔴 مستوى الخطورة: مرتفع"
    risk_description = "تم اكتشاف مستوى خطورة مرتفع."
    risk_color = "#b91c1c"
    risk_bg = "#fef2f2"
    risk_border = "#fecaca"

elif latest_ratio >= 0.50:

    risk_title = "🟠 مستوى الخطورة: متوسط"
    risk_description = "تم اكتشاف مستوى خطورة متوسط."
    risk_color = "#c2410c"
    risk_bg = "#fff7ed"
    risk_border = "#fed7aa"

elif latest_ratio >= 0.25:

    risk_title = "🟡 مستوى الخطورة: منخفض"
    risk_description = "تم اكتشاف مستوى خطورة منخفض."
    risk_color = "#a16207"
    risk_bg = "#fefce8"
    risk_border = "#fde68a"

else:

    risk_title = "🟢 مستوى الخطورة: آمن"
    risk_description = "لم يتم اكتشاف مستوى خطورة مرتفع."
    risk_color = "#15803d"
    risk_bg = "#f0fdf4"
    risk_border = "#bbf7d0"


st.html(
    f"""
    <div style="
        direction: rtl;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
        padding: 24px;
        margin: 15px 0 20px 0;
        border-radius: 18px;
        background: {risk_bg};
        border: 1px solid {risk_border};
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    ">

        <div style="
            font-size: 21px;
            font-weight: 800;
            color: {risk_color};
            margin-bottom: 8px;
        ">
            {risk_title}
        </div>

        <div style="
            font-size: 44px;
            font-weight: 800;
            color: {risk_color};
            line-height: 1.2;
            margin: 8px 0;
            direction: ltr;
        ">
            {latest_risk:.0f}%
        </div>

        <div style="
            font-size: 16px;
            font-weight: 500;
            color: #374151;
            margin-top: 8px;
        ">
            {risk_description}
        </div>

    </div>
    """
)


# =====================================================
# التنبيهات الأخيرة
# =====================================================

st.markdown(
    """
    <div class="section-title">
        🚨 التنبيهات الأخيرة
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# تجهيز جدول التنبيهات
# =====================================================

recent_alert_rows = []


for alert in alerts:

    recent_alert_rows.append(
        {
            "المحادثة": alert.get(
                "conversation_id",
                "-",
            ),
            "مستوى الخطورة": translate_severity(
                alert.get(
                    "severity",
                    "-",
                )
            ),
            "مستوى الخطورة (%)": (
                float(
                    alert.get(
                        "risk_score",
                        0,
                    )
                )
                * 100
            ),
            "الحالة": translate_status(
                alert.get(
                    "status",
                    "-",
                )
            ),
            "تم إرسال البريد": (
                "نعم"
                if alert.get(
                    "n8n_sent",
                    False,
                )
                else "لا"
            ),
        }
    )


# =====================================================
# عرض جدول التنبيهات
# =====================================================

if recent_alert_rows:

    recent_alert_df = pd.DataFrame(
        recent_alert_rows
    )

    recent_alert_df[
        "مستوى الخطورة (%)"
    ] = recent_alert_df[
        "مستوى الخطورة (%)"
    ].map(
        lambda value: f"{value:.1f}%"
    )

    st.dataframe(
        recent_alert_df,
        width="stretch",
        hide_index=True,
    )

else:

    st.info(
        "لا توجد تنبيهات حالياً."
    )


# =====================================================
# معلومات إضافية للتنبيهات
# =====================================================

if alerts:

    with st.expander(
        "🔎 عرض معلومات إضافية عن التنبيهات"
    ):

        additional_rows = []

        for alert in alerts:

            additional_rows.append(
                {
                    "رقم التنبيه": alert.get(
                        "id",
                        "-",
                    ),
                    "رقم الرسالة": alert.get(
                        "message_id",
                        "-",
                    ),
                    "تاريخ الإنشاء": alert.get(
                        "created_at",
                        "-",
                    ),
                }
            )

        additional_df = pd.DataFrame(
            additional_rows
        )

        st.dataframe(
            additional_df,
            width="stretch",
            hide_index=True,
        )


# =====================================================
# تفاصيل التنبيه
# =====================================================

st.markdown(
    """
    <div class="section-title">
        🔍 تفاصيل التنبيه
    </div>
    """,
    unsafe_allow_html=True,
)


if alerts:

    alert_options = []

    for alert in alerts:

        alert_id = alert.get(
            "id"
        )

        severity = translate_severity(
            alert.get(
                "severity",
                "-",
            )
        )

        risk = float(
            alert.get(
                "risk_score",
                0,
            )
        ) * 100

        alert_options.append(
            f"التنبيه #{alert_id} — {severity} — {risk:.1f}%"
        )


    selected_alert_label = st.selectbox(
        "اختر التنبيه",
        alert_options,
    )


    selected_index = alert_options.index(
        selected_alert_label
    )

    selected_alert = alerts[
        selected_index
    ]


    alert_id = selected_alert.get(
        "id"
    )


    # =================================================
    # جلب التفاصيل الكاملة للتنبيه
    # =================================================

    try:

        alert_details = client.get_alert(
            alert_id
        )

    except Exception:

        alert_details = selected_alert


    detail_col1, detail_col2, detail_col3 = st.columns(3)

    
    with detail_col1:
        risk_value = float(
            alert_details.get(
                "risk_score",
                0,
            )
        ) * 100

        st.metric(
            "مستوى الخطورة",
            f"{risk_value:.1f}%",
        )


    with detail_col2:

        st.metric(
            "مستوى الخطورة",
            translate_severity(
                alert_details.get(
                    "severity",
                    "-",
                )
            ),
        )


    with detail_col3:

        st.metric(
            "حالة التنبيه",
            translate_status(
                alert_details.get(
                    "status",
                    "-",
                )
            ),
        )


    # =================================================
    # معلومات التنبيه
    # =================================================

    st.markdown(
        """
        <div style="
            direction: rtl;
            text-align: right;
            margin-top: 20px;
            padding: 18px;
            border-radius: 14px;
            background: #f9fafb;
            border: 1px solid #e5e7eb;
        ">
            <strong>معلومات التنبيه</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


    info_col1, info_col2 = st.columns(2)


    with info_col1:

        st.write(
            f"**رقم التنبيه:** "
            f"{alert_details.get('id', '-')}"
        )

        st.write(
            f"**رقم الرسالة:** "
            f"{alert_details.get('message_id', '-')}"
        )

        st.write(
            f"**رقم المحادثة:** "
            f"{alert_details.get('conversation_id', '-')}"
        )


    with info_col2:

        st.write(
            f"**الحالة:** "
            f"{translate_status(alert_details.get('status', '-'))}"
        )

        st.write(
            f"**إرسال البريد:** "
            f"{'تم الإرسال' if alert_details.get('n8n_sent', False) else 'لم يتم الإرسال'}"
        )

        st.write(
            f"**تاريخ الإنشاء:** "
            f"{alert_details.get('created_at', '-')}"
        )


    # =================================================
    # الرسالة التي سببت التنبيه
    # =================================================

    st.markdown(
        """
        <div style="
            direction: rtl;
            text-align: right;
            margin-top: 25px;
            margin-bottom: 10px;
            font-size: 20px;
            font-weight: 800;
        ">
            💬 الرسالة التي سببت التنبيه
        </div>
        """,
        unsafe_allow_html=True,
    )


    conversation_id = alert_details.get(
        "conversation_id"
    )

    message_id = alert_details.get(
        "message_id"
    )

    triggering_message = None


    if conversation_id:

        try:

            conversation_messages = (
                client.get_conversation_messages(
                    conversation_id
                )
            )

            for message in conversation_messages:

                if message.get("id") == message_id:

                    triggering_message = message
                    break

        except Exception:
            triggering_message = None


    if triggering_message:

        st.markdown(
            f"""
            <div style="
                direction: rtl;
                text-align: right;
                padding: 20px;
                border-radius: 14px;
                background: #fff7ed;
                border: 1px solid #fed7aa;
                margin-bottom: 20px;
                line-height: 1.8;
            ">
                {triggering_message.get("text", "لا توجد رسالة")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "لم يتم العثور على نص الرسالة المرتبطة بهذا التنبيه."
        )


    # =================================================
    # أزرار تحديث حالة التنبيه
    # =================================================

    st.markdown(
        """
        <div style="
            direction: rtl;
            text-align: right;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 20px;
            font-weight: 800;
        ">
            ⚙️ إدارة التنبيه
        </div>
        """,
        unsafe_allow_html=True,
    )


    action_col1, action_col2, action_col3 = st.columns(3)


    with action_col1:

        if st.button(
            "🆕 وضع كتنبيه جديد",
            width="stretch",
        ):

            try:

                client.update_alert(
                    alert_id,
                    "NEW",
                )

                st.success(
                    "تم تحديث حالة التنبيه."
                )

                st.rerun()

            except Exception as exc:

                st.error(
                    f"حدث خطأ: {exc}"
                )


    with action_col2:

        if st.button(
            "✅ تمت المراجعة",
            width="stretch",
        ):

            try:

                client.update_alert(
                    alert_id,
                    "REVIEWED",
                )

                st.success(
                    "تمت مراجعة التنبيه."
                )

                st.rerun()

            except Exception as exc:

                st.error(
                    f"حدث خطأ: {exc}"
                )


    with action_col3:

        if st.button(
            "🚫 تجاهل التنبيه",
            width="stretch",
        ):

            try:

                client.update_alert(
                    alert_id,
                    "DISMISSED",
                )

                st.success(
                    "تم تجاهل التنبيه."
                )

                st.rerun()

            except Exception as exc:

                st.error(
                    f"حدث خطأ: {exc}"
                )


else:

    st.info(
        "لا توجد تنبيهات لعرض تفاصيلها."
    )
