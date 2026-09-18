from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import AnalyzeRequest, AnalyzeResponse
from ain.Risk.Engine import evaluate_risk
from ain.model.inference import analyze_message as run_model
from ain.database.database import get_db
from ain.database.repository import (
    create_message,
    create_alert,
    get_parent_by_conversation,
    get_recent_alert_for_conversation,
)
from ain.notifications.n8n import send_alert_to_n8n


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
            # تأكد هل في Alert سابق لنفس المحادثة خلال آخر
            # ALERT_COOLDOWN_MINUTES دقايق. لازم نتأكد قبل ما
            # ننشئ الـ Alert الحالي، وإلا رح يلاقي نفسه.
            recent_alert = get_recent_alert_for_conversation(
                db=db,
                conversation_id=request.conversation_id,
                minutes=ALERT_COOLDOWN_MINUTES,
            )
            in_cooldown = recent_alert is not None

            # نخزّن الـ Alert دايمًا بالـ Database، حتى لو بفترة
            # الـ Cooldown - بس ما نبعت Email/n8n إلا إذا خرجنا
            # من فترة الانتظار.
            alert = create_alert(
                db=db,
                conversation_id=request.conversation_id,
                message_id=message.id,
                risk_score=risk_score,
                severity=severity,
            )

            if not in_cooldown:
                # 5. Find parent from database
                parent = get_parent_by_conversation(
                    db=db,
                    conversation_id=request.conversation_id,
                )

                if parent:
                    # 6. Send alert to n8n
                    n8n_data = {
                        "alert_id": alert.id,
                        "conversation_id": alert.conversation_id,
                        "message_id": alert.message_id,
                        "risk_score": alert.risk_score,
                        "severity": alert.severity,
                        "status": alert.status,
                        "parent_email": parent.email,
                        "parent_name": parent.name,
                    }

                    n8n_sent = send_alert_to_n8n(n8n_data)

                    # 7. Update n8n status
                    alert.n8n_sent = n8n_sent
                    db.commit()

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