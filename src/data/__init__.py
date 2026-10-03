"""Data access and validation module for physics questions and student responses.

Owner: Member 2 (Physics dataset and intervention content)
Branch: member-2-data
"""

import os
from typing import Any, Dict, List, Optional
import pandas as pd


def load_dataset(filepath: str = os.path.join("data", "physics_misconceptions.csv")) -> pd.DataFrame:
    """Load the physics misconception dataset.

    Parameters
    ----------
    filepath : str
        Path to the dataset CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataframe.
    """
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=[
            "question_id", "topic", "question", "correct_answer",
            "student_answer", "misconception_label"
        ])
    return pd.read_csv(filepath)


def validate_dataset_schema(df: pd.DataFrame) -> List[str]:
    """Validate that the dataset meets required schema rules.

    Returns
    -------
    list of str
        List of validation error messages, or empty if valid.
    """
    required = ["question", "student_answer", "misconception_label"]
    errors = []
    for col in required:
        if col not in df.columns:
            errors.append(f"Missing mandatory column: '{col}'")
    return errors
