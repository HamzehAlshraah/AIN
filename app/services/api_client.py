import os
import uuid

import requests
import streamlit as st


class APIClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (
            base_url
            or os.getenv("API_BASE_URL")
            or "http://localhost:8000"
        ).rstrip("/")

    def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ):
        url = f"{self.base_url}{path}"

        response = requests.request(
            method,
            url,
            timeout=10,
            **kwargs,
        )

        response.raise_for_status()
        return response.json()

    # =========================
    # Conversation
    # =========================

    def get_or_create_conversation_id(self) -> str:
        if "conversation_id" not in st.session_state:
            st.session_state["conversation_id"] = (
                f"streamlit-{uuid.uuid4().hex[:8]}"
            )

        return st.session_state["conversation_id"]

    # =========================
    # Analyze Message
    # =========================

    def analyze_message(
        self,
        text: str,
        conversation_id: str | None = None,
        platform: str | None = None,
    ):
        if conversation_id is None:
            conversation_id = self.get_or_create_conversation_id()

        payload = {
            "text": text,
            "conversation_id": conversation_id,
            "platform": platform,
        }

        return self._request(
            "POST",
            "/api/v1/analyze",
            json=payload,
        )

    # =========================
    # Parent
    # =========================

    def register_parent(
        self,
        conversation_id: str,
        email: str,
        name: str | None = None,
    ):
        payload = {
            "conversation_id": conversation_id,
            "name": name,
            "email": email,
        }

        return self._request(
            "POST",
            "/api/v1/parents",
            json=payload,
        )

    # =========================
    # Dashboard Summary
    # =========================

    def get_dashboard_summary(self):
        return self._request(
            "GET",
            "/api/v1/dashboard/summary",
        )

    # =========================
    # Alerts
    # =========================

    def get_alerts(self):
        return self._request(
            "GET",
            "/api/v1/alerts",
        )

    def get_alert(self, alert_id: int):
        return self._request(
            "GET",
            f"/api/v1/alerts/{alert_id}",
        )

    def update_alert(
        self,
        alert_id: int,
        status: str,
    ):
        payload = {
            "status": status,
        }

        return self._request(
            "PATCH",
            f"/api/v1/alerts/{alert_id}",
            json=payload,
        )

    # =========================
    # Conversation Messages
    # =========================

    def get_conversation_messages(
        self,
        conversation_id: str,
    ):
        return self._request(
            "GET",
            f"/api/v1/conversations/{conversation_id}/messages",
        )


# =========================
# Backward Compatibility
# =========================

def get_or_create_conversation_id() -> str:
    client = APIClient()
    return client.get_or_create_conversation_id()


def analyze_message(
    text: str,
    conversation_id: str | None = None,
    platform: str | None = None,
):
    client = APIClient()

    return client.analyze_message(
        text=text,
        conversation_id=conversation_id,
        platform=platform,
    )


def register_parent(
    conversation_id: str,
    email: str,
    name: str | None = None,
):
    client = APIClient()

    return client.register_parent(
        conversation_id=conversation_id,
        email=email,
        name=name,
    )