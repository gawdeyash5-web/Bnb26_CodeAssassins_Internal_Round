"""Intervention content and lookup module for Re:Learn.

Loads pedagogical interventions, counterexamples, real-life analogies,
and Socratic hints from the canonical physics knowledge base.
"""

import json
import os
from typing import Any, Dict, Optional
from src.data import (
    MISCONCEPTION_ID_TO_LABEL,
    MISCONCEPTION_LABEL_TO_ID,
    get_reassessment_for_misconception,
)
from src.assessment.evaluator import get_transfer_reassessment_for_context

DEFAULT_INTERVENTIONS_FILE = os.path.join("data", "intervention_bank.json")

# In-memory cached catalog
_INTERVENTIONS_CACHE: Dict[str, Dict[str, Any]] = {}


def _get_interventions_catalog() -> Dict[str, Dict[str, Any]]:
    """Load and index interventions by id, label, and normalized name."""
    global _INTERVENTIONS_CACHE
    if _INTERVENTIONS_CACHE:
        return _INTERVENTIONS_CACHE

    catalog: Dict[str, Dict[str, Any]] = {}

    if os.path.exists(DEFAULT_INTERVENTIONS_FILE):
        try:
            with open(DEFAULT_INTERVENTIONS_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                m_id = item.get("misconception_id", "")
                m_label = MISCONCEPTION_ID_TO_LABEL.get(m_id, m_id.lower())
                m_name = item.get("misconception_name", "")

                card = {
                    "misconception_id": m_id,
                    "misconception_label": m_label,
                    "misconception_name": m_name,
                    "title": f"{m_name} ({m_id})",
                    "explanation": item.get("detailed_explanation") or item.get("short_explanation", ""),
                    "short_explanation": item.get("short_explanation", ""),
                    "key_concept": m_name,
                    "common_mistake": item.get("common_mistake", ""),
                    "real_life_analogy": item.get("real_life_analogy", ""),
                    "worked_example": item.get("worked_example", ""),
                    "guided_hint": item.get("hint", ""),
                    "reassessment_question": item.get("follow_up_question", ""),
                    "reassessment_answer": item.get("follow_up_answer", ""),
                    "status": "found"
                }

                # Index by all valid representations
                catalog[m_id.lower()] = card
                catalog[m_label.lower()] = card
                catalog[m_name.lower()] = card
        except Exception:
            pass

    # Canonical entry for no_misconception_detected (correct reasoning)
    correct_card = {
        "misconception_id": "NONE",
        "misconception_label": "no_misconception_detected",
        "misconception_name": "No misconception (correct reasoning)",
        "title": "Correct Understanding and Extension",
        "explanation": "Your explanation accurately reflects canonical physics principles. Deepen your understanding by applying this law in a new physical context.",
        "short_explanation": "Correct physical reasoning demonstrated.",
        "key_concept": "Canonical Physics Principles",
        "common_mistake": "None - concept correctly applied.",
        "real_life_analogy": "A physicist correctly applying conservation laws.",
        "worked_example": "Direct application of Newton's laws.",
        "guided_hint": "Notice how the principle holds across different masses and conditions.",
        "reassessment_question": "",
        "reassessment_answer": "",
        "status": "found"
    }
    catalog["none"] = correct_card
    catalog["no_misconception_detected"] = correct_card

    _INTERVENTIONS_CACHE = catalog
    return _INTERVENTIONS_CACHE


def get_intervention(
    misconception_label: str,
    question_text: str = "",
    target_misconception_id: str = "",
) -> Dict[str, Any]:
    """Retrieve pedagogical intervention content for a diagnosed misconception.

    Ensures the attached reassessment question is a genuine, authentic transfer
    question from the question bank matching the concept being taught.
    """
    normalized = (misconception_label or "").strip().lower()
    catalog = _get_interventions_catalog()

    if normalized in catalog:
        data = catalog[normalized].copy()
    else:
        clean_title = misconception_label.replace("_", " ").title() if misconception_label else "Fundamental Physics"
        data = {
            "misconception_id": "UNKNOWN",
            "misconception_label": normalized,
            "misconception_name": clean_title,
            "title": f"Review Concept: {clean_title}",
            "explanation": (
                "Review the fundamental definitions and Newton's laws governing this scenario. "
                "Consider drawing a free-body diagram to trace all active forces."
            ),
            "short_explanation": "Review fundamental physical principles.",
            "key_concept": "Fundamental Physics Principles",
            "common_mistake": "Assuming everyday intuition applies in idealized conditions.",
            "real_life_analogy": "Looking at an object's motion through a high-speed camera to isolate external forces.",
            "worked_example": "Apply net force F_net = m * a.",
            "guided_hint": "Break down the problem into forces acting on the object at that exact instant.",
            "reassessment_question": "",
            "reassessment_answer": "",
            "status": "fallback"
        }

    # Contextually select a real transfer question from the bank
    transfer_q = get_transfer_reassessment_for_context(
        question_text=question_text,
        diagnosed_misconception_label=normalized,
        target_misconception_id=target_misconception_id or data.get("misconception_id", ""),
    )

    if transfer_q:
        data["reassessment_question"] = transfer_q.get("question", "")
        data["reassessment_answer"] = transfer_q.get("correct_answer", "")
        data["reassessment_id"] = transfer_q.get("reassessment_id", "")
    elif not data.get("reassessment_question"):
        reassess = get_reassessment_for_misconception(normalized)
        if reassess:
            data["reassessment_question"] = reassess.get("question", "")
            data["reassessment_answer"] = reassess.get("correct_answer", "")
            data["reassessment_id"] = reassess.get("reassessment_id", "")

    return data
