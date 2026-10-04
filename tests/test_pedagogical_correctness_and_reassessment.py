"""Tests for pedagogical correctness, non-placeholder reassessment, and honest outcomes in Re:Learn."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.assessment.evaluator import (
    evaluate_answer_correctness,
    get_transfer_reassessment_for_context,
    evaluate_reassessment_answer,
)
from src.interventions import get_intervention

client = TestClient(app)

STEEL_WOODEN_Q = (
    "A steel ball and a wooden ball of the same size are dropped together from a balcony. "
    "Air resistance is small. Which one hits the ground first?"
)


def test_clearly_correct_answer():
    """Verify that a clearly correct answer is assessed as 'correct' with canonical explanation."""
    correct_ans = (
        "They land at almost exactly the same time because all objects experience "
        "the same gravitational acceleration near Earth's surface when air resistance is small."
    )
    eval_res = evaluate_answer_correctness(STEEL_WOODEN_Q, correct_ans)
    assert eval_res["was_correct"] == "correct"
    assert eval_res["was_it_correct_display"] == "Correct"
    assert "Both balls reach the ground at approximately the same time" in eval_res["correct_answer"]
    assert "same downward acceleration" in eval_res["why_explanation"]

    # Also test via API
    res = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": correct_ans,
        "learner_id": "test_correct_learner"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["answer_evaluation"]["was_correct"] == "correct"
    assert "looks correct" in data["diagnosis"]["explanation"].lower()


def test_clearly_incorrect_answer():
    """Verify that a clearly incorrect answer is assessed as 'incorrect'."""
    steel_first_ans = "The steel ball hits the ground first because heavier objects fall faster."
    eval_res = evaluate_answer_correctness(STEEL_WOODEN_Q, steel_first_ans)
    assert eval_res["was_correct"] == "incorrect"
    assert eval_res["was_it_correct_display"] == "Incorrect"
    assert "steel ball would land first" in eval_res["why_explanation"]

    # Via API: should identify target misconception or incorrect
    res = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": steel_first_ans,
        "learner_id": "test_incorrect_learner"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["answer_evaluation"]["was_correct"] == "incorrect"


def test_incorrect_answer_with_uncertain_misconception():
    """Verify student answer 'I think the wooden ball hits the ground first' is recognized as incorrect

    and uncertain, never as 'sound reasoning'.
    """
    wooden_ans = "I think the wooden ball hits the ground first."
    eval_res = evaluate_answer_correctness(STEEL_WOODEN_Q, wooden_ans)
    assert eval_res["was_correct"] == "incorrect"
    assert "wooden ball would land first" in eval_res["why_explanation"]

    res = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": wooden_ans,
        "learner_id": "test_wooden_learner"
    })
    assert res.status_code == 200
    data = res.json()

    # Must NOT say sound physical reasoning
    assert "sound physical reasoning" not in data["diagnosis"]["explanation"].lower()
    assert "concept applied correctly" not in data["diagnosis"]["explanation"].lower()

    # Must explain uncertainty honestly
    assert "misunderstanding" in data["diagnosis"]["explanation"].lower()
    assert data["diagnosis"]["status"] == "uncertain"

    # Must offer Diagnostic Fork probe
    assert data["diagnostic_fork"]["eligible"] is True
    assert data["diagnostic_fork"]["question"] is not None


def test_low_confidence_none_prediction_not_treated_as_correct():
    """Verify that a low-confidence prediction of NONE is never treated as proof of correctness."""
    res = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": "I think the wooden ball hits the ground first.",
        "learner_id": "test_none_learner"
    })
    assert res.status_code == 200
    data = res.json()

    # Raw model may have predicted NONE with low confidence
    assert data["diagnosis"]["raw_confidence_score"] < 0.60
    # But student-facing diagnosis was overridden
    assert data["diagnosis"]["was_correct"] == "incorrect"
    assert data["diagnosis"]["status"] == "uncertain"


def test_missing_reassessment_question_handled():
    """Verify that get_transfer_reassessment returns None if question bank has no match and never returns a placeholder."""
    # Searching for a totally bogus context with empty bank
    res = get_transfer_reassessment_for_context("A non-existent fantasy question with dragons", "NON_EXISTENT_ID")
    # If something returned from fallback, must be an authentic physics question, never the placeholder string
    if res:
        assert "Ready to test your understanding on an advanced scenario?" not in res.get("question", "")

    # Ensure get_intervention never has the placeholder string
    interv = get_intervention("NONE")
    assert interv["reassessment_question"] != "Ready to test your understanding on an advanced scenario?"


def test_valid_reassessment_question_returned_for_steel_wooden():
    """Verify that a complete, authentic physics question is selected for the steel/wooden ball scenario."""
    transfer_q = get_transfer_reassessment_for_context(STEEL_WOODEN_Q, "")
    assert transfer_q is not None
    assert "vacuum" in transfer_q["question"].lower()
    assert "Ready to test your understanding" not in transfer_q["question"]
    assert transfer_q.get("reassessment_id") in ["R-M4-06", "R-M4-01"]

    # Via API response
    res = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": "I think the wooden ball hits the ground first.",
        "learner_id": "test_transfer_q_learner"
    })
    assert res.status_code == 200
    reassess_text = res.json()["intervention"]["reassessment_question"]
    assert len(reassess_text) > 20
    assert "vacuum" in reassess_text.lower()


def test_correct_answer_and_explanation_shown():
    """Verify that the 4 required items for 'Correct Answer and Explanation' are populated."""
    wooden_ans = "I think the wooden ball hits the ground first."
    res = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": wooden_ans,
        "learner_id": "test_eval_four_items"
    })
    assert res.status_code == 200
    eval_data = res.json()["answer_evaluation"]

    # 1. Your answer
    assert eval_data["your_answer"] == wooden_ans
    # 2. Was it correct?
    assert eval_data["was_correct"] == "incorrect"
    assert eval_data["was_it_correct_display"] == "Incorrect"
    # 3. Correct answer (with explicit conditions)
    assert "Both balls reach the ground at approximately the same time" in eval_data["correct_answer"]
    assert "air resistance" in eval_data["correct_answer"].lower()
    # 4. Why? (connected directly to student's answer)
    assert "Gravity gives both objects approximately the same downward acceleration" in eval_data["why_explanation"]
    assert "wooden ball would land first" in eval_data["why_explanation"]


def test_reassessment_outcomes_improved_persistent_inconclusive():
    """Verify transfer reassessment outcomes for improved, persistent, and inconclusive answers."""
    transfer_q = (
        "A steel ball and a wooden ball are dropped at the same time inside a vacuum chamber. "
        "Which ball reaches the bottom first? Explain why."
    )

    # 1. Improved
    eval_improved = evaluate_reassessment_answer(
        transfer_q,
        "Both balls reach the bottom at the same time because in a vacuum they experience the exact same acceleration of gravity."
    )
    assert eval_improved["outcome"] == "improved"
    assert "improvement" in eval_improved["feedback"].lower()

    # 2. Persistent
    eval_persistent = evaluate_reassessment_answer(
        transfer_q,
        "The steel ball hits first because it has greater mass."
    )
    assert eval_persistent["outcome"] == "persistent"
    assert "misunderstanding may still be present" in eval_persistent["feedback"].lower()

    # 3. Inconclusive
    eval_inconclusive = evaluate_reassessment_answer(
        transfer_q,
        "It depends on the chamber."
    )
    assert eval_inconclusive["outcome"] == "inconclusive"
    assert "we need more evidence" in eval_inconclusive["feedback"].lower()


def test_no_duplicate_learner_attempts():
    """Verify that Diagnostic Fork and Reassessment update the original attempt in-place without duplicating entries."""
    learner_id = "test_no_dup_learner"
    client.delete(f"/api/history/{learner_id}")

    # 1. Initial diagnosis
    res1 = client.post("/api/diagnose", json={
        "question": STEEL_WOODEN_Q,
        "student_answer": "I think the wooden ball hits the ground first.",
        "learner_id": learner_id
    })
    assert res1.status_code == 200
    att1 = res1.json()["attempt"]
    attempt_idx = att1["attempt_index"]

    # History should have 1 attempt
    hist1 = client.get(f"/api/history/{learner_id}").json()
    assert len(hist1) == 1

    # 2. Evaluate Diagnostic Fork probe
    res2 = client.post("/api/diagnostic-fork/evaluate", json={
        "learner_id": learner_id,
        "attempt_index": attempt_idx,
        "question_id": "DF-M4-NONE",
        "selected_choice_id": "B",
        "reasoning_text": "Acceleration a = F/m = g for all masses in a vacuum."
    })
    assert res2.status_code == 200

    # History should STILL have 1 attempt (updated in-place)
    hist2 = client.get(f"/api/history/{learner_id}").json()
    assert len(hist2) == 1
    assert hist2[0]["diagnostic_fork_selected_choice_id"] == "B"

    # 3. Submit Transfer Reassessment
    res3 = client.post("/api/reassess", json={
        "learner_id": learner_id,
        "attempt_index": attempt_idx,
        "reassessment_question": "A steel ball and a wooden ball are dropped at the same time inside a vacuum chamber. Which ball reaches the bottom first? Explain why.",
        "reassessment_answer": "Both hit at the same time because gravity accelerates both equally in a vacuum.",
        "original_misconception": "heavier_objects_fall_faster"
    })
    assert res3.status_code == 200
    assert res3.json()["outcome"] == "improved"

    # History should STILL have exactly 1 attempt
    hist3 = client.get(f"/api/history/{learner_id}").json()
    assert len(hist3) == 1
    assert hist3[0]["reassessment_completed"] is True
    assert hist3[0]["reassessment_outcome"] == "improved"
