"""Data access and validation module for Re:Learn physics knowledge base.

Provides structured access to:
- Curated conceptual physics questions
- Full 70-sample misconception dataset
- Taxonomy catalog (M1-M5, NONE)
- Reassessment question bank
- Resolution status rules
"""

import json
import os
from typing import Any, Dict, List, Optional
import pandas as pd

DEFAULT_DATA_DIR = "data"
DEFAULT_DATASET_PATH = os.path.join(DEFAULT_DATA_DIR, "physics_misconceptions.csv")
DEFAULT_INTERVENTIONS_PATH = os.path.join(DEFAULT_DATA_DIR, "intervention_bank.json")
DEFAULT_REASSESSMENT_PATH = os.path.join(DEFAULT_DATA_DIR, "reassessment_bank.json")
DEFAULT_MISCONCEPTIONS_PATH = os.path.join(DEFAULT_DATA_DIR, "misconceptions.json")
DEFAULT_RULES_PATH = os.path.join(DEFAULT_DATA_DIR, "resolution_rules.json")
DEFAULT_DIAGNOSTIC_FORK_PATH = os.path.join(DEFAULT_DATA_DIR, "diagnostic_fork_bank.json")

MISCONCEPTION_ID_TO_LABEL: Dict[str, str] = {
    "M1": "impetus_force_persistence",
    "M2": "zero_net_force_zero_velocity",
    "M3": "action_reaction_same_object",
    "M4": "heavier_objects_fall_faster",
    "M5": "force_acceleration_conflation",
    "NONE": "no_misconception_detected",
}

MISCONCEPTION_LABEL_TO_ID: Dict[str, str] = {
    v: k for k, v in MISCONCEPTION_ID_TO_LABEL.items()
}


def load_dataset(filepath: str = DEFAULT_DATASET_PATH) -> pd.DataFrame:
    """Load the canonical physics misconception dataset."""
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=[
            "question_id", "topic", "subtopic", "difficulty", "question",
            "correct_answer", "student_answer", "misconception_id",
            "misconception_label", "misconception_name"
        ])
    return pd.read_csv(filepath)


def load_questions() -> List[Dict[str, Any]]:
    """Retrieve distinct curated questions with pedagogical metadata.

    Returns deduplicated questions grouped by scenario.
    """
    df = load_dataset()
    if df.empty:
        return []

    # Deduplicate by question_id or question text
    seen_questions = set()
    questions = []

    for _, row in df.iterrows():
        q_text = str(row["question"]).strip()
        if q_text in seen_questions:
            continue
        seen_questions.add(q_text)

        questions.append({
            "question_id": str(row.get("question_id", f"Q_{len(questions)+1}")),
            "topic": str(row.get("topic", "Newtonian Mechanics")),
            "subtopic": str(row.get("subtopic", "")),
            "difficulty": str(row.get("difficulty", "Medium")),
            "question": q_text,
            "question_type": str(row.get("question_type", "Conceptual")),
            "correct_answer": str(row.get("correct_answer", "")),
            "target_misconception_id": str(row.get("misconception_id", "")),
            "target_misconception_name": str(row.get("misconception_name", "")),
            "target_misconception_label": str(row.get("misconception_label", "")),
            "real_life_example": str(row.get("real_life_example", "")),
            "sample_misconception_answer": str(row.get("student_answer", "")) if str(row.get("is_correct", "")).lower() == "false" else "",
            "sample_correct_answer": str(row.get("correct_answer", "")),
        })

    return questions


