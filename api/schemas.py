from pydantic import BaseModel
from typing import Optional
class AnalyzeRequest(BaseModel):
    text: str
    conversation_id: str
    platform: Optional[str] = None

class AnalyzeResponse(BaseModel):
    message_id: str
    conversation_id: str
    label: str
    risk_score: float
    safe_score: float
    severity: str
    should_alert: bool
class ParentCreateRequest(BaseModel):
    conversation_id: str
    email: str
    name: Optional[str] = None


class ParentResponse(BaseModel):
    id: int
    conversation_id: str
    email: str
    name: Optional[str] = None
from datetime import datetime


class DashboardSummaryResponse(BaseModel):
    messages_analyzed: int
    risk_events: int
    high_risk_events: int
    highest_risk_score: float


class AlertResponse(BaseModel):
    id: int
    conversation_id: str
    message_id: int
    risk_score: float
    severity: str
    status: str
    n8n_sent: bool
    created_at: datetime
    reviewed_at: datetime | None = None

    class Config:
        from_attributes = True