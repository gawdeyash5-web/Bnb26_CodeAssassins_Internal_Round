"""Tests for the Re:Learn FastAPI backend service."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_api_health():
    """Verify health endpoint returns ready status and dataset metrics."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["dataset_samples"] >= 70


def test_api_questions():
    """Verify questions endpoint returns conceptual physics scenarios."""
    response = client.get("/api/questions")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)
    assert len(questions) > 0
    assert "question" in questions[0]
    assert "correct_answer" in questions[0]


def test_api_taxonomy():
    """Verify taxonomy endpoint returns misconception definitions."""
    response = client.get("/api/taxonomy")
    assert response.status_code == 200
    taxonomy = response.json()
    assert isinstance(taxonomy, list)
    assert len(taxonomy) >= 5
    ids = [item.get("misconception_id") for item in taxonomy]
    assert "M1" in ids


def test_api_diagnose_and_reassess_flow():
    """Verify complete end-to-end API learning loop: diagnose -> intervene -> reassess -> history."""
    learner = "test_api_student"

    # 1. Clean history
    client.delete(f"/api/history/{learner}")

    # 2. Diagnose initial misconception
    diag_payload = {
        "learner_id": learner,
        "question": "A hockey puck slides on ice after being hit. What keeps it moving?",
        "student_answer": "The force from the hit stays inside the puck making it glide forward."
    }
    diag_res = client.post("/api/diagnose", json=diag_payload)
    assert diag_res.status_code == 200
    diag_data = diag_res.json()

    assert "diagnosis" in diag_data
    assert "intervention" in diag_data
    assert "attempt" in diag_data

    attempt = diag_data["attempt"]
    assert attempt["learner_id"] == learner
    assert attempt["reassessment_completed"] is False

    # 3. Submit transfer reassessment
    reassess_payload = {
        "learner_id": learner,
        "attempt_index": 0,
        "reassessment_question": "A satellite drifts in deep space with engines off. Does it slow down?",
        "reassessment_answer": "No, without any external net force or friction, its velocity remains constant due to inertia.",
        "original_misconception": diag_data["diagnosis"]["misconception_label"]
    }
    reassess_res = client.post("/api/reassess", json=reassess_payload)
    assert reassess_res.status_code == 200
    reassess_data = reassess_res.json()

    assert reassess_data["outcome"] in ["improved", "persistent", "inconclusive"]
    assert reassess_data["attempt"]["reassessment_completed"] is True
    assert reassess_data["attempt"]["reassessment_answer"] != ""

    # 4. Check history: must have exactly 1 attempt (updated in place)
    hist_res = client.get(f"/api/history/{learner}")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) == 1
    assert history[0]["reassessment_completed"] is True
