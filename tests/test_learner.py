import pytest
from src.learner import (
    record_attempt,
    get_learner_history,
    clear_learner_history
)

@pytest.fixture(autouse=True)
def reset_history():
    """Fixture to ensure history is cleared before and after each test."""
    clear_learner_history()
    yield
    clear_learner_history()


def test_record_attempt_success():
    """1. & 2. record_attempt() successfully records an attempt with expected fields."""
    learner_id = "learner_01"
    question = "What is force?"
    student_answer = "Force is energy."
    diagnosis = {
        "misconception_label": "force_as_energy",
        "confidence_score": 0.85,
        "status": "success"
    }
    intervention = {
        "title": "Review: Force vs Energy",
    }
    
    result = record_attempt(
        learner_id=learner_id,
        question=question,
        student_answer=student_answer,
        diagnosis=diagnosis,
        intervention=intervention
    )
    
    assert result["learner_id"] == learner_id
    assert result["question"] == question
    assert result["student_answer"] == student_answer
    assert result["misconception_label"] == "force_as_energy"
    assert result["confidence_score"] == 0.85
    assert result["diagnosis_status"] == "success"
    assert result["intervention_title"] == "Review: Force vs Energy"
    assert result["reassessment_completed"] is False
    assert "timestamp" in result


def test_get_learner_history_correct():
    """3. get_learner_history() returns the correct history for a learner."""
    learner_id = "learner_02"
    diagnosis = {"misconception_label": "gravity_falls", "status": "success"}
    
    record_attempt(learner_id, "Q1", "A1", diagnosis)
    
    history = get_learner_history(learner_id)
    assert len(history) == 1
    assert history[0]["learner_id"] == learner_id
    assert history[0]["question"] == "Q1"


def test_get_learner_history_empty():
    """4. A learner with no history returns an empty list."""
    history = get_learner_history("unknown_learner")
    assert isinstance(history, list)
    assert len(history) == 0


def test_multiple_attempts_order():
    """5. Multiple attempts for the same learner are preserved in order."""
    learner_id = "learner_03"
    
    record_attempt(learner_id, "Question 1", "Answer 1", {"status": "success"})
    record_attempt(learner_id, "Question 2", "Answer 2", {"status": "uncertain"})
    record_attempt(learner_id, "Question 3", "Answer 3", {"status": "fallback"})
    
    history = get_learner_history(learner_id)
    assert len(history) == 3
    assert history[0]["question"] == "Question 1"
    assert history[1]["question"] == "Question 2"
    assert history[2]["question"] == "Question 3"


def test_clear_one_learner_history():
    """6. clear_learner_history() clears one learner's history if argument provided."""
    learner_a = "learner_A"
    learner_b = "learner_B"
    
    record_attempt(learner_a, "Q_A", "A_A", {"status": "success"})
    record_attempt(learner_b, "Q_B", "A_B", {"status": "success"})
    
    assert len(get_learner_history(learner_a)) == 1
    assert len(get_learner_history(learner_b)) == 1
    
    # Clear only learner A
    clear_learner_history(learner_id=learner_a)
    
    assert len(get_learner_history(learner_a)) == 0
    assert len(get_learner_history(learner_b)) == 1
