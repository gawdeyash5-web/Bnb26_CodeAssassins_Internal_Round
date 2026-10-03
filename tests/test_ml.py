"""Tests for Member 1 ML pipeline and diagnosis module.

Covers:
- Dataset loading, column validation, and handling of empty/whitespace values.
- Model training and artifact serialization.
- diagnose() with missing models, empty answers, valid predictions, uncertain predictions, and error handling.
"""

import os
import tempfile
import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from unittest.mock import MagicMock

from src.ml.train_model import load_data, build_pipeline, train_and_evaluate
from src.ml.diagnose import diagnose, CONFIDENCE_THRESHOLD

SAMPLE_FIXTURE_PATH = os.path.join("tests", "fixtures", "sample_dataset.csv")


# --- Dataset Loading & Validation Tests ---

def test_load_data_valid():
    """Verify that load_data loads the valid fixture and returns expected columns."""
    df = load_data(SAMPLE_FIXTURE_PATH)
    assert not df.empty
    assert "question" in df.columns
    assert "student_answer" in df.columns
    assert "misconception_label" in df.columns
    assert len(df) >= 4


def test_load_data_missing_file():
    """Verify FileNotFoundError is raised when file does not exist."""
    with pytest.raises(FileNotFoundError):
        load_data("data/non_existent_file_xyz.csv")


def test_load_data_missing_columns():
    """Verify ValueError is raised if core columns are missing."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tmp:
        tmp.write("question,student_answer\nWhat is inertia?,Resists change\n")
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="missing required columns"):
            load_data(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_load_data_strips_empty_and_whitespace_rows():
    """Verify rows with empty/whitespace or NaN in core fields are dropped."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tmp:
        tmp.write(
            "question,student_answer,misconception_label\n"
            "   ,Answer 1,label_1\n"  # empty question
            "Q2,   ,label_2\n"  # empty student_answer
            "Q3,Answer 3,   \n"  # empty misconception_label
            "Q4,Answer 4,label_4\n"  # valid
        )
        tmp_path = tmp.name

    try:
        df = load_data(tmp_path)
        assert len(df) == 1
        assert df.iloc[0]["question"] == "Q4"
    finally:
        os.unlink(tmp_path)


def test_load_data_all_empty_rows_raises_value_error():
    """Verify ValueError is raised when all rows are invalid or empty."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tmp:
        tmp.write(
            "question,student_answer,misconception_label\n"
            "   ,   ,   \n"
        )
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="No valid rows found"):
            load_data(tmp_path)
    finally:
        os.unlink(tmp_path)


# --- Model Training Tests ---

def test_build_pipeline():
    """Verify build_pipeline returns a scikit-learn Pipeline with tfidf and classifier."""
    pipeline = build_pipeline()
    assert isinstance(pipeline, Pipeline)
    assert "tfidf" in pipeline.named_steps
    assert "classifier" in pipeline.named_steps


def test_train_and_evaluate_reproducible():
    """Verify train_and_evaluate trains, prints evaluation, and exports model file."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_model_path = os.path.join(tmp_dir, "test_model.joblib")
        pipeline = train_and_evaluate(
            data_path=SAMPLE_FIXTURE_PATH,
            model_output_path=output_model_path,
            test_size=0.25,
            random_state=42
        )
        assert isinstance(pipeline, Pipeline)
        assert os.path.exists(output_model_path)
        assert os.path.getsize(output_model_path) > 0


def test_train_and_evaluate_insufficient_samples():
    """Verify ValueError is raised if dataset has fewer than 2 samples."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tmp:
        tmp.write(
            "question,student_answer,misconception_label\n"
            "Q1,Answer 1,label_1\n"
        )
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="at least 2 samples"):
            train_and_evaluate(data_path=tmp_path, model_output_path=None)
    finally:
        os.unlink(tmp_path)


# --- Diagnose Function Tests ---

def test_diagnose_empty_or_invalid_answer():
    """Verify diagnose returns status='fallback' and misconception_label='empty_answer' for empty inputs."""
    for empty_input in ["", "   ", None]:
        res = diagnose("What keeps the puck moving?", empty_input)
        assert res["status"] == "fallback"
        assert res["misconception_label"] == "empty_answer"
        assert res["confidence_score"] == 0.0


def test_diagnose_missing_model_file():
    """Verify diagnose returns graceful fallback when model artifact does not exist."""
    res = diagnose("What keeps the puck moving?", "Force stays in puck", model_path="models/non_existent.joblib")
    assert res["status"] == "fallback"
    assert res["misconception_label"] == "pending_model_training"
    assert res["confidence_score"] == 0.0
    assert "not found" in res["explanation"]


def test_diagnose_corrupted_model_file():
    """Verify diagnose returns error fallback when model file cannot be loaded."""
    with tempfile.NamedTemporaryFile("w", suffix=".joblib", delete=False) as tmp:
        tmp.write("NOT A REAL JOBLIB FILE")
        corrupted_path = tmp.name

    try:
        res = diagnose("What keeps the puck moving?", "Force stays in puck", model_path=corrupted_path)
        assert res["status"] == "fallback"
        assert res["misconception_label"] == "model_inference_error"
        assert res["confidence_score"] == 0.0
    finally:
        os.unlink(corrupted_path)


def test_diagnose_valid_trained_model():
    """Verify diagnose successfully classifies with confidence using a trained pipeline artifact."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path = os.path.join(tmp_dir, "model.joblib")
        train_and_evaluate(
            data_path=SAMPLE_FIXTURE_PATH,
            model_output_path=model_path,
            test_size=0.25,
            random_state=42
        )

        res = diagnose(
            question="A hockey puck slides on ice after being hit. What keeps it moving?",
            student_answer="The force from the stick stays inside the puck.",
            model_path=model_path
        )

        assert res["status"] in ["success", "uncertain"]
        assert isinstance(res["misconception_label"], str)
        assert 0.0 <= res["confidence_score"] <= 1.0
        assert res["model_version"] == "trained-pipeline-1.0"
        assert "explanation" in res


def test_diagnose_uncertain_threshold_behavior(monkeypatch):
    """Verify diagnose marks status='uncertain' when confidence is below 0.60."""
    # Mock joblib.load to return a dummy pipeline that outputs low confidence (< 0.60)
    mock_pipeline = MagicMock()
    mock_pipeline.predict.return_value = ["impetus_force_persistence"]
    mock_pipeline.predict_proba.return_value = np.array([[0.45, 0.35, 0.20]])

    with tempfile.NamedTemporaryFile("w", suffix=".joblib", delete=False) as tmp:
        tmp.write("dummy")
        dummy_path = tmp.name

    try:
        import joblib
        monkeypatch.setattr(joblib, "load", lambda path: mock_pipeline)

        res = diagnose(
            question="A hockey puck slides on ice. What keeps it moving?",
            student_answer="Maybe some force or maybe not.",
            model_path=dummy_path
        )

        assert res["status"] == "uncertain"
        assert res["confidence_score"] == 0.45
        assert "Low confidence" in res["explanation"]
    finally:
        os.unlink(dummy_path)
