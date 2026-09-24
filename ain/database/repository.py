from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ain.database.models import Alert, Feedback, Message, Parent


# =====================================================
# Messages
# =====================================================

def create_message(
    db: Session,
    conversation_id: str,
    text: str,
    risk_score: float,
    severity: str,
    platform: str | None = None,
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

def get_messages_by_conversation(
    db: Session,
    conversation_id: str,
):
    statement = (
        select(Message)
        .where(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.asc())
    )

    return list(
        db.scalars(statement).all()
    )


# =====================================================
# Alerts
# =====================================================

def create_alert(
    db: Session,
    conversation_id: str,
    message_id: int,
    risk_score: float,
    severity: str,
    n8n_sent: bool = False,
) -> Alert:

    alert = Alert(
        conversation_id=conversation_id,
        message_id=message_id,
        risk_score=risk_score,
        severity=severity,
        status="NEW",
        n8n_sent=n8n_sent,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_alert(
    db: Session,
    alert_id: int,
):
    return db.get(
        Alert,
        alert_id,
    )


def get_alerts(
    db: Session,
):
    statement = (
        select(Alert)
        .order_by(
            Alert.created_at.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def update_alert_status(
    db: Session,
    alert_id: int | Alert,
    status: str,
):

    if isinstance(alert_id, Alert):
        alert = alert_id
    else:
        alert = db.get(
            Alert,
            alert_id,
        )

    if alert is None:
        return None

    alert.status = status

    if status == "REVIEWED":
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
):
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)

    statement = (
        select(Alert)
        .where(
            Alert.conversation_id == conversation_id,
            Alert.n8n_sent.is_(True),
            Alert.created_at >= cutoff_time,
        )
        .order_by(
            Alert.created_at.desc()
        )
        .limit(1)
    )

    return db.scalars(
        statement
    ).first()


# =====================================================
# Risk History
# =====================================================

def get_risk_history(db: Session):

    statement = (
        select(
            Message.id,
            Message.conversation_id,
            Message.created_at,
            Message.risk_score,
            Message.severity,
        )
        .where(
            Message.conversation_id.in_(
                select(
                    Alert.conversation_id
                )
            )
        )
        .order_by(
            Message.created_at.asc()
        )
    )

    return list(
        db.execute(statement).all()
    )


# =====================================================
# Feedback
# =====================================================

def create_feedback(
    db: Session,
    conversation_id: str,
    message: str,
    feedback_type: str = "suggestion",
    name: str | None = None,
    email: str | None = None,
) -> Feedback:

    feedback = Feedback(
        conversation_id=conversation_id,
        name=name,
        email=email,
        message=message,
        feedback_type=feedback_type,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


# =====================================================
# Parent
# =====================================================

def get_parent_by_conversation(
    db: Session,
    conversation_id: str,
):

    statement = (
        select(Parent)
        .where(
            Parent.conversation_id
            == conversation_id
        )
    )

    return db.scalars(
        statement
    ).first()


def create_parent(
    db: Session,
    conversation_id: str,
    name: str,
    email: str,
):

    parent = Parent(
        conversation_id=conversation_id,
        name=name,
        email=email,
    )

    db.add(parent)
    db.commit()
    db.refresh(parent)

    return parent


# =====================================================
# Dashboard Statistics
# =====================================================

def count_messages(
    db: Session,
):

    statement = select(
        func.count(Message.id)
    )

    return db.scalar(
        statement
    ) or 0


def count_risk_events(
    db: Session,
):

    statement = select(
        func.count(Message.id)
    ).where(
        Message.risk_score >= 0.25
    )

    return db.scalar(
        statement
    ) or 0


def count_high_risk_events(
    db: Session,
):

    statement = select(
        func.count(Message.id)
    ).where(
        Message.risk_score >= 0.75
    )

    return db.scalar(
        statement
    ) or 0


def get_highest_risk_score(
    db: Session,
):

    statement = select(
        func.max(Message.risk_score)
    )

    return db.scalar(
        statement
    ) or 0