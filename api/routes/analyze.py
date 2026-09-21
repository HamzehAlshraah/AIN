from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ain.alerts.service import AlertService
from api.schemas import AnalyzeRequest, AnalyzeResponse
from ain.Risk.Engine import evaluate_risk
from ain.model.inference import analyze_message as run_model
from ain.database.database import get_db
from ain.database.repository import (
    create_message,
)



router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"],
)

# الحد الأدنى بالدقايق بين إشعار وإشعار لنفس المحادثة.
# رقم ثابت هون عشان يسهل نغيّره لاحقًا (نقطة 12 بالخطة).
ALERT_COOLDOWN_MINUTES = 5


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(
    request: AnalyzeRequest,
    db: Session = Depends(get_db),
):
    # Validate input
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    try:
        # 1. Run MARBERT model
        result = run_model(request.text)

        # 2. Evaluate risk using Risk Engine
        risk_result = evaluate_risk(result["risk_score"])

        risk_score = result["risk_score"]
        safe_score = result["safe_score"]
        label = result["label"]
        severity = risk_result["severity"]
        should_alert = risk_result["should_alert"]

        # 3. Save message in database
        message = create_message(
            db=db,
            conversation_id=request.conversation_id,
            text=request.text,
            platform=request.platform,
            risk_score=risk_score,
            severity=severity,
        )

        # 4. Create alert if HIGH risk
        if should_alert:
            alert_service = AlertService(db=db)

            alert_service.process_alert(
                conversation_id=request.conversation_id,
                message_id=message.id,
                risk_score=risk_score,
                severity=severity,
            )

        # 8. Return API response
        return AnalyzeResponse(
            message_id=str(message.id),
            conversation_id=request.conversation_id,
            label=label,
            risk_score=risk_score,
            safe_score=safe_score,
            severity=severity,
            should_alert=should_alert,
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while analyzing the message.",
        )