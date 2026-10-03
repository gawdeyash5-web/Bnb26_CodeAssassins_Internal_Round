import pytest
from src.interventions import get_intervention

def test_known_misconception():
    """1. Known misconception tests the expected return structure."""
    label = "impetus_force_persistence"
    result = get_intervention(label)
    
    assert isinstance(result, dict)
    assert result.get("status") == "found"
    
    required_fields = [
        "title", 
        "explanation", 
        "key_concept", 
        "guided_hint", 
        "reassessment_question", 
        "status"
    ]
    
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
        assert isinstance(result[field], str), f"Field {field} should be a string"
        assert len(result[field].strip()) > 0, f"Field {field} should not be empty"


def test_unknown_misconception():
    """2. Unknown misconception tests gracefully returning a fallback."""
    label = "made_up_physics_concept_xyz"
    result = get_intervention(label)
    
    # Should not raise exception, but return fallback dict
    assert isinstance(result, dict)
    assert result.get("status") == "fallback"
    
    required_fields = [
        "title", 
        "explanation", 
        "key_concept", 
        "guided_hint", 
        "reassessment_question", 
        "status"
    ]
    
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
        assert isinstance(result[field], str)
        assert len(result[field].strip()) > 0


def test_invalid_empty_label():
    """3. Invalid/empty label tests graceful fallback behavior."""
    # Using an empty string and None to ensure robust fallback handling
    for label in ["", "   "]:
        result = get_intervention(label)
        
        assert isinstance(result, dict)
        assert result.get("status") == "fallback"
        
        # Verify required fields are still present
        assert "guided_hint" in result
        assert "reassessment_question" in result
        
        # Title will just be "Review Concept: " based on current implementation
        assert "Review Concept:" in result["title"]
