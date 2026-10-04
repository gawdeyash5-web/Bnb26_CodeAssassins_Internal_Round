"""Tests for Diagnostic Fork and Misconception X-Ray backend functionality."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.data import (
    load_diagnostic_fork_bank,
    find_diagnostic_fork_question,
    get_diagnostic_fork_by_id
)
from src.learner import get_learner_history, clear_learner_history

client = TestClient(app)


def test_diagnostic_fork_bank_structure():
    """Verify diagnostic fork bank loads valid questions with candidate pairs and evidence mappings."""
    bank = load_diagnostic_fork_bank()
    assert len(bank) >= 5, "Bank should contain validated diagnostic discriminators"
    for item in bank:
        assert "question_id" in item
        assert "physics_concept" in item
        assert "candidate_misconceptions" in item
        assert len(item["candidate_misconceptions"]) >= 2
        assert "question" in item
        assert "choices" in item
        assert len(item["choices"]) >= 3
        for choice in item["choices"]:
            assert "choice_id" in choice
            assert "text" in choice
            assert "supported_misconception_id" in choice
            assert "evidence_type" in choice
            assert "diagnostic_interpretation" in choice


def test_find_diagnostic_fork_question():
    """Verify matching candidate misconceptions to specific discriminators."""
    # M1 and M2 discriminator
    q1 = find_diagnostic_fork_question(["M1", "M2"])
    assert q1 is not None
    assert q1["question_id"] == "DF-M1-M2"

    # M3 and M5 discriminator
    q2 = find_diagnostic_fork_question(["M3", "M5"])
    assert q2 is not None
    assert q2["question_id"] == "DF-M3-M5"

    # Non-existent pair should return None or fallback gracefully
    q_none = find_diagnostic_fork_question(["INVALID_A", "INVALID_B"])
    assert q_none is None


def test_diagnostic_fork_api_flow():
    """Verify the complete Diagnostic Fork workflow: diagnose -> fork evaluate -> intervention updated."""
    learner = "test_fork_student"
    client.delete(f"/api/history/{learner}")

    # 1. Run initial diagnosis with an ambiguous or low-confidence response
    diag_res = client.post("/api/diagnose", json={
        "learner_id": learner,
        "question": "An object moves at constant velocity. What forces act on it?",
        "student_answer": "It is moving so there could be a force pushing it or the forces are zero and it stops."
    })
    assert diag_res.status_code == 200
    diag_data = diag_res.json()
    assert "diagnostic_fork" in diag_data

    fork_meta = diag_data["diagnostic_fork"]
    assert "eligible" in fork_meta

    attempt = diag_data["attempt"]
    attempt_idx = attempt["attempt_index"]
    assert attempt["learner_id"] == learner

    # 2. Evaluate Diagnostic Fork choice supporting M1
    fork_eval_res = client.post("/api/diagnostic-fork/evaluate", json={
        "learner_id": learner,
        "attempt_index": attempt_idx,
        "question_id": "DF-M1-M2",
        "selected_choice_id": "A"
    })
    assert fork_eval_res.status_code == 200
    fork_eval_data = fork_eval_res.json()

    assert fork_eval_data["refined_diagnosis"]["misconception_id"] == "M1"
    assert fork_eval_data["refined_diagnosis"]["status"] == "success"
    assert fork_eval_data["attempt"]["diagnostic_fork_used"] is True
    assert fork_eval_data["attempt"]["diagnostic_fork_selected_choice_id"] == "A"
    assert fork_eval_data["intervention"]["misconception_id"] == "M1"

    # 3. Check history: must have exactly 1 attempt (updated in place, NO duplicates)
    hist_res = client.get(f"/api/history/{learner}")
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) == 1
    assert history[0]["diagnostic_fork_used"] is True
    assert history[0]["misconception_id"] == "M1"


def test_diagnostic_fork_inconclusive_preserves_uncertainty():
    """Verify choosing an inconclusive option preserves uncertainty rather than forcing a false positive."""
    learner = "test_uncertain_student"
    client.delete(f"/api/history/{learner}")

    diag_res = client.post("/api/diagnose", json={
        "learner_id": learner,
        "question": "A satellite moves through space.",
        "student_answer": "I don't know why it keeps going."
    })
    assert diag_res.status_code == 200

    fork_eval_res = client.post("/api/diagnostic-fork/evaluate", json={
        "learner_id": learner,
        "attempt_index": 0,
        "question_id": "DF-M1-M2",
        "selected_choice_id": "D"  # Inconclusive option
    })
    assert fork_eval_res.status_code == 200
    data = fork_eval_res.json()
    assert data["refined_diagnosis"]["status"] == "uncertain"
    assert data["attempt"]["diagnostic_fork_status"] == "inconclusive"


def test_diagnostic_fork_error_handling():
    """Verify invalid question ID and invalid choice ID yield proper HTTP errors."""
    learner = "test_err_student"

    # Invalid question ID
    res1 = client.post("/api/diagnostic-fork/evaluate", json={
        "learner_id": learner,
        "attempt_index": 0,
        "question_id": "NON_EXISTENT_QUESTION",
        "selected_choice_id": "A"
    })
    assert res1.status_code == 404

    # Invalid choice ID
    res2 = client.post("/api/diagnostic-fork/evaluate", json={
        "learner_id": learner,
        "attempt_index": 0,
        "question_id": "DF-M1-M2",
        "selected_choice_id": "Z"
    })
    assert res2.status_code == 400


def test_xray_attempt_retrieval():
    """Verify specific attempt record contains all 5 sequential stages for Misconception X-Ray."""
    learner = "test_xray_student"
    client.delete(f"/api/history/{learner}")

    # Step 1: Diagnose
    diag_res = client.post("/api/diagnose", json={
        "learner_id": learner,
        "question": "A 1000 kg car cruises at steady 20 m/s. What is the net force?",
        "student_answer": "The net force is 500 N because motion always requires a force."
    })
    assert diag_res.status_code == 200

    # Step 2: Diagnostic Fork
    client.post("/api/diagnostic-fork/evaluate", json={
        "learner_id": learner,
        "attempt_index": 0,
        "question_id": "DF-M1-NONE",
        "selected_choice_id": "A"
    })

    # Step 3: Reassessment
    client.post("/api/reassess", json={
        "learner_id": learner,
        "attempt_index": 0,
        "reassessment_question": "A comet drifts in deep space. Is any force needed?",
        "reassessment_answer": "No force is needed because inertia maintains constant velocity without friction.",
        "original_misconception": "impetus_force_persistence"
    })

    # Fetch attempt for X-Ray
    res = client.get(f"/api/attempts/{learner}/0")
    assert res.status_code == 200
    attempt = res.json()

    # Stage A: Initial Reasoning
    assert attempt["question"] != ""
    assert attempt["student_answer"] != ""
    assert "initial_misconception_label" in attempt
    assert "initial_confidence_score" in attempt

    # Stage B: Diagnostic Fork
    assert attempt["diagnostic_fork_used"] is True
    assert attempt["diagnostic_fork_question"] is not None
    assert attempt["diagnostic_fork_selected_choice_id"] == "A"
    assert attempt["diagnostic_fork_explanation"] is not None

    # Stage C: Targeted Intervention
    assert attempt["intervention_title"] != ""
    assert attempt["intervention_summary"] != ""

    # Stage D: Transfer Reassessment
    assert attempt["reassessment_completed"] is True
    assert attempt["reassessment_question"] != ""
    assert attempt["reassessment_answer"] != ""

    # Stage E: Observed Outcome
    assert attempt["reassessment_outcome"] in ["improved", "persistent", "inconclusive"]
    assert attempt["reassessment_feedback"] != ""
