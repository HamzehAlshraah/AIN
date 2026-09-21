from sqlalchemy.orm import Session

from ain.database.repository import (
    create_alert,
    get_parent_by_conversation,
    get_recent_alert_for_conversation,
)
from ain.notifications.n8n import send_alert_to_n8n
from ain.alerts.rules import should_create_alert


ALERT_COOLDOWN_MINUTES = 5


class AlertService:
    """
    Handles alert creation, cooldown checks, and n8n notification delivery.
    """

    def __init__(
        self,
        db: Session,
        cooldown_minutes: int = ALERT_COOLDOWN_MINUTES,
    ):
        self.db = db
        self.cooldown_minutes = cooldown_minutes

    def process_alert(
        self,
        conversation_id: str,
        message_id: int,
        risk_score: float,
        severity: str,
    ):
        """
        Create an alert when required and send it to n8n
        when the conversation is outside the cooldown period.

        Alerts are always stored in the database.
        Only successful n8n alerts start the cooldown period.
        """

        if not should_create_alert(severity):
            return None

        recent_alert = get_recent_alert_for_conversation(
            db=self.db,
            conversation_id=conversation_id,
            minutes=self.cooldown_minutes,
        )

        in_cooldown = recent_alert is not None

        alert = create_alert(
            db=self.db,
            conversation_id=conversation_id,
            message_id=message_id,
            risk_score=risk_score,
            severity=severity,
        )

        if not in_cooldown:
            parent = get_parent_by_conversation(
                db=self.db,
                conversation_id=conversation_id,
            )

            if parent:
                n8n_data = {
                    "alert_id": alert.id,
                    "conversation_id": alert.conversation_id,
                    "message_id": alert.message_id,
                    "risk_score": alert.risk_score,
                    "severity": alert.severity,
                    "status": alert.status,
                    "parent_email": parent.email,
                    "parent_name": parent.name,
                }

                alert.n8n_sent = send_alert_to_n8n(n8n_data)

        self.db.commit()

        return alert