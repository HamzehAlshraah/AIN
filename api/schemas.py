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
