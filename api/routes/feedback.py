from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import FeedbackCreateRequest, FeedbackResponse
from ain.database.database import get_db
from ain.database.repository import create_feedback
from ain.notifications.n8n import send_feedback_to_n8n


router = APIRouter(
    prefix="/api/v1",
    tags=["Feedback"],
)


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(
    request: FeedbackCreateRequest,
    db: Session = Depends(get_db),
):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Feedback message cannot be empty.",
        )

    feedback = create_feedback(
        db=db,
        message=request.message.strip(),
        feedback_type=request.feedback_type,
        name=request.name.strip() if request.name else None,
        email=request.email.strip() if request.email else None,
    )

    feedback_data = {
        "feedback_id": feedback.id,
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

    send_feedback_to_n8n(feedback_data)

    return feedback