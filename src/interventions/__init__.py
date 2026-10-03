"""Intervention content and lookup module.

Owner: Member 2 (Physics dataset and intervention content)
Branch: member-2-data

This module fulfills the intervention lookup contract:
    get_intervention(misconception_label: str) -> dict
"""

from typing import Any, Dict, Optional

# Baseline starter intervention catalog for common physics misconceptions
INTERVENTION_CATALOG: Dict[str, Dict[str, Any]] = {
    "impetus_force_persistence": {
        "title": "Impetus Fallacy (Newton's 1st Law)",
        "explanation": (
            "Objects do not require a continuous forward force to remain in motion. "
            "According to Newton's First Law, an object continues at constant velocity "
            "unless acted upon by an external net force (such as friction or air resistance)."
        ),
        "key_concept": "Inertia & Net Force",
        "guided_hint": "Think about what happens to a hockey puck sliding on frictionless ice.",
        "reassessment_question": (
            "A satellite travels through deep space far from any stars or planets. "
            "Its engines are turned off. What happens to its speed and direction?"
        )
    },
    "heavier_objects_fall_faster": {
        "title": "Gravitational Acceleration Equivalence",
        "explanation": (
            "In the absence of air resistance, all objects accelerate towards Earth at the same rate "
            "(g ≈ 9.8 m/s²), regardless of their mass. While gravitational force is proportional to mass (F = mg), "
            "inertia also scales with mass (a = F/m = g)."
        ),
        "key_concept": "Gravitational Acceleration",
        "guided_hint": "Recall Galileo's Leaning Tower thought experiment and Apollo 15's hammer and feather drop on the Moon.",
        "reassessment_question": (
            "A 10 kg cannonball and a 1 kg wooden sphere are dropped simultaneously in a vacuum chamber. "
            "Which lands first and why?"
        )
    },
    "no_misconception_detected": {
        "title": "Correct Understanding",
        "explanation": "Your response demonstrates sound understanding of the underlying physical principles.",
        "key_concept": "Concept Mastery",
        "guided_hint": "Great job! Keep challenging yourself with deeper problems.",
        "reassessment_question": "Ready for an advanced question on this topic?"
    }
}


def get_intervention(misconception_label: str) -> Dict[str, Any]:
    """Retrieve pedagogical intervention content for a diagnosed misconception.

    Parameters
    ----------
    misconception_label : str
        The identifier of the diagnosed misconception.

    Returns
    -------
    dict
        A dictionary containing:
            - title (str)
            - explanation (str)
            - key_concept (str)
            - guided_hint (str)
            - reassessment_question (str)
            - status (str): 'found' or 'fallback'
    """
    normalized = (misconception_label or "").strip().lower()

    if normalized in INTERVENTION_CATALOG:
        data = INTERVENTION_CATALOG[normalized].copy()
        data["status"] = "found"
        return data

    return {
        "title": f"Review Concept: {misconception_label.replace('_', ' ').title()}",
        "explanation": (
            "Review the fundamental definitions and Newton's laws governing this scenario. "
            "Consider drawing a free-body diagram to trace all active forces."
        ),
        "key_concept": "Fundamental Physics Principles",
        "guided_hint": "Break down the problem into forces acting on the object at that exact instant.",
        "reassessment_question": "Explain the forces acting on the object using a free-body diagram.",
        "status": "fallback"
    }
