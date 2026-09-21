import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "model" in data


def test_analyze_normal_message():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "مرحبا كيف الحال",
            "conversation_id": "pytest-normal-001",
            "platform": "test",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["conversation_id"] == "pytest-normal-001"
    assert "message_id" in data
    assert "label" in data
    assert "risk_score" in data
    assert "safe_score" in data
    assert "severity" in data
    assert "should_alert" in data


def test_analyze_high_risk_message():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": " تتصور ولا اذبحك",
            "conversation_id": "pytest-high-001",
            "platform": "test",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["severity"] == "HIGH"
    assert data["should_alert"] is True
    assert data["risk_score"] >= 0.75