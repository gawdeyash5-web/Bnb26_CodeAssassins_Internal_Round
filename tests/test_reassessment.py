import pytest
from src.learner import (
    update_attempt_reassessment, 
    record_attempt,
    get_learner_history,
    clear_learner_history
)

@pytest.fixture(autouse=True)
def reset_history():
    clear_learner_history()
    yield
    clear_learner_history()

def test_update_attempt_reassessment_success():
    """Test updating an existing learner attempt with reassessment fields."""
    learner = "learner_1"
    
    # 1. Record original
    diagnosis = {"misconception_label": "test_label", "status": "success", "confidence_score": 0.9}
    intervention = {"title": "Test Intervention"}
    record_attempt(learner, "Q1", "A1", diagnosis, intervention)
    
    history_before = get_learner_history(learner)
    assert len(history_before) == 1
    assert history_before[0]["reassessment_completed"] is False
    
    # 2. Update
    update_attempt_reassessment(
        learner_id=learner,
        attempt_index=0,
        reassessment_completed=True,
        reassessment_outcome="resolved",
        reassessment_answer="my reassessment answer",
        reassessment_feedback="good job"
    )
    
    history_after = get_learner_history(learner)
    assert len(history_after) == 1  # Not duplicated
    
    attempt = history_after[0]
    # Original diagnosis/intervention unchanged
    assert attempt["question"] == "Q1"
    assert attempt["student_answer"] == "A1"
    assert attempt["misconception_label"] == "test_label"
    assert attempt["intervention_title"] == "Test Intervention"
    
    # Reassessment fields stored correctly
    assert attempt["reassessment_completed"] is True
    assert attempt["reassessment_outcome"] == "resolved"
    assert attempt["reassessment_answer"] == "my reassessment answer"
    assert attempt["reassessment_feedback"] == "good job"

def test_update_attempt_invalid_learner():
    """Test safely handling invalid learner."""
    # Should not raise exception
    result = update_attempt_reassessment("fake", 0, True, "resolved")
    assert result == {}

def test_update_attempt_invalid_index():
    """Test safely handling invalid attempt index."""
    learner = "learner_2"
    diagnosis = {"misconception_label": "test_label"}
    record_attempt(learner, "Q", "A", diagnosis)
    
    # Should not raise exception
    result = update_attempt_reassessment(learner, 5, True, "resolved")
    assert result == {}
