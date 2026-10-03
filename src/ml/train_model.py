"""Model training script for Re: Physics Misconception Diagnostic System.

Owner: Member 1 (ML Model Development)
Branch: member-1-ml

This script defines the training pipeline using TF-IDF vectorization and
Logistic Regression to classify student physics answers into misconception categories.
"""

import argparse
import math
import os
from typing import Optional, Tuple
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

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
        Cleaned dataset containing at least 'question', 'student_answer',
        and 'misconception_label' with non-empty values.

    Raises
    ------
    FileNotFoundError
        If the dataset file does not exist at csv_path.
    ValueError
        If required columns are missing or no valid rows remain after cleaning.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at '{csv_path}'. Please ensure Member 2 has placed the dataset "
            "or provide a valid development fixture."
        )

    df = pd.read_csv(csv_path)
    required_cols = {"question", "student_answer", "misconception_label"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(list(missing))}")

    # Remove rows where required columns are null or whitespace-only
    for col in required_cols:
        df[col] = df[col].astype(str).str.strip()

    valid_mask = (
        (df["question"] != "") &
        (df["question"].str.lower() != "nan") &
        (df["student_answer"] != "") &
        (df["student_answer"].str.lower() != "nan") &
        (df["misconception_label"] != "") &
        (df["misconception_label"].str.lower() != "nan")
    )
    cleaned_df = df[valid_mask].copy()

    if cleaned_df.empty:
        raise ValueError(
            f"No valid rows found in '{csv_path}' after removing empty/null entries in core columns."
        )

    return cleaned_df


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
                sublinear_tf=True,
                min_df=1
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
    model_output_path: Optional[str] = DEFAULT_MODEL_OUTPUT,
    test_size: float = 0.20,
    random_state: int = 42
) -> Pipeline:
    """Train the model on the physics dataset, evaluate on test split, and save model.

    Parameters
    ----------
    data_path : str
        Input CSV path.
    model_output_path : str, optional
        Destination path for serialized .joblib artifact. If None, saving is skipped.
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
    X = "Question: " + df["question"] + " Answer: " + df["student_answer"]
    y = df["misconception_label"]

    n_samples = len(df)
    if n_samples < 2:
        raise ValueError("Dataset requires at least 2 samples to perform training and evaluation.")

    # Calculate expected test/train counts to ensure valid stratification
    class_counts = y.value_counts()
    n_classes = len(class_counts)
    
    if isinstance(test_size, float):
        n_test = int(math.ceil(test_size * n_samples)) if test_size < 1.0 else int(test_size)
    else:
        n_test = int(test_size)
    n_train = n_samples - n_test

    can_stratify = (
        (class_counts.min() >= 2)
        and (n_classes > 1)
        and (n_train >= n_classes)
        and (n_test >= n_classes)
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y if can_stratify else None
    )

    pipeline = build_pipeline()
    print(f"Training pipeline on {len(X_train)} samples across {y.nunique()} classes...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    predictions = pipeline.predict(X_test)
    print("\n--- Evaluation Report ---")
    print(classification_report(y_test, predictions, zero_division=0))

    # Save artifact
    if model_output_path:
        dir_name = os.path.dirname(model_output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        joblib.dump(pipeline, model_output_path)
        print(f"\nModel artifact saved to '{model_output_path}'")

    return pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Re:Learn Misconception Classifier")
    parser.add_argument("--data", default=DEFAULT_DATA_PATH, help="Path to input CSV data")
    parser.add_argument("--output", default=DEFAULT_MODEL_OUTPUT, help="Path to output .joblib")
    parser.add_argument("--test-size", type=float, default=0.20, help="Fraction of data for testing")
    parser.add_argument("--seed", type=int, default=42, help="Random state seed")
    args = parser.parse_args()

    try:
        train_and_evaluate(
            data_path=args.data,
            model_output_path=args.output,
            test_size=args.test_size,
            random_state=args.seed
        )
    except FileNotFoundError as err:
        print(f"Notice: {err}")
    except ValueError as err:
        print(f"Validation Error: {err}")
