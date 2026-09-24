import uuid

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def new_conversation_id():
    return f"test-{uuid.uuid4()}"


def test_feedback_first_submission():
    conversation_id = new_conversation_id()

    response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": conversation_id,
            "message": "This is my first feedback",
            "feedback_type": "suggestion",
            "name": "Test User",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["conversation_id"] == conversation_id
    assert data["message"] == "This is my first feedback"


def test_feedback_same_conversation_is_blocked():
    conversation_id = new_conversation_id()

    first_response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": conversation_id,
            "message": "First feedback",
            "feedback_type": "suggestion",
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": conversation_id,
            "message": "Second feedback",
            "feedback_type": "suggestion",
        },
    )

    assert second_response.status_code == 429


def test_feedback_different_conversation_is_allowed():
    first_conversation_id = new_conversation_id()
    second_conversation_id = new_conversation_id()

    first_response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": first_conversation_id,
            "message": "Feedback from user 1",
            "feedback_type": "suggestion",
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": second_conversation_id,
            "message": "Feedback from user 2",
            "feedback_type": "suggestion",
        },
    )

    assert second_response.status_code == 200


def test_feedback_empty_message_is_rejected():
    response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": new_conversation_id(),
            "message": "   ",
            "feedback_type": "suggestion",
        },
    )

    assert response.status_code == 400