def load_misconceptions_taxonomy() -> List[Dict[str, Any]]:
    """Load curated misconception definitions, principles, and analogies."""
    if not os.path.exists(DEFAULT_MISCONCEPTIONS_PATH):
        return []
    with open(DEFAULT_MISCONCEPTIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Augment with standardized snake_case labels
    for item in data:
        m_id = item.get("misconception_id", "")
        item["misconception_label"] = MISCONCEPTION_ID_TO_LABEL.get(m_id, m_id.lower())
    return data


def load_reassessment_bank() -> List[Dict[str, Any]]:
    """Load curated transfer reassessment questions."""
    if not os.path.exists(DEFAULT_REASSESSMENT_PATH):
        return []
    with open(DEFAULT_REASSESSMENT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        m_id = item.get("misconception_id", "")
        item["misconception_label"] = MISCONCEPTION_ID_TO_LABEL.get(m_id, m_id.lower())
    return data


def load_resolution_rules() -> Dict[str, Any]:
    """Load status transition rules and thresholds."""
    if not os.path.exists(DEFAULT_RULES_PATH):
        return {
            "statuses": ["not_assessed", "diagnosed", "intervened", "improved", "persistent", "inconclusive"],
            "diagnosis_confidence_threshold": 0.28
        }
    with open(DEFAULT_RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_reassessment_for_misconception(misconception_identifier: str) -> Optional[Dict[str, Any]]:
    """Get the best transfer reassessment question for a diagnosed misconception."""
    bank = load_reassessment_bank()
    norm = misconception_identifier.strip().lower()
    
    # Try match by misconception_id, misconception_label, or subtopic
    for item in bank:
        m_id = item.get("misconception_id", "").lower()
        m_label = item.get("misconception_label", "").lower()
        if norm in (m_id, m_label):
            return item

    # If no match in bank, fallback to dataset follow_up_question
    df = load_dataset()
    for _, row in df.iterrows():
        r_id = str(row.get("misconception_id", "")).lower()
        r_label = str(row.get("misconception_label", "")).lower()
        if norm in (r_id, r_label) and pd.notna(row.get("follow_up_question")):
            return {
                "reassessment_id": f"R-{row.get('misconception_id', 'GEN')}-01",
                "misconception_id": str(row.get("misconception_id", "")),
                "misconception_label": str(row.get("misconception_label", "")),
                "question": str(row.get("follow_up_question")),
                "correct_answer": str(row.get("follow_up_answer", "")),
                "difficulty": str(row.get("follow_up_difficulty", "Medium")),
                "why_this_tests_the_misconception": "Transfer scenario testing conceptual resolution."
            }


    return None


def load_diagnostic_fork_bank() -> List[Dict[str, Any]]:
    """Load the curated diagnostic fork question bank."""
    if not os.path.exists(DEFAULT_DIAGNOSTIC_FORK_PATH):
        return []
    with open(DEFAULT_DIAGNOSTIC_FORK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_diagnostic_fork_question(candidate_ids: List[str]) -> Optional[Dict[str, Any]]:
    """Find a diagnostic question that distinguishes between candidate misconception IDs.
    
    Parameters
    ----------
    candidate_ids : List[str]
        Candidate IDs (e.g. ['M1', 'M2'] or ['M1', 'NONE']).
        
    Returns
    -------
    dict or None
        Matching diagnostic question if a validated probe exists.
    """
    bank = load_diagnostic_fork_bank()
    if not bank or not candidate_ids:
        return None

    # Normalize candidate IDs to uppercase (e.g., M1, M2, NONE)
    cand_set = {str(c).upper().strip() for c in candidate_ids}

    # 1. Exact pair match
    for item in bank:
        q_cands = {str(c).upper().strip() for c in item.get("candidate_misconceptions", [])}
        if q_cands == cand_set:
            return item

    # 2. Subset match: both question candidates are within candidate list
    for item in bank:
        q_cands = {str(c).upper().strip() for c in item.get("candidate_misconceptions", [])}
        if q_cands.issubset(cand_set):
            return item

    # 3. Match top candidate with any validated discriminator
    if candidate_ids:
        primary = candidate_ids[0].upper().strip()
        for item in bank:
            q_cands = [str(c).upper().strip() for c in item.get("candidate_misconceptions", [])]
            if primary in q_cands:
                return item

    return None


def get_diagnostic_fork_by_id(question_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a specific diagnostic question by its stable ID."""
    bank = load_diagnostic_fork_bank()
    norm_id = (question_id or "").strip().upper()
    for item in bank:
        if item.get("question_id", "").upper() == norm_id:
            return item
    return None
