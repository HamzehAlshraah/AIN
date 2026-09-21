import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ain.database.database import SessionLocal
from ain.database.repository import (
    create_message,
    create_alert,
    get_alert,
    get_messages_by_conversation,
    update_alert_status,
)


def test_create_and_get_alert():
    db = SessionLocal()

    try:
        message = create_message(
            db=db,
            conversation_id="pytest-db-001",
            text="Database test message",
            platform="test",
            risk_score=0.90,
            severity="HIGH",
        )

        alert = create_alert(
            db=db,
            conversation_id="pytest-db-001",
            message_id=message.id,
            risk_score=0.90,
            severity="HIGH",
        )

        db.commit()

        saved_alert = get_alert(db, alert.id)

        assert saved_alert is not None
        assert saved_alert.id == alert.id
        assert saved_alert.conversation_id == "pytest-db-001"
        assert saved_alert.severity == "HIGH"

    finally:
        db.close()


def test_update_alert_status():
    db = SessionLocal()

    try:
        message = create_message(
            db=db,
            conversation_id="pytest-db-002",
            text="Status test message",
            platform="test",
            risk_score=0.90,
            severity="HIGH",
        )

        alert = create_alert(
            db=db,
            conversation_id="pytest-db-002",
            message_id=message.id,
            risk_score=0.90,
            severity="HIGH",
        )

        db.commit()

        updated_alert = update_alert_status(
                                            db,
                                            alert,
                                            "REVIEWED",
                                        )

        assert updated_alert is not None
        assert updated_alert.status == "REVIEWED"
        assert updated_alert.reviewed_at is not None

    finally:
        db.close()


def test_get_messages_by_conversation():
    db = SessionLocal()

    try:
        create_message(
            db=db,
            conversation_id="pytest-db-003",
            text="First message",
            platform="test",
            risk_score=0.10,
            severity="SAFE",
        )

        create_message(
            db=db,
            conversation_id="pytest-db-003",
            text="Second message",
            platform="test",
            risk_score=0.80,
            severity="HIGH",
        )

        db.commit()

        messages = get_messages_by_conversation(
            db=db,
            conversation_id="pytest-db-003",
        )

        assert len(messages) >= 2
        assert all(
            message.conversation_id == "pytest-db-003"
            for message in messages
        )

    finally:
        db.close()