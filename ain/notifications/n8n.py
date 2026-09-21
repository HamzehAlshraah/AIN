import os

from dotenv import load_dotenv
import requests

load_dotenv()


def send_alert_to_n8n(alert_data: dict) -> bool:
    webhook_url = os.getenv("N8N_WEBHOOK_URL")

    if not webhook_url:
        print("N8N_WEBHOOK_URL is not configured.")
        return False

    try:
        response = requests.post(
            webhook_url,
            json=alert_data,
            timeout=10,
        )

        response.raise_for_status()
        return True

    except requests.RequestException as exc:
        print(f"n8n request failed: {exc}")
        return False