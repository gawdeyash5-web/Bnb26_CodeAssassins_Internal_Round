"""Diagnosis card component for Re:Learn application.

Renders an AI diagnostic reveal with glowing status indicators,
human-readable misconception titles, visual confidence progress meter, and concise commentary.
"""

from typing import Any, Dict
import streamlit as st
from src.app.styles import render_html


def render_diagnosis_card(diag_result: Dict[str, Any]):
    """Render the AI diagnostic evaluation card with distinct visual states.

    Parameters
    ----------
    diag_result : dict
        Output from diagnose(question, student_answer).
    """
    misconception = diag_result.get("misconception_label", "unknown")
    raw_confidence = diag_result.get("confidence_score", 0.0)
    confidence_pct = raw_confidence * 100
    status = diag_result.get("status", "unknown")
    explanation = diag_result.get("explanation", "")
    model_version = diag_result.get("model_version", "unknown")

    # Map raw snake_case labels into human-friendly titles
    taxonomy_names = {
        "impetus_force_persistence": "Impetus Force Fallacy",
        "heavier_objects_fall_faster": "Gravitational Mass Fallacy",
        "acceleration_zero_at_top": "Peak Acceleration Misconception",
        "action_reaction_same_object": "Action-Reaction Cancellation Error",
        "no_misconception_detected": "Scientific Concept Mastery Verified",
        "pending_model_training": "Diagnostic Classifier Standby",
        "empty_answer": "Incomplete Explanation",
        "model_inference_error": "Model Diagnostic Exception"
    }
    human_title = taxonomy_names.get(misconception, misconception.replace("_", " ").title())

    # Visual states configuration
    if status == "success" or misconception == "no_misconception_detected":
        if misconception == "no_misconception_detected":
            status_text = "Mastery Confirmed"
            badge_bg = "rgba(16, 185, 129, 0.15)"
            badge_color = "#34d399"
            badge_border = "rgba(16, 185, 129, 0.4)"
            bar_gradient = "linear-gradient(90deg, #10b981 0%, #06b6d4 100%)"
            glow_border = "rgba(16, 185, 129, 0.35)"
            accent_title_color = "#34d399"
            icon = "✅"
        else:
            status_text = "Misconception Diagnosed (Confident)"
            badge_bg = "rgba(99, 102, 241, 0.18)"
            badge_color = "#a5b4fc"
            badge_border = "rgba(99, 102, 241, 0.45)"
            bar_gradient = "linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)"
            glow_border = "rgba(99, 102, 241, 0.35)"
            accent_title_color = "#c7d2fe"
            icon = "🎯"
    elif status == "uncertain":
        status_text = "Low Confidence (< 60%)"
        badge_bg = "rgba(245, 158, 11, 0.15)"
        badge_color = "#fbbf24"
        badge_border = "rgba(245, 158, 11, 0.4)"
        bar_gradient = "linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%)"
        glow_border = "rgba(245, 158, 11, 0.35)"
        accent_title_color = "#fbbf24"
        icon = "⚠️"
    else:  # fallback, error, pending
        status_text = "Baseline Pipeline Mode"
        badge_bg = "rgba(100, 116, 139, 0.15)"
        badge_color = "#94a3b8"
        badge_border = "rgba(100, 116, 139, 0.35)"
        bar_gradient = "linear-gradient(90deg, #64748b 0%, #818cf8 100%)"
        glow_border = "rgba(100, 116, 139, 0.25)"
        accent_title_color = "#cbd5e1"
        icon = "ℹ️"

    meter_width = min(max(confidence_pct, 6.0), 100.0)

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(16, 23, 40, 0.95) 0%, rgba(11, 16, 31, 0.95) 100%);
        border: 1px solid {glow_border};
        border-radius: 16px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px {glow_border};
    ">
        <!-- Top header row with AI indicator & status badge -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="
                    display: inline-block;
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #6366f1;
                    box-shadow: 0 0 10px #6366f1;
                "></span>
                <span style="
                    font-size: 0.72rem;
                    font-weight: 700;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    color: #818cf8;
                ">
                    AI DIAGNOSTIC ENGINE VERDICT
                </span>
            </div>
            <span style="
                font-size: 0.76rem;
                font-weight: 600;
                padding: 0.25rem 0.7rem;
                border-radius: 9999px;
                background: {badge_bg};
                color: {badge_color};
                border: 1px solid {badge_border};
            ">
                {icon} {status_text}
            </span>
        </div>

        <!-- Detected Misconception Hero -->
        <div style="
            background: rgba(14, 21, 38, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.85rem;
        ">
            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.2rem; font-weight: 500;">
                Diagnosed Conceptual Category
            </div>
            <div style="font-size: 1.25rem; font-weight: 800; color: {accent_title_color}; letter-spacing: -0.01em;">
                {human_title}
            </div>
        </div>

        <!-- Confidence Gauge -->
        <div style="margin-bottom: 0.85rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <span style="font-size: 0.78rem; color: #94a3b8; font-weight: 500;">Model Diagnostic Confidence</span>
                <span style="font-size: 0.88rem; font-weight: 700; color: #ffffff;">{confidence_pct:.1f}%</span>
            </div>
            <div style="
                width: 100%;
                height: 8px;
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 9999px;
                overflow: hidden;
            ">
                <div style="
                    width: {meter_width}%;
                    height: 100%;
                    background: {bar_gradient};
                    border-radius: 9999px;
                "></div>
            </div>
        </div>

        <!-- Concise Plain-Language Commentary -->
        <div style="
            background: rgba(255, 255, 255, 0.03);
            border-left: 3px solid {accent_title_color};
            border-radius: 0 8px 8px 0;
            padding: 0.75rem 0.95rem;
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.5;
            margin-bottom: 0.6rem;
        ">
            {explanation}
        </div>

        <!-- Engine metadata -->
        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748b; padding-top: 0.3rem;">
            <span>Classifier: TF-IDF + Logistic Regression</span>
            <span>Version: {model_version}</span>
        </div>
    </div>
    """
    render_html(card_html)
