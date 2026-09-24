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
    get_risk_history,
    update_alert_status,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Dashboard"],
)


# =====================================================
# Dashboard Summary
# =====================================================

@router.get(
    "/dashboard/summary",
    response_model=DashboardSummaryResponse,
)
def dashboard_summary(
    db: Session = Depends(get_db),
):

    return {
        "messages_analyzed": count_messages(db),
        "risk_events": count_risk_events(db),
        "high_risk_events": count_high_risk_events(db),
        "highest_risk_score": get_highest_risk_score(db),
    }


# =====================================================
# Alerts
# =====================================================

@router.get(
    "/alerts",
    response_model=list[AlertResponse],
)
def dashboard_alerts(
    db: Session = Depends(get_db),
):

    return get_alerts(db)


# =====================================================
# Risk History
# =====================================================

@router.get(
    "/dashboard/risk-history",
)
def dashboard_risk_history(
    db: Session = Depends(get_db),
):

    rows = get_risk_history(db)

    return [
        {
            "id": row.id,
            "conversation_id": row.conversation_id,
            "created_at": row.created_at,
            "risk_score": row.risk_score,
            "severity": row.severity,
        }
        for row in rows
    ]


# =====================================================
# Single Alert
# =====================================================

@router.get(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
def dashboard_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):

    alert = get_alert(
        db,
        alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# =====================================================
# Update Alert Status
# =====================================================

@router.patch(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
def dashboard_update_alert(
    alert_id: int,
    payload: AlertUpdateRequest,
    db: Session = Depends(get_db),
):

    allowed_statuses = {
        "NEW",
        "REVIEWED",
        "DISMISSED",
    }

    if payload.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid alert status",
        )

    alert = update_alert_status(
        db,
        alert_id,
        payload.status,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# =====================================================
# Conversation Messages
# =====================================================

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
):

    return get_messages_by_conversation(
        db,
        conversation_id,
    )