import requests
import streamlit as st

from app.services.api_client import (
    APIClient,
    get_or_create_conversation_id,
)
from app.components.sidebar import render_sidebar


st.set_page_config(
    page_title="الاقتراحات والملاحظات",
    page_icon="💡",
    layout="centered",
)

render_sidebar()

# =========================
# Conversation ID
# =========================

conversation_id = get_or_create_conversation_id()

st.caption(f"معرّف الجلسة: `{conversation_id}`")

st.title("💡 الاقتراحات والملاحظات")

st.write(
    "نقدّر رأيك ومساهمتك في تطوير النظام."
)

st.divider()


# =========================
# Feedback type
# =========================

feedback_type = st.radio(
    "ماذا تريد أن ترسل؟",
    options=[
        "اقتراح",
        "ملاحظة",
        "الإبلاغ عن مشكلة",
    ],
    horizontal=True,
)


# =========================
# Message
# =========================

message = st.text_area(
    "رسالتك",
    placeholder="اكتب اقتراحك أو ملاحظتك هنا...",
    height=180,
)


# =========================
# Optional information
# =========================

name = st.text_input(
    "الاسم",
    placeholder="اختياري",
)

email = st.text_input(
    "البريد الإلكتروني",
    placeholder="اختياري",
)


st.divider()


# =========================
# Send button
# =========================

if st.button(
    "إرسال",
    type="primary",
    use_container_width=True,
):

    if not message.strip():

        st.error(
            "⚠️ يرجى كتابة الرسالة قبل الإرسال."
        )

    else:

        type_mapping = {
            "اقتراح": "suggestion",
            "ملاحظة": "note",
            "الإبلاغ عن مشكلة": "bug",
        }

        payload = {
            "conversation_id": conversation_id,
            "message": message.strip(),
            "feedback_type": type_mapping[feedback_type],
            "name": name.strip() or None,
            "email": email.strip() or None,
        }

        try:

            client = APIClient()

            response = client._request(
                "POST",
                "/api/v1/feedback",
                json=payload,
            )

            if response:

                st.success(
                    "✅ تم إرسال رسالتك بنجاح، "
                    "شكرًا لمساهمتك."
                )

                st.rerun()

        except requests.HTTPError as e:

            # =========================
            # Backend cooldown = HTTP 429
            # =========================

            if (
                e.response is not None
                and e.response.status_code == 429
            ):

                try:

                    detail = e.response.json().get(
                        "detail",
                        "يرجى الانتظار قبل إرسال "
                        "رسالة أخرى.",
                    )

                except Exception:

                    detail = (
                        "يرجى الانتظار قبل إرسال "
                        "رسالة أخرى."
                    )

                st.warning(
                    f"⏳ {detail}"
                )

            else:

                st.error(
                    "❌ حدث خطأ أثناء إرسال الرسالة. "
                    "حاول مرة أخرى."
                )

        except requests.RequestException:

            st.error(
                "❌ تعذر الاتصال بالخادم. "
                "حاول مرة أخرى."
            )

        except Exception:

            st.error(
                "❌ حدث خطأ غير متوقع. "
                "حاول مرة أخرى."
            )
