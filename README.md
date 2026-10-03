# Re: AI/ML Physics Misconception Diagnostic & Intervention System

**Re** is an AI/ML-powered physics learning system that diagnoses student misconceptions, provides targeted pedagogical interventions, reassesses understanding, and tracks learner progress over time.

---

## The Learning Loop

```
           ┌──────────────────────┐
           │ 1. Question Prompt   │
           └──────────┬───────────┘
                      ▼
           ┌──────────────────────┐
           │ 2. Student Answer    │
           └──────────┬───────────┘
                      ▼
           ┌──────────────────────┐
           │ 3. ML Diagnosis      │ ◄── TF-IDF + Logistic Regression
           └──────────┬───────────┘
                      ▼
           ┌──────────────────────┐
           │ 4. Targeted          │
           │    Intervention      │ ◄── Conceptual explanation & hints
           └──────────┬───────────┘
                      ▼
           ┌──────────────────────┐
           │ 5. Reassessment      │
           └──────────┬───────────┘
                      ▼
           ┌──────────────────────┐
           │ 6. Learner History   │
           └──────────────────────┘
```

---

## Team Roles & Ownership

| Member | Focus Area | Working Branch | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Member 1** | **ML Model Development** | `member-1-ml` | Text vectorizer (TF-IDF), Classifier (Logistic Regression), `diagnose()` function, training script (`train_model.py`). |
| **Member 2** | **Physics Dataset & Interventions** | `member-2-data` | Curated physics questions, misconception taxonomy, tagged student answers (`data/`), intervention database (`src/interventions/`). |
| **Member 3** | **Frontend Development** | `member-3-frontend` | Streamlit user interface (`src/app/`), interactive question submission, diagnosis & intervention display cards. |
| **Member 4** | **Integration, History & Testing** | `member-4-integration` | Component wiring, session state & learner history tracker (`src/learner/`), test suite (`tests/`), validation. |

---

## Project Structure

```text
.
├── .gitignore                    # Python, venv, data, model binaries ignored
├── .env.example                  # Environment configuration template
├── requirements.txt              # Core dependencies (pandas, scikit-learn, streamlit)
├── README.md                     # Project overview and instructions
├── data/
│   ├── README.md                 # Dataset documentation and conventions
│   └── .gitkeep
├── models/
│   └── .gitkeep                  # Model binary artifacts directory (.joblib gitignored)
├── src/
│   ├── __init__.py
│   ├── ml/                       # Member 1: ML pipeline & diagnosis
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   └── diagnose.py
│   ├── data/                     # Member 2: Dataset loaders & validation
│   │   └── __init__.py
│   ├── interventions/            # Member 2: Misconception interventions & hints
│   │   └── __init__.py
│   ├── learner/                  # Member 4: History & progress tracking
│   │   └── __init__.py
│   └── app/                      # Member 3: Streamlit application
│       ├── app.py
│       └── components/
│           └── .gitkeep
├── tests/
│   └── .gitkeep                  # Member 4: Automated tests
└── docs/
    ├── architecture.md           # System architecture & component communication
    ├── dataset_schema.md         # Data schema and field specifications
    └── integration_contract.md   # Shared interface signatures & error handling
```

---

## Quickstart

### 1. Environment Setup

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

### 3. Run the Streamlit Application

```bash
streamlit run src/app/app.py
```

---

## Git Workflow for Team Members

1. **Check out your team branch**:
   ```bash
   git checkout member-<number>-<role>
   ```
2. **Pull latest baseline from main**:
   ```bash
   git pull origin main
   ```
3. **Commit your work with clear messages**:
   ```bash
   git add <modified-files>
   git commit -m "feat(scope): descriptive message"
   ```
4. **Push your branch to GitHub**:
   ```bash
   git push -u origin member-<number>-<role>
   ```
5. **Open a Pull Request** to merge into `main` after verification with Member 4.
