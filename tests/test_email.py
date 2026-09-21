import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ain.notifications.n8n import send_alert_to_n8n


def test_n8n_returns_true_on_success():
    fake_response = type("Response", (), {
        "raise_for_status": lambda self: None
    })()

    with patch.dict(
        "os.environ",
        {"N8N_WEBHOOK_URL": "https://example.com/webhook"},
    ):
        with patch(
            "ain.notifications.n8n.requests.post",
            return_value=fake_response,
        ) as mock_post:

            result = send_alert_to_n8n({
                "alert_id": 1,
                "conversation_id": "test-001",
                "message_id": 1,
                "risk_score": 0.99,
                "severity": "HIGH",
            })

    assert result is True
    mock_post.assert_called_once()


def test_n8n_returns_false_when_url_missing():
    with patch.dict("os.environ", {}, clear=True):
        result = send_alert_to_n8n({
            "alert_id": 1,
            "conversation_id": "test-002",
            "message_id": 2,
            "risk_score": 0.99,
            "severity": "HIGH",
        })

    assert result is False


def test_n8n_returns_false_when_request_fails():
    with patch.dict(
        "os.environ",
        {"N8N_WEBHOOK_URL": "https://example.com/webhook"},
    ):
        with patch(
            "ain.notifications.n8n.requests.post",
            side_effect=__import__("requests").RequestException("Webhook failed"),
        ):
            result = send_alert_to_n8n({
                "alert_id": 1,
                "conversation_id": "test-003",
                "message_id": 3,
                "risk_score": 0.99,
                "severity": "HIGH",
            })

    assert result is False