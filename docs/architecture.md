# Re: System Architecture

## Overview
**Re** is an AI/ML-assisted educational platform designed to identify, address, and reassess physics misconceptions in real time. The platform follows an iterative learning loop:

1. **Question Prompt**: The student is presented with a conceptual physics scenario.
2. **Free-Text Answer**: The student writes an open-ended explanation in natural language.
3. **ML Diagnosis**: The answer is processed by a text classification pipeline (TF-IDF + Logistic Regression) that detects specific misconception classes.
4. **Targeted Intervention**: If a misconception is detected, the platform serves structured remedial content (explanations, physical analogies, and guided hints).
5. **Reassessment**: A targeted follow-up question evaluates whether the misconception was resolved.
6. **Learner History**: Historical attempts, confidence scores, and remediation outcomes are recorded to track conceptual growth over time.

---

## Architecture Diagram

```mermaid
flowchart TD
    subgraph Frontend["Streamlit Frontend (Member 3)"]
        UI["src/app/app.py"]
        Inputs["Question & Answer Form"]
        Cards["Diagnosis & Intervention Cards"]
        HistoryView["Learner History Sidebar"]
    end

    subgraph ML["ML Diagnostic Service (Member 1)"]
        Diag["src/ml/diagnose.py : diagnose()"]
        Pipeline["TF-IDF + Logistic Regression"]
        ModelArtifact["models/misconception_classifier.joblib"]
    end

    subgraph Content["Physics Data & Interventions (Member 2)"]
        Dataset["data/physics_misconceptions.csv"]
        InterventionDB["src/interventions/ : get_intervention()"]
    end

    subgraph Integration["State & Learner Tracking (Member 4)"]
        Tracker["src/learner/ : record_attempt()"]
        SessionStore["In-memory / SQLite History"]
        Tests["tests/ : Automated Test Suite"]
    end

    Inputs -->|1. (question, answer)| Diag
    Diag -->|2. Check artifact| ModelArtifact
    ModelArtifact -->|3. Predict & Probabilities| Pipeline
    Pipeline -->|4. Return label & confidence| Diag
    Diag -->|5. Diagnosis result| UI
    UI -->|6. Query intervention(label)| InterventionDB
    InterventionDB -->|7. Remediation & Reassessment| UI
    UI -->|8. Record attempt| Tracker
    Tracker -->|9. Update session| SessionStore
    SessionStore -->|10. Stream history| HistoryView
```

---

## Component Boundaries & Responsibilities

| Component | Path | Owner | Responsibilities |
| :--- | :--- | :--- | :--- |
| **ML Engine** | `src/ml/` | Member 1 | Text preprocessing, TF-IDF vectorization, Logistic Regression classification, inference contract `diagnose()`. |
| **Physics Data & Interventions** | `src/data/`, `src/interventions/`, `data/` | Member 2 | Question bank, labeled student response dataset, misconception taxonomy, intervention text and hints. |
| **Web UI** | `src/app/` | Member 3 | Streamlit user interface, input validation, result rendering, responsive layout, interaction feedback. |
| **Integration & Analytics** | `src/learner/`, `tests/` | Member 4 | Session persistence, history logging, contract verification, end-to-end testing, error handling fallback. |

---

## Technology Stack

- **Language**: Python 3.10+
- **Machine Learning**: `scikit-learn` (Pipeline, TfidfVectorizer, LogisticRegression), `joblib`
- **Data Manipulation**: `pandas`, `numpy`
- **Application Interface**: `streamlit`
- **Configuration & Quality**: `python-dotenv`, `pytest`
