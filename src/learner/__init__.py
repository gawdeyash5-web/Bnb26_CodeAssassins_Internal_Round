"""Learner tracking and session history module for Re:Learn.

Maintains session history in-memory and persists to a local JSON store
(data/learner_history.json) so attempts survive application restarts.
"""

from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, List, Optional

HISTORY_FILE_PATH = os.path.join("data", "learner_history.json")

# In-memory session store
_LEARNER_HISTORY_STORE: Dict[str, List[Dict[str, Any]]] = {}


def _load_history_from_disk() -> None:
    """Load persisted learner history from disk if available."""
    global _LEARNER_HISTORY_STORE
    if os.path.exists(HISTORY_FILE_PATH):
        try:
            with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as f:
                _LEARNER_HISTORY_STORE = json.load(f)
        except Exception:
            _LEARNER_HISTORY_STORE = {}


def _save_history_to_disk() -> None:
    """Persist current learner history store to disk."""
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)
        with open(HISTORY_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(_LEARNER_HISTORY_STORE, f, indent=2)
    except Exception:
        pass


# Initialize history on module import
_load_history_from_disk()


def record_attempt(
    learner_id: str,
    question: str,
    student_answer: str,
    diagnosis: Dict[str, Any],
    intervention: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Record an initial learning interaction and diagnosis attempt.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the learner/session.
    question : str
        The question prompt presented.
    student_answer : str
        The student's submitted answer text.
    diagnosis : dict
        Output from diagnose().
    intervention : dict, optional
        Output from get_intervention().

    Returns
    -------
    dict
        The logged record containing metadata and attempt index.
    """
    if learner_id not in _LEARNER_HISTORY_STORE:
        _LEARNER_HISTORY_STORE[learner_id] = []

    attempt_index = len(_LEARNER_HISTORY_STORE[learner_id])
    now_iso = datetime.now(timezone.utc).isoformat()

    diag_id = (intervention or {}).get("misconception_id") or diagnosis.get("misconception_id", "")
    diag_label = diagnosis.get("misconception_label", "unknown")
    diag_conf = diagnosis.get("confidence_score", 0.0)
    diag_status = diagnosis.get("status", "unknown")
    diag_expl = diagnosis.get("explanation", "")
    evidence_kw = diagnosis.get("evidence_keywords", [])

    # Extract answer evaluation details if available
    eval_data = diagnosis.get("answer_evaluation") or {}
    was_correct = eval_data.get("was_correct") or diagnosis.get("was_correct", "not_assessed")
    correct_ans = eval_data.get("correct_answer") or diagnosis.get("correct_answer", "")
    why_expl = eval_data.get("why_explanation") or diagnosis.get("why_explanation", "")

    record: Dict[str, Any] = {
        "attempt_id": f"{learner_id}_{attempt_index}_{int(datetime.now().timestamp())}",
        "attempt_index": attempt_index,
        "timestamp": now_iso,
        "learner_id": learner_id,
        "question": question,
        "student_answer": student_answer,
        # Answer Correctness Assessment
        "was_correct": was_correct,
        "correct_answer": correct_ans,
        "why_explanation": why_expl,
        "answer_evaluation": eval_data,
        # Active diagnosis (can be refined by Diagnostic Fork)
        "misconception_id": diag_id,
        "misconception_label": diag_label,
        "confidence_score": diag_conf,
        "diagnosis_status": diag_status,
        "diagnosis_explanation": diag_expl,
        "evidence_keywords": evidence_kw,
        # Preserved baseline initial diagnosis
        "initial_misconception_id": diag_id,
        "initial_misconception_label": diag_label,
        "initial_confidence_score": diag_conf,
        "initial_diagnosis_status": diag_status,
        "initial_evidence_keywords": evidence_kw,
        # Diagnostic Fork interaction tracking
        "diagnostic_fork_eligible": False,
        "diagnostic_fork_used": False,
        "diagnostic_fork_status": "not_assessed",  # 'not_needed', 'available', 'completed', 'skipped', 'inconclusive'
        "diagnostic_fork_question_id": None,
        "diagnostic_fork_scenario_title": None,
        "diagnostic_fork_question": None,
        "diagnostic_fork_candidates": [],
        "diagnostic_fork_selected_choice_id": None,
        "diagnostic_fork_selected_text": None,
        "diagnostic_fork_evidence_type": None,
        "diagnostic_fork_interpretation": None,
        "diagnostic_fork_refined_label": None,
        "diagnostic_fork_refined_id": None,
        "diagnostic_fork_explanation": None,
        "diagnostic_fork_timestamp": None,
        # Pedagogical intervention
        "intervention_title": (intervention or {}).get("title", ""),
        "intervention_summary": (intervention or {}).get("short_explanation", ""),
        "intervention_key_concept": (intervention or {}).get("key_concept", ""),
        "intervention_analogy": (intervention or {}).get("real_life_analogy", ""),
        "intervention_hint": (intervention or {}).get("guided_hint", ""),
        # Transfer reassessment
        "reassessment_completed": False,
        "reassessment_question": (intervention or {}).get("reassessment_question", ""),
        "reassessment_answer": "",
        "reassessment_outcome": "not_assessed",  # 'improved', 'persistent', 'inconclusive', 'not_assessed'
        "reassessment_feedback": "",
        "reassessment_timestamp": None
    }

    _LEARNER_HISTORY_STORE[learner_id].append(record)
    _save_history_to_disk()

    return record


def update_attempt_reassessment(
    learner_id: str,
    attempt_index: int,
    reassessment_completed: bool,
    reassessment_outcome: str,
    reassessment_answer: str = "",
    reassessment_feedback: str = "",
    reassessment_question: str = ""
) -> Dict[str, Any]:
    """Update an existing attempt in-place with transfer reassessment information.

    Prevents duplicate learner attempts and tracks pedagogical resolution.
    """
    if learner_id not in _LEARNER_HISTORY_STORE:
        return {}

    history = _LEARNER_HISTORY_STORE[learner_id]
    if attempt_index < 0 or attempt_index >= len(history):
        # Support -1 for most recent attempt
        if attempt_index == -1 and len(history) > 0:
            attempt_index = len(history) - 1
        else:
            return {}

    attempt = history[attempt_index]
    attempt["reassessment_completed"] = bool(reassessment_completed)
    attempt["reassessment_outcome"] = str(reassessment_outcome)
    attempt["reassessment_answer"] = str(reassessment_answer)
    attempt["reassessment_feedback"] = str(reassessment_feedback)
    if reassessment_question:
        attempt["reassessment_question"] = str(reassessment_question)
    attempt["reassessment_timestamp"] = datetime.now(timezone.utc).isoformat()

    _save_history_to_disk()
    return attempt


def update_attempt_diagnostic_fork(
    learner_id: str,
    attempt_index: int,
    fork_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update an existing attempt in-place with Diagnostic Fork investigation results.

    Maintains identical attempt identity while augmenting reasoning evidence.
    """
    if learner_id not in _LEARNER_HISTORY_STORE:
        return {}

    history = _LEARNER_HISTORY_STORE[learner_id]
    if attempt_index < 0 or attempt_index >= len(history):
        if attempt_index == -1 and len(history) > 0:
            attempt_index = len(history) - 1
        else:
            return {}

    attempt = history[attempt_index]
    attempt["diagnostic_fork_used"] = True
    attempt["diagnostic_fork_status"] = fork_data.get("status", "completed")
    attempt["diagnostic_fork_question_id"] = fork_data.get("question_id")
    attempt["diagnostic_fork_scenario_title"] = fork_data.get("scenario_title")
    attempt["diagnostic_fork_question"] = fork_data.get("question")
    attempt["diagnostic_fork_candidates"] = fork_data.get("candidates", [])
    attempt["diagnostic_fork_selected_choice_id"] = fork_data.get("selected_choice_id")
    attempt["diagnostic_fork_selected_text"] = fork_data.get("selected_text")
    attempt["diagnostic_fork_evidence_type"] = fork_data.get("evidence_type")
    attempt["diagnostic_fork_interpretation"] = fork_data.get("interpretation")
    attempt["diagnostic_fork_refined_label"] = fork_data.get("refined_label")
    attempt["diagnostic_fork_refined_id"] = fork_data.get("refined_id")
    attempt["diagnostic_fork_explanation"] = fork_data.get("explanation")
    attempt["diagnostic_fork_timestamp"] = datetime.now(timezone.utc).isoformat()

    # Update active diagnosis if refined
    if fork_data.get("refined_label"):
        attempt["misconception_label"] = fork_data["refined_label"]
    if fork_data.get("refined_id"):
        attempt["misconception_id"] = fork_data["refined_id"]
    if fork_data.get("refined_confidence") is not None:
        attempt["confidence_score"] = fork_data["refined_confidence"]
    if fork_data.get("refined_status"):
        attempt["diagnosis_status"] = fork_data["refined_status"]

    # Update intervention if provided
    intervention = fork_data.get("intervention")
    if intervention:
        attempt["intervention_title"] = intervention.get("title", attempt.get("intervention_title", ""))
        attempt["intervention_summary"] = intervention.get("short_explanation", attempt.get("intervention_summary", ""))
        attempt["intervention_key_concept"] = intervention.get("key_concept", attempt.get("intervention_key_concept", ""))
        attempt["intervention_analogy"] = intervention.get("real_life_analogy", attempt.get("intervention_analogy", ""))
        attempt["intervention_hint"] = intervention.get("guided_hint", attempt.get("intervention_hint", ""))
        if intervention.get("reassessment_question"):
            attempt["reassessment_question"] = intervention["reassessment_question"]

    _save_history_to_disk()
    return attempt


def get_learner_history(learner_id: str) -> List[Dict[str, Any]]:
    """Retrieve all recorded attempts for a given learner."""
    return list(_LEARNER_HISTORY_STORE.get(learner_id, []))


def clear_learner_history(learner_id: Optional[str] = None) -> None:
    """Clear history for a specific learner or all learners."""
    global _LEARNER_HISTORY_STORE
    if learner_id is not None:
        _LEARNER_HISTORY_STORE.pop(learner_id, None)
    else:
        _LEARNER_HISTORY_STORE.clear()
    _save_history_to_disk()
