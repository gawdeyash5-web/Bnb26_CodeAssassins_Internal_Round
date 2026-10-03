"""Progress and history analytics component for Re:Learn application.

Renders authentic learning progression metrics, misconception transitions,
and historical attempts derived strictly from get_learner_history().
"""

from typing import Any, Dict, List
import streamlit as st
from src.learner import get_learner_history
from src.app.styles import render_html


def render_progress_history(learner_id: str):
    """Render the learner progress analytics and historical attempts feed.

    Parameters
    ----------
    learner_id : str
        Active learner identifier.
    """
    history: List[Dict[str, Any]] = get_learner_history(learner_id)

    if not history:
        render_html(
            """
            <div style="
                background: rgba(14, 21, 38, 0.45);
                border: 1px dashed rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 2.2rem;
                text-align: center;
                color: #94a3b8;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;">
                    No History Recorded Yet
                </div>
                <div style="font-size: 0.86rem; color: #64748b; max-width: 400px; margin: 0 auto;">
                    Submit diagnostic questions on the learning tab to track your attempts and conceptual trajectory.
                </div>
            </div>
            """
        )
        return

    # Real data metrics strictly from actual history
    total_attempts = len(history)
    correct_count = sum(1 for item in history if item.get("misconception_label") == "no_misconception_detected")
    misconception_count = total_attempts - correct_count

    scores = [item.get("confidence_score", 0.0) for item in history if "confidence_score" in item]
    avg_conf = (sum(scores) / len(scores) * 100) if scores else 0.0

    summary_html = f"""
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.9rem;
        margin-bottom: 1.4rem;
    ">
        <div style="
            background: rgba(14, 21, 38, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
        ">
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Total Attempts</div>
            <div style="font-size: 1.7rem; font-weight: 800; color: #ffffff; margin-top: 0.2rem;">{total_attempts}</div>
            <div style="font-size: 0.74rem; color: #64748b; margin-top: 0.2rem;">Recorded student interactions</div>
        </div>
        <div style="
            background: rgba(14, 21, 38, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
        ">
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Misconceptions Detected</div>
            <div style="font-size: 1.7rem; font-weight: 800; color: #fbbf24; margin-top: 0.2rem;">{misconception_count}</div>
            <div style="font-size: 0.74rem; color: #64748b; margin-top: 0.2rem;">Targeted for guided remediation</div>
        </div>
        <div style="
            background: rgba(14, 21, 38, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
        ">
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Mastery Verifications</div>
            <div style="font-size: 1.7rem; font-weight: 800; color: #34d399; margin-top: 0.2rem;">{correct_count}</div>
            <div style="font-size: 0.74rem; color: #64748b; margin-top: 0.2rem;">Scientifically canonical responses</div>
        </div>
        <div style="
            background: rgba(14, 21, 38, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.1rem 1.2rem;
        ">
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Mean Confidence</div>
            <div style="font-size: 1.7rem; font-weight: 800; color: #818cf8; margin-top: 0.2rem;">{avg_conf:.1f}%</div>
            <div style="font-size: 0.74rem; color: #64748b; margin-top: 0.2rem;">Average ML classifier confidence</div>
        </div>
    </div>
    """
    render_html(summary_html)

    render_html("<div style='font-size: 1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.75rem;'>Interaction History Feed</div>")

    for idx, item in enumerate(reversed(history)):
        attempt_number = total_attempts - idx
        question_text = item.get("question", "")
        student_ans = item.get("student_answer", "")
        label = item.get("misconception_label", "unknown")
        confidence = item.get("confidence_score", 0.0) * 100
        timestamp = item.get("timestamp", "")[:19].replace("T", " ")
        status = item.get("diagnosis_status", "unknown")

        is_correct = label == "no_misconception_detected"
        status_color = "#34d399" if is_correct else ("#fbbf24" if status == "uncertain" else "#f59e0b")
        formatted_label = label.replace("_", " ").title()

        with st.expander(f"Attempt #{attempt_number} • {formatted_label} ({confidence:.1f}%) • {timestamp}", expanded=(idx == 0)):
            item_detail_html = f"""
            <div style="font-size: 0.88rem; line-height: 1.55;">
                <div style="margin-bottom: 0.5rem;">
                    <span style="color: #94a3b8; font-weight: 600;">Question Prompt:</span>
                    <div style="color: #ffffff; margin-top: 0.15rem; font-weight: 500;">{question_text}</div>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <span style="color: #94a3b8; font-weight: 600;">Student's Submitted Answer:</span>
                    <div style="color: #cbd5e1; margin-top: 0.2rem; font-style: italic; background: rgba(0,0,0,0.3); padding: 0.6rem 0.8rem; border-radius: 8px;">
                        "{student_ans}"
                    </div>
                </div>
                <div style="display: flex; gap: 1.2rem; flex-wrap: wrap; margin-top: 0.7rem; padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.06);">
                    <div><span style="color: #64748b;">Diagnosed:</span> <span style="color: {status_color}; font-weight: 700;">{formatted_label}</span></div>
                    <div><span style="color: #64748b;">Confidence:</span> <span style="color: #ffffff; font-weight: 700;">{confidence:.1f}%</span></div>
                    <div><span style="color: #64748b;">Pipeline Status:</span> <span style="color: #94a3b8;">{status}</span></div>
                </div>
            </div>
            """
            render_html(item_detail_html)
