import os
import uuid
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_or_create_conversation_id() -> str:
    """
    كل جلسة متصفح إلها conversation_id ثابت طول الجلسة،
    مشترك بين كل صفحات Streamlit (تسجيل ولي الأمر، Live Demo، Dashboard).
    """
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = f"streamlit-{uuid.uuid4().hex[:8]}"
    return st.session_state.conversation_id


def analyze_message(text: str, conversation_id: str, platform: str | None = None) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/api/v1/analyze",
        json={"text": text, "conversation_id": conversation_id, "platform": platform},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def register_parent(conversation_id: str, email: str, name: str | None = None) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/api/v1/parents",
        json={"conversation_id": conversation_id, "email": email, "name": name},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def get_dashboard_summary() -> dict:
    response = requests.get(f"{API_BASE_URL}/api/v1/dashboard/summary", timeout=10)
    response.raise_for_status()
    return response.json()


def get_alerts() -> list[dict]:
    response = requests.get(f"{API_BASE_URL}/api/v1/alerts", timeout=10)
    response.raise_for_status()
    return response.json()