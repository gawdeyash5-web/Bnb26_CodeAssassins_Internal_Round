"""Question card component for Re:Learn application.

Renders the physics diagnostic question as the central focal point of the learning session,
with topic category, large readable question typography, polished answer input, and primary CTA.
"""

from typing import Tuple
import streamlit as st
from src.app.styles import render_html

CURATED_QUESTIONS = [
    {
        "id": "Q1",
        "num": "01",
        "topic": "Newtonian Mechanics",
        "subtopic": "Newton's 1st Law (Inertia)",
        "title": "Sliding Hockey Puck",
        "question": "A hockey puck is sliding across frictionless ice after being struck. What force keeps it moving forward?",
        "misconception_sample": "The forward force from the stick stays inside the puck and keeps pushing it until it runs out.",
        "correct_sample": "No forward force is required; once set in motion, the puck continues forward at constant velocity because of inertia (Newton's 1st Law)."
    },
    {
        "id": "Q2",
        "num": "02",
        "topic": "Gravitational Kinematics",
        "subtopic": "Equivalence Principle (Free Fall)",
        "title": "Stone & Pebble Vacuum Drop",
        "question": "If a heavy stone and a light pebble are dropped from the same height in a vacuum, which hits the ground first?",
        "misconception_sample": "The heavy stone hits first because gravity pulls heavier masses with much more force.",
        "correct_sample": "Both hit the ground at the exact same instant because gravitational acceleration g is identical for all objects regardless of mass in a vacuum."
    },
    {
        "id": "Q3",
        "num": "03",
        "topic": "Kinematics & Gravity",
        "subtopic": "Acceleration at Trajectory Peak",
        "title": "Vertical Ball Trajectory",
        "question": "A ball is thrown straight up. At the highest point of its trajectory, is the acceleration zero?",
        "misconception_sample": "Yes, because the ball momentarily stops at the top, its speed is zero so acceleration must be zero too.",
        "correct_sample": "No, although the instantaneous velocity is momentarily zero, the downward acceleration due to gravity is still 9.8 m/s²."
    },
    {
        "id": "Q4",
        "num": "04",
        "topic": "Newtonian Mechanics",
        "subtopic": "Newton's 3rd Law (Action-Reaction)",
        "title": "Baseball & Bat Collision",
        "question": "When a baseball hits a heavy bat, does the bat exert a greater force on the ball than the ball exerts on the bat?",
        "misconception_sample": "The bat exerts a greater force on the ball because the bat is much heavier and moving faster.",
        "correct_sample": "By Newton's Third Law, the force exerted by the bat on the ball is exactly equal in magnitude and opposite in direction to the force of the ball on the bat."
    }
]


