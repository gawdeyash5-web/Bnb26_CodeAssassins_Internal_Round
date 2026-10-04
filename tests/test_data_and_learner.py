"""Unit tests for Re:Learn data layer, interventions, and learner tracking."""

import os
import pytest
from src.data import (
    load_dataset,
    load_questions,
    load_misconceptions_taxonomy,
    load_reassessment_bank,
    get_reassessment_for_misconception,
    MISCONCEPTION_ID_TO_LABEL
)
from src.interventions import get_intervention
from src.learner import (
    record_attempt,
    update_attempt_reassessment,
    get_learner_history,
    clear_learner_history
)


@pytest.fixture(autouse=True)
def clean_history():
    """Ensure clean history state for tests."""
    clear_learner_history("test_unit_user")
    yield
    clear_learner_history("test_unit_user")


def test_load_dataset_canonical():
    """Verify canonical dataset loads with 70 records and required columns."""
    df = load_dataset()
    assert len(df) == 70
    assert "question_id" in df.columns
    assert "misconception_label" in df.columns
    assert "misconception_id" in df.columns


def test_load_questions():
    """Verify questions loader returns deduplicated scenarios with metadata."""
    questions = load_questions()
    assert len(questions) > 0
    q = questions[0]
    assert "question" in q
    assert "question_id" in q
    assert "topic" in q
    assert "correct_answer" in q


def test_taxonomy_and_interventions():
    """Verify all 5 misconceptions plus mastery have valid taxonomy and interventions."""
    for m_id, label in MISCONCEPTION_ID_TO_LABEL.items():
        intervention = get_intervention(label)
        assert intervention["status"] == "found"
        assert len(intervention["explanation"]) > 0
        assert len(intervention["guided_hint"]) > 0
        assert len(intervention["reassessment_question"]) > 0


def test_reassessment_lookup():
    """Verify reassessment question bank lookup."""
    reassess = get_reassessment_for_misconception("M1")
    assert reassess is not None
    assert "question" in reassess
    assert len(reassess["question"]) > 0


def test_learner_record_and_reassessment_update():
    """Verify initial attempt creation and in-place reassessment update."""
    user = "test_unit_user"
    q = "A hockey puck slides on ice. What keeps it moving?"
    ans = "Force from stick"
    diag = {
        "misconception_label": "impetus_force_persistence",
        "confidence_score": 0.45,
        "status": "uncertain",
        "explanation": "Low confidence diagnosis."
    }
    interv = get_intervention("impetus_force_persistence")

    # 1. Initial attempt
    rec = record_attempt(user, q, ans, diag, interv)
    assert rec["reassessment_completed"] is False
    assert rec["reassessment_outcome"] == "not_assessed"

    history_1 = get_learner_history(user)
    assert len(history_1) == 1

    # 2. Update with reassessment outcome
    updated = update_attempt_reassessment(
        learner_id=user,
        attempt_index=0,
        reassessment_completed=True,
        reassessment_outcome="improved",
        reassessment_answer="No force is required due to inertia.",
        reassessment_feedback="Demonstrates understanding of Newton's 1st Law."
    )
    assert updated["reassessment_completed"] is True
    assert updated["reassessment_outcome"] == "improved"

    # 3. Verify history is updated in-place without duplicate
    history_2 = get_learner_history(user)
    assert len(history_2) == 1
    assert history_2[0]["reassessment_completed"] is True
    assert history_2[0]["reassessment_outcome"] == "improved"
