"""FastAPI backend API service for Re:Learn physics misconception tutor.

Connects the React frontend to the Python ML diagnostic pipeline,
data layer, interventions catalog, and learner history tracker.
"""

from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.data import (
    load_questions,
    load_misconceptions_taxonomy,
    load_reassessment_bank,
    load_dataset,
    load_diagnostic_fork_bank,
    find_diagnostic_fork_question,
    get_diagnostic_fork_by_id,
    MISCONCEPTION_LABEL_TO_ID,
    MISCONCEPTION_ID_TO_LABEL
)
from src.interventions import get_intervention
from src.learner import (
    record_attempt,
    update_attempt_reassessment,
    update_attempt_diagnostic_fork,
    get_learner_history,
    clear_learner_history
)
from src.ml.diagnose import diagnose, CONFIDENCE_THRESHOLD, LABEL_TO_INFO
from src.assessment import (
    evaluate_answer_correctness,
    evaluate_reassessment_answer,
    get_transfer_reassessment_for_context,
)

app = FastAPI(
    title="Re:Learn Physics Misconception Diagnostic API",
    description="Backend API powering AI-driven misconception identification, targeted pedagogy, and conceptual reassessment.",
    version="1.0.0"
)

# Enable CORS for React frontend (Vite default is localhost:5173 / localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request & Response Models ---

class DiagnoseRequest(BaseModel):
    question: str = Field(..., description="The conceptual physics scenario prompt.")
    student_answer: str = Field(..., description="Student's free-text explanation.")
    learner_id: str = Field(default="student_01", description="Identifier for learner session.")


class ReassessRequest(BaseModel):
    learner_id: str = Field(default="student_01")
    attempt_index: int = Field(default=-1, description="Index of attempt to update, or -1 for most recent.")
    reassessment_question: str = Field(..., description="Transfer reassessment prompt.")
    reassessment_answer: str = Field(..., description="Student's explanation on transfer question.")
    original_misconception: str = Field(..., description="The initially diagnosed misconception label.")


class DiagnosticForkEvaluateRequest(BaseModel):
    learner_id: str = Field(default="student_01")
    attempt_index: int = Field(default=-1, description="Index of attempt to update, or -1 for most recent.")
    question_id: str = Field(..., description="ID of diagnostic fork question.")
    selected_choice_id: str = Field(..., description="Selected option key ('A', 'B', 'C', 'D').")
    reasoning_text: Optional[str] = Field(default="", description="Optional free-text rationale given by student.")


# --- Endpoints ---

