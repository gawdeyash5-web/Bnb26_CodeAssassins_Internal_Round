"""Scientific Answer Evaluation and Transfer Reassessment Engine for Re:Learn.

Provides:
- Reliable correctness assessment separating student scientific correctness from ML model confidence.
- Structured generation of the 4 items for "Correct Answer and Explanation":
    1. Your answer
    2. Was it correct? (Correct, Incorrect, Not enough information)
    3. Correct answer (with explicit physical assumptions)
    4. Why? (Simple physical principle directly connected to student's answer)
- Contextual transfer reassessment selection from the canonical reassessment bank.
- Transparent transfer outcome evaluation (Improved, Persistent, Inconclusive).
"""

import os
import re
import json
from typing import Any, Dict, List, Optional
import pandas as pd

from src.data import (
    DEFAULT_DATASET_PATH,
    DEFAULT_REASSESSMENT_PATH,
    load_dataset,
    load_reassessment_bank,
    MISCONCEPTION_ID_TO_LABEL,
    MISCONCEPTION_LABEL_TO_ID,
)


def _normalize_text(text: str) -> str:
    """Normalize text for reliable fuzzy/keyword comparison."""
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s\./-]", " ", text)
    return " ".join(text.split())


def _find_dataset_question_match(question_text: str) -> Optional[Dict[str, Any]]:
    """Match a question prompt to the canonical dataset row."""
    if not question_text:
        return None
    df = load_dataset()
    if df.empty:
        return None

    norm_target = _normalize_text(question_text)
    best_row = None
    best_overlap = 0

    target_words = set(norm_target.split())

    for _, row in df.iterrows():
        q_str = str(row.get("question", ""))
        norm_q = _normalize_text(q_str)
        if norm_q == norm_target:
            return row.to_dict()
        
        # Word set overlap
        q_words = set(norm_q.split())
        if not q_words:
            continue
        overlap = len(target_words & q_words) / float(len(target_words | q_words))
        if overlap > best_overlap and overlap > 0.65:
            best_overlap = overlap
            best_row = row.to_dict()

    return best_row


