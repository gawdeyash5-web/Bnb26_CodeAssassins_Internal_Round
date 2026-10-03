import json
import os
from typing import List, Dict, Any, Optional

from src.learner import get_learner_history

_REASSESSMENT_BANK: Optional[List[Dict[str, Any]]] = None
_RESOLUTION_RULES: Optional[Dict[str, Any]] = None

def _get_project_root() -> str:
    # Assuming this file is at src/learner/reassessment_data.py
    # Root is two directories up
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _load_reassessment_bank() -> List[Dict[str, Any]]:
    global _REASSESSMENT_BANK
    if _REASSESSMENT_BANK is None:
        path = os.path.join(_get_project_root(), "reassessment_bank.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _REASSESSMENT_BANK = json.load(f)
        except Exception:
            _REASSESSMENT_BANK = []
    return _REASSESSMENT_BANK

def _load_resolution_rules() -> Dict[str, Any]:
    global _RESOLUTION_RULES
    if _RESOLUTION_RULES is None:
        path = os.path.join(_get_project_root(), "resolution_rules.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _RESOLUTION_RULES = json.load(f)
        except Exception:
            _RESOLUTION_RULES = {}
    return _RESOLUTION_RULES

def get_reassessment_questions(misconception_id: str) -> List[Dict[str, Any]]:
    """Retrieve all reassessment questions for a given misconception."""
    bank = _load_reassessment_bank()
    return [q for q in bank if q.get("misconception_id") == misconception_id]

def get_next_reassessment_question(
    learner_id: str, 
    misconception_id: str, 
    allowed_difficulties: List[str],
    original_question: str = ""
) -> Optional[Dict[str, Any]]:
    """Select the next eligible reassessment question for a learner."""
    if not learner_id:
        return None
        
    bank = _load_reassessment_bank()
    rules = _load_resolution_rules()
    
    max_attempts = rules.get("max_reassessment_attempts_per_misconception_per_session", 3)
    
    history = get_learner_history(learner_id)
    
    reassessment_attempts = 0
    seen_reassessment_ids = set()
    
    # Iterate through history to find attempts for this misconception
    for attempt in history:
        if attempt.get("misconception_label") == misconception_id:
            # Check if this attempt involved a recorded reassessment
            if attempt.get("reassessment_id"):
                reassessment_attempts += 1
                seen_reassessment_ids.add(attempt.get("reassessment_id"))
                    
    if reassessment_attempts >= max_attempts:
        return None
        
    eligible_questions = []
    for q in bank:
        if q.get("misconception_id") != misconception_id:
            continue
        if q.get("difficulty") not in allowed_difficulties:
            continue
        if q.get("reassessment_id") in seen_reassessment_ids:
            continue
        if q.get("question") == original_question:
            continue
        eligible_questions.append(q)
        
    if not eligible_questions:
        return None
        
    return eligible_questions[0]

def evaluate_reassessment_answer(
    student_answer: str, 
    expected_answer: Optional[str] = None, 
    rubric: Optional[str] = None
) -> Dict[str, str]:
    """
    Placeholder interface for answer evaluation.
    Will receive authoritative evaluation logic later.
    """
    return {
        "status": "not_evaluable",
        "outcome": "unknown",
        "feedback": "Evaluation logic pending."
    }
