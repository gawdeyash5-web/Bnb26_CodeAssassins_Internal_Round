"""Sidebar component for Re:Learn application.

Renders a sleek learner profile panel with learner identity management,
authentic session metrics derived strictly from get_learner_history(), and attempt history.
"""

from typing import Any, Dict, List
import streamlit as st
from src.learner import get_learner_history, clear_learner_history
from src.app.styles import render_html


def render_sidebar() -> str:
    """Render the learner profile, session progress, and history sidebar.

    Returns
    -------
    str
        The currently active learner_id.
    """
    with st.sidebar:
        # Learner Profile Header
        render_html(
            """
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding-bottom: 0.85rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                margin-bottom: 1rem;
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    border-radius: 10px;
                    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
                ">
                    🧑‍🎓
                </div>
                <div>
                    <div style="font-weight: 800; font-size: 1.05rem; color: #ffffff; letter-spacing: -0.01em;">
                        Learner Panel
                    </div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">
                        Profile & Adaptive Diagnostics
                    </div>
                </div>
            </div>
            """
        )

        # Learner ID selection & editing
        current_id = st.session_state.get("learner_id", "student_01")
        new_learner_id = st.text_input(
            "Learner ID",
            value=current_id,
            help="Unique learner identifier used to record diagnostic attempts."
        ).strip()
        
        if new_learner_id:
            st.session_state.learner_id = new_learner_id
        else:
            new_learner_id = current_id

        # Fetch authentic history from Member 4
        history: List[Dict[str, Any]] = get_learner_history(new_learner_id)
        attempt_count = len(history)

        # Session Metrics derived strictly from real history
        if attempt_count > 0:
            labels = [item.get("misconception_label") for item in history if item.get("misconception_label")]
            misconceptions_found = set(
                lbl for lbl in labels 
                if lbl and lbl not in ["no_misconception_detected", "empty_answer", "pending_model_training"]
            )
            
            metrics_html = f"""
            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.6rem;
                margin-top: 0.9rem;
                margin-bottom: 1.1rem;
            ">
                <div style="
                    background: rgba(14, 21, 38, 0.8);
                    border: 1px solid rgba(255, 255, 255, 0.07);
                    border-radius: 10px;
                    padding: 0.65rem 0.8rem;
                ">
                    <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Attempts</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-top: 0.1rem;">{attempt_count}</div>
                </div>
                <div style="
                    background: rgba(14, 21, 38, 0.8);
                    border: 1px solid rgba(255, 255, 255, 0.07);
                    border-radius: 10px;
                    padding: 0.65rem 0.8rem;
                ">
                    <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Misconceptions</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #fbbf24; margin-top: 0.1rem;">{len(misconceptions_found)}</div>
                </div>
            </div>
            """
            render_html(metrics_html)

            # Detected misconceptions tags
            if misconceptions_found:
                render_html("<div style='font-size: 0.76rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.4rem; text-transform: uppercase;'>Detected Misconceptions</div>")
                tags_str = ""
                for tag in misconceptions_found:
                    formatted_tag = tag.replace("_", " ").title()
                    tags_str += f"""
                    <span style="
                        font-size: 0.72rem;
                        font-weight: 600;
                        background: rgba(245, 158, 11, 0.12);
                        color: #fbbf24;
                        border: 1px solid rgba(245, 158, 11, 0.3);
                        padding: 0.2rem 0.55rem;
                        border-radius: 6px;
                        display: inline-block;
                        margin: 0.15rem;
                    ">{formatted_tag}</span>
                    """
                render_html(f"<div style='margin-bottom: 1rem;'>{tags_str}</div>")

        else:
            render_html(
                """
                <div style="
                    background: rgba(14, 21, 38, 0.45);
                    border: 1px dashed rgba(255, 255, 255, 0.08);
                    border-radius: 10px;
                    padding: 0.85rem;
                    margin-top: 0.8rem;
                    margin-bottom: 1rem;
                    text-align: center;
                ">
                    <div style="font-size: 0.78rem; color: #94a3b8;">No attempts recorded yet for this learner profile.</div>
                </div>
                """
            )

        # Attempt History Feed Header
        render_html(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 0.8rem;
                margin-bottom: 0.6rem;
            ">
                <span style="font-weight: 700; font-size: 0.92rem; color: #ffffff;">📜 Attempt History</span>
            </div>
            """
        )

        if not history:
            render_html(
                """
                <div style="color: #64748b; font-size: 0.8rem; line-height: 1.45; padding: 0.4rem 0;">
                    Complete diagnostic challenges to populate your persistent attempt log.
                </div>
                """
            )
        else:
            # Display history in reverse chronological order
            for idx, item in enumerate(reversed(history)):
                attempt_num = len(history) - idx
                label = item.get("misconception_label", "unknown")
                confidence = item.get("confidence_score", 0.0) * 100
                timestamp = item.get("timestamp", "")[:16].replace("T", " ")
                status = item.get("diagnosis_status", "unknown")

                is_correct = label == "no_misconception_detected"
                conf_color = "#34d399" if is_correct else ("#fbbf24" if status == "uncertain" else "#a5b4fc")
                formatted_label = label.replace("_", " ").title()

                item_html = f"""
                <div style="
                    background: rgba(14, 21, 38, 0.7);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 8px;
                    padding: 0.65rem 0.8rem;
                    margin-bottom: 0.55rem;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                        <span style="font-size: 0.74rem; font-weight: 700; color: #818cf8;">Attempt #{attempt_num}</span>
                        <span style="font-size: 0.68rem; color: #64748b;">{timestamp}</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #f1f5f9; font-weight: 600; margin-bottom: 0.2rem;">
                        {formatted_label}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8;">
                        <span>Confidence:</span>
                        <span style="color: {conf_color}; font-weight: 700;">{confidence:.1f}%</span>
                    </div>
                </div>
                """
                render_html(item_html)

        st.markdown("---")
        
        # Reset / Clear history button
        if history:
            if st.button("🧹 Clear Learner History", use_container_width=True, type="secondary"):
                clear_learner_history(new_learner_id)
                st.rerun()

    return new_learner_id
