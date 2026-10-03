import pytest
from src.learner.reassessment_data import (
    _load_reassessment_bank,
    _load_resolution_rules,
    get_reassessment_questions,
    get_next_reassessment_question,
)
from src.learner import record_attempt, update_attempt_reassessment, clear_learner_history, get_learner_history

@pytest.fixture(autouse=True)
def reset_history():
    clear_learner_history()
    yield
    clear_learner_history()

def test_load_real_reassessment_bank():
    bank = _load_reassessment_bank()
    rules = _load_resolution_rules()
    assert isinstance(bank, list)
    assert len(bank) > 0
    assert "reassessment_id" in bank[0]
    
    assert isinstance(rules, dict)
    assert "max_reassessment_attempts_per_misconception_per_session" in rules

def test_retrieve_questions_by_misconception_id():
    questions = get_reassessment_questions("M1")
    assert len(questions) > 0
    for q in questions:
        assert q["misconception_id"] == "M1"

def test_unknown_misconception_id():
    questions = get_reassessment_questions("unknown_id")
    assert questions == []
    
    next_q = get_next_reassessment_question("learner1", "unknown_id", ["Easy", "Medium"])
    assert next_q is None

def test_select_eligible_question():
    q = get_next_reassessment_question("learner1", "M1", ["Easy", "Medium", "Hard"])
    assert q is not None
    assert q["misconception_id"] == "M1"
    assert q["difficulty"] in ["Easy", "Medium", "Hard"]

def test_prevent_reuse_of_reassessment_id():
    learner = "learner_reuse"
    # First question
    q1 = get_next_reassessment_question(learner, "M1", ["Easy", "Medium", "Hard"])
    assert q1 is not None
    
    # Record it
    record_attempt(learner, "Original Q", "A", {"misconception_label": "M1"})
    update_attempt_reassessment(learner, 0, True, "resolved", "answer", "feedback", reassessment_id=q1["reassessment_id"])
    
    # Second question
    q2 = get_next_reassessment_question(learner, "M1", ["Easy", "Medium", "Hard"])
    assert q2 is not None
    assert q2["reassessment_id"] != q1["reassessment_id"]

def test_respect_difficulty_filtering():
    # Only ask for Hard
    q = get_next_reassessment_question("learner_diff", "M1", ["Hard"])
    assert q is not None
    assert q["difficulty"] == "Hard"

def test_respect_maximum_attempts_rule():
    learner = "learner_max"
    rules = _load_resolution_rules()
    max_attempts = rules.get("max_reassessment_attempts_per_misconception_per_session", 3)
    
    # Record max_attempts attempts with reassessment_id
    for i in range(max_attempts):
        record_attempt(learner, f"Q{i}", "A", {"misconception_label": "M1"})
        update_attempt_reassessment(learner, i, True, "unresolved", "ans", "fb", reassessment_id=f"R-M1-{i+100}")
        
    q = get_next_reassessment_question(learner, "M1", ["Easy", "Medium", "Hard"])
    assert q is None

def test_non_reassessment_does_not_count_toward_max():
    learner = "learner_non_reassessment"
    rules = _load_resolution_rules()
    max_attempts = rules.get("max_reassessment_attempts_per_misconception_per_session", 3)
    
    # Record one attempt WITHOUT reassessment_id
    record_attempt(learner, "Q_no_reassess", "A", {"misconception_label": "M1"})
    
    # Record (max_attempts - 1) attempts WITH reassessment_id
    for i in range(max_attempts - 1):
        record_attempt(learner, f"Q{i}", "A", {"misconception_label": "M1"})
        update_attempt_reassessment(learner, i+1, True, "unresolved", "ans", "fb", reassessment_id=f"R-M1-{i+100}")
    
    # The first attempt doesn't have a reassessment_id, so we should still be under the max
    q = get_next_reassessment_question(learner, "M1", ["Easy", "Medium", "Hard"])
    assert q is not None

def test_empty_invalid_learner_id():
    q = get_next_reassessment_question("", "M1", ["Easy"])
    assert q is None
    
def test_preserving_existing_learner_history():
    learner = "learner_pres"
    record_attempt(learner, "Q1", "A1", {"misconception_label": "M1"}, {"title": "int"})
    update_attempt_reassessment(learner, 0, True, "res", "ans", "feedback_stored", reassessment_id="R-M1-01")
    
    history = get_learner_history(learner)
    assert len(history) == 1
    attempt = history[0]
    assert attempt["question"] == "Q1"
    assert attempt["reassessment_id"] == "R-M1-01"
    assert attempt["reassessment_feedback"] == "feedback_stored"
    assert attempt["reassessment_outcome"] == "res"
