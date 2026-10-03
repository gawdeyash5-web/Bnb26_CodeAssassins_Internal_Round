"""Re:Learn — Adaptive Multimodal Learning Environment.

Physics misconception diagnosis and adaptive learning platform.
Frontend Redesign by Member 3.

Run with:
    python -m streamlit run src/app/app.py
"""

import streamlit as st

# Strict preservation of required backend interfaces
from src.ml.diagnose import diagnose
from src.interventions import get_intervention
from src.learner import record_attempt, get_learner_history

# Modular UI components & safe HTML rendering
from src.app.styles import apply_custom_styles, render_html
from src.app.components.header import render_header
from src.app.components.sidebar import render_sidebar
from src.app.components.question_card import render_question_card
from src.app.components.diagnosis_card import render_diagnosis_card
from src.app.components.intervention_card import render_intervention_card
from src.app.components.reassessment_card import render_reassessment_card
from src.app.components.progress_history import render_progress_history
from src.app.components.empty_states import render_empty_state


# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Re:Learn — Adaptive Physics Learning",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark premium glassmorphic styling
apply_custom_styles()


# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "learner_id" not in st.session_state:
    st.session_state.learner_id = "student_01"

if "current_diag_result" not in st.session_state:
    st.session_state.current_diag_result = None

if "current_intervention" not in st.session_state:
    st.session_state.current_intervention = None

if "last_analyzed_question" not in st.session_state:
    st.session_state.last_analyzed_question = ""


# -----------------------------------------------------------------------------
# 3. SIDEBAR & HEADER
# -----------------------------------------------------------------------------
active_learner_id = render_sidebar()
learner_history = get_learner_history(active_learner_id)
render_header(active_learner_id, learner_history)


# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE TABS
# -----------------------------------------------------------------------------
tab_diagnostics, tab_progress, tab_taxonomy = st.tabs([
    "🎯 Guided Learning Session",
    "📊 Learner Progress History",
    "📚 Physics Misconception Taxonomy"
])

# -----------------------------------------------------------------------------
# TAB 1: GUIDED LEARNING SESSION
# -----------------------------------------------------------------------------
with tab_diagnostics:
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        active_question, student_answer, is_submitted = render_question_card()

        # Handle Submission
        if is_submitted:
            if not student_answer.strip():
                st.warning("⚠️ Please formulate your physics explanation before submitting.")
            else:
                try:
                    with st.spinner("🧠 AI diagnostic model analyzing your response..."):
                        diag_result = diagnose(active_question, student_answer)
                        misconception = diag_result.get("misconception_label", "unknown")
                        intervention = get_intervention(misconception)

                        # Record interaction via Member 4 module
                        record_attempt(
                            learner_id=active_learner_id,
                            question=active_question,
                            student_answer=student_answer,
                            diagnosis=diag_result,
                            intervention=intervention
                        )

                        # Store in session state for persistent rendering
                        st.session_state.current_diag_result = diag_result
                        st.session_state.current_intervention = intervention
                        st.session_state.last_analyzed_question = active_question

                    st.toast("Diagnostic analysis complete!", icon="✅")
                    st.rerun()

                except Exception as exc:
                    # User-friendly error message, avoiding raw tracebacks
                    st.error(
                        "An unexpected error occurred while analyzing your answer. "
                        "The diagnostic service has logged this event. Please try again."
                    )

    with col_output:
        diag = st.session_state.get("current_diag_result")
        interv = st.session_state.get("current_intervention")

        if diag and interv:
            # 1. AI Diagnosis Reveal Card
            render_diagnosis_card(diag)

            # 2. Targeted Remediation ("Let's Fix This Misconception")
            raw_misconception = diag.get("misconception_label", "")
            render_intervention_card(interv, raw_misconception)

            # 3. Dedicated "Prove Your Understanding" Reassessment
            render_reassessment_card(interv, active_learner_id)

        else:
            # Polished empty state prior to submission
            render_empty_state("no_diagnosis")


# -----------------------------------------------------------------------------
# TAB 2: LEARNER PROGRESS & ANALYTICS
# -----------------------------------------------------------------------------
with tab_progress:
    render_html(
        f"""
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff;">
                📈 Conceptual Progression: <span style="color: #818cf8;">{active_learner_id}</span>
            </div>
            <div style="font-size: 0.86rem; color: #94a3b8; margin-top: 0.2rem;">
                Historical log of diagnosed physics misconceptions, confidence metrics, and remediation attempts.
            </div>
        </div>
        """
    )
    render_progress_history(active_learner_id)


