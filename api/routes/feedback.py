from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import FeedbackCreateRequest, FeedbackResponse
from ain.database.database import get_db
from ain.database.repository import create_feedback
from ain.database.models import Feedback
from ain.notifications.n8n import send_feedback_to_n8n


router = APIRouter(
    prefix="/api/v1",
    tags=["Feedback"],
)


COOLDOWN_SECONDS = 10 * 60  # 10 minutes


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(
    request: FeedbackCreateRequest,
    db: Session = Depends(get_db),
):
    # ========================================
    # Validate message
    # ========================================

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Feedback message cannot be empty.",
        )

    # ========================================
    # Check cooldown for THIS conversation only
    # ========================================

    cooldown_time = datetime.utcnow() - timedelta(
        seconds=COOLDOWN_SECONDS
    )

    latest_feedback = (
        db.query(Feedback)
        .filter(
            Feedback.conversation_id
            == request.conversation_id,
            Feedback.created_at >= cooldown_time,
        )
        .order_by(Feedback.created_at.desc())
        .first()
    )

    if latest_feedback:
        remaining_seconds = int(
            COOLDOWN_SECONDS
            - (
                datetime.utcnow()
                - latest_feedback.created_at
            ).total_seconds()
        )

        if remaining_seconds < 0:
            remaining_seconds = 0

        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        raise HTTPException(
            status_code=429,
            detail=(
                f"Please wait {minutes} minutes "
                f"and {seconds} seconds before "
                f"sending another feedback."
            ),
        )

    # ========================================
    # Create feedback
    # ========================================

    feedback = create_feedback(
        db=db,
        conversation_id=request.conversation_id,
        message=request.message.strip(),
        feedback_type=request.feedback_type,
        name=request.name.strip()
        if request.name
        else None,
        email=request.email.strip()
        if request.email
        else None,
    )

    # ========================================
    # Prepare n8n data
    # ========================================

    feedback_data = {
        "feedback_id": feedback.id,
        "conversation_id": feedback.conversation_id,
        "feedback_type": feedback.feedback_type,
        "message": feedback.message,
        "name": feedback.name or "",
        "email": feedback.email or "",
        "created_at": (
            feedback.created_at.isoformat()
            if feedback.created_at
            else ""
        ),
    }

    # ========================================
    # Send to n8n
    # ========================================

    send_feedback_to_n8n(feedback_data)

    return feedback

