import pytest
from src.interventions import get_intervention
from src.learner import record_attempt, get_learner_history, clear_learner_history

@pytest.fixture(autouse=True)
def reset_history():
    """Ensure a clean learner history state before and after each test."""
    clear_learner_history()
    yield
    clear_learner_history()


def test_integration_flow_known_misconception():
    """1. Test the end-to-end integration flow with a known misconception label."""
    learner_id = "test_learner_integration_1"
    question = "A hockey puck is sliding on frictionless ice. What force keeps it moving?"
    student_answer = "The force of the hit keeps pushing it forward."
    
    # 1. Use a controlled/mocked diagnosis result matching the documented schema
    controlled_diagnosis = {
        "misconception_label": "impetus_force_persistence",
        "confidence_score": 0.95,
        "model_version": "mock-v1.0",
        "status": "success",
        "explanation": "Mocked diagnosis for integration test."
    }
    
    # 2. Call get_intervention() using the misconception_label from the controlled diagnosis
    intervention = get_intervention(controlled_diagnosis["misconception_label"])
    
    # 3. Verify the intervention is successfully returned with status == "found"
    assert intervention["status"] == "found"
    assert "title" in intervention
    
    # 4. Call record_attempt()
    record_attempt(
        learner_id=learner_id,
        question=question,
        student_answer=student_answer,
        diagnosis=controlled_diagnosis,
        intervention=intervention
    )
    
    # 5. Call get_learner_history() and verify
    history = get_learner_history(learner_id)
    assert len(history) == 1
    
    attempt = history[0]
    assert attempt["question"] == question
    assert attempt["student_answer"] == student_answer
    assert attempt["misconception_label"] == controlled_diagnosis["misconception_label"]
    assert attempt["intervention_title"] == intervention["title"]
    assert attempt["misconception_label"] == "impetus_force_persistence"


def test_integration_flow_unknown_misconception():
    """2. Test that an unknown ML label gracefully falls back without breaking the learning-history pipeline."""
    learner_id = "test_learner_integration_2"
    question = "What happens to the object?"
    student_answer = "It starts dancing."
    
    # 1. Use a controlled diagnosis with an unknown label
    controlled_diagnosis = {
        "misconception_label": "dancing_object_syndrome",
        "confidence_score": 0.40,
        "model_version": "mock-v1.0",
        "status": "uncertain",
        "explanation": "Mocked uncertain diagnosis."
    }
    
    # 2. Pass it to get_intervention() and verify fallback
    intervention = get_intervention(controlled_diagnosis["misconception_label"])
    assert intervention["status"] == "fallback"
    
    # 3. Record the attempt
    record_attempt(
        learner_id=learner_id,
        question=question,
        student_answer=student_answer,
        diagnosis=controlled_diagnosis,
        intervention=intervention
    )
    
    # 4. Verify learner history still records the attempt successfully
    history = get_learner_history(learner_id)
    assert len(history) == 1
    
    attempt = history[0]
    assert attempt["question"] == question
    assert attempt["student_answer"] == student_answer
    assert attempt["misconception_label"] == "dancing_object_syndrome"
    assert attempt["intervention_title"] == intervention["title"]
