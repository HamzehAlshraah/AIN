from uuid import uuid4

from fastapi import APIRouter, HTTPException

from api.schemas import AnalyzeRequest, AnalyzeResponse
from ain.model.inference import analyze_message
from ain.Risk.Engine import evaluate_risk


router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"],
)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    try:
        result = analyze_message(request.text)
        risk_info = evaluate_risk(result["risk_score"])

        return {
            "message_id": str(uuid4()),
            "conversation_id": request.conversation_id,
            "label": result["label"],
            "risk_score": result["risk_score"],
            "safe_score": result["safe_score"],
            "severity": risk_info["severity"],
            "should_alert": risk_info["should_alert"],
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Message analysis failed.",
        )
