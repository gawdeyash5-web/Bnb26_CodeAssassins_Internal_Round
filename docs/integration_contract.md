# Re: Integration Contract & Shared Interfaces

This document outlines the strict API boundaries between team members so that everyone can develop independently without blocking each other.

---

## 1. Member 1 (ML Model) Contract

### Function Signature
```python
def diagnose(
    question: str,
    student_answer: str,
    model_path: str = "models/misconception_classifier.joblib"
) -> dict:
    ...
```

### Return Dictionary Schema
```json
{
  "misconception_label": "impetus_force_persistence",
  "confidence_score": 0.875,
  "model_version": "trained-pipeline-1.0",
  "status": "success",
  "explanation": "Classified with 87.5% confidence."
}
```

### Field Requirements
- `misconception_label` (string, required): A recognized category from the taxonomy (e.g. `impetus_force_persistence`) or `no_misconception_detected`.
- `confidence_score` (float, required): Probability estimate between `0.0` and `1.0`.
- `model_version` (string, required): Identifier of the active model.
- `status` (string, required):
  - `"success"`: Prediction confidence >= 0.60.
  - `"uncertain"`: Prediction confidence < 0.60.
  - `"fallback"`: Input invalid, model missing, or runtime error gracefully caught.
- `explanation` (string, optional): Human-readable diagnosis commentary.

---

## 2. Member 2 (Interventions) Contract

### Function Signature
```python
def get_intervention(misconception_label: str) -> dict:
    ...
```

### Return Dictionary Schema
```json
{
  "title": "Impetus Fallacy (Newton's 1st Law)",
  "explanation": "Objects do not require a continuous forward force to remain in motion...",
  "key_concept": "Inertia & Net Force",
  "guided_hint": "Think about what happens to a hockey puck sliding on frictionless ice.",
  "reassessment_question": "A satellite travels in deep space with engines off. What happens to its motion?",
  "status": "found"
}
```

### Field Requirements
- `status`: Either `"found"` (matched known misconception) or `"fallback"` (generic guidance).
- `guided_hint`: Socratic prompt guiding the student to discover their own logical gap.
- `reassessment_question`: Follow-up diagnostic question testing the same underlying concept.

---

## 3. Member 3 (Frontend Interface) Contract

The frontend (`src/app/app.py`) is built using **Streamlit**:
- Must call `diagnose(question, answer)` upon submission.
- Must query `get_intervention(result["misconception_label"])`.
- Must call `record_attempt(learner_id, question, answer, diagnosis, intervention)` to persist the session.
- Must display visual indicators for `status == "uncertain"` (warning banner) vs `status == "success"` (success badge).
- Must never crash or display raw tracebacks to the user.

---

## 4. Member 4 (Integration, Learner History & Testing) Contract

### Tracker Signatures
```python
def record_attempt(
    learner_id: str,
    question: str,
    student_answer: str,
    diagnosis: dict,
    intervention: dict = None
) -> dict:
    ...

def get_learner_history(learner_id: str) -> list[dict]:
    ...
```

### Responsibilities
- Maintain session stability in `src/learner/`.
- Verify that `diagnose()` and `get_intervention()` return valid dicts matching this contract.
- Write pytest suites under `tests/` covering:
  - Empty or invalid input handling.
  - Baseline fallback when no model file exists.
  - Integration between diagnosis, intervention, and learner history logging.

---

## 5. Error & Uncertainty Handling Protocols

1. **Missing Model File (`models/misconception_classifier.joblib`)**:
   - `diagnose()` must NOT throw an unhandled exception.
   - Returns `status="fallback"` and `misconception_label="pending_model_training"`.
2. **Empty Answer**:
   - Returns `status="fallback"` and `misconception_label="empty_answer"`.
3. **Low Confidence (< 0.60)**:
   - Returns `status="uncertain"`.
   - The UI displays a caution banner encouraging the learner to clarify their reasoning.
4. **Unknown Misconception Label**:
   - `get_intervention()` provides a generalized physics review fallback rather than throwing a `KeyError`.
