"""Diagnosis module for classifying student answers and identifying misconceptions.

This module fulfills the Member 1 interface contract:
    diagnose(question: str, student_answer: str) -> dict
"""

import os
from typing import Any, Dict, Optional
import joblib

DEFAULT_MODEL_PATH = os.path.join("models", "misconception_classifier.joblib")


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
            - misconception_label (str): Identified misconception category or 'no_misconception_detected'.
            - confidence_score (float): Confidence score between 0.0 and 1.0.
            - model_version (str): Identifier/version of the diagnostic model.
            - status (str): 'success', 'uncertain', or 'fallback'.
            - explanation (str): Diagnostic description of the finding.
    """
    cleaned_question = (question or "").strip()
    cleaned_answer = (student_answer or "").strip()

    if not cleaned_answer:
        return {
            "misconception_label": "empty_answer",
            "confidence_score": 0.0,
            "model_version": "baseline-0.1.0",
            "status": "fallback",
            "explanation": "No answer was provided by the student."
        }

    # Attempt to load trained scikit-learn pipeline if available
    if os.path.exists(model_path):
        try:
            pipeline = joblib.load(model_path)
            # Combine question and answer text for context-aware classification
            input_text = f"Question: {cleaned_question} Answer: {cleaned_answer}"
            prediction = pipeline.predict([input_text])[0]

            confidence = 1.0
            if hasattr(pipeline, "predict_proba"):
                probabilities = pipeline.predict_proba([input_text])[0]
                confidence = float(max(probabilities))

            status = "success" if confidence >= 0.60 else "uncertain"

            return {
                "misconception_label": str(prediction),
                "confidence_score": round(confidence, 4),
                "model_version": "trained-pipeline-1.0",
                "status": status,
                "explanation": f"Classified with {confidence * 100:.1f}% confidence."
            }
        except Exception as exc:
            return {
                "misconception_label": "model_inference_error",
                "confidence_score": 0.0,
                "model_version": "error-fallback",
                "status": "fallback",
                "explanation": f"Failed to infer from model: {str(exc)}"
            }

    # Baseline stub until Member 1 completes model training
    return {
        "misconception_label": "pending_model_training",
        "confidence_score": 0.50,
        "model_version": "baseline-stub-0.1.0",
        "status": "fallback",
        "explanation": "Trained model artifact not yet found at models/misconception_classifier.joblib. Using baseline stub."
    }
