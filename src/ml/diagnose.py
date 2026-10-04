"""Diagnosis module for classifying student answers and identifying misconceptions.

Owner: Member 1 (ML Model Development)
Branch: member-1-ml

This module fulfills the Member 1 interface contract:
    diagnose(question: str, student_answer: str, model_path: str) -> dict
"""

import os
from typing import Any, Dict, List
import joblib
import numpy as np

DEFAULT_MODEL_PATH = os.path.join("models", "misconception_classifier.joblib")
CONFIDENCE_THRESHOLD = 0.60

LABEL_TO_INFO: Dict[str, Dict[str, str]] = {
    "impetus_force_persistence": {
        "id": "M1",
        "name": "Force required for motion (Impetus fallacy)"
    },
    "zero_net_force_zero_velocity": {
        "id": "M2",
        "name": "Zero net force means zero velocity"
    },
    "action_reaction_same_object": {
        "id": "M3",
        "name": "Action-reaction forces cancel each other"
    },
    "heavier_objects_fall_faster": {
        "id": "M4",
        "name": "Heavier objects fall faster"
    },
    "force_acceleration_conflation": {
        "id": "M5",
        "name": "Force and acceleration are the same thing"
    },
    "no_misconception_detected": {
        "id": "NONE",
        "name": "Canonical scientific understanding (No misconception)"
    }
}


def _extract_evidence_tokens(pipeline: Any, input_text: str, predicted_label: str) -> List[str]:
    """Extract top contributing tokens from the student response for diagnosis transparency."""
    try:
        tfidf = pipeline.named_steps.get("tfidf")
        clf = pipeline.named_steps.get("classifier")
        if not tfidf or not clf or not hasattr(clf, "classes_"):
            return []

        classes_list = list(clf.classes_)
        if predicted_label not in classes_list:
            return []

        pred_idx = classes_list.index(predicted_label)
        feat_names = tfidf.get_feature_names_out()
        feat_vec = tfidf.transform([input_text]).toarray()[0]
        active_indices = np.where(feat_vec > 0)[0]

        # Extract weights for the predicted class
        coefs = clf.coef_[pred_idx] if clf.coef_.ndim > 1 else clf.coef_[0]
        token_scores = []
        for idx in active_indices:
            token = feat_names[idx]
            # Exclude generic prompt prefixes
            if token in ["question", "answer", "question answer"]:
                continue
            score = float(coefs[idx] * feat_vec[idx])
            if score > 0:
                token_scores.append((token, score))

        token_scores.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in token_scores[:5]]
    except Exception:
        return []


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
        Path to the serialized scikit-learn pipeline (.joblib).

    Returns
    -------
    dict
        Diagnostic outcome adhering to the shared integration contract.
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
            "misconception_id": "EMPTY",
            "misconception_name": "No answer provided",
            "confidence_score": 0.0,
            "model_version": "baseline-0.1.0",
            "status": "fallback",
            "explanation": "No valid answer was provided by the student.",
            "evidence_keywords": [],
            "probabilities": {}
        }

    # Verify model artifact existence
    if not os.path.exists(model_path):
        return {
            "misconception_label": "pending_model_training",
            "misconception_id": "PENDING",
            "misconception_name": "Model training pending",
            "confidence_score": 0.0,
            "model_version": "baseline-stub-0.1.0",
            "status": "fallback",
            "explanation": f"Trained model artifact not found at '{model_path}'. Using baseline stub.",
            "evidence_keywords": [],
            "probabilities": {}
        }

    # Attempt inference with trained pipeline
    try:
        pipeline = joblib.load(model_path)
        input_text = f"Question: {cleaned_question} Answer: {cleaned_answer}"

        prediction = str(pipeline.predict([input_text])[0])

        confidence = 1.0
        probabilities_dict = {}
        if hasattr(pipeline, "predict_proba"):
            probs = pipeline.predict_proba([input_text])[0]
            confidence = float(max(probs))
            classes = getattr(pipeline, "classes_", [])
            probabilities_dict = {
                str(cls_name): round(float(p), 4) for cls_name, p in zip(classes, probs)
            }

        rounded_confidence = round(confidence, 4)
        evidence_tokens = _extract_evidence_tokens(pipeline, input_text, prediction)

        # Lookup taxonomy information
        meta = LABEL_TO_INFO.get(prediction, {"id": prediction, "name": prediction.replace("_", " ").title()})

        if confidence >= CONFIDENCE_THRESHOLD:
            status = "success"
            explanation = (
                f"Classified as '{meta['name']}' with {rounded_confidence * 100:.1f}% estimated probability. "
                "Statistical ML estimate; verify pedagogical evidence."
            )
        else:
            status = "uncertain"
            explanation = (
                f"Low confidence diagnosis ({rounded_confidence * 100:.1f}%, below {CONFIDENCE_THRESHOLD * 100:.0f}% threshold). "
                "The student reasoning is ambiguous or non-canonical across multiple concept categories."
            )

        return {
            "misconception_label": prediction,
            "misconception_id": meta["id"],
            "misconception_name": meta["name"],
            "confidence_score": rounded_confidence,
            "model_version": "trained-pipeline-1.0",
            "status": status,
            "explanation": explanation,
            "evidence_keywords": evidence_tokens,
            "probabilities": probabilities_dict
        }

    except Exception as exc:
        return {
            "misconception_label": "model_inference_error",
            "misconception_id": "ERROR",
            "misconception_name": "Inference Error",
            "confidence_score": 0.0,
            "model_version": "error-fallback",
            "status": "fallback",
            "explanation": f"Failed to infer from model: {str(exc)}",
            "evidence_keywords": [],
            "probabilities": {}
        }
