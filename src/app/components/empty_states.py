"""Polished empty states components for Re:Learn application.

Renders modern glassmorphic visual placeholder states when data is not yet available,
guiding the learner on what action to take next.
"""

from typing import Literal
from src.app.styles import render_html


def render_empty_state(state_type: Literal["no_diagnosis", "no_history", "no_intervention", "no_reassessment"]):
    """Render a modern glassmorphic empty state card.

    Parameters
    ----------
    state_type : str
        One of 'no_diagnosis', 'no_history', 'no_intervention', 'no_reassessment'.
    """
    states = {
        "no_diagnosis": {
            "icon": "🧠",
            "title": "Awaiting Student Answer",
            "description": "Select a physics scenario on the left, formulate your scientific explanation, and click 'Analyze My Answer' to trigger the AI diagnostic pipeline.",
            "hint": "Try one of the quick preset answers if you'd like to test the system immediately!"
        },
        "no_history": {
            "icon": "📜",
            "title": "No Diagnostic Attempts Recorded",
            "description": "Your learning journey for this profile will appear here as you submit responses and verify conceptual mastery.",
            "hint": "Each attempt tracks misconception diagnoses, confidence scores, and timestamps."
        },
        "no_intervention": {
            "icon": "🎯",
            "title": "No Active Remediation Needed",
            "description": "Submit a response to receive personalized conceptual feedback, physical analogies, and guided Socratic hints.",
            "hint": "Our model identifies underlying root causes rather than just grading answers right or wrong."
        },
        "no_reassessment": {
            "icon": "🔄",
            "title": "Reassessment Available After Diagnosis",
            "description": "Once a concept or misconception is identified, a targeted scenario will appear here to test whether your conceptual understanding has resolved.",
            "hint": "True learning is confirmed through novel scenarios, not rote repetition."
        }
    }

    item = states.get(state_type, states["no_diagnosis"])

    html = f"""
    <div style="
        background: rgba(14, 21, 38, 0.45);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.2rem 1.8rem;
        text-align: center;
        margin-bottom: 1.25rem;
    ">
        <div style="
            width: 52px;
            height: 52px;
            margin: 0 auto 0.9rem auto;
            border-radius: 12px;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.22);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        ">
            {item['icon']}
        </div>
        <div style="
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.35rem;
        ">
            {item['title']}
        </div>
        <div style="
            font-size: 0.86rem;
            color: #94a3b8;
            max-width: 440px;
            margin: 0 auto 0.85rem auto;
            line-height: 1.5;
        ">
            {item['description']}
        </div>
        <div style="
            font-size: 0.76rem;
            color: #818cf8;
            background: rgba(99, 102, 241, 0.08);
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 9999px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        ">
            💡 {item['hint']}
        </div>
    </div>
    """
    render_html(html)