def render_question_card() -> Tuple[str, str, bool]:
    """Render the primary diagnostic learning challenge and answer area.

    Returns
    -------
    tuple of (active_question, student_answer, is_submitted)
    """
    # Subtle top challenge switcher bar (non-dominant, keeps focus on the question)
    col_nav1, col_nav2 = st.columns([3, 1])
    with col_nav1:
        options = [f"Challenge {q['num']}: {q['title']} ({q['topic']})" for q in CURATED_QUESTIONS]
        options.append("✏️ Custom Physics Challenge")

        if "selected_q_idx" not in st.session_state:
            st.session_state.selected_q_idx = 0

        selected_option = st.selectbox(
            "Select challenge",
            options=options,
            index=st.session_state.selected_q_idx,
            label_visibility="collapsed"
        )
    with col_nav2:
        render_html(
            """
            <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
                <span style="
                    font-size: 0.74rem;
                    font-weight: 600;
                    color: #818cf8;
                    background: rgba(99, 102, 241, 0.1);
                    border: 1px solid rgba(99, 102, 241, 0.25);
                    padding: 0.35rem 0.65rem;
                    border-radius: 6px;
                ">
                    AI Diagnostic Ready
                </span>
            </div>
            """
        )

    is_custom = "Custom" in selected_option
    current_q_data = None

    if not is_custom:
        selected_title = selected_option.split(":")[1].split("(")[0].strip()
        current_q_data = next((q for q in CURATED_QUESTIONS if q["title"] == selected_title), CURATED_QUESTIONS[0])
        active_question = current_q_data["question"]
        active_topic = current_q_data["topic"]
        active_subtopic = current_q_data["subtopic"]
        q_num = current_q_data["num"]
    else:
        custom_question = st.text_input(
            "Enter your custom conceptual physics question prompt:",
            value=st.session_state.get("custom_q_text", "A person jumps off a raft into the water. What happens to the raft?"),
            placeholder="Type a conceptual physics problem here..."
        )
        active_question = custom_question.strip() if custom_question.strip() else "Conceptual physics scenario"
        active_topic = "Custom Scenario"
        active_subtopic = "Freeform Conceptual Reasoning"
        q_num = "Custom"

    # THE VISUAL CENTERPIECE: Prominent, high-contrast, beautiful Question Card
    question_card_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(18, 27, 49, 0.95) 0%, rgba(13, 19, 36, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-top: 0.5rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 20px rgba(99, 102, 241, 0.15);
    ">
        <!-- Top metadata tags -->
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="
                    font-size: 0.72rem;
                    font-weight: 700;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    padding: 0.22rem 0.65rem;
                    border-radius: 9999px;
                    background: rgba(99, 102, 241, 0.2);
                    color: #c7d2fe;
                    border: 1px solid rgba(99, 102, 241, 0.4);
                ">
                    DIAGNOSTIC QUESTION {q_num}
                </span>
                <span style="
                    font-size: 0.76rem;
                    font-weight: 600;
                    color: #94a3b8;
                ">
                    {active_topic}
                </span>
            </div>
            <span style="
                font-size: 0.74rem;
                color: #818cf8;
                font-weight: 500;
            ">
                {active_subtopic}
            </span>
        </div>

        <!-- Large readable question text -->
        <div style="
            font-size: 1.22rem;
            font-weight: 600;
            line-height: 1.55;
            color: #ffffff;
            margin-top: 0.2rem;
        ">
            {active_question}
        </div>
    </div>
    """
    render_html(question_card_html)

    # State for student answer
    if "student_answer_input" not in st.session_state:
        st.session_state.student_answer_input = ""

    # Instant demo fill pills for judges/reviewers
    if current_q_data:
        render_html(
            """
            <div style="font-size: 0.76rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.35rem;">
                💡 Quick Demo Presets (Click to test with real evaluator responses):
            </div>
            """
        )
        col_p1, col_p2 = st.columns([1, 1], gap="small")
        with col_p1:
            if st.button("⚠️ Test Misconception Answer", use_container_width=True, type="secondary"):
                st.session_state.student_answer_input = current_q_data["misconception_sample"]
                st.rerun()
        with col_p2:
            if st.button("✅ Test Scientific Answer", use_container_width=True, type="secondary"):
                st.session_state.student_answer_input = current_q_data["correct_sample"]
                st.rerun()

    # Free-text student answer input
    student_answer = st.text_area(
        label="Your Scientific Reasoning & Explanation:",
        value=st.session_state.student_answer_input,
        placeholder="Explain your reasoning, not just your final answer. What physical laws, principles, or forces apply in this scenario?",
        height=135,
        help="Type your conceptual physics explanation in your own words."
    )
    st.session_state.student_answer_input = student_answer

    # Guidance & character count
    char_len = len(student_answer.strip())
    render_html(
        f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: #64748b;
            margin-top: -0.35rem;
            margin-bottom: 0.9rem;
        ">
            <span>Focus on cause and effect: why does the object behave this way?</span>
            <span>{char_len} characters</span>
        </div>
        """
    )

    # Primary Action CTA Button
    submit_button = st.button(
        "⚡ Analyze My Answer",
        type="primary",
        use_container_width=True,
        help="Run AI diagnostic pipeline to identify physics misconceptions."
    )

    return active_question, student_answer, submit_button
