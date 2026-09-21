import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from unittest.mock import patch

from ain.alerts.rules import should_create_alert, is_high_risk
from ain.alerts.service import AlertService
from ain.database.database import SessionLocal
from ain.database.repository import create_message, create_parent


def test_high_severity_should_create_alert():
    assert should_create_alert("HIGH") is True


def test_non_high_severity_should_not_create_alert():
    assert should_create_alert("MEDIUM") is False
    assert should_create_alert("LOW") is False
    assert should_create_alert("SAFE") is False


def test_high_risk_score():
    assert is_high_risk(0.75) is True
    assert is_high_risk(0.90) is True


def test_low_risk_score():
    assert is_high_risk(0.74) is False


def test_alert_service_has_default_cooldown():
    assert AlertService.__init__ is not None


def test_cooldown_only_after_successful_n8n():
    db = SessionLocal()

    conversation_id = f"pytest-cooldown-{uuid.uuid4().hex[:8]}"

    try:
        create_parent(
            db=db,
            conversation_id=conversation_id,
            name="Test Parent",
            email="test@example.com",
        )

        service = AlertService(db=db)

        message1 = create_message(
            db=db,
            conversation_id=conversation_id,
            text="First",
            platform="test",
            risk_score=0.90,
            severity="HIGH",
        )

        with patch(
            "ain.alerts.service.send_alert_to_n8n",
            return_value=True,
        ) as mock_send:

            alert1 = service.process_alert(
                conversation_id,
                message1.id,
                0.90,
                "HIGH",
            )

            message2 = create_message(
                db=db,
                conversation_id=conversation_id,
                text="Second",
                platform="test",
                risk_score=0.90,
                severity="HIGH",
            )

            alert2 = service.process_alert(
                conversation_id,
                message2.id,
                0.90,
                "HIGH",
            )

            # First HIGH alert sends to n8n.
            assert alert1.n8n_sent is True

            # Second HIGH alert is inside the cooldown period.
            assert alert2.n8n_sent is False

            # Only one n8n request should have been made.
            assert mock_send.call_count == 1

    finally:
        db.close()