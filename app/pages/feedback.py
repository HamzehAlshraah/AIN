import requests
import streamlit as st

from app.services.api_client import APIClient


st.set_page_config(
    page_title="الاقتراحات والملاحظات",
    page_icon="💡",
    layout="centered",
)


st.title("💡 الاقتراحات والملاحظات")
st.write("نقدّر رأيك ومساهمتك في تطوير النظام.")


st.divider()


feedback_type = st.radio(
    "ماذا تريد أن ترسل؟",
    options=[
        "اقتراح",
        "ملاحظة",
        "الإبلاغ عن مشكلة",
    ],
    horizontal=True,
)


message = st.text_area(
    "رسالتك",
    placeholder="اكتب اقتراحك أو ملاحظتك هنا...",
    height=180,
)


name = st.text_input(
    "الاسم",
    placeholder="اختياري",
)


email = st.text_input(
    "البريد الإلكتروني",
    placeholder="اختياري",
)


st.divider()


if st.button("إرسال", type="primary", use_container_width=True):

    if not message.strip():
        st.error("⚠️ يرجى كتابة الرسالة قبل الإرسال.")

    else:

        type_mapping = {
            "اقتراح": "suggestion",
            "ملاحظة": "note",
            "الإبلاغ عن مشكلة": "bug",
        }

        payload = {
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
                    "✅ تم إرسال رسالتك بنجاح، شكرًا لمساهمتك."
                )

                st.session_state["feedback_sent"] = True

        except requests.RequestException:
            st.error(
                "❌ حدث خطأ أثناء إرسال الرسالة. حاول مرة أخرى."
            )

        except Exception:
            st.error(
                "❌ تعذر الاتصال بالخادم. حاول مرة أخرى."
            )