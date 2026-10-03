"""Model training script for Re: Physics Misconception Diagnostic System.

Owner: Member 1 (ML Model Development)
Branch: member-1-ml

This script defines the training pipeline using TF-IDF vectorization and
Logistic Regression to classify student physics answers into misconception categories.
"""

import os
from typing import Optional, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib

DEFAULT_DATA_PATH = os.path.join("data", "physics_misconceptions.csv")
DEFAULT_MODEL_OUTPUT = os.path.join("models", "misconception_classifier.joblib")


def load_data(csv_path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load and validate the physics misconceptions dataset.

    Parameters
    ----------
    csv_path : str
        Path to the CSV dataset file.

    Returns
    -------
    pd.DataFrame
        Dataset containing at least 'question', 'student_answer', and 'misconception_label'.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at '{csv_path}'. Please ensure Member 2 has placed the dataset."
        )

    df = pd.read_csv(csv_path)
    required_cols = {"question", "student_answer", "misconception_label"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    return df


def build_pipeline() -> Pipeline:
    """Construct the TF-IDF + Logistic Regression classification pipeline.

    Returns
    -------
    Pipeline
        Unfitted scikit-learn Pipeline.
    """
    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=5000,
                stop_words="english",
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            )
        )
    ])
    return pipeline


def train_and_evaluate(
    data_path: str = DEFAULT_DATA_PATH,
    model_output_path: str = DEFAULT_MODEL_OUTPUT,
    test_size: float = 0.20,
    random_state: int = 42
) -> Pipeline:
    """Train the model on the physics dataset, evaluate on test split, and save model.

    Parameters
    ----------
    data_path : str
        Input CSV path.
    model_output_path : str
        Destination path for serialized .joblib artifact.
    test_size : float
        Fraction of data for testing.
    random_state : int
        Seed for reproducibility.

    Returns
    -------
    Pipeline
        Fitted scikit-learn pipeline.
    """
    df = load_data(data_path)

    # Combine question and answer context
    X = "Question: " + df["question"].fillna("") + " Answer: " + df["student_answer"].fillna("")
    y = df["misconception_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if len(y.unique()) > 1 else None
    )

    pipeline = build_pipeline()
    print(f"Training pipeline on {len(X_train)} samples...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    predictions = pipeline.predict(X_test)
    print("\n--- Evaluation Report ---")
    print(classification_report(y_test, predictions, zero_division=0))

    # Save artifact
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(pipeline, model_output_path)
    print(f"\nModel artifact saved to '{model_output_path}'")

    return pipeline


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train Re:Learn Misconception Classifier")
    parser.add_argument("--data", default=DEFAULT_DATA_PATH, help="Path to input CSV data")
    parser.add_argument("--output", default=DEFAULT_MODEL_OUTPUT, help="Path to output .joblib")
    args = parser.parse_args()

    try:
        train_and_evaluate(data_path=args.data, model_output_path=args.output)
    except FileNotFoundError as err:
        print(f"Notice: {err}")