# -----------------------------------------------------------------------------
# TAB 3: PHYSICS TAXONOMY & STANDARDS
# -----------------------------------------------------------------------------
with tab_taxonomy:
    render_html(
        """
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff;">
                ⚛️ Common Physics Misconception Taxonomy
            </div>
            <div style="font-size: 0.86rem; color: #94a3b8; margin-top: 0.2rem;">
                Curated pedagogical taxonomy referenced by the Re:Learn diagnostic classifier.
            </div>
        </div>
        """
    )

    col_t1, col_t2 = st.columns([1, 1], gap="medium")

    with col_t1:
        render_html(
            """
            <div style="
                background: rgba(14, 21, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 1.3rem;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <span style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">Impetus Force Persistence</span>
                    <span style="font-size: 0.72rem; font-weight: 700; color: #a5b4fc; background: rgba(99, 102, 241, 0.16); padding: 0.2rem 0.55rem; border-radius: 4px; border: 1px solid rgba(99, 102, 241, 0.3);">NEWTON'S 1ST LAW</span>
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.55; margin-bottom: 0.6rem;">
                    <strong>Common Misconception:</strong> Belief that motion requires a continuous internal or carried force; an object stops when its "force" runs out.
                </div>
                <div style="font-size: 0.88rem; color: #a5b4fc; line-height: 1.55;">
                    <strong>Physics Principle:</strong> In the absence of an external net force (like friction), an object in motion remains in motion at constant velocity (Inertia).
                </div>
            </div>

            <div style="
                background: rgba(14, 21, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 1.3rem;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <span style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">Acceleration Zero at Peak</span>
                    <span style="font-size: 0.72rem; font-weight: 700; color: #a5b4fc; background: rgba(99, 102, 241, 0.16); padding: 0.2rem 0.55rem; border-radius: 4px; border: 1px solid rgba(99, 102, 241, 0.3);">KINEMATICS</span>
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.55; margin-bottom: 0.6rem;">
                    <strong>Common Misconception:</strong> When a projectile reaches its peak height, its velocity is zero, so acceleration must also be zero.
                </div>
                <div style="font-size: 0.88rem; color: #a5b4fc; line-height: 1.55;">
                    <strong>Physics Principle:</strong> Gravity acts continuously downward ($a = -9.8\\text{ m/s}^2$) regardless of instantaneous velocity.
                </div>
            </div>
            """
        )

    with col_t2:
        render_html(
            """
            <div style="
                background: rgba(14, 21, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 1.3rem;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <span style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">Heavier Objects Fall Faster</span>
                    <span style="font-size: 0.72rem; font-weight: 700; color: #a5b4fc; background: rgba(99, 102, 241, 0.16); padding: 0.2rem 0.55rem; border-radius: 4px; border: 1px solid rgba(99, 102, 241, 0.3);">EQUIVALENCE PRINCIPLE</span>
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.55; margin-bottom: 0.6rem;">
                    <strong>Common Misconception:</strong> Heavier masses always accelerate faster toward Earth due to greater gravitational pull.
                </div>
                <div style="font-size: 0.88rem; color: #a5b4fc; line-height: 1.55;">
                    <strong>Physics Principle:</strong> While gravitational force is proportional to mass ($F = mg$), inertia is also proportional to mass ($a = F/m = g$), meaning all masses accelerate identically in a vacuum.
                </div>
            </div>

            <div style="
                background: rgba(14, 21, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 1.3rem;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <span style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">Action-Reaction Cancellation</span>
                    <span style="font-size: 0.72rem; font-weight: 700; color: #a5b4fc; background: rgba(99, 102, 241, 0.16); padding: 0.2rem 0.55rem; border-radius: 4px; border: 1px solid rgba(99, 102, 241, 0.3);">NEWTON'S 3RD LAW</span>
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.55; margin-bottom: 0.6rem;">
                    <strong>Common Misconception:</strong> Newton's Third Law force pairs cancel each other out on the same body, or a larger object exerts a greater force.
                </div>
                <div style="font-size: 0.88rem; color: #a5b4fc; line-height: 1.55;">
                    <strong>Physics Principle:</strong> Action and reaction forces act on two entirely distinct bodies and therefore never cancel each other out.
                </div>
            </div>
            """
        )