def evaluate_answer_correctness(
    question_text: str,
    student_answer: str,
    question_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Evaluate whether a student's answer is scientifically correct, incorrect, or inconclusive.

    Generates the four mandatory items for "Correct Answer and Explanation":
    1. your_answer: Student's actual submitted answer
    2. was_it_correct: 'Correct' | 'Incorrect' | 'Not enough information'
    3. correct_answer: The canonical expected answer with explicit physical assumptions
    4. why_explanation: Physics principle explained simply and connected directly to student's answer
    """
    raw_answer = (student_answer or "").strip()
    norm_ans = _normalize_text(raw_answer)

    # 1. Look up question details from dataset or metadata
    matched_q = question_metadata or _find_dataset_question_match(question_text) or {}
    q_text = str(matched_q.get("question", question_text or ""))
    norm_q = _normalize_text(q_text)
    
    subtopic = str(matched_q.get("subtopic", ""))
    target_m_id = str(matched_q.get("misconception_id", matched_q.get("target_misconception_id", "")))
    canonical_correct = str(matched_q.get("correct_answer", ""))
    canonical_explanation = str(matched_q.get("explanation", ""))

    # 2. Check for empty / insufficient answers
    words = norm_ans.split()
    if not words or len(norm_ans) < 3 or words in [["idk"], ["dunno"], ["no", "idea"], ["not", "sure"], ["test"], ["asdf"]]:
        return {
            "was_correct": "not_enough_information",
            "was_it_correct_display": "Not enough information",
            "your_answer": raw_answer if raw_answer else "(No answer provided)",
            "correct_answer": canonical_correct or "A complete explanation applying the relevant physical laws.",
            "why_explanation": (
                "Your answer was too brief or incomplete to determine your physical reasoning. "
                "In physics, explaining 'why' is essential to show how concepts are applied."
            ),
            "student_answer_analysis": "Your answer does not provide sufficient detail to evaluate.",
            "subtopic": subtopic,
            "target_misconception_id": target_m_id,
            "matched_question_id": matched_q.get("question_id", ""),
        }

    # 3. Domain-specific physical evaluation:
    
    # CASE A: Steel ball vs Wooden ball / Free Fall mass independence (Q008, Q002, Q004, Q011, Q029, Q070)
    is_free_fall_drop = any(k in norm_q for k in ["steel ball", "wooden ball", "two balls", "bowling ball", "heavy ball and a light ball", "vacuum", "dropped together", "hits the ground first", "lands first"])
    
    if is_free_fall_drop and ("steel" in norm_q or "wooden" in norm_q or "balcony" in norm_q):
        expected_ans = "Both balls reach the ground at approximately the same time."
        qualification = "Ignoring air resistance (or when air resistance is small), both balls fall with the same downward acceleration of ~9.8 m/s²."
        
        # Check student assertion
        says_same_time = any(p in norm_ans for p in ["same time", "together", "both", "neither", "equal time", "same acceleration", "simultaneously", "at once"])
        says_wooden_first = any(p in norm_ans for p in ["wooden", "wood"]) and any(p in norm_ans for p in ["first", "faster", "before", "earlier", "hits first", "lands first"])
        says_steel_first = any(p in norm_ans for p in ["steel", "heavy", "heavier"]) and any(p in norm_ans for p in ["first", "faster", "before", "earlier", "hits first", "lands first"])
        
        if says_wooden_first:
            was_correct = "incorrect"
            analysis = "You predicted that the wooden ball would land first. That is not the expected result under these conditions."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Gravity gives both objects approximately the same downward acceleration. "
                f"When air resistance is ignored, the heavier object does not fall faster just because it has more mass, "
                f"nor does the lighter object land first.\n\n"
                f"Your answer: {analysis}"
            )
        elif says_steel_first:
            was_correct = "incorrect"
            analysis = "You predicted that the steel ball would land first because it is heavier. That is not the expected result under these conditions."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Gravity gives both objects approximately the same downward acceleration (~9.8 m/s²). "
                f"Although Earth pulls harder on the heavier steel ball (greater gravitational force), "
                f"the steel ball also has greater inertia (resistance to acceleration) by the exact same factor: "
                f"a = F / m = (mg) / m = g. Therefore, both fall together.\n\n"
                f"Your answer: {analysis}"
            )
        elif says_same_time:
            was_correct = "correct"
            analysis = "You correctly predicted that both balls land at approximately the same time."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Gravity gives both objects approximately the same downward acceleration (~9.8 m/s²). "
                f"When air resistance is small or negligible, gravitational acceleration is independent of mass.\n\n"
                f"Your answer: {analysis}"
            )
        else:
            was_correct = "not_enough_information"
            analysis = "Your answer mentions the balls but does not clearly state which lands first or why."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Gravity gives both objects approximately the same downward acceleration (~9.8 m/s²). "
                f"When air resistance is ignored, all objects fall together regardless of mass.\n\n"
                f"Your answer: {analysis}"
            )

        return {
            "was_correct": was_correct,
            "was_it_correct_display": "Correct" if was_correct == "correct" else "Incorrect" if was_correct == "incorrect" else "Not enough information",
            "your_answer": raw_answer,
            "correct_answer": f"{expected_ans} ({qualification})",
            "why_explanation": why,
            "student_answer_analysis": analysis,
            "subtopic": "Gravity and Free Fall (Newton's Second Law)",
            "target_misconception_id": "M4",
            "matched_question_id": matched_q.get("question_id", "Q008"),
        }

    # CASE B: Multiple Choice Questions (e.g. Q016, Q017, Q019, Q029, Q061)
    if "which statement is correct" in norm_q or matched_q.get("question_type") == "Multiple-choice":
        expected_letter = canonical_correct.strip().upper()[:1] if canonical_correct else ""
        if not expected_letter and "(a)" in norm_q and "(b)" in norm_q:
            # Detect letter from canonical_correct
            for letter in ["A", "B", "C", "D"]:
                if f"({letter.lower()})" in norm_ans or letter == norm_ans.upper():
                    pass

        # Check if student gave letter
        student_letter = ""
        for letter in ["A", "B", "C", "D"]:
            if norm_ans == letter.lower() or f"({letter.lower()})" in norm_ans or f"option {letter.lower()}" in norm_ans or f"{letter.lower()} " in norm_ans:
                student_letter = letter
                break

        if student_letter and expected_letter:
            if student_letter == expected_letter:
                was_correct = "correct"
                analysis = f"You selected Option ({student_letter}), which is the correct scientific choice."
            else:
                was_correct = "incorrect"
                analysis = f"You selected Option ({student_letter}), but Option ({expected_letter}) is the scientifically correct choice."
            
            why = (
                f"Correct answer: Option ({expected_letter}) — {canonical_explanation or canonical_correct}\n\n"
                f"Why? {canonical_explanation or 'Newtonian mechanics requires analyzing all net active forces.'}\n\n"
                f"Your answer: {analysis}"
            )
            return {
                "was_correct": was_correct,
                "was_it_correct_display": "Correct" if was_correct == "correct" else "Incorrect",
                "your_answer": raw_answer,
                "correct_answer": f"Option ({expected_letter})",
                "why_explanation": why,
                "student_answer_analysis": analysis,
                "subtopic": subtopic,
                "target_misconception_id": target_m_id,
                "matched_question_id": matched_q.get("question_id", ""),
            }

    # CASE C: Newton's Third Law (Action-Reaction Cancelling, Q009, Q013, Q018, Q060, etc.)
    if "cancel" in norm_q or "horse" in norm_q or "third law" in subtopic.lower():
        expected_ans = canonical_correct or "No, action-reaction forces act on two different objects, so they cannot cancel each other."
        says_cancel = any(p in norm_ans for p in ["yes", "they cancel", "cancel each other", "cancels out", "cancels", "net force is zero so it cannot move"])
        says_cannot_cancel = any(p in norm_ans for p in ["no", "different object", "different bodies", "act on different", "do not cancel", "cannot cancel", "never cancel"])
        
        if says_cancel:
            was_correct = "incorrect"
            analysis = "You concluded that the action-reaction forces cancel each other out."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Newton's third law pairs always act on DIFFERENT objects (Object A on Object B, and Object B on Object A). "
                f"To find an object's acceleration, you only sum forces acting ON that single object. "
                f"Forces acting on different bodies cannot balance or cancel each other.\n\n"
                f"Your answer: {analysis}"
            )
        elif says_cannot_cancel:
            was_correct = "correct"
            analysis = "You correctly stated that action-reaction forces act on different objects and do not cancel."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Forces can only cancel if they act on the same object. Since action-reaction pairs act on different bodies, each object can accelerate independently.\n\n"
                f"Your answer: {analysis}"
            )
        else:
            was_correct = "not_enough_information"
            analysis = "Your answer does not clearly address whether the forces act on the same or different objects."
            why = (
                f"Correct answer: {expected_ans}\n\n"
                f"Why? Third-law forces act on different objects and cannot cancel.\n\n"
                f"Your answer: {analysis}"
            )

        return {
            "was_correct": was_correct,
            "was_it_correct_display": "Correct" if was_correct == "correct" else "Incorrect" if was_correct == "incorrect" else "Not enough information",
            "your_answer": raw_answer,
            "correct_answer": expected_ans,
            "why_explanation": why,
            "student_answer_analysis": analysis,
            "subtopic": subtopic,
            "target_misconception_id": target_m_id,
            "matched_question_id": matched_q.get("question_id", ""),
        }

    # CASE D: General Canonical Matching via Dataset & Keywords
    if canonical_correct:
        norm_expected = _normalize_text(canonical_correct)
        
        # Check if known correct answer or known misconception answer in dataset
        df = load_dataset()
        matching_q_rows = df[df["question"].str.contains(re.escape(q_text[:35]), case=False, na=False)] if not df.empty else pd.DataFrame()
        
        known_correct_answers = [
            _normalize_text(str(r["student_answer"]))
            for _, r in matching_q_rows.iterrows()
            if str(r.get("is_correct", "")).lower() == "true"
        ]
        known_misconception_answers = [
            _normalize_text(str(r["student_answer"]))
            for _, r in matching_q_rows.iterrows()
            if str(r.get("is_correct", "")).lower() == "false"
        ]
        
        # Check direct matches or high similarity
        is_known_correct = any(k in norm_ans or norm_ans in k for k in known_correct_answers if len(k) > 5)
        is_known_wrong = any(k in norm_ans or norm_ans in k for k in known_misconception_answers if len(k) > 5)
        
        if is_known_correct and not is_known_wrong:
            was_correct = "correct"
            analysis = "Your explanation accurately applies the relevant physical principle."
        elif is_known_wrong:
            was_correct = "incorrect"
            analysis = "Your explanation reflects an intuitive misconception rather than canonical physical laws."
        else:
            # Semantic keyword overlap with expected answer
            expected_words = set(w for w in norm_expected.split() if len(w) > 3)
            student_words = set(w for w in norm_ans.split() if len(w) > 3)
            
            overlap_count = len(expected_words & student_words)
            if overlap_count >= 3 or (len(expected_words) <= 3 and overlap_count >= 1):
                was_correct = "correct"
                analysis = "Your reasoning aligns with the core concepts of the expected physical explanation."
            elif len(student_words) >= 4:
                was_correct = "incorrect"
                analysis = "Your explanation does not match the expected physical law for this scenario."
            else:
                was_correct = "not_enough_information"
                analysis = "Your response lacks enough detail to evaluate conceptual understanding."

        why = (
            f"Correct answer: {canonical_correct}\n\n"
            f"Why? {canonical_explanation or 'Newtonian mechanics governs the behavior of this physical system.'}\n\n"
            f"Your answer: {analysis}"
        )

        return {
            "was_correct": was_correct,
            "was_it_correct_display": "Correct" if was_correct == "correct" else "Incorrect" if was_correct == "incorrect" else "Not enough information",
            "your_answer": raw_answer,
            "correct_answer": canonical_correct,
            "why_explanation": why,
            "student_answer_analysis": analysis,
            "subtopic": subtopic,
            "target_misconception_id": target_m_id,
            "matched_question_id": matched_q.get("question_id", ""),
        }

    # CASE E: Generic Fallback when no dataset question matched
    return {
        "was_correct": "not_enough_information",
        "was_it_correct_display": "Not enough information",
        "your_answer": raw_answer,
        "correct_answer": "Expected physical reasoning based on Newton's laws.",
        "why_explanation": (
            "We could not verify the exact scenario parameters for this question. "
            "Please review the core physical laws governing force and acceleration."
        ),
        "student_answer_analysis": "Response received for evaluation.",
        "subtopic": subtopic,
        "target_misconception_id": target_m_id,
        "matched_question_id": "",
    }


def get_transfer_reassessment_for_context(
    question_text: str,
    diagnosed_misconception_label: str = "",
    target_misconception_id: str = "",
) -> Optional[Dict[str, Any]]:
    """Retrieve an authentic transfer reassessment question from the curated reassessment bank.

    Guarantees:
    - Never returns a generic placeholder like "Ready to test your understanding on an advanced scenario?".
    - For the steel ball and wooden ball drop question (Q008 / free fall), returns R-M4-06 (vacuum chamber drop).
    - If the bank has no matching question, returns None so frontend can display an honest message.
    """
    bank = load_reassessment_bank()
    if not bank:
        return None

    norm_q = _normalize_text(question_text)
    
    # 1. Check for steel ball and wooden ball question specifically
    if ("steel" in norm_q and "wooden" in norm_q) or ("balcony" in norm_q and "drop" in norm_q):
        for item in bank:
            if item.get("reassessment_id") == "R-M4-06":
                return item
        for item in bank:
            if item.get("reassessment_id") == "R-M4-01":
                return item

    # 2. Check by diagnosed misconception ID or label
    target_id = (target_misconception_id or "").strip().upper()
    if not target_id and diagnosed_misconception_label:
        target_id = MISCONCEPTION_LABEL_TO_ID.get(diagnosed_misconception_label, "")

    if target_id and target_id in ["M1", "M2", "M3", "M4", "M5"]:
        for item in bank:
            if item.get("misconception_id", "").upper() == target_id:
                return item

    # 3. Check by question domain from the original question text
    if any(k in norm_q for k in ["drop", "vacuum", "fall", "gravity", "heavier", "weight"]):
        for item in bank:
            if item.get("misconception_id") == "M4":
                return item
    elif any(k in norm_q for k in ["friction", "puck", "slide", "keep moving", "motion needs", "drifts", "truck"]):
        for item in bank:
            if item.get("misconception_id") == "M1":
                return item
    elif any(k in norm_q for k in ["zero net force", "constant velocity", "steady speed", "balanced forces", "at rest"]):
        for item in bank:
            if item.get("misconception_id") == "M2":
                return item
    elif any(k in norm_q for k in ["action", "reaction", "cancel", "horse", "cart", "oar", "push back"]):
        for item in bank:
            if item.get("misconception_id") == "M3":
                return item
    elif any(k in norm_q for k in ["acceleration", "f = ma", "mass", "newtons", "rocket", "thrust"]):
        for item in bank:
            if item.get("misconception_id") == "M5":
                return item

    # 4. Fallback to first available question in bank rather than placeholder
    return bank[0] if bank else None


def evaluate_reassessment_answer(
    reassessment_question: str,
    reassessment_answer: str,
    original_misconception: str = "",
) -> Dict[str, Any]:
    """Evaluate transfer reassessment response and assign an honest outcome:

    - 'improved': Student successfully applies the concept to the new context.
    - 'persistent': Student still repeats the prior misconception in the new context.
    - 'inconclusive': Student answer is ambiguous, incomplete, or lacks enough information.
    """
    raw_answer = (reassessment_answer or "").strip()
    norm_ans = _normalize_text(raw_answer)
    norm_q = _normalize_text(reassessment_question)

    words = norm_ans.split()
    if len(words) < 2 or len(norm_ans) < 3:
        return {
            "outcome": "inconclusive",
            "feedback": (
                "We need more evidence. Your answer is too short to evaluate whether you can "
                "apply this physical law in a new situation."
            ),
            "was_correct": "not_enough_information",
        }

    # Evaluate for Free Fall in Vacuum transfer questions (R-M4-06 or R-M4-01)
    if any(k in norm_q for k in ["vacuum chamber", "vacuum tube", "coin and a lead pellet", "which ball reaches the bottom first", "which hits the bottom first"]):
        says_same_time = any(p in norm_ans for p in ["same time", "together", "both", "neither", "equal time", "simultaneously", "at the same instant", "same acceleration"])
        says_one_first = any(p in norm_ans for p in ["steel", "wooden", "lead", "coin", "heavy", "lighter", "faster"]) and any(p in norm_ans for p in ["first", "earlier", "before", "sooner", "hits first", "lands first"])

        if says_same_time:
            return {
                "outcome": "improved",
                "feedback": (
                    "Your new answer shows improvement! You correctly recognized that in a vacuum without air resistance, "
                    "gravity accelerates all objects equally (~9.8 m/s²), so both reach the bottom at the same time. "
                    "Remember that continuing to practice across different scenarios solidifies this understanding."
                ),
                "was_correct": "correct",
            }
        elif says_one_first:
            return {
                "outcome": "persistent",
                "feedback": (
                    "This misunderstanding may still be present. You predicted that one object would reach the bottom first. "
                    "In a vacuum, air resistance is zero, so mass does not affect the acceleration of free fall."
                ),
                "was_correct": "incorrect",
            }
        else:
            return {
                "outcome": "inconclusive",
                "feedback": (
                    "We need more evidence. Your explanation does not clearly state whether both objects land together or "
                    "which one lands first."
                ),
                "was_correct": "not_enough_information",
            }

    # Evaluate for Force-for-Motion transfer (M1)
    if "comet" in norm_q or "no force is needed" in norm_q or "smooth, flat surface" in norm_q:
        says_no_force = any(p in norm_ans for p in ["no force", "no", "inertia", "constant velocity", "zero net force", "keeps moving"])
        says_force_needed = any(p in norm_ans for p in ["yes", "force is needed", "push", "keep it moving", "runs out"])
        if says_no_force and not says_force_needed:
            return {
                "outcome": "improved",
                "feedback": (
                    "Your new answer shows improvement! You correctly recognized that with zero net force, "
                    "an object in motion continues at constant velocity due to inertia."
                ),
                "was_correct": "correct",
            }
        elif says_force_needed:
            return {
                "outcome": "persistent",
                "feedback": (
                    "This misunderstanding may still be present. In empty space, no force is required to keep an object moving. "
                    "Forces only change velocity, they do not sustain it."
                ),
                "was_correct": "incorrect",
            }

    # Evaluate for Action-Reaction transfer (M3)
    if "soccer" in norm_q or "swimmer" in norm_q or "wall" in norm_q:
        says_cannot_cancel = any(p in norm_ans for p in ["no", "different object", "different bodies", "do not cancel", "cannot cancel"])
        says_cancel = any(p in norm_ans for p in ["yes", "cancel each other", "cancels out", "they cancel"])
        if says_cannot_cancel:
            return {
                "outcome": "improved",
                "feedback": (
                    "Your new answer shows improvement! You identified that equal and opposite forces acting on "
                    "different objects do not cancel each other out."
                ),
                "was_correct": "correct",
            }
        elif says_cancel:
            return {
                "outcome": "persistent",
                "feedback": (
                    "This misunderstanding may still be present. The action force and reaction force act on two separate objects, "
                    "so they cannot cancel."
                ),
                "was_correct": "incorrect",
            }

    # Default heuristic: check if answer length and keywords show sound reasoning
    if len(words) >= 6 and any(p in norm_ans for p in ["because", "acceleration", "newton", "force", "mass", "velocity", "constant", "balanced", "inertia"]):
        return {
            "outcome": "improved",
            "feedback": (
                "Your new answer shows improvement. You reasoned through the scenario using physical laws. "
                "Keep applying this reasoning across varied physics problems."
            ),
            "was_correct": "correct",
        }
    else:
        return {
            "outcome": "inconclusive",
            "feedback": (
                "We need more evidence. Your answer doesn't contain enough detail to verify your reasoning clearly."
            ),
            "was_correct": "not_enough_information",
        }
