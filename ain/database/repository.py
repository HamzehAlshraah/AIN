from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ain.database.models import Alert, Feedback, Message, Parent


def create_message(
    db: Session,
    conversation_id: str,
    text: str,
    platform: str | None,
    risk_score: float,
    severity: str,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        text=text,
        platform=platform,
        risk_score=risk_score,
        severity=severity,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def create_alert(
    db: Session,
    conversation_id: str,
    message_id: int,
    risk_score: float,
    severity: str,
) -> Alert:
    alert = Alert(
        conversation_id=conversation_id,
        message_id=message_id,
        risk_score=risk_score,
        severity=severity,
        status="NEW",
        n8n_sent=False,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_alert(
    db: Session,
    alert_id: int,
) -> Alert | None:
    return db.get(Alert, alert_id)


def get_alerts(
    db: Session,
) -> list[Alert]:
    statement = (
        select(Alert)
        .order_by(Alert.created_at.desc())
    )

    return list(db.scalars(statement).all())


def update_alert_status(
    db: Session,
    alert: Alert,
    status: str,
) -> Alert:
    alert.status = status

    if status in {"REVIEWED", "DISMISSED"}:
        alert.reviewed_at = datetime.utcnow()
    else:
        alert.reviewed_at = None

    db.commit()
    db.refresh(alert)

    return alert


def get_recent_alert_for_conversation(
    db: Session,
    conversation_id: str,
    minutes: int = 5,
) -> Alert | None:
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)

    statement = (
        select(Alert)
        .where(
            Alert.conversation_id == conversation_id,
            Alert.created_at >= cutoff,
            Alert.n8n_sent.is_(True),
        )
        .order_by(Alert.created_at.desc())
    )

    return db.scalars(statement).first()


def get_messages_by_conversation(
    db: Session,
    conversation_id: str,
) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )

    return list(db.scalars(statement).all())


def create_feedback(
    db: Session,
    message: str,
    feedback_type: str = "suggestion",
    name: str | None = None,
    email: str | None = None,
) -> Feedback:
    feedback = Feedback(
        name=name,
        email=email,
        message=message,
        feedback_type=feedback_type,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


def get_parent_by_conversation(
    db: Session,
    conversation_id: str,
) -> Parent | None:
    statement = (
        select(Parent)
        .where(Parent.conversation_id == conversation_id)
    )

    return db.scalars(statement).first()


def create_parent(
    db: Session,
    conversation_id: str,
    email: str,
    name: str | None = None,
) -> Parent:
    parent = Parent(
        conversation_id=conversation_id,
        email=email,
        name=name,
    )

    db.add(parent)
    db.commit()
    db.refresh(parent)

    return parent


def count_messages(db: Session) -> int:
    return db.scalar(
        select(func.count(Message.id))
    ) or 0


def count_risk_events(
    db: Session,
) -> int:
    statement = select(
        func.count(Message.id)
    ).where(
        Message.severity != "SAFE"
    )

    return db.scalar(statement) or 0


def count_high_risk_events(
    db: Session,
) -> int:
    return db.scalar(
        select(func.count(Alert.id))
    ) or 0


def get_highest_risk_score(
    db: Session,
) -> float:
    result = db.scalar(
        select(func.max(Message.risk_score))
    )

    return result if result is not None else 0.0