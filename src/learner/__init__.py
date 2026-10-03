"""Learner tracking and session history module.

Owner: Member 4 (Integration, learner history and testing)
Branch: member-4-integration

This module fulfills the learner tracking interface:
    record_attempt(learner_id, question, student_answer, diagnosis, intervention)
    get_learner_history(learner_id)
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# In-memory session store (can be extended to SQLite or JSON by Member 4)
_LEARNER_HISTORY_STORE: Dict[str, List[Dict[str, Any]]] = {}


def record_attempt(
    learner_id: str,
    question: str,
    student_answer: str,
    diagnosis: Dict[str, Any],
    intervention: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Record a learning interaction and diagnosis attempt.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the learner/session.
    question : str
        The question prompt answered.
    student_answer : str
        The student's submitted answer text.
    diagnosis : dict
        Output from diagnose().
    intervention : dict, optional
        Output from get_intervention().

    Returns
    -------
    dict
        The logged record containing timestamp and attempt metadata.
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "learner_id": learner_id,
        "question": question,
        "student_answer": student_answer,
        "misconception_label": diagnosis.get("misconception_label", "unknown"),
        "confidence_score": diagnosis.get("confidence_score", 0.0),
        "diagnosis_status": diagnosis.get("status", "unknown"),
        "intervention_title": (intervention or {}).get("title", ""),
        "reassessment_completed": False
    }

    if learner_id not in _LEARNER_HISTORY_STORE:
        _LEARNER_HISTORY_STORE[learner_id] = []
    _LEARNER_HISTORY_STORE[learner_id].append(record)

    return record


def get_learner_history(learner_id: str) -> List[Dict[str, Any]]:
    """Retrieve all recorded attempts for a given learner.

    Parameters
    ----------
    learner_id : str
        Identifier of the learner.

    Returns
    -------
    list of dict
        Chronological list of attempt records.
    """
    return list(_LEARNER_HISTORY_STORE.get(learner_id, []))


def clear_learner_history(learner_id: Optional[str] = None) -> None:
    """Clear history for a specific learner or all learners (useful for testing)."""
    if learner_id is not None:
        _LEARNER_HISTORY_STORE.pop(learner_id, None)
    else:
        _LEARNER_HISTORY_STORE.clear()


def update_attempt_reassessment(
    learner_id: str,
    attempt_index: int,
    reassessment_completed: bool,
    reassessment_outcome: str,
    reassessment_answer: str = "",
    reassessment_feedback: str = "",
    reassessment_id: Optional[str] = None
) -> Dict[str, Any]:
    """Update an existing attempt with reassessment information."""
    if learner_id not in _LEARNER_HISTORY_STORE:
        return {}
    
    history = _LEARNER_HISTORY_STORE[learner_id]
    if attempt_index < 0 or attempt_index >= len(history):
        return {}
        
    attempt = history[attempt_index]
    attempt["reassessment_completed"] = reassessment_completed
    attempt["reassessment_outcome"] = reassessment_outcome
    attempt["reassessment_answer"] = reassessment_answer
    attempt["reassessment_feedback"] = reassessment_feedback
    if reassessment_id is not None:
        attempt["reassessment_id"] = reassessment_id
    
    return attempt



