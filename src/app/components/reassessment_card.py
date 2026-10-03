"""Reassessment card component for Re:Learn application.

Renders the dedicated "Prove Your Understanding" stage to test whether
conceptual misconceptions have genuinely resolved via follow-up scenarios.
"""

from typing import Any, Dict
import streamlit as st
from src.ml.diagnose import diagnose
from src.learner import record_attempt
from src.app.styles import render_html


def render_reassessment_card(intervention: Dict[str, Any], learner_id: str):
    """Render the 'Prove Your Understanding' reassessment module and verification flow.

    Parameters
    ----------
    intervention : dict
        The current active intervention object.
    learner_id : str
        The active learner identifier for tracking.
    """
    reassessment_question = intervention.get("reassessment_question")
    if not reassessment_question:
        render_html(
            """
            <div style="
                background: rgba(14, 21, 38, 0.4);
                border: 1px dashed rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 1.2rem;
                text-align: center;
                color: #94a3b8;
                font-size: 0.86rem;
            ">
                No follow-up reassessment question defined for this concept.
            </div>
            """
        )
        return

    card_intro_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(16, 26, 42, 0.95) 0%, rgba(10, 18, 30, 0.95) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-top: 1.1rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 25px rgba(16, 185, 129, 0.12);
    ">
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; flex-wrap: wrap; gap: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <div style="
                    width: 34px;
                    height: 34px;
                    border-radius: 9px;
                    background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 17px;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
                ">
                    🔄
                </div>
                <div>
                    <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #34d399;">
                        STAGE 2: PROVE YOUR UNDERSTANDING
                    </div>
                    <div style="font-size: 1.22rem; font-weight: 800; color: #ffffff; letter-spacing: -0.015em;">
                        Conceptual Resolution Check
                    </div>
                </div>
            </div>

            <span style="
                font-size: 0.74rem;
                font-weight: 600;
                padding: 0.25rem 0.65rem;
                border-radius: 9999px;
                background: rgba(16, 185, 129, 0.15);
                color: #34d399;
                border: 1px solid rgba(16, 185, 129, 0.35);
            ">
                Transfer Scenario
            </span>
        </div>

        <!-- Purpose Explanation -->
        <div style="
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.5;
            margin-bottom: 0.95rem;
        ">
            We are checking whether the misconception is <strong>actually resolved</strong>.
            True understanding is confirmed by applying the correct physical principle to a new situation,
            not simply correcting the initial response.
        </div>

        <!-- Reassessment Prompt Card -->
        <div style="
            background: rgba(14, 21, 38, 0.85);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 12px;
            padding: 1.1rem 1.25rem;
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 600;
            line-height: 1.5;
        ">
            {reassessment_question}
        </div>
    </div>
    """
    render_html(card_intro_html)

    # Reassessment answer textarea
    reassess_key = f"reassess_input_{abs(hash(reassessment_question))}"
    reassess_ans = st.text_area(
        label="Your Reassessment Scientific Reasoning:",
        key=reassess_key,
        placeholder="Apply the scientific principle you learned above. What happens in this new situation?",
        height=110
    )

    reassess_submit = st.button("🔬 Submit Reassessment for AI Verification", type="primary", use_container_width=True)

    if reassess_submit:
        if not reassess_ans.strip():
            st.warning("⚠️ Please provide your explanation for the reassessment scenario before submitting.")
        else:
            with st.spinner("Analyzing follow-up answer against conceptual diagnostic models..."):
                reassess_diag = diagnose(reassessment_question, reassess_ans)
                reassess_label = reassess_diag.get("misconception_label", "unknown")
                reassess_conf = reassess_diag.get("confidence_score", 0.0)
                reassess_status = reassess_diag.get("status", "unknown")

                # Record attempt via Member 4 module
                record_attempt(
                    learner_id=learner_id,
                    question=reassessment_question,
                    student_answer=reassess_ans,
                    diagnosis=reassess_diag,
                    intervention=None
                )

            is_resolved = (
                reassess_label == "no_misconception_detected" or
                (reassess_status == "success" and reassess_label == "no_misconception_detected")
            )

            if is_resolved:
                resolved_html = f"""
                <div style="
                    background: rgba(16, 185, 129, 0.12);
                    border: 1px solid rgba(16, 185, 129, 0.4);
                    border-radius: 12px;
                    padding: 1.1rem 1.25rem;
                    margin-top: 1rem;
                    box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
                ">
                    <div style="display: flex; align-items: center; gap: 0.5rem; font-weight: 800; color: #34d399; font-size: 1.05rem; margin-bottom: 0.35rem;">
                        <span>🎉</span> Misconception Resolved
                    </div>
                    <div style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.55;">
                        Your reasoning on this follow-up scenario accurately applies the physical law without the prior misconception.
                        The AI classifier verified canonical scientific understanding ({reassess_conf * 100:.1f}% confidence).
                    </div>
                </div>
                """
                render_html(resolved_html)
            else:
                formatted_label = reassess_label.replace("_", " ").title()
                persisting_html = f"""
                <div style="
                    background: rgba(245, 158, 11, 0.1);
                    border: 1px solid rgba(245, 158, 11, 0.35);
                    border-radius: 12px;
                    padding: 1.1rem 1.25rem;
                    margin-top: 1rem;
                ">
                    <div style="display: flex; align-items: center; gap: 0.5rem; font-weight: 800; color: #fbbf24; font-size: 1.05rem; margin-bottom: 0.35rem;">
                        <span>⚠️</span> Misconception Still Persisting: {formatted_label}
                    </div>
                    <div style="font-size: 0.9rem; color: #e2e8f0; line-height: 1.55;">
                        The diagnostic model identified that the non-canonical reasoning is still present ({reassess_conf * 100:.1f}% confidence).
                        Review the conceptual explanation and Socratic guided hint above before attempting another problem.
                    </div>
                </div>
                """
                render_html(persisting_html)
