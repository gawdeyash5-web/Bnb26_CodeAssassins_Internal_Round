import pytest
from src.ml.diagnose import diagnose

def test_empty_student_answer():
    """1. Empty student answer tests fallback behavior."""
    question = "Explain Newton's First Law."
    answer = "   "  # Whitespace only
    
    result = diagnose(question, answer)
    
    assert isinstance(result, dict)
    assert result.get("status") == "fallback"
    assert result.get("misconception_label") == "empty_answer"


def test_missing_model_fallback():
    """2. Missing model tests fallback behavior."""
    question = "Explain Newton's First Law."
    answer = "Things keep moving because of force."
    
    # Provide a path that definitely doesn't exist
    result = diagnose(question, answer, model_path="nonexistent_path/fake_model.joblib")
    
    assert isinstance(result, dict)
    assert result.get("status") == "fallback"
    assert result.get("misconception_label") == "pending_model_training"


def test_return_schema(monkeypatch):
    """3. Return schema checking with a mock artifact."""
    class MockPipeline:
        def predict(self, X):
            return ["mock_misconception_label"]
            
        def predict_proba(self, X):
            # Max probability is 0.85 -> success
            return [[0.15, 0.85]]
            
    import os
    import joblib
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    monkeypatch.setattr(joblib, "load", lambda path: MockPipeline())
    
    question = "What is gravity?"
    answer = "It's an energy."
    
    result = diagnose(question, answer, model_path="mock_model.joblib")
    
    assert isinstance(result, dict)
    
    required_fields = ["misconception_label", "confidence_score", "model_version", "status"]
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
        
    conf_score = result["confidence_score"]
    assert isinstance(conf_score, (float, int)), "confidence_score must be numeric"
    assert 0.0 <= conf_score <= 1.0, "confidence_score must be between 0.0 and 1.0"
    
    valid_statuses = ["success", "uncertain", "fallback"]
    assert result["status"] in valid_statuses, f"status must be one of {valid_statuses}"
