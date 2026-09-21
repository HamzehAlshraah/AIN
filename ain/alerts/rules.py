from typing import Final


HIGH_RISK_THRESHOLD: Final[float] = 0.75


def should_create_alert(severity: str) -> bool:
    """
    Return True when the risk severity requires an alert.
    """
    return severity.upper() == "HIGH"


def is_high_risk(risk_score: float) -> bool:
    """
    Return True when the risk score is at or above the HIGH threshold.
    """
    return risk_score >= HIGH_RISK_THRESHOLD