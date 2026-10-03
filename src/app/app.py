"""Streamlit application for Re: AI/ML Physics Misconception Diagnostic System.

Owner: Member 3 (Frontend development)
Branch: member-3-frontend
"""

import streamlit as st
from src.ml.diagnose import diagnose
from src.interventions import get_intervention
from src.learner import record_attempt, get_learner_history

# Page configuration
st.set_page_config(
    page_title="Re — Physics Diagnostic & Intervention System",
    page_icon="⚛️",
    layout="wide"
)

# Initialize Session State
if "learner_id" not in st.session_state:
    st.session_state.learner_id = "student_01"

# Header
st.title("⚛️ Re: Physics Misconception Diagnostic System")
st.caption("AI-powered diagnostic and intervention platform for high-school & undergraduate physics.")

# Sidebar - Learner Profile & History
with st.sidebar:
    st.header("👤 Learner Profile")
    learner_id = st.text_input("Learner ID", value=st.session_state.learner_id)
    st.session_state.learner_id = learner_id

    st.markdown("---")
    st.header("📜 Attempt History")
    history = get_learner_history(st.session_state.learner_id)
    if not history:
        st.info("No attempts recorded yet.")
    else:
        for idx, item in enumerate(reversed(history)):
            st.markdown(
                f"**Attempt #{len(history) - idx}**  \n"
                f"*Diagnosis:* `{item['misconception_label']}`  \n"
                f"*Confidence:* `{item['confidence_score'] * 100:.1f}%`  \n"
                f"<small>{item['timestamp'][:19]}</small>",
                unsafe_allow_html=True
            )
            st.divider()

# Sample Questions for Quick Testing
SAMPLE_QUESTIONS = [
    "A hockey puck is sliding across frictionless ice after being struck. What force keeps it moving forward?",
    "If a heavy stone and a light pebble are dropped from the same height in a vacuum, which hits the ground first?",
    "A ball is thrown straight up. At the highest point of its trajectory, is the acceleration zero?"
]

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Diagnostic Prompt")
    selected_question = st.selectbox("Select a physics question:", SAMPLE_QUESTIONS)
    custom_question = st.text_input("Or enter a custom question (optional):")
    active_question = custom_question if custom_question.strip() else selected_question

    st.info(f"**Current Question:** {active_question}")

    student_answer = st.text_area(
        "Student Answer",
        height=150,
        placeholder="Type the student's physics explanation here..."
    )

    submit_button = st.button("🔍 Diagnose Answer", type="primary", use_container_width=True)

with col2:
    st.subheader("2. AI Diagnosis & Intervention")

    if submit_button:
        with st.spinner("Analyzing response against misconception models..."):
            diag_result = diagnose(active_question, student_answer)
            misconception = diag_result.get("misconception_label", "unknown")
            confidence = diag_result.get("confidence_score", 0.0)
            status = diag_result.get("status", "unknown")

            intervention = get_intervention(misconception)

            # Record attempt via Member 4 module
            record_attempt(
                learner_id=st.session_state.learner_id,
                question=active_question,
                student_answer=student_answer,
                diagnosis=diag_result,
                intervention=intervention
            )

        if misconception == "empty_answer":
            st.warning("Please provide a student answer to diagnose.")
        else:
            # Display Diagnosis Status
            if status == "success":
                st.success(f"**Identified Misconception:** `{misconception}` (Confidence: {confidence * 100:.1f}%)")
            elif status == "uncertain":
                st.warning(f"**Low Confidence Prediction:** `{misconception}` ({confidence * 100:.1f}%)")
            else:
                st.info(f"**Status [{status}]:** `{misconception}`")

            st.write(diag_result.get("explanation", ""))

            # Display Targeted Intervention Card
            st.markdown("### 🎯 Targeted Pedagogical Intervention")
            st.markdown(f"**{intervention.get('title', 'Concept Review')}**")
            st.write(intervention.get("explanation", ""))

            with st.expander("💡 Guided Hint", expanded=True):
                st.write(intervention.get("guided_hint", "No hint available."))

            with st.expander("🔄 Reassessment Question", expanded=True):
                st.write(intervention.get("reassessment_question", "No reassessment question defined."))
    else:
        st.markdown(
            "> Submit a student answer on the left to view the ML diagnosis, confidence metrics, and targeted intervention."
        )
