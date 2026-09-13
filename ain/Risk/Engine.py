SAFE_MAX = 0.30
LOW_MAX = 0.50
MEDIUM_MAX = 0.75
SEVERITY_LEVELS = { "SAFE": "🟢",
                    "LOW": "🟡",
                    "MEDIUM": "🟠",
                    "HIGH": "🔴"}

def get_severity(risk_score: float) -> str:
    if risk_score < SAFE_MAX:
        return "SAFE"
    elif risk_score < LOW_MAX:
        return "LOW"
    elif risk_score < MEDIUM_MAX:
        return "MEDIUM"
    else:
        return "HIGH"

def evaluate_risk(risk_score: float) -> dict:
    severity = get_severity(risk_score)
    should_alert = severity == "HIGH"
    return {
        "risk_score": round(risk_score, 4),
        "severity": severity,
        "should_alert": should_alert}
