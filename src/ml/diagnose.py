"""Diagnosis module for classifying student answers and identifying misconceptions.

Owner: Member 1 (ML Model Development)
Branch: member-1-ml

This module fulfills the Member 1 interface contract:
    diagnose(question: str, student_answer: str, model_path: str) -> dict
"""

import os
from typing import Any, Dict
import joblib

DEFAULT_MODEL_PATH = os.path.join("models", "misconception_classifier.joblib")
CONFIDENCE_THRESHOLD = 0.60


def diagnose(
    question: str,
    student_answer: str,
    model_path: str = DEFAULT_MODEL_PATH
) -> Dict[str, Any]:
    """Diagnose a student's answer to identify underlying physics misconceptions.

    Parameters
    ----------
    question : str
        The physics question prompt presented to the student.
    student_answer : str
        The student's free-text response.
    model_path : str, optional
        Path to the serialized scikit-learn pipeline (.joblib), by default DEFAULT_MODEL_PATH.

    Returns
    -------
    dict
        A dictionary containing:
            - misconception_label (str): Identified misconception category or contract label.
            - confidence_score (float): Probability estimate between 0.0 and 1.0.
            - model_version (str): Identifier/version of the diagnostic model.
            - status (str): 'success', 'uncertain', or 'fallback'.
            - explanation (str): Human-readable diagnosis commentary.
    """
    # Defensive input validation
    if question is None or not isinstance(question, str):
        cleaned_question = ""
    else:
        cleaned_question = question.strip()

    if student_answer is None or not isinstance(student_answer, str):
        cleaned_answer = ""
    else:
        cleaned_answer = student_answer.strip()

    # Handle empty answer according to contract
    if not cleaned_answer:
        return {
            "misconception_label": "empty_answer",
            "confidence_score": 0.0,
            "model_version": "baseline-0.1.0",
            "status": "fallback",
            "explanation": "No valid answer was provided by the student."
        }

    # Verify model artifact existence
    if not os.path.exists(model_path):
        return {
            "misconception_label": "pending_model_training",
            "confidence_score": 0.0,
            "model_version": "baseline-stub-0.1.0",
            "status": "fallback",
            "explanation": f"Trained model artifact not found at '{model_path}'. Using baseline stub."
        }

    # Attempt inference with trained pipeline
    try:
        pipeline = joblib.load(model_path)
        input_text = f"Question: {cleaned_question} Answer: {cleaned_answer}"

        prediction = pipeline.predict([input_text])[0]

        confidence = 1.0
        if hasattr(pipeline, "predict_proba"):
            probabilities = pipeline.predict_proba([input_text])[0]
            confidence = float(max(probabilities))

        rounded_confidence = round(confidence, 4)

        if confidence >= CONFIDENCE_THRESHOLD:
            status = "success"
            explanation = (
                f"Classified with {rounded_confidence * 100:.1f}% estimated probability. "
                "Note: Statistical ML estimate, pedagogical verification recommended."
            )
        else:
            status = "uncertain"
            explanation = (
                f"Low confidence diagnosis ({rounded_confidence * 100:.1f}%, below {CONFIDENCE_THRESHOLD * 100:.0f}% threshold). "
                "Student reasoning may be ambiguous or outside model training distribution."
            )

        return {
            "misconception_label": str(prediction),
            "confidence_score": rounded_confidence,
            "model_version": "trained-pipeline-1.0",
            "status": status,
            "explanation": explanation
        }

    except Exception as exc:
        return {
            "misconception_label": "model_inference_error",
            "confidence_score": 0.0,
            "model_version": "error-fallback",
            "status": "fallback",
            "explanation": f"Failed to infer from model: {str(exc)}"
        }
