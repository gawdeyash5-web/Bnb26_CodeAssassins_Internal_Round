# Dataset Directory (`data/`)

This directory holds the raw and processed physics diagnostic datasets used by the ML model and intervention engine.

## Guidelines for Team Members (Specifically Member 2)

- Large dataset files (`*.csv`, `*.parquet`, `*.json`) are intentionally **ignored by Git** via `.gitignore` to prevent repository bloat.
- Place local training and evaluation datasets in this folder (e.g., `data/physics_misconceptions.csv`).
- Refer to [`docs/dataset_schema.md`](../docs/dataset_schema.md) for the exact column schema and validation rules.
- For sharing small sample datasets with the team, consider storing a small sample fixture under `tests/fixtures/sample_dataset.csv`.

## Recommended File Naming
- `physics_misconceptions.csv` — Primary labeled dataset for training and validation.
- `interventions.json` — Misconception-to-intervention mapping dictionary.
- `questions.json` — Question bank with diagnostic and reassessment prompts.
