from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import ParentCreateRequest, ParentResponse
from ain.database.database import get_db
from ain.database.repository import create_parent, get_parent_by_conversation


router = APIRouter(
    prefix="/api/v1",
    tags=["Parents"],
)


@router.post("/parents", response_model=ParentResponse)
def register_parent(
    request: ParentCreateRequest,
    db: Session = Depends(get_db),
):
    """
    تسجيل ولي أمر مرتبط بـ conversation_id معيّن.
    لازم يصير هاد قبل ما أي Alert يقدر يوصل عن طريق n8n،
    لأنه send_alert_to_n8n بحتاج parent.email.
    """
    existing = get_parent_by_conversation(db=db, conversation_id=request.conversation_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Parent already registered for this conversation_id.",
        )

    parent = create_parent(
        db=db,
        conversation_id=request.conversation_id,
        email=request.email,
        name=request.name,
    )

    return ParentResponse(
        id=parent.id,
        conversation_id=parent.conversation_id,
        email=parent.email,
        name=parent.name,
    )