@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Return system readiness, dataset size, and model status."""
    df = load_dataset()
    return {
        "status": "online",
        "service": "Re:Learn AI Diagnostic Engine",
        "dataset_samples": len(df),
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "taxonomy_classes": ["M1", "M2", "M3", "M4", "M5", "NONE"]
    }


@app.get("/api/questions")
def get_questions() -> List[Dict[str, Any]]:
    """Return all curated diagnostic questions from the canonical dataset."""
    questions = load_questions()
    if not questions:
        raise HTTPException(status_code=404, detail="No diagnostic questions found in knowledge base.")
    return questions


@app.get("/api/taxonomy")
def get_taxonomy() -> List[Dict[str, Any]]:
    """Return the complete physics misconception taxonomy and physical principles."""
    return load_misconceptions_taxonomy()


@app.get("/api/diagnostic-fork/questions")
def get_diagnostic_fork_questions() -> List[Dict[str, Any]]:
    """Return all curated diagnostic questions used for investigatory follow-ups."""
    return load_diagnostic_fork_bank()


@app.post("/api/diagnose")
def run_diagnosis(payload: DiagnoseRequest) -> Dict[str, Any]:
    """Execute ML diagnosis on student answer, check for diagnostic fork eligibility, and record attempt."""
    cleaned_ans = payload.student_answer.strip()
    
    # 1. Run diagnostic classifier
    diag_result = diagnose(payload.question, cleaned_ans)
    misconception_label = diag_result.get("misconception_label", "unknown")
    status = diag_result.get("status", "unknown")
    confidence = diag_result.get("confidence_score", 0.0)
    probabilities = diag_result.get("probabilities", {})

    # 2. Evaluate scientific correctness independently of ML classifier confidence
    eval_result = evaluate_answer_correctness(payload.question, cleaned_ans)
    was_correct = eval_result.get("was_correct", "not_enough_information")
    target_m_id = eval_result.get("target_misconception_id", "")

    # Save raw model outputs for technical inspection
    diag_result["raw_model_prediction"] = misconception_label
    diag_result["raw_confidence_score"] = confidence

    # 3. Apply Pedagogical Safeguards (BUG 2):
    # A scientifically incorrect answer must NEVER be presented as sound reasoning or no_misconception_detected!
    if was_correct == "incorrect":
        if misconception_label == "no_misconception_detected" or confidence < CONFIDENCE_THRESHOLD or status == "uncertain":
            diag_result["misconception_label"] = "uncertain_misunderstanding"
            diag_result["misconception_id"] = target_m_id or "UNCERTAIN"
            diag_result["misconception_name"] = "Potential Misunderstanding"
            diag_result["status"] = "uncertain"
            diag_result["explanation"] = "You may have a misunderstanding here. We couldn't identify the exact reason from this answer yet."
            misconception_label = "uncertain_misunderstanding"
            status = "uncertain"
    elif was_correct == "not_enough_information":
        diag_result["status"] = "uncertain"
        diag_result["explanation"] = "We're not sure yet. Let's check your thinking with one more question."
        status = "uncertain"
    elif was_correct == "correct":
        diag_result["misconception_label"] = "no_misconception_detected"
        diag_result["misconception_id"] = "NONE"
        diag_result["misconception_name"] = "Canonical scientific understanding"
        diag_result["status"] = "success"
        diag_result["explanation"] = "Your answer looks correct based on canonical physics principles."
        misconception_label = "no_misconception_detected"
        status = "success"

    # Attach evaluation to diagnosis object
    diag_result["answer_evaluation"] = eval_result
    diag_result["was_correct"] = was_correct

    # 4. Fetch initial pedagogical intervention and authentic reassessment question
    intervention = get_intervention(
        misconception_label=misconception_label if misconception_label != "uncertain_misunderstanding" else (target_m_id or "M4"),
        question_text=payload.question,
        target_misconception_id=target_m_id,
    )

    # 5. Determine Diagnostic Fork eligibility based on explicit uncertainty rules
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    top_candidates = []
    fork_question = None
    is_fork_eligible = False
    fork_reason = ""

    if was_correct in ["incorrect", "not_enough_information"] or status == "uncertain" or confidence < CONFIDENCE_THRESHOLD:
        candidate_pool = []
        if target_m_id:
            candidate_pool.append(target_m_id)
        for lbl, _ in sorted_probs:
            c_id = MISCONCEPTION_LABEL_TO_ID.get(lbl, lbl)
            if c_id not in candidate_pool:
                candidate_pool.append(c_id)
        if "NONE" not in candidate_pool:
            candidate_pool.append("NONE")

        fork_question = find_diagnostic_fork_question(candidate_pool[:3])
        if fork_question:
            is_fork_eligible = True
            top_candidates = fork_question.get("candidate_misconceptions", candidate_pool[:2])
            fork_reason = (
                "One More Question to Understand Your Thinking: "
                "We noticed multiple interpretations in your answer. "
                "Let's explore a targeted scenario to clarify your physical reasoning."
            )
        else:
            fork_reason = (
                "Additional evidence is needed to clarify your reasoning. Proceeding with guided explanation."
            )
    elif len(sorted_probs) >= 2:
        top_lbl, top_p = sorted_probs[0]
        second_lbl, second_p = sorted_probs[1]
        top_id = MISCONCEPTION_LABEL_TO_ID.get(top_lbl, top_lbl)
        second_id = MISCONCEPTION_LABEL_TO_ID.get(second_lbl, second_lbl)
        top_candidates = [top_id, second_id]
        prob_gap = round(top_p - second_p, 4)
        if prob_gap < 0.15:
            fork_question = find_diagnostic_fork_question([top_id, second_id])
            if fork_question:
                is_fork_eligible = True
                fork_reason = f"Multiple plausible interpretations detected ({top_id} vs {second_id}). A clarifying probe is recommended."
        else:
            fork_reason = f"Initial diagnosis sufficiently supported ({confidence * 100:.1f}% probability)."

    diagnostic_fork_meta = {
        "eligible": is_fork_eligible,
        "reason": fork_reason,
        "candidates": top_candidates,
        "question": fork_question
    }

    # Record attempt in session history
    attempt = record_attempt(
        learner_id=payload.learner_id,
        question=payload.question,
        student_answer=cleaned_ans,
        diagnosis=diag_result,
        intervention=intervention
    )

    # Attach diagnostic fork eligibility info to the attempt
    attempt["diagnostic_fork_eligible"] = is_fork_eligible
    if is_fork_eligible and fork_question:
        attempt["diagnostic_fork_status"] = "available"
        attempt["diagnostic_fork_question_id"] = fork_question.get("question_id")
        attempt["diagnostic_fork_scenario_title"] = fork_question.get("scenario_title")
        attempt["diagnostic_fork_question"] = fork_question.get("question")
        attempt["diagnostic_fork_candidates"] = top_candidates
        attempt["diagnostic_fork_explanation"] = fork_reason
    else:
        attempt["diagnostic_fork_status"] = "not_needed" if confidence >= CONFIDENCE_THRESHOLD and was_correct == "correct" else "no_question_available"
        attempt["diagnostic_fork_explanation"] = fork_reason

    return {
        "diagnosis": diag_result,
        "intervention": intervention,
        "attempt": attempt,
        "diagnostic_fork": diagnostic_fork_meta,
        "answer_evaluation": eval_result,
    }


@app.post("/api/diagnostic-fork/evaluate")
def evaluate_diagnostic_fork(payload: DiagnosticForkEvaluateRequest) -> Dict[str, Any]:
    """Evaluate student response to a diagnostic fork follow-up question.

    Refines diagnosis based on transparent evidence rules, updates attempt in-place,
    and returns tailored intervention for the refined misconception.
    """
    question = get_diagnostic_fork_by_id(payload.question_id)
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"Diagnostic question with ID '{payload.question_id}' not found in question bank."
        )

    # Find the chosen option
    chosen_choice = None
    target_id = payload.selected_choice_id.strip().upper()
    for choice in question.get("choices", []):
        if choice.get("choice_id", "").upper() == target_id:
            chosen_choice = choice
            break

    if not chosen_choice:
        valid_keys = [c.get("choice_id") for c in question.get("choices", [])]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid choice '{payload.selected_choice_id}'. Available choices: {valid_keys}"
        )

    supp_id = chosen_choice.get("supported_misconception_id", "INCONCLUSIVE")
    supp_label = chosen_choice.get("supported_misconception_label", "inconclusive")
    evidence_type = chosen_choice.get("evidence_type", "ambiguous")
    interpretation = chosen_choice.get("diagnostic_interpretation", "")

    # Explicit, evidence-based refinement rules
    # 1. Canonical reasoning (NONE)
    if supp_id == "NONE":
        refined_id = "NONE"
        refined_label = "no_misconception_detected"
        refined_status = "success"
        refined_confidence = 0.85
        evidence_summary = (
            f"Your follow-up choice ({chosen_choice['choice_id']}) demonstrates canonical scientific reasoning: "
            f"{interpretation}"
        )
    # 2. Specific Misconception (M1, M2, M3, M4, M5)
    elif supp_id in ["M1", "M2", "M3", "M4", "M5"]:
        refined_id = supp_id
        refined_label = MISCONCEPTION_ID_TO_LABEL.get(supp_id, supp_label)
        refined_status = "success"
        refined_confidence = 0.82 if evidence_type == "strong_support" else 0.74
        m_info = LABEL_TO_INFO.get(refined_label, {"name": refined_id})
        evidence_summary = (
            f"Your follow-up choice ({chosen_choice['choice_id']}) confirms the misconception '{m_info['name']}': "
            f"{interpretation}"
        )
    # 3. Inconclusive or ambiguous
    else:
        refined_id = "INCONCLUSIVE"
        refined_label = "uncertain_reasoning"
        refined_status = "uncertain"
        refined_confidence = 0.35
        evidence_summary = (
            f"Your follow-up response ({chosen_choice['choice_id']}) remains inconclusive: "
            f"{interpretation} Additional evidence is required to pinpoint your mental model."
        )

    # Fetch updated pedagogical intervention for the refined misconception
    intervention = get_intervention(refined_label)

    fork_update = {
        "status": "completed" if supp_id != "INCONCLUSIVE" else "inconclusive",
        "question_id": question.get("question_id"),
        "scenario_title": question.get("scenario_title"),
        "question": question.get("question"),
        "candidates": question.get("candidate_misconceptions", []),
        "selected_choice_id": chosen_choice.get("choice_id"),
        "selected_text": chosen_choice.get("text"),
        "evidence_type": evidence_type,
        "interpretation": interpretation,
        "refined_label": refined_label,
        "refined_id": refined_id,
        "refined_confidence": refined_confidence,
        "refined_status": refined_status,
        "explanation": evidence_summary,
        "intervention": intervention
    }

    # Update attempt in-place (preserves identity without creating duplicate attempts)
    updated_attempt = update_attempt_diagnostic_fork(
        learner_id=payload.learner_id,
        attempt_index=payload.attempt_index,
        fork_data=fork_update
    )

    refined_diag = {
        "misconception_label": refined_label,
        "misconception_id": refined_id,
        "misconception_name": LABEL_TO_INFO.get(refined_label, {}).get("name", refined_id),
        "confidence_score": refined_confidence,
        "status": refined_status,
        "explanation": evidence_summary,
        "evidence_type": evidence_type,
        "interpretation": interpretation
    }

    return {
        "refined_diagnosis": refined_diag,
        "evidence_summary": evidence_summary,
        "post_answer_explanation": question.get("post_answer_explanation", ""),
        "intervention": intervention,
        "attempt": updated_attempt
    }


@app.post("/api/reassess")
def evaluate_reassessment(payload: ReassessRequest) -> Dict[str, Any]:
    """Evaluate student's transfer reassessment answer, determine outcome, and update attempt in-place."""
    cleaned_ans = payload.reassessment_answer.strip()
    if not cleaned_ans:
        raise HTTPException(status_code=400, detail="Reassessment answer cannot be empty.")

    # 1. Run ML diagnostic classifier for telemetry and technical audit
    reassess_diag = diagnose(payload.reassessment_question, cleaned_ans)

    # 2. Evaluate transfer reassessment with authentic pedagogical resolution rules
    reassess_eval = evaluate_reassessment_answer(
        reassessment_question=payload.reassessment_question,
        reassessment_answer=cleaned_ans,
        original_misconception=payload.original_misconception,
    )
    outcome = reassess_eval.get("outcome", "inconclusive")
    feedback = reassess_eval.get("feedback", "Your response has been evaluated.")

    # 3. Update the original attempt in place (no duplicate records)
    updated_attempt = update_attempt_reassessment(
        learner_id=payload.learner_id,
        attempt_index=payload.attempt_index,
        reassessment_completed=True,
        reassessment_outcome=outcome,
        reassessment_answer=cleaned_ans,
        reassessment_feedback=feedback,
        reassessment_question=payload.reassessment_question
    )

    return {
        "outcome": outcome,
        "feedback": feedback,
        "reassessment_diagnosis": reassess_diag,
        "reassessment_evaluation": reassess_eval,
        "attempt": updated_attempt
    }


@app.get("/api/history/{learner_id}")
def fetch_learner_history(learner_id: str) -> List[Dict[str, Any]]:
    """Retrieve full chronological learning progress for a student."""
    return get_learner_history(learner_id)


@app.delete("/api/history/{learner_id}")
def reset_learner_history(learner_id: str) -> Dict[str, str]:
    """Reset learning session history for a student."""
    clear_learner_history(learner_id)
    return {"message": f"History cleared for learner '{learner_id}'."}


@app.get("/api/attempts/{learner_id}/{attempt_index}")
def get_learner_attempt(learner_id: str, attempt_index: int) -> Dict[str, Any]:
    """Retrieve a specific attempt record for Misconception X-Ray inspection."""
    history = get_learner_history(learner_id)
    if not history:
        raise HTTPException(status_code=404, detail=f"No attempts found for learner '{learner_id}'.")
    if attempt_index < -1 or attempt_index >= len(history):
        raise HTTPException(status_code=404, detail=f"Attempt index {attempt_index} out of range.")
    return history[attempt_index]
