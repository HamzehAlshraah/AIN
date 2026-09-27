from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import (
    AlertResponse,
    AlertUpdateRequest,
    DashboardSummaryResponse,
    MessageResponse,
)
from ain.database.database import get_db
from ain.database.repository import (
    count_high_risk_events,
    count_messages,
    count_risk_events,
    get_alert,
    get_alerts,
    get_highest_risk_score,
    get_messages_by_conversation,
    update_alert_status,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Dashboard"],
)


@router.get(
    "/dashboard/summary",
    response_model=DashboardSummaryResponse,
)
def dashboard_summary(
    db: Session = Depends(get_db),
):
    return DashboardSummaryResponse(
        messages_analyzed=count_messages(db),
        risk_events=count_risk_events(db),
        high_risk_events=count_high_risk_events(db),
        highest_risk_score=get_highest_risk_score(db),
    )


@router.get(
    "/alerts",
    response_model=list[AlertResponse],
)
def list_alerts(
    db: Session = Depends(get_db),
):
    return get_alerts(db)


@router.get(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
def get_alert_details(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = get_alert(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found.",
        )

    return alert


@router.patch(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
def update_alert(
    alert_id: int,
    request: AlertUpdateRequest,
    db: Session = Depends(get_db),
):
    allowed_statuses = {
        "NEW",
        "REVIEWED",
        "DISMISSED",
    }

    if request.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. "
                "Use NEW, REVIEWED, or DISMISSED."
            ),
        )

    alert = get_alert(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found.",
        )

    return update_alert_status(
        db=db,
        alert=alert,
        status=request.status,
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    return get_messages_by_conversation(
        db=db,
        conversation_id=conversation_id,
    )
