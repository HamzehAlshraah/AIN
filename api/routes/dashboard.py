from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas import DashboardSummaryResponse, AlertResponse
from ain.database.database import get_db
from ain.database.repository import (
    count_messages,
    count_risk_events,
    count_high_risk_events,
    get_highest_risk_score,
    get_alerts,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Dashboard"],
)


@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(db: Session = Depends(get_db)):
    return DashboardSummaryResponse(
        messages_analyzed=count_messages(db),
        risk_events=count_risk_events(db),
        high_risk_events=count_high_risk_events(db),
        highest_risk_score=get_highest_risk_score(db),
    )


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(db: Session = Depends(get_db)):
    return get_alerts(db)